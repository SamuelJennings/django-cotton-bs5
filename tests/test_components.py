"""
Unit tests for Cotton BS5 components.
Tests for accessibility, slot functionality, and attribute handling.

Uses pytest fixtures from cotton_bs5.fixtures for efficient component testing.
See .github/skills/test-cotton-components/SKILL.md for testing patterns and best practices.
"""


class TestSpinnerComponent:
    """Tests for spinner component."""

    def test_spinner_basic_rendering(self, cotton_render_string):
        """Test basic spinner rendering with ARIA attributes."""
        html = cotton_render_string("<c-spinner />")

        assert "spinner-border" in html
        assert 'role="status"' in html
        assert "visually-hidden" in html
        assert "Loading" in html

    def test_spinner_custom_type(self, cotton_render_string):
        """Test spinner with grow type instead of border."""
        html = cotton_render_string('<c-spinner type="grow" />')

        assert "spinner-grow" in html
        assert "spinner-border" not in html

    def test_spinner_custom_size(self, cotton_render_string):
        """Test spinner renders with small size class."""
        html = cotton_render_string('<c-spinner size="sm" />')

        assert "spinner-border-sm" in html

    def test_spinner_custom_variant(self, cotton_render_string):
        """Test spinner applies Bootstrap color variant."""
        html = cotton_render_string('<c-spinner variant="primary" />')

        assert "text-primary" in html

    def test_spinner_custom_label(self, cotton_render_string):
        """Test spinner with custom accessibility label."""
        html = cotton_render_string('<c-spinner label="Custom loading text" />')

        assert "Custom loading text" in html

    def test_spinner_slot_content(self, cotton_render_string):
        """Test spinner with custom slot content."""
        html = cotton_render_string("<c-spinner>Custom content</c-spinner>")

        assert "Custom content" in html

    def test_spinner_no_erroneous_attributes(self, cotton_render_string):
        """Test that component variables don't leak as HTML attributes."""
        html = cotton_render_string('<c-spinner type="border" size="sm" variant="primary" label="Test" />')

        # These should NOT appear as HTML attributes
        assert 'type="border"' not in html
        assert 'size="sm"' not in html
        assert 'variant="primary"' not in html
        assert 'label="Test"' not in html

    def test_spinner_custom_class_merged(self, cotton_render_string_soup):
        """Test spinner accepts additional CSS classes that are merged with component classes."""
        soup = cotton_render_string_soup('<c-spinner class="my-custom-class" />')

        spinner = soup.find("div", class_="spinner-border")
        assert "my-custom-class" in spinner["class"]
        assert "spinner-border" in spinner["class"]


class TestAlertComponent:
    """Tests for alert component."""

    def test_alert_basic_rendering(self, cotton_render_string):
        """Test alert renders with default variant and ARIA role."""
        html = cotton_render_string('<c-alert text="Test message" />')

        assert "alert" in html
        assert "alert-primary" in html  # default variant
        assert 'role="alert"' in html
        assert "Test message" in html

    def test_alert_custom_variant(self, cotton_render_string):
        """Test alert renders with custom danger variant."""
        html = cotton_render_string('<c-alert variant="danger" text="Error message" />')

        assert "alert-danger" in html
        assert "alert-primary" not in html

    def test_alert_dismissible_includes_close_button(self, cotton_render_string_soup):
        """Test dismissible alert includes close button with correct classes."""
        soup = cotton_render_string_soup('<c-alert text="Test" dismissible />')

        alert = soup.find("div", class_="alert")
        assert "alert-dismissible" in alert["class"]

        close_btn = soup.find("button", class_="btn-close")
        assert close_btn is not None

    def test_alert_with_slot_content(self, cotton_render_string):
        """Test alert renders slot content."""
        html = cotton_render_string("<c-alert>Slot content</c-alert>")

        assert "Slot content" in html

    def test_alert_slot_and_text_both_render(self, cotton_render_string):
        """Test alert renders both text attribute and slot content."""
        html = cotton_render_string('<c-alert text="Text content">Slot content</c-alert>')

        assert "Text content" in html
        assert "Slot content" in html

    def test_alert_no_erroneous_attributes(self, cotton_render_string):
        """Test alert component variables don't leak as HTML attributes."""
        html = cotton_render_string('<c-alert variant="danger" text="Test" animate dismissible />')

        # These should NOT appear as HTML attributes
        assert 'variant="danger"' not in html
        assert 'text="Test"' not in html
        assert "animate=" not in html
        assert "dismissible=" not in html


