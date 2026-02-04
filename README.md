# Django Cotton BS5

Bootstrap 5 components for Django Cotton - A comprehensive library of reusable, modular components.

**Note:** This project is currently a work in progress. Users are encouraged to request new components or features via the [issue tracker](https://github.com/SamuelJennings/cotton-bs5/issues).

[View demo](https://samueljennings.github.io/cotton-bs5/)

## Installation

```bash
pip install django-cotton-bs5
```

Add `cotton_bs5` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "django_cotton",
    "cotton_bs5",
    ...
]
```

## Available Components

The following Bootstrap 5 components are currently available as Django Cotton components:

- **Alert** (`<c-alert>`) — Bootstrap alerts with variants, dismissible, slot/text support
- **Accordion** (`<c-accordion>`, `<c-accordion.item>`, `<c-accordion.header>`) — Collapsible accordion panels
- **Breadcrumbs** (`<c-breadcrumbs>`, `<c-breadcrumbs.item>`) — Navigation breadcrumbs
- **Button** (`<c-button>`) — Button/link with variants, outline, icon, slot/text
- **Button Group** (`<c-button_group>`) — Grouped buttons, vertical/size/label support
- **Card** (`<c-card>`, `<c-card.body>`, `<c-card.title>`) — Card container, body, and title
- **List Group** (`<c-list_group>`, `<c-list_group.item>`) — List group and items, horizontal/numbered/active/disabled
- **Modal** (`<c-modal>`, `<c-modal.title>`, `<c-modal.body>`) — Modal dialog, title, and body
- **Navbar** (`<c-navbar>`) — Responsive navigation bar with brand, expand, toggler
- **Progress** (`<c-progress>`) — Progress bar with value, min/max, variant, striped, animated, label
- **Spinner** (`<c-spinner>`) — Loading spinner, border/grow, size, variant, label
- **Table** (`<c-table>`) — Responsive table, striped, bordered, hover, small, variant, caption
- **Tabs** (`<c-tabs>`, `<c-tabs.item>`, `<c-tabs.pane>`) — Tab navigation and tab panes

More components are planned. Please request additional Bootstrap 5 components or features via the [issue tracker](https://github.com/SamuelJennings/cotton-bs5/issues).

## Testing Components

This package provides four pytest fixtures for testing Django Cotton components:

### `cotton_render` Fixture

Renders a component and returns the raw HTML as a string.

```python
def test_alert_component(cotton_render):
    html = cotton_render(
        'cotton_bs5.alert',
        message="Hello World",
        variant="success"
    )
    assert 'alert-success' in html
    assert 'Hello World' in html
```

### `cotton_render_soup` Fixture

Renders a component and returns a BeautifulSoup parsed HTML object for easier DOM traversal and assertions.

```python
def test_alert_component(cotton_render_soup):
    soup = cotton_render_soup(
        'cotton_bs5.alert',
        message="Hello World",
        variant="success"
    )
    alert_div = soup.find('div', class_='alert')
    assert 'alert-success' in alert_div['class']
    assert alert_div.get_text() == 'Hello World'
```

### `cotton_render_string` Fixture

Compiles and renders template strings containing Cotton component syntax. Useful for testing multi-component markup and complex layouts inline without creating separate template files.

```python
def test_button_inline(cotton_render_string):
    html = cotton_render_string("<c-button variant='primary'>Click me</c-button>")
    assert 'btn-primary' in html

def test_nested_components(cotton_render_string):
    html = cotton_render_string(
        "<c-ul><c-li text='first' /><c-li text='second' /></c-ul>"
    )
    assert 'first' in html
    assert 'second' in html
```

### `cotton_render_string_soup` Fixture

Combines `cotton_render_string` with BeautifulSoup parsing for easier DOM traversal and assertions on multi-component structures.

```python
def test_nested_list(cotton_render_string_soup):
    soup = cotton_render_string_soup(
        "<c-ul><c-li text='first' /><c-li text='second' /></c-ul>"
    )
    items = soup.find_all('li')
    assert len(items) == 2
    assert items[0].get_text() == 'first'

def test_complex_layout(cotton_render_string_soup):
    template = '''
        <c-card>
            <c-card.title>{{ title }}</c-card.title>
            <c-card.body>
                <c-button variant='primary'>{{ action }}</c-button>
            </c-card.body>
        </c-card>
    '''
    soup = cotton_render_string_soup(template, context={
        'title': 'My Card',
        'action': 'Click Here'
    })
    assert soup.find('h5').get_text() == 'My Card'
    assert 'btn-primary' in soup.find('button')['class']
```

All fixtures automatically inject a request object, so you don't need to create one manually.

## Contributing

This library follows django-cotton conventions and Bootstrap 5 standards. When adding new components:

1. Use `<c-vars />` for default values
2. Include proper accessibility attributes
3. Support all relevant Bootstrap 5 options
4. Maintain consistent naming conventions
5. Test with various configurations

## License

MIT License - see [LICENSE](LICENSE) file for details.
