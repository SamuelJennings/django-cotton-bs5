"""Template tags and filters for MVP navbar widgets."""

import secrets
import string
import textwrap

from django import template
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django_cotton.compiler_regex import CottonCompiler  # type: ignore[import-untyped]

# Conditional import for BeautifulSoup
try:
    from bs4 import BeautifulSoup

    HAS_BEAUTIFULSOUP = True
except ImportError:
    HAS_BEAUTIFULSOUP = False

register = template.Library()

compiler = CottonCompiler()


@register.filter
def prefix(value, arg):
    """Prefix a string with a given argument.

    Args:
        value (str): The original string to be prefixed.
        arg (str): The prefix to add to the original string.

    Returns:
        str: The resulting string with the prefix added.

    Example:
        {{ "world"|prefix:"hello " }}  # Output: "hello-world"
    """
    if value:
        return f"{arg}-{value}"
    return ""


@register.filter
def postfix(value, arg):
    """Postfix a string with a given argument.

    Args:
        value (str): The original string to be postfixed.
        arg (str): The postfix to add to the original string.

    Returns:
        str: The resulting string with the postfix added.

    Example:
        {{ "hello"|postfix:" world" }}  # Output: "hello-world"
    """
    if value:
        return f"{value}-{arg}"
    return ""


@register.filter
def split(value, delimiter=","):
    return value.split(delimiter)


@register.filter
def slot_is_empty(slot):
    """Check if a template slot is empty after stripping whitespace.

    Django Cotton slots may contain strings with unwanted whitespace or newlines,
    making direct template checks unreliable. This filter properly handles these
    cases by stripping whitespace before comparison.

    Args:
        slot: The slot content to check (typically a string, but may be other types).

    Returns:
        bool: True if slot is a string with only whitespace or is empty, False otherwise.
              Returns None implicitly if slot is not a string type.

    Example:
        {% if slot_content|slot_is_empty %}
            <p>No content provided</p>
        {% else %}
            {{ slot_content }}
        {% endif %}
    """
    if isinstance(slot, str):
        return slot.strip() == ""


@register.filter
def beautify_html(html):
    """Clean up and format unformatted HTML with proper indentation.

    Removes common leading whitespace and strips leading/trailing blank lines
    to produce clean, readable HTML.

    Args:
        html (str): Unformatted HTML string

    Returns:
        str: Formatted HTML with normalized indentation

    Example:
        Input:  "    <div>\n        <p>Hello</p>\n    </div>"
        Output: "<div>\n    <p>Hello</p>\n</div>"
    """
    return textwrap.dedent(html).strip("\n")


@register.simple_tag
def genid(prefix="", length=6):
    """Generate a unique random ID for use in HTML attributes.

    Produces a short random string suitable for use as unique HTML element IDs.
    Can optionally include a prefix for semantic naming.

    Args:
        prefix (str): Optional prefix to prepend to the random string.
                     If provided, the format is "{prefix}-{random_string}".
                     Defaults to empty string (no prefix).
        length (int): Length of the random string to generate.
                     Defaults to 6 characters.

    Returns:
        str: Generated ID. If prefix is provided, returns "{prefix}-{random_string}",
             otherwise returns just the random string.

    Example:
        {% genid %}                              # Returns something like "a3b2c1"
        {% genid "tab" %}                        # Returns something like "tab-a3b2c1"
        {% genid "modal" 8 %}                    # Returns something like "modal-a3b2c1d9"
        {% genid prefix="button" length=10 %}   # Returns something like "button-a3b2c1d9e7"
    """
    random_str = "".join(
        secrets.choice(string.ascii_lowercase + string.digits) for _ in range(length)
    )
    if prefix:
        return f"{prefix}-{random_str}"
    return random_str


@register.simple_tag(takes_context=True)
def cotton_parent(context):
    cotton_data = context.get("cotton_data", {})
    if not cotton_data:
        return None
    stack = cotton_data.get("stack", [])
    if not stack:
        return None

    stack_length = len(stack)

    parent_idx = stack_length - 2  # Get the index of the parent element

    # this will ONLY return attrs declared on the component itself, not c-vars
    return stack[parent_idx]["attrs"]