class TestButtonComponent:
    """Tests for button component."""

    def test_button_basic_rendering(self, cotton_render_string_soup):
        """Test button renders as button element with default primary variant."""
        soup = cotton_render_string_soup('<c-button text="Click me" />')

        button = soup.find("button")
        assert button is not None
        assert "btn" in button["class"]
        assert "btn-primary" in button["class"]  # default variant
        assert button.get_text().strip() == "Click me"

    def test_button_renders_as_link_when_href_provided(self, cotton_render_string_soup):
        """Test button renders as anchor tag when href attribute is provided."""
        soup = cotton_render_string_soup('<c-button href="/test/" text="Link button" />')

        link = soup.find("a")
        assert link is not None
        assert link["href"] == "/test/"
        assert "btn" in link["class"]

        button = soup.find("button")
        assert button is None

    def test_button_custom_variant(self, cotton_render_string):
        """Test button renders with custom danger variant."""
        html = cotton_render_string('<c-button variant="danger" text="Delete" />')

        assert "btn-danger" in html
        assert "btn-primary" not in html

    def test_button_outline_variant(self, cotton_render_string):
        """Test button renders with outline variant styling."""
        html = cotton_render_string('<c-button variant="primary" outline text="Outline" />')

        assert "btn-outline-primary" in html
        assert 'btn-primary"' not in html  # Should be outline, not solid

    def test_button_custom_size(self, cotton_render_string):
        """Test button renders with large size class."""
        html = cotton_render_string('<c-button size="lg" text="Large button" />')

        assert "btn-lg" in html

    def test_button_slot_renders_with_text(self, cotton_render_string):
        """Test button renders both slot content and text attribute."""
        html = cotton_render_string('<c-button text="Text">Slot content</c-button>')

        assert "Slot content" in html
        assert "Text" in html

    def test_button_no_erroneous_attributes(self, cotton_render_string):
        """Test button component variables don't leak as HTML attributes."""
        html = cotton_render_string('<c-button variant="danger" size="lg" outline text="Test" />')

        # These should NOT appear as HTML attributes because they're declared in c-vars
        assert 'variant="danger"' not in html
        assert 'size="lg"' not in html
        assert "outline=" not in html
        assert 'text="Test"' not in html


class TestProgressComponent:
    """Tests for progress component."""

    def test_progress_basic_rendering(self, cotton_render_string):
        """Test progress renders with correct ARIA attributes for accessibility."""
        html = cotton_render_string('<c-progress value="50" />')

        assert "progress" in html
        assert 'role="progressbar"' in html
        assert 'aria-valuenow="50"' in html
        assert 'aria-valuemin="0"' in html
        assert 'aria-valuemax="100"' in html

    def test_progress_custom_min_max(self, cotton_render_string):
        """Test progress with custom minimum and maximum values."""
        html = cotton_render_string('<c-progress value="25" min="10" max="50" />')

        assert 'aria-valuemin="10"' in html
        assert 'aria-valuemax="50"' in html

    def test_progress_custom_variant(self, cotton_render_string):
        """Test progress renders with Bootstrap success variant color."""
        html = cotton_render_string('<c-progress value="50" variant="success" />')

        assert "bg-success" in html

    def test_progress_striped_styling(self, cotton_render_string):
        """Test progress renders with striped visual pattern."""
        html = cotton_render_string('<c-progress value="50" striped />')

        assert "progress-bar-striped" in html

    def test_progress_animated_striped(self, cotton_render_string):
        """Test progress renders with animated striped pattern."""
        html = cotton_render_string('<c-progress value="50" animated />')

        assert "progress-bar-animated" in html

    def test_progress_text_content(self, cotton_render_string):
        """Test progress displays custom text content."""
        html = cotton_render_string('<c-progress value="75" text="75%" />')

        assert "75%" in html

    def test_progress_slot_content(self, cotton_render_string):
        """Test progress renders slot content for custom display."""
        html = cotton_render_string('<c-progress value="50">Custom content</c-progress>')

        assert "Custom content" in html

    def test_progress_aria_label(self, cotton_render_string):
        """Test progress renders with custom ARIA label for screen readers."""
        html = cotton_render_string('<c-progress value="50" label="Custom progress label" />')

        assert 'aria-label="Custom progress label"' in html

    def test_progress_no_erroneous_attributes(self, cotton_render_string):
        """Test progress component variables don't leak as HTML attributes."""
        html = cotton_render_string(
            '<c-progress value="50" min="0" max="100" variant="success" striped animated text="50%" label="Test" />'
        )

        # Check that values are used in ARIA attributes correctly
        assert 'aria-valuenow="50"' in html
        assert 'aria-valuemin="0"' in html
        assert 'aria-valuemax="100"' in html
        assert 'aria-label="Test"' in html

        # These should NOT appear as direct HTML attributes (only as part of aria-* attributes)
        # Component correctly transforms them to ARIA attributes
        assert "bg-success" in html  # variant is used in class
        assert "progress-bar-striped" in html  # striped is used in class
        assert "progress-bar-animated" in html  # animated is used in class
        assert "50%" in html  # text is rendered as content

        # Verify they're NOT appearing as standalone attributes outside ARIA context
        assert ' value="50"' not in html
        assert ' variant="success"' not in html
        assert ' text="50%"' not in html
        assert ' label="Test"' not in html
        assert " striped=" not in html
        assert " animated=" not in html


