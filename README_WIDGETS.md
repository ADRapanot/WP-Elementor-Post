# Elementor Widget Customization Guide

Complete guide for customizing Elementor widgets in the `publish_elementor_widgets_meta()` function.

---

## Table of Contents

1. [Overall Structure](#overall-structure)
2. [Section Settings](#section-settings)
3. [Column Settings](#column-settings)
4. [Table of Contents Widget](#table-of-contents-widget)
5. [Text Editor Widget](#text-editor-widget)
6. [Heading Widget](#heading-widget)
7. [Accordion Widget (FAQ)](#accordion-widget-faq)
8. [Common Widget Properties](#common-widget-properties)
9. [Advanced Customizations](#advanced-customizations)

---

## Overall Structure

### Elementor Data Hierarchy

```python
elementor_data = [
    {
        "id": "unique_section_id",      # Unique identifier
        "elType": "section",             # Element type: section, column, widget, container
        "settings": {},                  # Section/column/widget settings
        "elements": []                   # Child elements
    }
]
```

### Element Types

- **section**: Top-level container (horizontal wrapper)
- **column**: Child of section (vertical wrapper)
- **widget**: Actual content element (TOC, text editor, accordion, etc.)
- **container**: Modern flexbox container (Elementor 3.16+)

---

## Section Settings

### Basic Section Configuration

```python
{
    "id": "section_unique_id",
    "elType": "section",
    "settings": {
        # Layout
        "layout": "boxed",              # "boxed" or "full_width"
        "content_width": {
            "unit": "px",
            "size": 1140                # Max content width (1140px standard)
        },
        "gap": "default",               # Column gap: "default", "narrow", "extended", "wide", "wider"

        # Spacing
        "padding": {
            "unit": "px",
            "top": "40",
            "right": "20",
            "bottom": "40",
            "left": "20",
            "isLinked": False           # True = all sides same value
        },
        "margin": {
            "unit": "px",
            "top": "0",
            "right": "0",
            "bottom": "20",
            "left": "0",
            "isLinked": False
        },

        # Background
        "background_background": "classic",  # "classic", "gradient", "video", "slideshow"
        "background_color": "#ffffff",       # Hex color
        "background_image": {
            "url": "https://example.com/image.jpg",
            "id": 123
        },

        # Border
        "border_border": "solid",       # "none", "solid", "double", "dotted", "dashed"
        "border_width": {
            "unit": "px",
            "top": "1",
            "right": "1",
            "bottom": "1",
            "left": "1",
            "isLinked": True
        },
        "border_color": "#000000",
        "border_radius": {
            "unit": "px",
            "top": "0",
            "right": "0",
            "bottom": "0",
            "left": "0",
            "isLinked": True
        },

        # Advanced
        "z_index": 10,
        "css_classes": "my-custom-class",
        "html_tag": "section"           # HTML tag: "div", "section", "article", etc.
    },
    "elements": []  # Columns go here
}
```

---

## Column Settings

### Basic Column Configuration

```python
{
    "id": "column_unique_id",
    "elType": "column",
    "settings": {
        # Width
        "_column_size": 100,            # Percentage (50 = 50%, 100 = 100%)
        "_inline_size": None,           # Custom width override

        # Spacing
        "padding": {
            "unit": "px",
            "top": "20",
            "right": "20",
            "bottom": "20",
            "left": "20",
            "isLinked": False
        },

        # Background
        "background_background": "classic",
        "background_color": "#f5f5f5",

        # Border
        "border_border": "solid",
        "border_width": {
            "unit": "px",
            "top": "1",
            "right": "1",
            "bottom": "1",
            "left": "1",
            "isLinked": True
        },
        "border_color": "#dddddd",
        "border_radius": {
            "unit": "px",
            "top": "5",
            "right": "5",
            "bottom": "5",
            "left": "5",
            "isLinked": True
        },

        # Alignment
        "content_position": "top",      # "top", "center", "bottom"
        "vertical_align": "top",        # "top", "middle", "bottom"

        # Advanced
        "css_classes": "my-column-class"
    },
    "elements": []  # Widgets go here
}
```

### Multi-Column Layout

```python
{
    "id": "section_two_columns",
    "elType": "section",
    "settings": {},
    "elements": [
        {
            "id": "column_left",
            "elType": "column",
            "settings": {"_column_size": 50},  # 50% width
            "elements": [/* widgets */]
        },
        {
            "id": "column_right",
            "elType": "column",
            "settings": {"_column_size": 50},  # 50% width
            "elements": [/* widgets */]
        }
    ]
}
```

---

## Table of Contents Widget

### Complete TOC Configuration

```python
{
    "id": "widget_toc",
    "elType": "widget",
    "widgetType": "table-of-contents",
    "settings": {
        # Content
        "title": "In This Article",          # TOC heading
        "html_tag": "h2",                    # Title HTML tag: "h1"-"h6", "div", "span"

        # Headings Selection
        "headings_by_tags": ["h2", "h3"],   # Which headings to include
        "container": "",                     # CSS selector of container (empty = whole page)
        "exclude_headings_by_selector": ".no-toc",  # Exclude headings with this class

        # Display
        "hierarchical_view": "yes",          # "yes" or "no" - show hierarchy
        "collapse_subitems": "no",           # "yes" or "no" - collapse h3 by default
        "marker_view": "numbers",            # "numbers", "bullets", "none"

        # Icon
        "icon": {
            "value": "fas fa-list",          # Font Awesome icon
            "library": "fa-solid"            # "fa-solid", "fa-regular", "fa-brands"
        },

        # Behavior
        "word_wrap": "ellipsis",             # "ellipsis", "normal"
        "minimized_on": "mobile",            # "mobile", "tablet", "mobile_extra", "none"
        "minimize_box": "yes",               # Show minimize button

        # Style - Title
        "title_color": "#000000",
        "title_typography_typography": "custom",
        "title_typography_font_size": {
            "unit": "px",
            "size": 20
        },
        "title_typography_font_weight": "600",

        # Style - List Items
        "list_text_color": "#333333",
        "list_text_hover_color": "#0073aa",
        "list_typography_typography": "custom",
        "list_typography_font_size": {
            "unit": "px",
            "size": 14
        },

        # Box Style
        "box_background_color": "#f9f9f9",
        "box_border_border": "solid",
        "box_border_width": {
            "unit": "px",
            "top": "1",
            "right": "1",
            "bottom": "1",
            "left": "1",
            "isLinked": True
        },
        "box_border_color": "#dddddd",
        "box_border_radius": {
            "unit": "px",
            "top": "5",
            "right": "5",
            "bottom": "5",
            "left": "5",
            "isLinked": True
        },
        "box_padding": {
            "unit": "px",
            "top": "20",
            "right": "20",
            "bottom": "20",
            "left": "20",
            "isLinked": False
        }
    },
    "elements": []
}
```

### TOC Examples

**Minimal TOC (H2 only):**

```python
"settings": {
    "title": "Contents",
    "headings_by_tags": ["h2"],
    "marker_view": "bullets",
    "hierarchical_view": "no"
}
```

**Detailed TOC (H2-H4 with styling):**

```python
"settings": {
    "title": "Table of Contents",
    "headings_by_tags": ["h2", "h3", "h4"],
    "hierarchical_view": "yes",
    "collapse_subitems": "yes",
    "marker_view": "numbers",
    "box_background_color": "#e3f2fd",
    "box_border_radius": {"unit": "px", "top": "8", "right": "8", "bottom": "8", "left": "8", "isLinked": True}
}
```

---

## Text Editor Widget

### Complete Text Editor Configuration

```python
{
    "id": "widget_text",
    "elType": "widget",
    "widgetType": "text-editor",
    "settings": {
        # Content
        "editor": "<h2>Heading</h2><p>Your HTML content here...</p>",

        # Typography
        "text_color": "#333333",
        "typography_typography": "custom",
        "typography_font_family": "Roboto, sans-serif",
        "typography_font_size": {
            "unit": "px",
            "size": 16
        },
        "typography_font_weight": "400",
        "typography_line_height": {
            "unit": "em",
            "size": 1.6
        },
        "typography_letter_spacing": {
            "unit": "px",
            "size": 0
        },

        # Alignment
        "align": "left",                     # "left", "center", "right", "justify"

        # Advanced
        "drop_cap": "no",                    # "yes" or "no" - first letter styling
        "text_columns": "1",                 # Number of columns
        "column_gap": {
            "unit": "px",
            "size": 20
        }
    },
    "elements": []
}
```

### HTML Content Examples

**With Images:**

```python
"editor": """
<h2>Main Heading</h2>
<p>Introduction paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
<img src="https://example.com/image.jpg" alt="Description" style="max-width: 100%;">
<h3>Subheading</h3>
<ul>
    <li>List item 1</li>
    <li>List item 2</li>
</ul>
"""
```

**With Code Blocks:**

```python
"editor": """
<h2>Code Example</h2>
<pre><code>def hello_world():
    print("Hello, World!")</code></pre>
"""
```

---

## Heading Widget

### Complete Heading Configuration

```python
{
    "id": "widget_heading",
    "elType": "widget",
    "widgetType": "heading",
    "settings": {
        # Content
        "title": "Your Heading Text",
        "link": {
            "url": "https://example.com",
            "is_external": True,            # Open in new tab
            "nofollow": False
        },

        # HTML Tag
        "header_size": "h2",                # "h1", "h2", "h3", "h4", "h5", "h6", "div", "span", "p"

        # Alignment
        "align": "left",                    # "left", "center", "right", "justify"

        # Style - Text
        "title_color": "#000000",
        "typography_typography": "custom",
        "typography_font_family": "Helvetica, Arial, sans-serif",
        "typography_font_size": {
            "unit": "px",
            "size": 32,
            "sizes": []
        },
        "typography_font_weight": "700",
        "typography_text_transform": "none",  # "none", "uppercase", "lowercase", "capitalize"
        "typography_font_style": "normal",    # "normal", "italic", "oblique"
        "typography_text_decoration": "none", # "none", "underline", "overline", "line-through"
        "typography_line_height": {
            "unit": "em",
            "size": 1.2
        },
        "typography_letter_spacing": {
            "unit": "px",
            "size": 0
        },

        # Text Shadow
        "text_shadow_text_shadow_type": "yes",
        "text_shadow_text_shadow": {
            "horizontal": 2,
            "vertical": 2,
            "blur": 3,
            "color": "rgba(0,0,0,0.3)"
        },

        # Blend Mode
        "blend_mode": "normal",             # "normal", "multiply", "screen", "overlay", etc.

        # Spacing
        "_margin": {
            "unit": "px",
            "top": "0",
            "right": "0",
            "bottom": "20",
            "left": "0",
            "isLinked": False
        },
        "_padding": {
            "unit": "px",
            "top": "0",
            "right": "0",
            "bottom": "0",
            "left": "0",
            "isLinked": False
        }
    },
    "elements": []
}
```

### Heading Examples

**Centered Title:**

```python
"settings": {
    "title": "Welcome to Our Site",
    "header_size": "h1",
    "align": "center",
    "title_color": "#2c3e50",
    "typography_font_size": {"unit": "px", "size": 48}
}
```

**Subtitle with Link:**

```python
"settings": {
    "title": "Learn More →",
    "header_size": "h3",
    "link": {"url": "/about", "is_external": False},
    "title_color": "#3498db",
    "typography_font_weight": "500"
}
```

---

## Accordion Widget (FAQ)

### Complete Accordion Configuration

```python
{
    "id": "widget_faq",
    "elType": "widget",
    "widgetType": "accordion",
    "settings": {
        # Content - FAQ Items
        "tabs": [
            {
                "_id": "faq_1",                    # Unique ID for each item
                "tab_title": "What is your question?",
                "tab_content": "<p>This is the answer with <strong>HTML formatting</strong>.</p>"
            },
            {
                "_id": "faq_2",
                "tab_title": "Another question?",
                "tab_content": """
                    <p>You can use multi-line answers.</p>
                    <ul>
                        <li>Point 1</li>
                        <li>Point 2</li>
                    </ul>
                """
            }
        ],

        # Behavior
        "multiple_open": "no",              # Allow multiple items open: "yes" or "no"
        "selected_item": "1",               # Which item is open by default (1-indexed)

        # Icon
        "icon": {
            "value": "fas fa-plus",         # Closed state icon
            "library": "fa-solid"
        },
        "icon_active": {
            "value": "fas fa-minus",        # Open state icon
            "library": "fa-solid"
        },
        "icon_align": "left",               # "left" or "right"

        # Style - Title
        "title_background": "#f8f9fa",
        "title_color": "#000000",
        "title_typography_typography": "custom",
        "title_typography_font_size": {
            "unit": "px",
            "size": 18
        },
        "title_typography_font_weight": "600",
        "title_padding": {
            "unit": "px",
            "top": "15",
            "right": "20",
            "bottom": "15",
            "left": "20",
            "isLinked": False
        },

        # Style - Active Title
        "tab_active_color": "#ffffff",
        "tab_active_background": "#0073aa",

        # Style - Content
        "content_background_color": "#ffffff",
        "content_color": "#333333",
        "content_typography_typography": "custom",
        "content_typography_font_size": {
            "unit": "px",
            "size": 16
        },
        "content_padding": {
            "unit": "px",
            "top": "20",
            "right": "20",
            "bottom": "20",
            "left": "20",
            "isLinked": False
        },

        # Border
        "border_width": {
            "unit": "px",
            "top": "1",
            "right": "1",
            "bottom": "1",
            "left": "1",
            "isLinked": True
        },
        "border_color": "#dddddd",
        "border_radius": {
            "unit": "px",
            "top": "5",
            "right": "5",
            "bottom": "5",
            "left": "5",
            "isLinked": True
        },

        # Spacing between items
        "box_space": {
            "unit": "px",
            "size": 10
        }
    },
    "elements": []
}
```

### Dynamic FAQ Generation

```python
# From a list of FAQ objects
faq_items = [
    {"question": "How do I get started?", "answer": "Simply create an account."},
    {"question": "What are the costs?", "answer": "Plans start at $9/month."},
    {"question": "Can I cancel anytime?", "answer": "Yes, cancel anytime without fees."}
]

# Generate tabs
"tabs": [
    {
        "_id": f"faq_{i+1}",
        "tab_title": item["question"],
        "tab_content": f"<p>{item['answer']}</p>"
    }
    for i, item in enumerate(faq_items)
]
```

### Styled FAQ Examples

**Minimal Design:**

```python
"settings": {
    "tabs": [...],
    "title_background": "transparent",
    "border_width": {"unit": "px", "top": "0", "right": "0", "bottom": "1", "left": "0", "isLinked": False},
    "border_color": "#eeeeee"
}
```

**Card Design:**

```python
"settings": {
    "tabs": [...],
    "title_background": "#ffffff",
    "border_radius": {"unit": "px", "top": "8", "right": "8", "bottom": "8", "left": "8", "isLinked": True},
    "box_space": {"unit": "px", "size": 15},
    "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
    "border_color": "#e0e0e0"
}
```

---

## Common Widget Properties

### Spacing (All Widgets)

```python
"_margin": {
    "unit": "px",              # "px", "em", "%", "rem", "vw"
    "top": "10",
    "right": "0",
    "bottom": "20",
    "left": "0",
    "isLinked": False          # True = all values same
}

"_padding": {
    "unit": "px",
    "top": "15",
    "right": "15",
    "bottom": "15",
    "left": "15",
    "isLinked": True
}
```

### Visibility

```python
# Hide on specific devices
"_element_width": "initial",           # Widget width
"hide_desktop": "no",                  # Hide on desktop
"hide_tablet": "no",                   # Hide on tablet
"hide_mobile": "no",                   # Hide on mobile
```

### Animation

```python
"_animation": "fadeIn",                # Animation type
"_animation_duration": "normal",       # "slow", "normal", "fast"
"_animation_delay": 200                # Delay in ms
```

**Available Animations:**

- Fade: `fadeIn`, `fadeInDown`, `fadeInUp`, `fadeInLeft`, `fadeInRight`
- Zoom: `zoomIn`, `zoomInDown`, `zoomInUp`, `zoomInLeft`, `zoomInRight`
- Bounce: `bounceIn`, `bounceInDown`, `bounceInUp`, `bounceInLeft`, `bounceInRight`
- Slide: `slideInDown`, `slideInUp`, `slideInLeft`, `slideInRight`
- Rotate: `rotateIn`, `rotateInDownLeft`, `rotateInDownRight`

### Custom CSS

```python
"_css_classes": "my-custom-class another-class",
"_element_id": "unique-element-id"
```

---

## Advanced Customizations

### 1. Responsive Settings

Most size/spacing properties support responsive values:

```python
"typography_font_size": {
    "unit": "px",
    "size": 32,              # Desktop
    "sizes": {
        "mobile": 24,        # Mobile override
        "tablet": 28         # Tablet override
    }
}
```

### 2. Background Gradient

```python
"background_background": "gradient",
"background_color": "#667eea",
"background_color_b": "#764ba2",
"background_gradient_type": "linear",
"background_gradient_angle": {
    "unit": "deg",
    "size": 135
}
```

### 3. Background Video

```python
"background_background": "video",
"background_video_link": "https://example.com/video.mp4",
"background_video_fallback": {
    "url": "https://example.com/fallback.jpg",
    "id": 456
}
```

### 4. Shape Divider

```python
"shape_divider_top": "waves",          # Divider type
"shape_divider_top_color": "#ffffff",
"shape_divider_top_height": {
    "unit": "px",
    "size": 100
},
"shape_divider_top_flip": "yes",       # Flip horizontally
"shape_divider_top_negative": "no"     # Flip vertically
```

**Available Shapes:**

- `waves`, `clouds`, `curve`, `triangle`, `mountains`, `tilt`, `arrow`, `split`, `book`

### 5. Custom Meta Fields

```python
payload = {
    "title": "My Post",
    "content": "",
    "meta": {
        "_elementor_data": json.dumps(elementor_data),
        "_elementor_edit_mode": "builder",
        "_elementor_version": "3.22.2",

        # Custom fields
        "_elementor_page_settings": json.dumps({
            "container_width": {"unit": "px", "size": 1200},
            "page_title": "no",              # Hide page title
            "post_status": "draft"
        }),

        # AIOSEO
        "_aioseo_description": "SEO meta description",
        "_aioseo_title": "SEO title",

        # Custom meta
        "custom_field_name": "custom_value"
    }
}
```

### 6. Complete Multi-Section Example

```python
elementor_data = [
    # Hero Section
    {
        "id": "section_hero",
        "elType": "section",
        "settings": {
            "layout": "full_width",
            "height": "min-height",
            "custom_height": {"unit": "vh", "size": 80},
            "background_background": "gradient",
            "background_color": "#667eea",
            "background_color_b": "#764ba2",
            "padding": {"unit": "px", "top": "100", "right": "20", "bottom": "100", "left": "20", "isLinked": False}
        },
        "elements": [{
            "id": "column_hero",
            "elType": "column",
            "settings": {"_column_size": 100, "content_position": "center"},
            "elements": [
                {
                    "id": "heading_hero",
                    "elType": "widget",
                    "widgetType": "heading",
                    "settings": {
                        "title": "Welcome to Our Platform",
                        "header_size": "h1",
                        "align": "center",
                        "title_color": "#ffffff",
                        "typography_font_size": {"unit": "px", "size": 56}
                    },
                    "elements": []
                }
            ]
        }]
    },

    # Content Section
    {
        "id": "section_content",
        "elType": "section",
        "settings": {
            "layout": "boxed",
            "padding": {"unit": "px", "top": "80", "right": "20", "bottom": "80", "left": "20", "isLinked": False}
        },
        "elements": [
            # Left column
            {
                "id": "column_left",
                "elType": "column",
                "settings": {"_column_size": 50},
                "elements": [{
                    "id": "text_left",
                    "elType": "widget",
                    "widgetType": "text-editor",
                    "settings": {"editor": "<h2>Feature 1</h2><p>Description here...</p>"},
                    "elements": []
                }]
            },
            # Right column
            {
                "id": "column_right",
                "elType": "column",
                "settings": {"_column_size": 50},
                "elements": [{
                    "id": "text_right",
                    "elType": "widget",
                    "widgetType": "text-editor",
                    "settings": {"editor": "<h2>Feature 2</h2><p>Description here...</p>"},
                    "elements": []
                }]
            }
        ]
    }
]
```

---

## Quick Reference

### Widget Types

- `table-of-contents` - Table of Contents
- `text-editor` - Rich text content
- `heading` - Headings (H1-H6)
- `accordion` - Accordion/FAQ
- `toggle` - Toggle boxes (similar to accordion)
- `image` - Images
- `button` - Buttons
- `divider` - Dividers
- `spacer` - Spacing element
- `video` - Video player
- `icon` - Icons
- `icon-box` - Icon with text
- `image-box` - Image with text
- `html` - Custom HTML/JS

### Common Units

- `px` - Pixels
- `%` - Percentage
- `em` - Relative to font size
- `rem` - Relative to root font size
- `vh` - Viewport height
- `vw` - Viewport width

### Color Formats

- Hex: `#ffffff`
- RGB: `rgb(255, 255, 255)`
- RGBA: `rgba(255, 255, 255, 0.5)`

---

## Testing Your Configuration

```python
# Test function to verify structure
async def test_widget_configuration(self):
    """Test widget configuration before publishing"""

    # Your elementor_data here
    elementor_data = [...]

    # Validate JSON structure
    try:
        json_str = json.dumps(elementor_data)
        json.loads(json_str)
        print("✓ JSON structure is valid")
    except Exception as e:
        print(f"✗ JSON error: {e}")
        return

    # Create draft post
    payload = {
        "title": "TEST: Widget Configuration",
        "status": "draft",
        "content": "",
        "meta": {
            "_elementor_data": json.dumps(elementor_data),
            "_elementor_edit_mode": "builder",
            "_elementor_version": "3.22.2"
        }
    }

    res = await self.client.post(f"{self.api_url}/posts", json=payload)
    res.raise_for_status()
    data = res.json()

    print(f"✓ Draft created: {data.get('link')}")
    print("  Open in Elementor editor to verify appearance")

    return data
```

---

## Troubleshooting

### Common Issues

1. **Widgets not displaying**: Check `widgetType` spelling
2. **Styles not applying**: Verify property names (e.g., `title_color` not `titleColor`)
3. **TOC not showing headings**: Ensure HTML content has proper `<h2>`, `<h3>` tags
4. **FAQ questions wrong**: Use `tab_title` and `tab_content`, not `title` and `content`
5. **Sections horizontal**: Missing column wrapper or wrong `_column_size`

### Debugging Steps

1. Create widget manually in Elementor
2. Use `inspect_existing_faq()` to get correct structure
3. Compare with your generated structure
4. Test with draft posts before publishing

---

## Additional Resources

- Elementor Developer Docs: https://developers.elementor.com/
- WordPress REST API: https://developer.wordpress.org/rest-api/
- Font Awesome Icons: https://fontawesome.com/icons

---

**Version**: 1.0  
**Last Updated**: October 2025  
**Compatible with**: Elementor 3.16+, WordPress 6.0+
