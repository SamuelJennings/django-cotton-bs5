"""
URL configuration for GitHub Pages deployment.

This wraps the main urls.py with a prefix path for subdirectory deployment.
"""

import os

from django.urls import include, path

# Get the repository name from environment variable
GITHUB_PAGES_REPO = os.environ.get("GITHUB_PAGES_REPO", "django-cotton-bs5")

urlpatterns = [
    path(f"{GITHUB_PAGES_REPO}/", include("example.urls")),
]
