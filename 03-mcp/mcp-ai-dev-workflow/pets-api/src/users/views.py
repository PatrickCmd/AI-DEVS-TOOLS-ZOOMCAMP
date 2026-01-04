"""
User views for the Petstore API.
"""

from django.contrib.auth import authenticate, get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserUpdateSerializer,
)

User = get_user_model()


def get_tokens_for_user(user):
    """Generate JWT tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    Provides CRUD operations and authentication actions.
    """

    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["user_status", "is_active"]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering_fields = ["username", "date_joined", "email"]
    ordering = ["-date_joined"]
    lookup_field = "username"

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == "create" or self.action == "create_with_list":
            return UserCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        elif self.action == "login":
            return UserLoginSerializer
        return UserSerializer

    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ["create", "login", "create_with_list"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Create a new user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens for the new user
        tokens = get_tokens_for_user(user)

        # Return the created user with tokens
        response_serializer = UserSerializer(user)
        return Response(
            {
                "user": response_serializer.data,
                **tokens
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """Update an existing user."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        # Only allow users to update their own profile or admins to update anyone
        if instance != request.user and not request.user.is_staff:
            return Response(
                {"error": "You can only update your own profile"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Return the updated user
        response_serializer = UserSerializer(user)
        return Response(response_serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Delete a user."""
        instance = self.get_object()

        # Only allow users to delete their own account or admins to delete anyone
        if instance != request.user and not request.user.is_staff:
            return Response(
                {"error": "You can only delete your own account"},
                status=status.HTTP_403_FORBIDDEN
            )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"])
    def login(self, request):
        """
        Login endpoint.
        Returns user details and JWT tokens (access and refresh).
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"error": "User account is disabled"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Generate JWT tokens
        tokens = get_tokens_for_user(user)

        # Return user details and tokens
        user_serializer = UserSerializer(user)
        return Response({
            "user": user_serializer.data,
            **tokens
        })

    @action(detail=False, methods=["get"])
    def me(self, request):
        """
        Get current authenticated user's profile.
        Returns the details of the currently logged-in user.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def logout(self, request):
        """
        Logout endpoint.
        Blacklists the refresh token.
        Expects 'refresh' token in the request body.
        """
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post"], url_path="createWithList")
    def create_with_list(self, request):
        """
        Create multiple users with a list input.
        Expects a list of user objects in the request body.
        """
        if not isinstance(request.data, list):
            return Response(
                {"error": "Expected a list of user objects"},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_users = []
        errors = []

        for idx, user_data in enumerate(request.data):
            serializer = UserCreateSerializer(data=user_data)
            if serializer.is_valid():
                user = serializer.save()
                created_users.append(UserSerializer(user).data)
            else:
                errors.append({
                    "index": idx,
                    "data": user_data,
                    "errors": serializer.errors
                })

        response_data = {
            "created": len(created_users),
            "users": created_users
        }

        if errors:
            response_data["errors"] = errors
            return Response(response_data, status=status.HTTP_207_MULTI_STATUS)

        return Response(response_data, status=status.HTTP_201_CREATED)