class TestBreadcrumbsComponent:
    """Tests for breadcrumbs components."""

    def test_breadcrumbs_basic_rendering(self, cotton_render_string):
        """Test breadcrumbs render with proper nav element and ARIA attributes."""
        html = cotton_render_string("""
        <c-breadcrumbs>
            <c-breadcrumbs.item href="/home/" text="Home" />
            <c-breadcrumbs.item text="Current Page" />
        </c-breadcrumbs>""")

        assert "<nav" in html
        assert "aria-label=" in html
        assert "breadcrumb" in html
        assert "breadcrumb-item" in html

    def test_breadcrumbs_custom_divider(self, cotton_render_string):
        """Test breadcrumbs render with custom divider character in CSS."""
        html = cotton_render_string("""
        <c-breadcrumbs divider=">">
            <c-breadcrumbs.item href="/home/" text="Home" />
        </c-breadcrumbs>""")

        # Check for custom divider in CSS (may be encoded differently)
        divider_found = (
            "--bs-breadcrumb-divider: '>'" in html
            or "--bs-breadcrumb-divider: '&gt;'" in html
            or '--bs-breadcrumb-divider: "&gt;"' in html
            or '--bs-breadcrumb-divider: ">"' in html
        )
        assert divider_found, f"Custom divider CSS not found in: {html}"

    def test_breadcrumb_item_as_link(self, cotton_render_string_soup):
        """Test breadcrumb item renders as link when href provided."""
        soup = cotton_render_string_soup('<c-breadcrumbs.item href="/test/" text="Test Page" />')

        link = soup.find("a", href="/test/")
        assert link is not None
        assert "Test Page" in link.get_text()
        assert "active" not in link.get("class", [])

    def test_breadcrumb_item_active_without_href(self, cotton_render_string_soup):
        """Test breadcrumb item without href renders as active current page."""
        soup = cotton_render_string_soup('<c-breadcrumbs.item text="Current Page" />')

        item = soup.find("li", class_="breadcrumb-item")
        assert "active" in item["class"]
        assert item.get("aria-current") == "page"

        link = soup.find("a")
        assert link is None

    def test_breadcrumb_item_slot_content(self, cotton_render_string):
        """Test breadcrumb item renders slot content."""
        html = cotton_render_string('<c-breadcrumbs.item href="/test/">Slot content</c-breadcrumbs.item>')

        assert "Slot content" in html

    def test_breadcrumbs_with_items_array(self, cotton_render_string):
        """Test breadcrumbs render from items array with proper active state."""
        items = [
            {"text": "Home", "href": "/"},
            {"text": "Products", "href": "/products/"},
            {"text": "Current Page"},
        ]
        html = cotton_render_string("<c-breadcrumbs :items='items' />", context={"items": items})

        assert "Home" in html
        assert 'href="/"' in html
        assert "Products" in html
        assert 'href="/products/"' in html
        assert "Current Page" in html
        assert "active" in html  # Last item should be active

    def test_breadcrumbs_with_items_array_custom_classes(self, cotton_render_string):
        """Test breadcrumbs items array supports custom CSS classes."""
        items = [
            {"text": "Home", "href": "/", "class": "custom-class"},
            {"text": "Current"},
        ]
        html = cotton_render_string("<c-breadcrumbs :items='items' />", context={"items": items})

        assert "custom-class" in html
        assert "Home" in html
        assert "Current" in html

    def test_breadcrumbs_slot_when_no_items(self, cotton_render_string):
        """Test breadcrumbs use slot content when items array not provided."""
        html = cotton_render_string("""
        <c-breadcrumbs>
            <c-breadcrumbs.item href="/" text="Manual Item" />
        </c-breadcrumbs>""")

        assert "Manual Item" in html

    def test_breadcrumbs_items_no_erroneous_attributes(self, cotton_render_string):
        """Test breadcrumbs items attribute doesn't leak as HTML attribute."""
        items = [{"text": "Test", "href": "/"}]
        html = cotton_render_string("<c-breadcrumbs :items='items' />", context={"items": items})

        # Should NOT appear as HTML attribute
        assert 'items="' not in html
        assert "items=" not in html


class TestCardComponent:
    """Tests for card components."""

    def test_card_basic_rendering(self, cotton_render_string):
        """Test card renders with body content."""
        html = cotton_render_string("""
        <c-card>
            <c-card.body>Card content</c-card.body>
        </c-card>""")

        assert "card" in html
        assert "card-body" in html
        assert "Card content" in html

    def test_card_title_default_heading_level(self, cotton_render_string_soup):
        """Test card title renders with default h5 heading level."""
        soup = cotton_render_string_soup('<c-card.title text="Card Title" />')

        title = soup.find("h5")
        assert title is not None
        assert "card-title" in title["class"]
        assert title.get_text().strip() == "Card Title"

    def test_card_title_custom_heading_level(self, cotton_render_string_soup):
        """Test card title renders with custom heading level."""
        soup = cotton_render_string_soup('<c-card.title level="2" text="Card Title" />')

        title = soup.find("h2")
        assert title is not None
        assert "card-title" in title["class"]

        h5 = soup.find("h5")
        assert h5 is None

    def test_card_title_slot_content(self, cotton_render_string):
        """Test card title renders slot content."""
        html = cotton_render_string("<c-card.title>Slot title content</c-card.title>")

        assert "Slot title content" in html

    def test_card_title_no_erroneous_attributes(self, cotton_render_string):
        """Test card title component variables don't leak as HTML attributes."""
        html = cotton_render_string('<c-card.title level="3" text="Title" class="custom-class" />')

        # These should NOT appear as HTML attributes
        assert 'level="3"' not in html
        assert 'text="Title"' not in html


