# Template System Documentation

This document explains how to use the template inheritance system in the Subscription Management System.

## Base Template (`base.html`)

The `base.html` template provides a complete, responsive layout with:

### Features
- **Modern Bootstrap 5 Design**: Professional, mobile-responsive interface
- **Custom CSS Variables**: Easy theme customization through CSS custom properties
- **Navigation Bar**: Auto-collapsing navbar with user authentication states
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile devices
- **Message System**: Django messages support with dismissible alerts
- **Footer**: Professional footer with links and social media icons

### CSS Theme Variables
```css
:root {
    --primary-color: #2c3e50;      /* Main brand color */
    --secondary-color: #3498db;    /* Accent blue */
    --accent-color: #e74c3c;       /* Red accents */
    --success-color: #27ae60;      /* Success green */
    --warning-color: #f39c12;      /* Warning orange */
    --light-gray: #ecf0f1;         /* Light backgrounds */
    --dark-gray: #34495e;          /* Dark text/elements */
}
```

### Template Blocks

The base template provides several blocks that child templates can override:

#### Required Blocks
- `{% block content %}` - Main page content area

#### Optional Blocks
- `{% block title %}` - Page title (defaults to "Subscription Management System")
- `{% block extra_css %}` - Additional CSS specific to the page
- `{% block extra_js %}` - Additional JavaScript specific to the page

## Creating Child Templates

### Basic Structure
```html
{% extends 'base.html' %}

{% block title %}Your Page Title - {{ block.super }}{% endblock %}

{% block content %}
<!-- Your page content here -->
{% endblock %}
```

### Example: Dashboard Template
```html
{% extends 'base.html' %}

{% block title %}Dashboard - {{ block.super }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1 class="page-title">
            <i class="fas fa-tachometer-alt me-2"></i>
            Dashboard
        </h1>
    </div>
</div>
<!-- Rest of your content -->
{% endblock %}

{% block extra_js %}
<script>
    // Page-specific JavaScript
    console.log('Dashboard loaded');
</script>
{% endblock %}
```

## Available CSS Classes

### Status Badges
```html
<span class="status-badge status-active">Active</span>
<span class="status-badge status-cancelled">Cancelled</span>
<span class="status-badge status-expired">Expired</span>
```

### Page Titles
```html
<h1 class="page-title">
    <i class="fas fa-icon me-2"></i>
    Page Title
</h1>
```

### Cards with Hover Effects
```html
<div class="card">
    <div class="card-body">
        <!-- Card content -->
    </div>
</div>
```

### Gradient Buttons
- `btn-primary` - Blue gradient
- `btn-success` - Green gradient  
- `btn-warning` - Orange gradient
- `btn-danger` - Red gradient

## Navigation Structure

The navigation automatically handles:
- Active states based on current URL
- User authentication status
- Responsive collapsing on mobile devices

### Adding New Navigation Items
To add new navigation items, update the navbar section in `base.html`:

```html
<li class="nav-item">
    <a class="nav-link" href="{% url 'your_app:your_view' %}">
        <i class="fas fa-your-icon me-1"></i>
        Your Link Text
    </a>
</li>
```

## Icons

The template uses Font Awesome 6 icons. Common icons used:
- `fas fa-home` - Dashboard/Home
- `fas fa-box` - Plans
- `fas fa-calendar-alt` - Subscriptions
- `fas fa-exchange-alt` - Exchange Rates
- `fas fa-user-circle` - User profile
- `fas fa-crown` - Premium/Special items

## Responsive Design

The template is fully responsive with:
- Bootstrap 5 grid system
- Mobile-first approach
- Collapsible navigation
- Responsive tables with horizontal scrolling
- Adaptive card layouts

## Best Practices

1. **Always extend base.html**: Every template should inherit from the base template
2. **Use semantic HTML**: Proper heading hierarchy and meaningful markup
3. **Include page titles**: Always set a descriptive page title
4. **Use Bootstrap classes**: Leverage Bootstrap's utility classes for consistent styling
5. **Add page-specific CSS/JS**: Use the extra blocks for page-specific code
6. **Follow naming conventions**: Use descriptive class names and IDs

## Examples

See the following template examples:
- `templates/subscriptions/dashboard.html` - Dashboard with stats and tables
- `templates/subscriptions/plans.html` - Plans display with pricing cards

## URL Configuration

Make sure your URLs are properly namespaced:

```python
# urls.py
app_name = 'subscriptions'
urlpatterns = [
    path('', views.index, name='index'),
    # other patterns
]
```

Then reference them in templates:
```html
<a href="{% url 'subscriptions:index' %}">Dashboard</a>
```
