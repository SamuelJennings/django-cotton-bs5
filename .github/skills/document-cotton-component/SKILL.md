---
name: document-cotton-component
description: Guide for creating comprehensive documentation pages for django-cotton-bs5 components and utilities. Use when adding or improving component documentation in the example app - covers component analysis, documentation structure, section organization, description writing, and example patterns.
---

# Document Cotton Component

This skill guides you through creating comprehensive, user-friendly documentation for django-cotton-bs5 components and utilities in the demo/example app.

## Core Workflow

### 1. Analyze the Component First

**Before writing any documentation**, thoroughly examine the component's source code to identify ALL features:

```django-html
<!-- Example: cotton_bs5/templates/cotton/button/index.html -->
<c-vars small          <!-- Boolean attribute -->
        large          <!-- Boolean attribute -->
        text           <!-- Text content attribute -->
        variant="default"  <!-- String with default value -->
        outline        <!-- Boolean attribute -->
        align="center" <!-- String with default value -->
        icon           <!-- Optional icon name -->
        gap="2"        <!-- Numeric/string with default -->
        :condition="True"  <!-- Python expression with default -->
        reverse />     <!-- Boolean attribute -->
```

**Key things to identify:**

1. **Required attributes** - No default value in c-vars
2. **Optional attributes** - Has default value or omitted safely
3. **Boolean attributes** - No value assignment in c-vars
4. **String/numeric attributes** - Has default value like `="value"`
5. **Python expression attributes** - Prefixed with `:` like `:condition`
6. **Slot usage** - Look for `{{ slot }}`, named slots, or conditional slot rendering
7. **Special logic** - Conditional rendering (`{% if condition %}`), dynamic element types, CSS class manipulation
8. **HTML attribute passthrough** - `{{ attrs }}` means component accepts any HTML attribute
9. **CSS class passthrough** - `{{ class }}` means component accepts additional CSS classes

### 2. Documentation Structure

All component documentation pages follow this structure:

```django-html
<c-page title="Component Name">
  <c-page.section title="Section Title">
    <c-slot name="description">
      Clear explanation of what this section demonstrates.
      Include attribute names in <code>tags</code>.
    </c-slot>
    {% cotton:verbatim %}
      <!-- Example code here -->
    {% endcotton:verbatim %}
  </c-page.section>

  <!-- More sections... -->
</c-page>
```

**Critical rules:**

- Every `<c-page.section>` MUST have a description slot
- All examples MUST be wrapped in `{% cotton:verbatim %}`
- Use `<code>attribute</code>` tags when mentioning attribute names
- Use `{# djlint:off #}` and `{# djlint:on #}` to disable linting for compact multi-line loops

### 3. Section Organization

Organize sections in order of common usage and complexity:

1. **Basic Usage** - Most common pattern, simplest example
2. **Variants/Types** - Different styles or types (if applicable)
3. **Sizes** - Size variations (if applicable)
4. **Icons/Decorations** - Visual enhancements (if applicable)
5. **Layout/Alignment** - Positioning and alignment options
6. **Advanced Features** - Complex attributes, slot content
7. **HTML Attributes** - Passthrough attributes, custom classes/IDs
8. **Conditional Rendering** - Using `:condition` attribute
9. **Integration Examples** - Bootstrap JS interactions, form usage

### 4. Writing Descriptions

Each section description should:

- **Explain the feature clearly** - What it does and why you'd use it
- **List available values** - For attributes with limited options
- **Note defaults** - Mention default values when relevant
- **Provide context** - When to use this feature
- **Be concise** - 1-3 sentences typically

**Good examples:**

```html
<!-- Clear, lists options, notes default -->
<c-slot name="description">
  Control button size using <code>small</code> or <code>large</code> boolean
  attributes. Omit both for the default normal size.
</c-slot>

<!-- Explains purpose, shows attribute usage -->
<c-slot name="description">
  Add the <code>outline</code> boolean attribute to create outline-style buttons
  with transparent backgrounds and colored borders.
</c-slot>

<!-- Provides context for when to use -->
<c-slot name="description">
  Instead of using the <code>text</code> attribute, you can use slot content for
  more complex button content like multiple elements or custom markup.
</c-slot>
```