@register.simple_tag(takes_context=True)
def responsive(context, root: str, attrs=None):
    """Generate responsive Bootstrap grid classes from context variables.

    This tag generates responsive variants of a root class name (e.g., 'col')
    by combining it with responsive breakpoint suffixes (xs, sm, md, lg, xl, xxl).
    Context variables for each breakpoint determine whether the suffix is included
    and its value.

    Args:
        context (dict): Django template context, expected to contain optional keys:
            - xs (str): Extra small breakpoint value
            - sm (str): Small breakpoint value
            - md (str): Medium breakpoint value
            - lg (str): Large breakpoint value
            - xl (str): Extra large breakpoint value
            - xxl (str): Extra extra large breakpoint value
        root (str): Base class name to which responsive variants are appended
                    (e.g., 'col', 'offset', 'gutter')

    Returns:
        str: Space-separated responsive class names. For each breakpoint variable
             present in context, returns "{root}-{breakpoint}-{value}".
             Returns empty string if no breakpoint variables are defined.

    Example:
        Context: {'md': '6', 'lg': '4', 'xl': '3'}
        Tag:     {% responsive 'col' %}
        Output:  'col-md-6 col-lg-4 col-xl-3'
    """
    # The idea is to take a root class name (e.g., "col") and
    # and generate responsive variants based on context variables xs, sm, md, lg, xl, xxl).
    # If an attrs variable is present, it should be the value should be added to root along with the responsive
    # name (e.g., "col-md-6").
    attrs = attrs or context.get("attrs", {})
    if not attrs:
        return ""
    responsive_values = {
        responsive: attrs.get(responsive)
        for responsive in ["xs", "sm", "md", "lg", "xl", "xxl"]
    }

    return " ".join(
        f"{root}-{key}-{value}"
        for key, value in responsive_values.items()
        if value is not None
    )


@register.tag(name="show_code")
def show_code(parser, token):
    """Parse the show_code block tag.

    Collects the template content between {% show_code %} and {% endshow_code %} tags
    for processing and rendering.

    Args:
        parser: Django template parser
        token: Template token with tag name

    Returns:
        ShowCodeNode: Node instance that will handle rendering
    """
    nodelist = parser.parse(("endshow_code",))
    parser.delete_first_token()
    return ShowCodeNode(nodelist)


class ShowCodeNode(template.Node):
    """Template node for the show_code tag.

    Processes template content to display both executable code and its rendered output.
    Handles indentation normalization, HTML escaping, Cotton template compilation,
    and HTML rendering.

    Attributes:
        nodelist (NodeList): Template nodes between show_code block start and end tags
    """

    def __init__(self, nodelist):
        """Initialize the node with template content.

        Args:
            nodelist: Template node list from parser between block tags
        """
        self.nodelist = nodelist

    def render(self, context):
        """Render the code block with normalized formatting and display.

        Processes the captured template content through the following steps:
        1. Render the template content to raw text
        2. Normalize indentation (remove common leading whitespace)
        3. Remove leading/trailing blank lines
        4. Escape HTML special characters for safe display
        5. Compile Cotton template syntax
        6. Execute the compiled template
        7. Display both formatted code and rendered output side-by-side

        Args:
            context: Django template context for rendering

        Returns:
            str: HTML markup displaying the code and its rendered result
        """
        raw = self.nodelist.render(context)

        # Beautifulsoup does annoying things to the Cotton syntax, so we'll skip that step and clean ourselves
        # soup = BeautifulSoup(raw, "html.parser")
        # cleaned = soup.prettify(formatter="html5")

        cleaned = textwrap.dedent(raw).strip("\n")

        # 3. Escape Cotton syntax for HTML display in code tag
        code = escape(cleaned)

        # 4. Compile Cotton syntax
        compiled = compiler.process(cleaned)

        # 5. Render the compiled template
        t = template.Template(compiled)
        rendered_raw = t.render(context)

        # 6. Clean the rendered HTML using BeautifulSoup for proper formatting
        if not HAS_BEAUTIFULSOUP:
            raise ImportError(
                "BeautifulSoup4 is required for the show_code template tag. "
                "Install it with: pip install beautifulsoup4"
            )

        soup = BeautifulSoup(rendered_raw, "html.parser")
        rendered_cleaned = soup.prettify()

        # rendered_cleaned = textwrap.dedent(rendered_raw).strip("\n")
        # rendered_cleaned = re.sub(r'\n\s*\n(\s*\n)+', '\n\n', rendered_cleaned)

        # Remove excessive blank lines (more than one consecutive blank line)
        # rendered_cleaned = rendered_cleaned.strip()

        # 7. Mark safe for actual rendering on page
        rendered = mark_safe(rendered_cleaned)

        # 8. Escape cleaned HTML for display in code tag
        html = escape(rendered_cleaned)

        return render_to_string(
            "cotton_bs5/document_component.html",
            {"code": code, "rendered": rendered, "html": html},
        )