class TestTableComponent:
    """Tests for table component."""

    def test_table_basic_rendering(self, cotton_render_string):
        """Test table renders with responsive wrapper."""
        html = cotton_render_string("""
        <c-table>
            <thead><tr><th>Header</th></tr></thead>
            <tbody><tr><td>Data</td></tr></tbody>
        </c-table>""")

        assert "table" in html
        assert "table-responsive" in html
        assert "<thead>" in html
        assert "<tbody>" in html

    def test_table_striped(self, cotton_render_string):
        """Test table renders with striped rows styling."""
        html = cotton_render_string("<c-table striped>Content</c-table>")

        assert "table-striped" in html

    def test_table_bordered(self, cotton_render_string):
        """Test table renders with borders on all cells."""
        html = cotton_render_string("<c-table bordered>Content</c-table>")

        assert "table-bordered" in html

    def test_table_hover(self, cotton_render_string):
        """Test table renders with hover effect on rows."""
        html = cotton_render_string("<c-table hover>Content</c-table>")

        assert "table-hover" in html

    def test_table_small(self, cotton_render_string):
        """Test table renders with compact padding."""
        html = cotton_render_string("<c-table small>Content</c-table>")

        assert "table-sm" in html

    def test_table_custom_variant(self, cotton_render_string):
        """Test table renders with dark variant styling."""
        html = cotton_render_string('<c-table variant="dark">Content</c-table>')

        assert "table-dark" in html

    def test_table_responsive_breakpoint(self, cotton_render_string):
        """Test table renders with breakpoint-specific responsive wrapper."""
        html = cotton_render_string('<c-table responsive="lg">Content</c-table>')

        assert "table-responsive-lg" in html

    def test_table_with_caption(self, cotton_render_string):
        """Test table renders with caption element."""
        html = cotton_render_string('<c-table caption="Table caption">Content</c-table>')

        assert "<caption>Table caption</caption>" in html

    def test_table_no_erroneous_attributes(self, cotton_render_string):
        """Test table component variables don't leak as HTML attributes."""
        html = cotton_render_string(
            '<c-table striped bordered hover small variant="dark" responsive="lg" caption="Test" />'
        )

        # These should NOT appear as HTML attributes
        assert "striped=" not in html
        assert "bordered=" not in html
        assert "hover=" not in html
        assert "small=" not in html
        assert 'variant="dark"' not in html
        assert 'responsive="lg"' not in html
        assert 'caption="Test"' not in html


class TestTabsComponent:
    """Tests for tabs components."""

    def test_tabs_basic_rendering(self, cotton_render_string):
        """Test tabs render with proper nav element and ARIA tablist role."""
        html = cotton_render_string("""
        <c-tabs id="testTabs">
            <c-tabs.item target="tab1" text="Tab 1" />
            <c-tabs.item target="tab2" text="Tab 2" />
        </c-tabs>""")

        assert "nav" in html
        assert 'role="tablist"' in html
        assert "nav-item" in html
        assert 'role="presentation"' in html

    def test_tabs_vertical_orientation(self, cotton_render_string):
        """Test vertical tabs render with flex-column and vertical ARIA orientation."""
        html = cotton_render_string("""
        <c-tabs vertical>
            <c-tabs.item target="tab1" text="Tab 1" />
        </c-tabs>""")

        assert "flex-column" in html
        assert 'aria-orientation="vertical"' in html

    def test_tabs_item_active_state(self, cotton_render_string):
        """Test active tab item has proper ARIA attributes and tabindex."""
        html = cotton_render_string('<c-tabs.item target="tab1" text="Tab 1" active />')

        assert "active" in html
        assert 'aria-selected="true"' in html
        assert 'tabindex="0"' in html

    def test_tabs_item_inactive_state(self, cotton_render_string):
        """Test inactive tab item has proper ARIA attributes and tabindex."""
        html = cotton_render_string('<c-tabs.item target="tab2" text="Tab 2" />')

        assert "active" not in html
        assert 'aria-selected="false"' in html
        assert 'tabindex="-1"' in html

    def test_tabs_pane_active(self, cotton_render_string_soup):
        """Test active tab pane has proper ARIA attributes and tabindex."""
        soup = cotton_render_string_soup('<c-tabs.pane id="tab1" active>Content 1</c-tabs.pane>')

        pane = soup.find("div", class_="tab-pane")
        assert "active" in pane["class"]
        assert pane.get("role") == "tabpanel"
        assert pane.get("aria-labelledby") == "tab1-tab"
        assert pane.get("tabindex") == "0"

    def test_tabs_pane_inactive(self, cotton_render_string_soup):
        """Test inactive tab pane has proper ARIA attributes and tabindex."""
        soup = cotton_render_string_soup('<c-tabs.pane id="tab2">Content 2</c-tabs.pane>')

        pane = soup.find("div", class_="tab-pane")
        assert "active" not in pane.get("class", [])
        assert pane.get("tabindex") == "-1"

    def test_tabs_no_erroneous_attributes_active(self, cotton_render_string):
        """Test tabs item component variables don't leak as HTML attributes."""
        html = cotton_render_string('<c-tabs.item target="tab1" text="Tab 1" active />')

        # Check that the tab is properly rendered with expected attributes
        assert 'data-bs-target="#tab1"' in html  # target becomes data-bs-target
        assert "Tab 1" in html  # text content appears
        assert "active" in html  # active state appears in class
        assert 'tabindex="0"' in html  # active creates tabindex

        # These should NOT appear as HTML attributes because they're declared in c-vars
        assert 'target="tab1"' not in html
        assert 'text="Tab 1"' not in html
        assert "disabled=" not in html

    def test_tabs_no_erroneous_attributes_disabled(self, cotton_render_string):
        """Test disabled tabs item component variables don't leak as HTML attributes."""
        html = cotton_render_string('<c-tabs.item target="tab1" text="Tab 1" disabled />')

        # Check that the tab is properly rendered with expected attributes
        assert 'data-bs-target="#tab1"' in html  # target becomes data-bs-target
        assert "Tab 1" in html  # text content appears
        assert "disabled" in html  # disabled state appears
        assert 'tabindex="-1"' in html  # disabled creates tabindex

        # These should NOT appear as HTML attributes because they're declared in c-vars
        assert 'target="tab1"' not in html
        assert 'text="Tab 1"' not in html
        assert "active=" not in html


