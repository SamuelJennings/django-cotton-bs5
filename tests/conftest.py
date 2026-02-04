"""Pytest configuration for django-cotton-bs5 tests."""

# Import fixtures from cotton_bs5.fixtures to make them available to tests
from cotton_bs5.fixtures import (
    cotton_render,
    cotton_render_soup,
    cotton_render_string,
    cotton_render_string_soup,
)

__all__ = ["cotton_render", "cotton_render_soup", "cotton_render_string", "cotton_render_string_soup"]

