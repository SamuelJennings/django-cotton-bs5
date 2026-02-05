# Static Site Deployment

This project uses [django-distill](https://github.com/meeb/django-distill) to generate a static version of the example app, which is automatically deployed to GitHub Pages.

## Overview

The example app showcases Bootstrap 5 components built with Django Cotton. By converting it to a static site, we can:

- Host a live demo on GitHub Pages without running a Django server
- Improve performance and reduce hosting costs
- Provide an accessible reference for users exploring the component library

## How It Works

### django-distill Integration

django-distill converts Django views into static HTML files by:

1. **URL Configuration**: All URL patterns in `example/urls.py` use `distill_path()` instead of Django's standard `path()`
2. **distill_func**: Each route defines a function that tells distill what pages to generate
3. **Relative URLs**: Custom `{% static_url %}` template tag generates relative URLs that work both as files and on web servers
4. **Static Generation**: Running `python manage.py distill-local` renders all pages and copies static files

### Relative URL Support

To ensure links work correctly in the static site (whether opened as files or served from a subdirectory), we use a custom template tag:

```python
# example/templatetags/example.py
@register.simple_tag(takes_context=True)
def static_url(context, view_name):
    """Generate relative URLs for static sites."""
    # Returns './' or '../' based on current page depth
    # Example: from index.html -> './accordion/'
    # Example: from accordion/index.html -> '../' (home) or '../alerts/' (other component)
```

Templates use `{% static_url 'view_name' %}` instead of `{% url 'view_name' %}`:

```django
{% load example %}
<a href="{% static_url 'home' %}">Home</a>
<a href="{% static_url 'accordion' %}">Accordion</a>
```

This generates:

- From root: `href="./accordion/"`
- From component page: `href="../accordion/"`

### URL Pattern Example

```python
from django_distill import distill_path

def get_index():
    """For parameterless URLs, return None"""
    return None

urlpatterns = [
    distill_path(
        "",
        DemoPageView.as_view(template_name="home.html"),
        name="home",
        distill_func=get_index,
        distill_file="index.html",
    ),
]
```

For dynamic component pages, we use a generator:

```python
def get_all_components():
    """Generate a page for each component template"""
    templates_dir = Path(__file__).parent / "templates" / "components"
    if templates_dir.exists():
        for template_file in sorted(templates_dir.glob("*.html")):
            yield None  # No URL parameters needed
```

## Configuration

### Django Settings (`tests/settings.py`)

```python
INSTALLED_APPS = [
    # ... other apps
    "django_distill",
]

# Output directory for static site
DISTILL_DIR = os.path.join(BASE_DIR, "dist")

# Required for static files
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
```

### Poetry Dependencies (`pyproject.toml`)

```toml
[tool.poetry.group.dev.dependencies]
django-distill = "^3.0"
```

## Local Development

### Generate Static Site Locally

```bash
# Generate static site to dist/ directory
poetry run python manage.py distill-local --force --collectstatic

# Preview the static site (requires a web server)
cd dist
python -m http.server 8000
```

Visit `http://localhost:8000` to view the static site.

### Directory Structure

After running `distill-local`, the output structure is:

```
dist/
├── index.html              # Home page
├── accordion/
│   └── index.html          # Accordion component demo
├── alerts/
│   └── index.html          # Alerts component demo
├── badges/
│   └── index.html          # Badges component demo
├── ...                     # Other component pages
└── static/                 # Collected static files
    ├── bs5/                # Bootstrap 5 styles
    └── ...
```

## GitHub Pages Deployment

### Automatic Deployment

The `.github/workflows/deploy-static-site.yml` workflow automatically:

1. **Triggers** on pushes to `main` branch or manual workflow dispatch
2. **Builds** the static site using Poetry and django-distill
3. **Deploys** to GitHub Pages using the official actions

### Workflow Steps

1. **Setup**: Checkout code, install Python 3.12, install Poetry
2. **Cache**: Cache Poetry virtualenv for faster builds
3. **Install**: Install project dependencies
4. **Generate**: Run `distill-local --force --collectstatic`
5. **Upload**: Upload dist/ directory as Pages artifact
6. **Deploy**: Deploy artifact to GitHub Pages

### GitHub Repository Settings

To enable GitHub Pages deployment, configure in your repository:

1. Go to **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. The workflow will handle the rest automatically

### URL

Once deployed, the site will be available at:

```
https://<username>.github.io/<repository-name>/
```

For example: `https://samueljennings.github.io/django-cotton-bs5/`

## Maintenance

### Adding New Components

When adding a new component template to `example/templates/components/`:

1. Create the template file (e.g., `new-component.html`)
2. The `generate_component_routes()` function automatically discovers it
3. No URL configuration changes needed
4. Push to `main` to trigger deployment

### Updating Existing Components

Simply update the template files and push. The GitHub Actions workflow will:

1. Detect the push to `main`
2. Regenerate all static pages
3. Deploy the updated site

## Troubleshooting

### Build Failures

Check the GitHub Actions logs for errors:

- Poetry installation issues
- Django configuration errors
- Template rendering errors

### Missing Static Files

Ensure `STATIC_ROOT` is configured and `collectstatic` runs successfully:

```bash
poetry run python manage.py collectstatic --noinput
```

### URL Issues

If URLs are broken in the static site:

- Use relative URLs in templates: `{% url 'component-name' %}`
- Avoid hardcoded absolute paths
- Test locally before pushing

## Further Reading

- [django-distill Documentation](https://github.com/meeb/django-distill)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions for Pages](https://github.com/actions/deploy-pages)