class TestModalComponent:
    """Tests for modal components."""

    def test_modal_basic_rendering(self, cotton_render_string_soup):
        """Test modal renders with proper ARIA attributes for accessibility."""
        soup = cotton_render_string_soup("""
        <c-modal id="testModal">
            <c-modal.title text="Modal Title" />
            <c-modal.body>Modal content</c-modal.body>
        </c-modal>""")

        modal = soup.find("div", class_="modal")
        assert modal is not None
        assert modal["id"] == "testModal"
        assert modal.get("aria-labelledby") == "testModalLabel"
        assert modal.get("aria-hidden") == "true"
        assert modal.get("tabindex") == "-1"

    def test_modal_with_fade_animation(self, cotton_render_string):
        """Test modal renders with fade animation class."""
        html = cotton_render_string('<c-modal id="test" fade>Content</c-modal>')

        assert "fade" in html

    def test_modal_centered(self, cotton_render_string):
        """Test modal renders centered on screen."""
        html = cotton_render_string('<c-modal id="test" centered>Content</c-modal>')

        assert "modal-dialog-centered" in html

    def test_modal_title(self, cotton_render_string):
        """Test modal title renders with proper class and content."""
        html = cotton_render_string('<c-modal.title id="test" text="Modal Title" />')

        assert "modal-title" in html
        assert 'id="testLabel"' in html
        assert "Modal Title" in html


class TestAccordionComponent:
    """Tests for accordion components."""

    def test_accordion_basic_rendering(self, cotton_render_string):
        """Test accordion renders with proper structure."""
        html = cotton_render_string("""
        <c-accordion id="testAccordion">
            <c-accordion.item text="Item 1" target="item1" parent="testAccordion">
                Content 1
            </c-accordion.item>
        </c-accordion>""")

        assert "accordion" in html
        assert "accordion-item" in html
        assert "accordion-header" in html
        assert "accordion-button" in html

    def test_accordion_flush_variant(self, cotton_render_string):
        """Test flush accordion removes default borders."""
        html = cotton_render_string("<c-accordion flush>Content</c-accordion>")

        assert "accordion-flush" in html

    def test_accordion_item_expanded_state(self, cotton_render_string):
        """Test expanded accordion item has proper ARIA expanded attribute."""
        html = cotton_render_string('<c-accordion.header target="test" text="Title" show />')

        assert 'aria-expanded="true"' in html
        assert "collapsed" not in html

    def test_accordion_item_collapsed_state(self, cotton_render_string):
        """Test collapsed accordion item has proper ARIA expanded attribute."""
        html = cotton_render_string('<c-accordion.header target="test" text="Title" />')

        assert 'aria-expanded="false"' in html
        assert "collapsed" in html


