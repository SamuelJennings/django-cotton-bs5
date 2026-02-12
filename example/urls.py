import os
from pathlib import Path

from django.conf import settings
from django.urls import include, path
from django.utils.text import slugify
from django.views.generic import TemplateView
from django_distill import distill_path

MENU_SECTIONS = [
    "layout",
    "components",
    "utilities",
]


class DemoPageView(TemplateView):
    """
    Custom view for component demo pages that injects a menu of all components
    into the template context.
    """

    # Mapping of component names (slugified) to Bootstrap documentation URLs
    BOOTSTRAP_DOCS_URLS = {
        "accordion": "https://getbootstrap.com/docs/5.3/components/accordion/",
        "alerts": "https://getbootstrap.com/docs/5.3/components/alerts/",
        "badges": "https://getbootstrap.com/docs/5.3/components/badge/",
        "breadcrumbs": "https://getbootstrap.com/docs/5.3/components/breadcrumb/",
        "button-groups": "https://getbootstrap.com/docs/5.3/components/button-group/",
        "buttons": "https://getbootstrap.com/docs/5.3/components/buttons/",
        "cards": "https://getbootstrap.com/docs/5.3/components/card/",
        "carousel": "https://getbootstrap.com/docs/5.3/components/carousel/",
        "collapse": "https://getbootstrap.com/docs/5.3/components/collapse/",
        "dropdown": "https://getbootstrap.com/docs/5.3/components/dropdowns/",
        "grid-system": "https://getbootstrap.com/docs/5.3/layout/grid/",
        "list-group": "https://getbootstrap.com/docs/5.3/components/list-group/",
        "modals-offcanvas": "https://getbootstrap.com/docs/5.3/components/modal/",
        "navbar": "https://getbootstrap.com/docs/5.3/components/navbar/",
        "navigation": "https://getbootstrap.com/docs/5.3/components/navs-tabs/",
        "pagination": "https://getbootstrap.com/docs/5.3/components/pagination/",
        "placeholder": "https://getbootstrap.com/docs/5.3/components/placeholders/",
        "progress": "https://getbootstrap.com/docs/5.3/components/progress/",
        "ratio": "https://getbootstrap.com/docs/5.3/helpers/ratio/",
        "spinner": "https://getbootstrap.com/docs/5.3/components/spinners/",
        "table": "https://getbootstrap.com/docs/5.3/content/tables/",
        "tabs": "https://getbootstrap.com/docs/5.3/components/navs-tabs/",
        "toast": "https://getbootstrap.com/docs/5.3/components/toasts/",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["component_menu"] = self.get_component_menu()
        context["variants"] = [
            "primary",
            "secondary",
            "success",
            "danger",
            "warning",
            "info",
            "light",
            "dark",
        ]
        context["breakpoints"] = ["sm", "md", "lg", "xl", "xxl"]
        # Add Bootstrap docs URL if available for this component
        # Get the current URL name from the resolved URL match
        if self.request.resolver_match:
            url_name = self.request.resolver_match.url_name
            if url_name and url_name in self.BOOTSTRAP_DOCS_URLS:
                context["bs_docs_url"] = self.BOOTSTRAP_DOCS_URLS[url_name]
            # Add component name for bug reporting
            if url_name:
                context["component_name"] = url_name.replace("-", " ").title()

        return context

    @staticmethod
    def get_component_menu():
        """
        Generate a dictionary of all component demo pages organized by section.
        Returns a dict where keys are section names and values are lists of menu items.
        Each menu item is a dict with 'name' (display name) and 'url_name' (for {% url %} tag).
        """
        menu_sections = {}

        for section in MENU_SECTIONS:
            templates_dir = Path(__file__).parent / "templates" / section

            if templates_dir.exists():
                menu_items = []
                for template_file in sorted(templates_dir.glob("*.html")):
                    name = template_file.stem
                    slug = slugify(name)
                    menu_items.append(
                        {
                            "name": name.replace("_", " ").replace("-", " ").title(),
                            "url_name": slug,
                        }
                    )
                menu_sections[section] = menu_items

        return menu_sections


def get_index():
    """
    distill_func for the home page - returns None for parameterless URLs
    """
    return None


# def get_all_components():
#     """
#     distill_func for component pages - returns None for each component
#     since they don't have URL parameters
#     """
#     templates_dir = Path(__file__).parent / "templates" / "components"

#     if templates_dir.exists():
#         for _template_file in sorted(templates_dir.glob("*.html")):
#             # Return None for each component - no URL parameters needed
#             yield None


# Dynamically generate URL patterns for component templates
def generate_routes(template_dir):
    """
    Dynamically create URL routes for any template listed in templates/components/.
    Each template gets a URL with:
    - path: slugified name (minus extension)
    - view: TemplateView with template_name set to the template path
    - name: same as the URL path
    """
    routes = []
    templates_dir = Path(__file__).parent / "templates" / template_dir

    if templates_dir.exists():
        for template_file in templates_dir.glob("*.html"):
            # Get filename without extension
            name = template_file.stem
            # Create slugified path
            slug = slugify(name)
            # Create template path
            template_path = f"{template_dir}/{template_file.name}"

            routes.append(
                distill_path(
                    f"{slug}/",
                    DemoPageView.as_view(template_name=template_path),
                    name=slug,
                    distill_file=f"{slug}/index.html",
                )
            )

    return routes


urlpatterns = [
    distill_path(
        "",
        DemoPageView.as_view(template_name="home.html"),
        name="home",
        distill_func=get_index,
        distill_file="index.html",
    ),
]

for section in MENU_SECTIONS:
    urlpatterns += generate_routes(section)

# Add browser reload URLs only in DEBUG mode
if settings.DEBUG and not os.environ.get("GITHUB_PAGES_REPO"):
    from django.urls import include, path

    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