**Avoid:**

- Empty descriptions
- Copy-pasted descriptions that don't match the section
- Overly technical implementation details
- Vague explanations like "Various options are available"

### 5. Creating Effective Examples

Examples should be:

1. **Minimal** - Show only what's needed to demonstrate the feature
2. **Visual** - Use `<c-hstack>` or `<c-vstack>` to layout examples nicely
3. **Practical** - Show real-world use cases
4. **Progressive** - Start simple, add complexity in sub-examples

**Layout Components:**

- `<c-hstack>` - Horizontal layout with gap spacing (default for buttons, badges)
- `<c-vstack>` - Vertical layout with gap spacing (for full-width demonstrations)
- Add `class="w-100"` when demonstrating alignment features

**Example patterns:**

```django-html
<!-- Simple horizontal showcase -->
<c-hstack>
  <c-button variant="primary" text="Button 1" />
  <c-button variant="secondary" text="Button 2" />
  <c-button variant="success" text="Button 3" />
</c-hstack>

<!-- Loop through variants (compact formatting) -->
{# djlint:off #}
<c-hstack>
  {% for v in variants %}<c-button variant="{{ v }}" text="{{ v|title }}" />
  {% endfor %}
</c-hstack>
{# djlint:on #}

<!-- Full-width vertical stack for alignment demos -->
<c-vstack class="w-100">
  <c-button variant="primary"
            text="Left Aligned"
            align="start"
            class="w-100" />
  <c-button variant="secondary"
            text="Centered"
            align="center"
            class="w-100" />
</c-vstack>

<!-- Progressive complexity with subsections -->
<h5>Basic Usage</h5>
<c-hstack>
  <!-- Simple example -->
</c-hstack>

<h5 class="mt-3">Advanced Usage</h5>
<c-hstack>
  <!-- Complex example -->
</c-hstack>
```

### 6. Common Section Patterns

#### Basic Usage

Show the simplest possible usage first:

```django-html
<c-page.section title="Basic Usage">
  <c-slot name="description">
    Basic description of the component's primary purpose.
  </c-slot>
  {% cotton:verbatim %}
    <c-component text="Simple Example" />
  {% endcotton:verbatim %}
</c-page.section>
```

#### Variants Section

When component has style/color variants:

```django-html
<c-page.section title="Variants">
  <c-slot name="description">
    Bootstrap 5 provides contextual variants: primary, secondary, success,
    danger, warning, info, light, dark. Use the <code>variant</code>
    attribute to apply styling.
  </c-slot>
  {% cotton:verbatim %}
    {# djlint:off #}
    <c-hstack>
      {% for v in variants %}<c-component variant="{{ v }}" text="{{ v|title }}" />
      {% endfor %}
    </c-hstack>
    {# djlint:on #}
  {% endcotton:verbatim %}
</c-page.section>
```

#### Size Variations

For components with size options:

```django-html
<c-page.section title="Sizes">
  <c-slot name="description">
    Control size using <code>small</code> or <code>large</code> boolean
    attributes. Omit both for the default normal size.
  </c-slot>
  {% cotton:verbatim %}
    <c-hstack>
      <c-component large variant="primary" text="Large" />
      <c-component variant="primary" text="Normal" />
      <c-component small variant="primary" text="Small" />
    </c-hstack>
  {% endcotton:verbatim %}
</c-page.section>
```

#### Slot Content

For components supporting slot content:

```django-html
<c-page.section title="Slot Content">
  <c-slot name="description">
    Instead of using the <code>text</code> attribute, use slot content for
    complex markup with multiple elements.
  </c-slot>
  {% cotton:verbatim %}
    <c-hstack>
      <c-component variant="primary">
        <strong>Bold</strong> and <em>italic</em> text
      </c-component>
      <c-component variant="success">
        <span class="badge bg-light">Badge</span>
      </c-component>
    </c-hstack>
  {% endcotton:verbatim %}
</c-page.section>
```

#### HTML Attributes Passthrough

For components with `{{ attrs }}`:

```django-html
<c-page.section title="Additional HTML Attributes">
  <c-slot name="description">
    The component accepts any HTML attribute via <code>{{ attrs }}</code>,
    including <code>disabled</code>, <code>data-*</code>, and form-related
    attributes.
  </c-slot>
  {% cotton:verbatim %}
    <c-hstack>
      <c-component variant="primary" text="Disabled" disabled />
      <c-component variant="success"
                   text="With Tooltip"
                   data-bs-toggle="tooltip"
                   data-bs-title="Tooltip text" />
      <c-component variant="info"
                   text="Custom Class"
                   class="shadow-lg" />
    </c-hstack>
  {% endcotton:verbatim %}
</c-page.section>
```

#### Conditional Rendering

For components with `:condition` attribute:

```django-html
<c-page.section title="Conditional Rendering">
  <c-slot name="description">
    Use the <code>condition</code> attribute (Python expression) to
    conditionally render the component. When <code>False</code>, the component
    won't be rendered at all.
  </c-slot>
  {% cotton:verbatim %}
    <c-hstack>
      <c-component text="Always Visible" :condition="True" />
      <c-component text="Never Visible" :condition="False" />
      <c-component text="Conditional" :condition="user.is_authenticated" />
    </c-hstack>
    <p class="text-muted mt-2">
      <small>
        Note: The "Never Visible" component is not rendered in the DOM.
        The third component's visibility depends on the condition.
      </small>
    </p>
  {% endcotton:verbatim %}
</c-page.section>
```

#### Alignment/Positioning

For components with layout control:

```django-html
<c-page.section title="Content Alignment">
  <c-slot name="description">
    Control content alignment using the <code>align</code> attribute.
    Accepts Bootstrap flexbox values: <code>start</code>, <code>center</code>
    (default), or <code>end</code>.
  </c-slot>
  {% cotton:verbatim %}
    <c-vstack class="w-100">
      <c-component text="Left" align="start" class="w-100" />
      <c-component text="Center" align="center" class="w-100" />
      <c-component text="Right" align="end" class="w-100" />
    </c-vstack>
  {% endcotton:verbatim %}
</c-page.section>
```

## Checklist

Before considering documentation complete, verify:

- [ ] Analyzed component source code thoroughly
- [ ] Identified ALL attributes in `<c-vars>`
- [ ] Documented slot content usage (if supported)
- [ ] Documented `{{ attrs }}` passthrough (if supported)
- [ ] Documented `{{ class }}` passthrough (if supported)
- [ ] Documented `:condition` attribute (if supported)
- [ ] Every section has a description
- [ ] Descriptions are clear and concise
- [ ] Examples demonstrate real use cases
- [ ] Examples are minimal and focused
- [ ] Used appropriate layout components (`c-hstack`/`c-vstack`)
- [ ] Default values are mentioned where relevant
- [ ] Available options are listed for limited-value attributes

## Common Mistakes to Avoid

1. **Missing descriptions** - Every section needs one
2. **Copy-pasted wrong descriptions** - Each section is unique
3. **Incomplete feature coverage** - Check component source for ALL attributes
4. **Forgetting `:condition` attribute** - Most components support this
5. **Not demonstrating `{{ attrs }}`** - Show disabled, data-*, custom classes
6. **Poor example layout** - Use `c-hstack`/`c-vstack` for visual clarity
7. **Overly complex examples** - Keep each example focused on ONE feature
8. **Missing `{% cotton:verbatim %}`** - All examples must be wrapped
9. **No default value mentions** - Users need to know what happens when omitted
10. **Forgetting slot content** - If component has `{{ slot }}`, document it

## Quick Reference

**Component analysis locations:**

- Component source: `cotton_bs5/templates/cotton/<component>/index.html`
- Documentation page: `example/templates/components/<component>.html`

**Essential tags:**

- `<c-page title="...">` - Page wrapper
- `<c-page.section title="...">` - Section container
- `<c-slot name="description">` - Section description
- `{% cotton:verbatim %}` - Example code wrapper
- `<c-hstack>` / `<c-vstack>` - Layout helpers
- `<code>attribute</code>` - Inline code formatting