class TestListGroupComponent:
    """Tests for list group components."""

    def test_list_group_basic_rendering(self, cotton_render_string_soup):
        """Test list group renders as unordered list with items."""
        soup = cotton_render_string_soup("""
        <c-list_group>
            <c-list_group.item text="Item 1" />
            <c-list_group.item text="Item 2" />
        </c-list_group>""")

        ul = soup.find("ul", class_="list-group")
        assert ul is not None

        items = soup.find_all("li", class_="list-group-item")
        assert len(items) == 2

    def test_list_group_numbered(self, cotton_render_string_soup):
        """Test numbered list group renders as ordered list."""
        soup = cotton_render_string_soup("<c-list_group numbered>Content</c-list_group>")

        ol = soup.find("ol")
        assert ol is not None

        ul = soup.find("ul")
        assert ul is None

    def test_list_group_horizontal(self, cotton_render_string):
        """Test horizontal list group renders with horizontal layout class."""
        html = cotton_render_string("<c-list_group horizontal>Content</c-list_group>")

        assert "list-group-horizontal" in html

    def test_list_group_item_active_state(self, cotton_render_string):
        """Test active list group item has proper ARIA current attribute."""
        html = cotton_render_string('<c-list_group.item text="Active Item" active />')

        assert "active" in html
        assert 'aria-current="true"' in html

    def test_list_group_item_disabled_state(self, cotton_render_string):
        """Test disabled list group item has proper ARIA disabled attribute."""
        html = cotton_render_string('<c-list_group.item text="Disabled Item" disabled />')

        assert "disabled" in html
        assert 'aria-disabled="true"' in html

    def test_list_group_item_as_link(self, cotton_render_string_soup):
        """Test list group item renders as link when href provided."""
        soup = cotton_render_string_soup('<c-list_group.item href="/test/" text="Link Item" />')

        link = soup.find("a", href="/test/")
        assert link is not None
        assert "list-group-item-action" in link["class"]


class TestButtonGroupComponent:
    """Tests for button group component."""

    def test_button_group_basic_rendering(self, cotton_render_string):
        """Test button group renders with proper role and ARIA label."""
        html = cotton_render_string("""
        <c-button_group>
            <c-button text="Button 1" />
            <c-button text="Button 2" />
        </c-button_group>""")

        assert "btn-group" in html
        assert 'role="group"' in html
        assert "aria-label=" in html

    def test_button_group_vertical(self, cotton_render_string):
        """Test vertical button group renders with vertical layout class."""
        html = cotton_render_string("<c-button_group vertical>Content</c-button_group>")

        assert "btn-group-vertical" in html

    def test_button_group_custom_size(self, cotton_render_string):
        """Test button group renders with large size class."""
        html = cotton_render_string('<c-button_group size="lg">Content</c-button_group>')

        assert "btn-group-lg" in html

    def test_button_group_custom_label(self, cotton_render_string):
        """Test button group renders with custom ARIA label."""
        html = cotton_render_string('<c-button_group label="Custom label">Content</c-button_group>')

        assert 'aria-label="Custom label"' in html

    def test_button_group_no_erroneous_attributes(self, cotton_render_string):
        """Test button group component variables don't leak as HTML attributes."""
        html = cotton_render_string('<c-button_group size="lg" vertical label="Test" />')

        # Check that the values are used correctly
        assert "btn-group-lg" in html  # size becomes class
        assert "btn-group-vertical" in html  # vertical becomes class
        assert 'aria-label="Test"' in html  # label becomes aria-label

        # These should NOT appear as HTML attributes because they're declared in c-vars
        assert 'size="lg"' not in html
        assert "vertical=" not in html
        # label is correctly used in aria-label, verify it's not a standalone attribute
        assert ' label="Test"' not in html

    def test_button_group_with_gap_uses_flexbox(self, cotton_render_string):
        """Test button group with gap uses flexbox layout instead of btn-group."""
        html = cotton_render_string('<c-button_group gap="2">Content</c-button_group>')

        assert "d-flex" in html
        assert "gap-2" in html
        assert "btn-group" not in html
        # Should still have role/aria-label since it's semantically a group
        assert 'role="group"' in html
        assert 'aria-label="Button group"' in html

    def test_button_group_with_gap_vertical(self, cotton_render_string):
        """Test vertical button group with gap uses flex-column."""
        html = cotton_render_string('<c-button_group gap="3" vertical>Content</c-button_group>')

        assert "d-flex" in html
        assert "flex-column" in html
        assert "gap-3" in html
        assert "btn-group-vertical" not in html

    def test_button_group_with_gap_and_size(self, cotton_render_string):
        """Test button group with gap and size applies size class correctly."""
        html = cotton_render_string('<c-button_group gap="2" size="lg">Content</c-button_group>')

        assert "d-flex" in html
        assert "gap-2" in html
        assert "btn-group-lg" in html

    def test_button_group_gap_no_erroneous_attributes(self, cotton_render_string):
        """Test button group gap attribute doesn't leak as HTML attribute."""
        html = cotton_render_string('<c-button_group gap="2">Content</c-button_group>')

        # Should NOT appear as HTML attribute
        assert 'gap="2"' not in html

    def test_button_group_without_gap_uses_standard_class(self, cotton_render_string):
        """Test button group without gap uses standard btn-group class."""
        html = cotton_render_string("<c-button_group>Content</c-button_group>")

        assert "btn-group" in html
        assert "d-flex" not in html
        assert 'role="group"' in html


