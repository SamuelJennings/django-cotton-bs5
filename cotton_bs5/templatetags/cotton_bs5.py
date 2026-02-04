"""Template tags and filters for MVP navbar widgets."""

import textwrap

from django import template
from django.template.loader import render_to_string
from django.utils.html import escape
from django_cotton.compiler_regex import CottonCompiler

register = template.Library()

compiler = CottonCompiler()


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


@register.simple_tag(takes_context=True)
def responsive(context, root: str):
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
    # If a context variable is present, the value should be added to root along with the responsive
    # name (e.g., "col-md-6").

    responsive_values = {
        responsive: context.get(responsive)
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

        # 1. Normalize indentation
        dedented = textwrap.dedent(raw)

        # 2. Remove leading/trailing blank lines
        cleaned = dedented.strip("\n")

        # 3. Escape for HTML
        escaped = escape(cleaned)

        compiled = compiler.process(cleaned)

        t = template.Template(compiled)
        rendered = t.render(context)
        return render_to_string(
            "cotton_bs5/document_component.html",
            {"code": escaped, "rendered": rendered},
        )
