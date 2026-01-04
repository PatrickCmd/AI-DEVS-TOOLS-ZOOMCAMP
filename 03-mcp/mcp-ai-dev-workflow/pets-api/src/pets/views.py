"""
Pet views for the Petstore API.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from pets.models import Category, Pet, Tag
from pets.serializers import (
    CategorySerializer,
    PetCreateSerializer,
    PetSerializer,
    PetUpdateSerializer,
    TagSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category model.
    Provides CRUD operations for pet categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "id"]
    ordering = ["name"]


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Tag model.
    Provides CRUD operations for pet tags.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "id"]
    ordering = ["name"]


class PetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Pet model.
    Provides CRUD operations and custom actions for pets.
    """

    queryset = Pet.objects.select_related("category").prefetch_related("tags").all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "category"]
    search_fields = ["name", "tags__name"]
    ordering_fields = ["name", "created_at", "status"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == "create":
            return PetCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return PetUpdateSerializer
        return PetSerializer

    def create(self, request, *args, **kwargs):
        """Create a new pet."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pet = serializer.save()

        # Return the created pet with full details
        response_serializer = PetSerializer(pet)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update an existing pet."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        pet = serializer.save()

        # Return the updated pet with full details
        response_serializer = PetSerializer(pet)
        return Response(response_serializer.data)

    @action(detail=False, methods=["get"], url_path="findByStatus")
    def find_by_status(self, request):
        """
        Find pets by status.
        Query parameter: status (can be comma-separated for multiple statuses)
        """
        status_param = request.query_params.get("status", "")

        if not status_param:
            return Response(
                {"error": "Status parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Split comma-separated statuses
        statuses = [s.strip() for s in status_param.split(",") if s.strip()]

        # Validate statuses
        valid_statuses = [choice[0] for choice in Pet.Status.choices]
        invalid_statuses = [s for s in statuses if s not in valid_statuses]

        if invalid_statuses:
            return Response(
                {
                    "error": f"Invalid status values: {', '.join(invalid_statuses)}",
                    "valid_statuses": valid_statuses
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filter pets by statuses
        pets = self.queryset.filter(status__in=statuses)
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="findByTags")
    def find_by_tags(self, request):
        """
        Find pets by tags.
        Query parameter: tags (comma-separated tag names)
        """
        tags_param = request.query_params.get("tags", "")

        if not tags_param:
            return Response(
                {"error": "Tags parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Split comma-separated tags
        tag_names = [t.strip() for t in tags_param.split(",") if t.strip()]

        # Filter pets that have any of these tags
        pets = self.queryset.filter(tags__name__in=tag_names).distinct()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="uploadImage")
    def upload_image(self, request, pk=None):
        """
        Upload an image for a pet.
        Expects multipart/form-data with 'file' field.
        Optional: additionalMetadata field for image description.
        """
        # Validate that pet exists (raises 404 if not found)
        self.get_object()

        if "file" not in request.FILES:
            return Response(
                {"error": "No file provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_file = request.FILES["file"]
        additional_metadata = request.data.get("additionalMetadata", "")

        # For now, we'll just return a success response
        # In production, you would upload to cloud storage (S3, etc.)
        # and add the URL to pet.photo_urls

        response_data = {
            "code": 200,
            "type": "success",
            "message": f"File '{uploaded_file.name}' uploaded successfully"
        }

        if additional_metadata:
            response_data["metadata"] = additional_metadata

        return Response(response_data)

    def destroy(self, request, *args, **kwargs):
        """Delete a pet."""
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