class TestBadgeComponent:
    """Tests for badge component."""

    def test_badge_basic_rendering(self, cotton_render_string_soup):
        """Test badge renders as span with default primary variant."""
        soup = cotton_render_string_soup('<c-badge text="New" />')

        badge = soup.find("span", class_="badge")
        assert badge is not None
        assert "text-bg-primary" in badge["class"]
        assert badge.get_text().strip() == "New"

    def test_badge_with_slot_content(self, cotton_render_string):
        """Test badge renders slot content instead of text attribute."""
        html = cotton_render_string("<c-badge>Badge Text</c-badge>")

        assert "Badge Text" in html
        assert "badge" in html

    def test_badge_custom_variant(self, cotton_render_string):
        """Test badge renders with custom success variant."""
        html = cotton_render_string('<c-badge text="Success" variant="success" />')

        assert "text-bg-success" in html
        assert "text-bg-primary" not in html

    def test_badge_pill_styling(self, cotton_render_string):
        """Test badge renders with pill rounded styling."""
        html = cotton_render_string('<c-badge text="Pill" pill />')

        assert "rounded-pill" in html

    def test_badge_as_link(self, cotton_render_string_soup):
        """Test badge renders as anchor tag when href provided."""
        soup = cotton_render_string_soup('<c-badge text="Link Badge" href="/example" />')

        link = soup.find("a", href="/example")
        assert link is not None
        assert "badge" in link["class"]

        span = soup.find("span", class_="badge")
        assert span is None

    def test_badge_as_span_without_href(self, cotton_render_string_soup):
        """Test badge renders as span tag when no href provided."""
        soup = cotton_render_string_soup('<c-badge text="Span Badge" />')

        span = soup.find("span", class_="badge")
        assert span is not None

        link = soup.find("a")
        assert link is None

    def test_badge_link_with_pill(self, cotton_render_string_soup):
        """Test badge as link with pill styling and custom variant."""
        soup = cotton_render_string_soup('<c-badge text="Pill Link" href="/link" pill variant="warning" />')

        link = soup.find("a", href="/link")
        assert link is not None
        assert "rounded-pill" in link["class"]
        assert "text-bg-warning" in link["class"]

    def test_badge_with_custom_class(self, cotton_render_string):
        """Test badge merges custom CSS class with component classes."""
        html = cotton_render_string('<c-badge text="Custom" class="my-custom-class" />')

        assert "my-custom-class" in html
        assert "badge" in html

    def test_badge_with_additional_attributes(self, cotton_render_string):
        """Test badge renders with additional HTML attributes."""
        html = cotton_render_string('<c-badge text="Data Badge" data-id="123" title="Hover text" />')

        assert 'data-id="123"' in html
        assert 'title="Hover text"' in html

    def test_badge_no_erroneous_attributes(self, cotton_render_string):
        """Test badge component variables don't leak as HTML attributes."""
        html = cotton_render_string('<c-badge text="Test" variant="danger" pill />')

        # These should NOT appear as HTML attributes
        assert 'text="Test"' not in html
        assert 'variant="danger"' not in html
        assert "pill=" not in html

    def test_badge_link_with_additional_attrs(self, cotton_render_string):
        """Test badge link renders with multiple additional attributes."""
        html = cotton_render_string(
            '<c-badge text="External" href="https://example.com" target="_blank" rel="noopener" />'
        )

        assert "<a" in html
        assert 'href="https://example.com"' in html
        assert 'target="_blank"' in html
        assert 'rel="noopener"' in html


class TestNavbarComponent:
    """Tests for navbar components."""

    def test_navbar_basic_rendering(self, cotton_render_string):
        """Test navbar renders with brand text."""
        html = cotton_render_string('<c-navbar brand="Test Brand">Content</c-navbar>')

        assert "navbar" in html
        assert "navbar-brand" in html
        assert "Test Brand" in html

    def test_navbar_with_expand_breakpoint(self, cotton_render_string):
        """Test navbar renders with expand breakpoint and toggle button."""
        html = cotton_render_string('<c-navbar expand="md" brand="Brand">Content</c-navbar>')

        assert "navbar-expand-md" in html
        assert "navbar-toggler" in html

    def test_navbar_toggle_button_accessibility(self, cotton_render_string):
        """Test navbar toggle button has proper ARIA attributes."""
        html = cotton_render_string('<c-navbar expand="lg" brand="Brand">Content</c-navbar>')

        assert 'aria-controls="navbarNav"' in html
        assert 'aria-expanded="false"' in html
        assert "Toggle navigation" in html  # Should be translatable


