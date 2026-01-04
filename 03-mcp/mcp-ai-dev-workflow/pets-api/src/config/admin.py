"""
Custom admin site configuration.
"""

from django.contrib import admin


class PetStoreAdminSite(admin.AdminSite):
    """Custom admin site for Pets Store."""

    site_header = "Pets Store Admin"
    site_title = "Pets Store Admin Portal"
    index_title = "Welcome to Pets Store Administration"


# Create custom admin site instance
admin_site = PetStoreAdminSite(name="petstoreAdmin")