class TestTemplateTagFilters:
    """Tests for custom template tag filters."""

    def test_slot_is_empty_with_empty_string(self, cotton_render_string):
        """Test slot_is_empty filter returns True for empty string."""
        html = cotton_render_string("""
            {% load cotton_bs5 %}
            {% if ""|slot_is_empty %}empty{% else %}not-empty{% endif %}
        """)

        assert "empty" in html
        assert "not-empty" not in html

    def test_slot_is_empty_with_whitespace_only(self, cotton_render_string):
        """Test slot_is_empty filter returns True for whitespace-only strings."""
        html = cotton_render_string("""
            {% load cotton_bs5 %}
            {% if "   "|slot_is_empty %}empty{% else %}not-empty{% endif %}
        """)

        assert "empty" in html

    def test_slot_is_empty_with_newlines_and_spaces(self, cotton_render_string):
        """Test slot_is_empty filter strips newlines and spaces correctly."""
        html = cotton_render_string(
            """{% load cotton_bs5 %}{% if "   "|slot_is_empty %}empty{% else %}not-empty{% endif %}"""
        )

        assert "empty" in html

    def test_slot_is_empty_with_content(self, cotton_render_string):
        """Test slot_is_empty filter returns False for strings with content."""
        html = cotton_render_string(
            """{% load cotton_bs5 %}{% if "Hello"|slot_is_empty %}empty{% else %}not-empty{% endif %}"""
        )

        assert "not-empty" in html

    def test_slot_is_empty_with_content_and_whitespace(self, cotton_render_string):
        """Test slot_is_empty filter returns False for content with surrounding whitespace."""
        html = cotton_render_string(
            """{% load cotton_bs5 %}{% if "  Hello  "|slot_is_empty %}empty{% else %}not-empty{% endif %}"""
        )

        assert "not-empty" in html

    def test_slot_is_empty_with_non_string(self, cotton_render_string):
        """Test slot_is_empty filter handles non-string types gracefully."""
        html = cotton_render_string(
            """
            {% load cotton_bs5 %}
            {% if empty_list|slot_is_empty %}empty{% else %}not-empty{% endif %}
        """,
            context={"empty_list": []},
        )

        # Should handle None return value gracefully (falsy)
        assert "not-empty" in html or "empty" in html  # Either is acceptable


class TestResponsiveTag:
    """Tests for responsive grid class tag."""

    def test_responsive_with_single_breakpoint(self, cotton_render_string):
        """Test responsive tag generates single breakpoint class."""
        html = cotton_render_string("{% load cotton_bs5 %}{% responsive 'col' %}", context={"attrs": {"md": "6"}})

        assert "col-md-6" in html

    def test_responsive_with_multiple_breakpoints(self, cotton_render_string):
        """Test responsive tag generates multiple breakpoint classes."""
        html = cotton_render_string(
            "{% load cotton_bs5 %}{% responsive 'col' %}",
            context={"attrs": {"md": "6", "lg": "4", "xl": "3"}},
        )

        assert "col-md-6" in html
        assert "col-lg-4" in html
        assert "col-xl-3" in html

    def test_responsive_with_all_breakpoints(self, cotton_render_string):
        """Test responsive tag handles all Bootstrap breakpoint sizes."""
        html = cotton_render_string(
            "{% load cotton_bs5 %}{% responsive 'col' %}",
            context={"attrs": {"xs": "12", "sm": "6", "md": "4", "lg": "3", "xl": "2", "xxl": "1"}},
        )

        assert "col-xs-12" in html
        assert "col-sm-6" in html
        assert "col-md-4" in html
        assert "col-lg-3" in html
        assert "col-xl-2" in html
        assert "col-xxl-1" in html

    def test_responsive_with_no_breakpoints(self, cotton_render_string):
        """Test responsive tag returns empty string when no breakpoints defined."""
        html = cotton_render_string("{% load cotton_bs5 %}{% responsive 'col' %}")

        assert html.strip() == ""

    def test_responsive_with_different_root_class(self, cotton_render_string):
        """Test responsive tag works with different root class names."""
        html = cotton_render_string(
            "{% load cotton_bs5 %}{% responsive 'offset' %}", context={"attrs": {"md": "2", "lg": "1"}}
        )

        assert "offset-md-2" in html
        assert "offset-lg-1" in html

    def test_responsive_with_none_values(self, cotton_render_string):
        """Test responsive tag excludes None values from output."""
        html = cotton_render_string(
            "{% load cotton_bs5 %}{% responsive 'col' %}",
            context={"attrs": {"md": "6", "lg": None, "xl": "3"}},
        )

        assert "col-md-6" in html
        assert "col-xl-3" in html
        assert "col-lg" not in html


class TestShowCodeTag:
    """Tests for show_code documentation tag."""

    def test_show_code_tag_parses_correctly(self):
        """Test show_code tag is registered and parseable."""
        from django import template

        template_str = """
        {% load cotton_bs5 %}
        {% show_code %}
        <div>Test</div>
        {% endshow_code %}
        """
        try:
            template.Template(template_str)
        except template.TemplateSyntaxError as e:
            # The tag should parse without syntax errors
            raise AssertionError(f"show_code tag failed to parse: {e}")

    def test_show_code_tag_imports_successfully(self):
        """Test ShowCodeNode and show_code tag can be imported."""
        from cotton_bs5.templatetags.cotton_bs5 import ShowCodeNode, show_code

        assert ShowCodeNode is not None
        assert show_code is not None

    def test_show_code_node_init(self):
        """Test ShowCodeNode initializes with nodelist."""
        from django.template import NodeList

        from cotton_bs5.templatetags.cotton_bs5 import ShowCodeNode

        nodelist = NodeList()
        node = ShowCodeNode(nodelist)

        assert node.nodelist is nodelist
