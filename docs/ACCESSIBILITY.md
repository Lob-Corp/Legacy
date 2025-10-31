# Accessibility Guidelines

## Table of Contents

1. [Overview](#overview)
4. [Accessibility Principles](#accessibility-principles)
5. [Implementation Guidelines](#implementation-guidelines)
6. [Testing for Accessibility](#testing-for-accessibility)
7. [Common Issues and Solutions](#common-issues-and-solutions)
8. [Tools and Resources](#tools-and-resources)
9. [Checklist](#checklist)

---

## Overview

Accessibility ensures that GenewebPy can be used by everyone, including people with disabilities. This includes users with:
- **Visual impairments** (blindness, low vision, color blindness)
- **Hearing impairments** (deafness, hard of hearing)
- **Motor disabilities** (limited dexterity, tremors)
- **Cognitive disabilities** (dyslexia, learning disabilities, memory issues)
- **Temporary disabilities** (broken arm, situational limitations)
- **Age-related limitations** (declining vision, hearing, dexterity)

---

## Accessibility Principles

### 1. Semantic HTML

**Why**: Screen readers rely on proper HTML structure to convey meaning.

✅ **Good Example**:
```html
<!-- Proper semantic structure -->
<header>
  <h1>John Smith</h1>
  <nav aria-label="Person navigation">
    <ul>
      <li><a href="#family">Family</a></li>
      <li><a href="#timeline">Timeline</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h2>Biography</h2>
    <p>John was born in...</p>
  </article>
  
  <aside aria-label="Related persons">
    <h3>Children</h3>
    <ul>
      <li><a href="/person/123">Mary Smith</a></li>
    </ul>
  </aside>
</main>
```

❌ **Bad Example**:
```html
<!-- Meaningless divs -->
<div class="header">
  <div class="title">John Smith</div>
  <div class="nav">
    <div class="link">Family</div>
    <div class="link">Timeline</div>
  </div>
</div>
```

### 2. Keyboard Navigation

**Why**: Some users cannot use a mouse and rely on keyboard navigation.

**Requirements**:
- All interactive elements must be keyboard accessible
- Logical tab order
- Visible focus indicators
- Skip navigation links

✅ **Good Example**:
```html
<!-- Skip to main content link -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<nav>
  <!-- Navigation -->
</nav>

<main id="main-content" tabindex="-1">
  <!-- Main content -->
</main>
```

```css
/* Visible focus indicator */
a:focus, button:focus, input:focus {
  outline: 3px solid #4A90E2;
  outline-offset: 2px;
}

/* Skip link (visible on focus) */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

### 3. ARIA Labels and Roles

**Why**: ARIA (Accessible Rich Internet Applications) provides additional context for screen readers.

**When to Use**:
- When semantic HTML isn't sufficient
- For dynamic content
- For custom widgets
- To provide additional context

✅ **Good Examples**:
```html
<!-- Descriptive button -->
<button aria-label="Search for person named John Smith">
  <svg aria-hidden="true"><!-- search icon --></svg>
  Search
</button>

<!-- Live regions for dynamic updates -->
<div role="alert" aria-live="polite">
  Person record updated successfully
</div>

<!-- Landmark roles -->
<nav aria-label="Primary navigation">
  <!-- Main navigation -->
</nav>

<nav aria-label="Breadcrumb" aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/persons">Persons</a></li>
    <li aria-current="page">John Smith</li>
  </ol>
</nav>

<!-- Form labels -->
<label for="first-name">First Name *</label>
<input 
  id="first-name" 
  type="text" 
  required 
  aria-required="true"
  aria-describedby="first-name-help"
>
<span id="first-name-help">Enter the person's given name</span>
```

⚠️ **ARIA First Rule**: No ARIA is better than bad ARIA. Use semantic HTML first!

### 4. Color and Contrast

**Why**: Users with low vision or color blindness need sufficient contrast.

**Requirements**:
- **Normal text**: Minimum contrast ratio of 4.5:1
- **Large text** (18pt+ or 14pt+ bold): Minimum 3:1
- **Interactive elements**: Minimum 3:1 against background
- Don't rely on color alone to convey information

✅ **Good Examples**:
```css
/* High contrast text */
body {
  color: #212121;  /* Dark gray on white: 16:1 ratio */
  background: #FFFFFF;
}

/* Error messages - not just red */
.error {
  color: #D32F2F;
  border-left: 4px solid #D32F2F;
}

.error::before {
  content: "⚠ Error: ";
  font-weight: bold;
}

/* Link styling - not just color */
a {
  color: #1976D2;
  text-decoration: underline;
}

a:hover {
  text-decoration: none;
  background-color: #E3F2FD;
}
```

❌ **Bad Example**:
```css
/* Light gray on white - insufficient contrast */
.secondary-text {
  color: #CCCCCC;  /* Only 1.6:1 ratio - fails WCAG */
}

/* Color-only indication */
.required {
  color: red;  /* Screen readers can't "see" red */
}
```

### 5. Alternative Text

**Why**: Screen readers need text descriptions of images.

**Guidelines**:
- All `<img>` tags must have `alt` attribute
- Decorative images: `alt=""`
- Informative images: Describe the content
- Complex images: Provide detailed description nearby

✅ **Good Examples**:
```html
<!-- Portrait photo -->
<img 
  src="john-smith.jpg" 
  alt="Portrait photograph of John Smith from 1945"
>

<!-- Decorative divider -->
<img src="decorative-line.svg" alt="" role="presentation">

<!-- Family tree diagram -->
<figure>
  <img 
    src="family-tree.png" 
    alt="Family tree showing three generations"
    aria-describedby="tree-description"
  >
  <figcaption id="tree-description">
    Three generation family tree starting with John and Mary Smith at the top,
    their five children in the middle row, and twelve grandchildren at the bottom.
    Detailed relationships listed below.
  </figcaption>
</figure>

<!-- Icon with text -->
<button>
  <svg aria-hidden="true"><!-- icon --></svg>
  <span>Delete Person</span>
</button>
```

### 6. Responsive and Zoom-Friendly

**Why**: Users may need to zoom in or use mobile devices.

**Requirements**:
- Text must be resizable up to 200% without loss of functionality
- No horizontal scrolling at 320px width
- Touch targets at least 44×44 pixels
- Content reflows on small screens

✅ **Good Example**:
```css
/* Relative units for text */
body {
  font-size: 16px;  /* Base size */
}

h1 {
  font-size: 2rem;  /* Scales with user preferences */
}

/* Touch-friendly buttons */
button {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 16px;
}

/* Responsive layout */
.person-card {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}
```

### 7. Forms and Input

**Why**: Forms must be accessible for data entry and search.

**Requirements**:
- All inputs have associated labels
- Required fields clearly marked
- Error messages are clear and associated with fields
- Provide instructions before fields
- Group related fields

✅ **Good Example**:
```html
<form>
  <fieldset>
    <legend>Person Details</legend>
    
    <div class="form-group">
      <label for="first-name">
        First Name <span aria-label="required">*</span>
      </label>
      <input 
        id="first-name"
        name="first_name"
        type="text"
        required
        aria-required="true"
        aria-describedby="first-name-help first-name-error"
      >
      <span id="first-name-help" class="help-text">
        Enter the person's given name
      </span>
      <span id="first-name-error" class="error" role="alert">
        <!-- Populated on validation error -->
      </span>
    </div>
    
    <div class="form-group">
      <label for="birth-date">Birth Date</label>
      <input 
        id="birth-date"
        name="birth_date"
        type="date"
        aria-describedby="birth-date-help"
      >
      <span id="birth-date-help" class="help-text">
        Format: YYYY-MM-DD (e.g., 1945-06-15)
      </span>
    </div>
  </fieldset>
  
  <button type="submit">Save Person</button>
</form>
```

### 8. Time-Based Content

**Why**: Users need control over time-sensitive content.

**Requirements**:
- No time limits on forms (or make them adjustable)
- Pause/stop auto-playing content
- No flashing content (can trigger seizures)

✅ **Good Example**:
```html
<!-- Slideshow with controls -->
<div class="slideshow" role="region" aria-label="Family photos">
  <button aria-label="Pause slideshow">Pause</button>
  <button aria-label="Previous photo">Previous</button>
  <button aria-label="Next photo">Next</button>
  
  <img src="photo1.jpg" alt="Family gathering, 1950">
</div>
```

---

## Implementation Guidelines

### Page Structure Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>John Smith - GenewebPy</title>
</head>
<body>
  <!-- Skip link -->
  <a href="#main-content" class="skip-link">Skip to main content</a>
  
  <!-- Header -->
  <header role="banner">
    <h1>GenewebPy</h1>
    <nav aria-label="Primary navigation">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/search">Search</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
  </header>
  
  <!-- Main content -->
  <main id="main-content" tabindex="-1">
    <h1>John Smith</h1>
    <!-- Content -->
  </main>
  
  <!-- Footer -->
  <footer role="contentinfo">
    <p>&copy; 2025 GenewebPy</p>
  </footer>
</body>
</html>
```

### Flask Template Best Practices

```html+jinja
{# templates/person.html #}
{% extends "base.html" %}

{% block title %}{{ person.first_name }} {{ person.surname }} - GenewebPy{% endblock %}

{% block content %}
<article aria-labelledby="person-name">
  <header>
    <h1 id="person-name">
      {{ person.first_name }} {{ person.surname }}
      {% if person.occ > 0 %}
        <span class="occurrence" aria-label="occurrence {{ person.occ }}">
          ({{ person.occ }})
        </span>
      {% endif %}
    </h1>
  </header>
  
  <section aria-labelledby="vital-records">
    <h2 id="vital-records">Vital Records</h2>
    <dl>
      {% if person.birth_date %}
      <dt>Born:</dt>
      <dd>
        <time datetime="{{ person.birth_date.iso_format }}">
          {{ person.birth_date.display }}
        </time>
      </dd>
      {% endif %}
      
      {% if person.death_date %}
      <dt>Died:</dt>
      <dd>
        <time datetime="{{ person.death_date.iso_format }}">
          {{ person.death_date.display }}
        </time>
      </dd>
      {% endif %}
    </dl>
  </section>
  
  {% if person.families %}
  <section aria-labelledby="families">
    <h2 id="families">Families</h2>
    <ul>
      {% for family in person.families %}
      <li>
        <a href="{{ url_for('person', person_id=family.spouse.index) }}">
          {{ family.spouse.first_name }} {{ family.spouse.surname }}
        </a>
        {% if family.marriage_date %}
        (married 
        <time datetime="{{ family.marriage_date.iso_format }}">
          {{ family.marriage_date.display }}
        </time>)
        {% endif %}
      </li>
      {% endfor %}
    </ul>
  </section>
  {% endif %}
</article>
{% endblock %}
```

---

## Testing for Accessibility

### Automated Testing Tools

1. **axe DevTools** (Browser Extension)
   - Catches ~57% of WCAG issues
   - Free browser extension
   - Integrates with dev tools

2. **WAVE** (Web Accessibility Evaluation Tool)
   - Visual feedback on page
   - Free browser extension and API

3. **Lighthouse** (Chrome DevTools)
   - Built into Chrome
   - Provides accessibility score
   - Actionable recommendations

4. **Pa11y** (Command Line)
   ```bash
   npm install -g pa11y
   pa11y http://localhost:8080/person/1
   ```

5. **axe-core** (pytest integration)
   ```python
   from pytest_axe import axe
   
   def test_person_page_accessibility(client, axe):
       response = client.get('/person/1')
       assert response.status_code == 200
       
       results = axe.run(response.data)
       assert len(results['violations']) == 0
   ```

### Manual Testing

**Keyboard Navigation Test**:
1. Unplug mouse
2. Use Tab to navigate forward
3. Use Shift+Tab to navigate backward
4. Use Enter/Space to activate
5. Verify all interactive elements are reachable

**Screen Reader Test**:
1. **NVDA** (Windows, free): https://www.nvaccess.org/
2. **JAWS** (Windows, paid): https://www.freedomscientific.com/
3. **VoiceOver** (macOS/iOS, built-in): Cmd+F5
4. **TalkBack** (Android, built-in): Settings → Accessibility

**Zoom Test**:
1. Zoom to 200% (Ctrl/Cmd + Plus)
2. Verify no horizontal scrolling
3. Verify text is readable
4. Verify functionality still works

**Color Blindness Test**:
- Use browser extensions to simulate color blindness
- Verify information isn't conveyed by color alone

### Testing Checklist

- [ ] Run automated tool (axe, WAVE, Lighthouse)
- [ ] Test keyboard navigation (no mouse)
- [ ] Test with screen reader
- [ ] Zoom to 200%
- [ ] Check color contrast
- [ ] Validate HTML (https://validator.w3.org/)
- [ ] Test on mobile device
- [ ] Check form error handling

---

## Common Issues and Solutions

### Issue 1: Missing Form Labels

❌ **Problem**:
```html
<input type="text" placeholder="First name">
```

✅ **Solution**:
```html
<label for="first-name">First Name</label>
<input id="first-name" type="text" placeholder="e.g., John">
```

### Issue 2: Insufficient Color Contrast

❌ **Problem**:
```css
.help-text {
  color: #999999;  /* 2.8:1 ratio - fails WCAG AA */
}
```

✅ **Solution**:
```css
.help-text {
  color: #666666;  /* 5.7:1 ratio - passes WCAG AA */
}
```

### Issue 3: Icon-Only Buttons

❌ **Problem**:
```html
<button><i class="icon-delete"></i></button>
```

✅ **Solution**:
```html
<button aria-label="Delete person">
  <i class="icon-delete" aria-hidden="true"></i>
</button>
```

### Issue 4: Non-Semantic Markup

❌ **Problem**:
```html
<div class="button" onclick="deletePerson()">Delete</div>
```

✅ **Solution**:
```html
<button type="button" onclick="deletePerson()">Delete</button>
```

### Issue 5: Missing Skip Link

❌ **Problem**: Users must tab through entire navigation on every page.

✅ **Solution**:
```html
<a href="#main-content" class="skip-link">Skip to main content</a>
<nav>...</nav>
<main id="main-content" tabindex="-1">...</main>
```

### Issue 6: Empty Links

❌ **Problem**:
```html
<a href="/person/123"></a>
```

✅ **Solution**:
```html
<a href="/person/123">View John Smith's profile</a>
```

---

## Tools and Resources

### Testing Tools

- **axe DevTools**: https://www.deque.com/axe/devtools/
- **WAVE**: https://wave.webaim.org/
- **Lighthouse**: Built into Chrome DevTools
- **Color Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **NVDA Screen Reader**: https://www.nvaccess.org/

### Learning Resources

- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **MDN Accessibility**: https://developer.mozilla.org/en-US/docs/Web/Accessibility
- **WebAIM**: https://webaim.org/
- **A11y Project**: https://www.a11yproject.com/
- **Inclusive Components**: https://inclusive-components.design/

### Browser Extensions

- **axe DevTools** (Chrome, Firefox, Edge)
- **WAVE** (Chrome, Firefox)
- **Accessibility Insights** (Chrome, Edge)
- **Color Blindness Simulator** (Chrome, Firefox)

---

## Checklist

### Development Phase

- [ ] Use semantic HTML elements
- [ ] Include proper ARIA labels where needed
- [ ] Ensure all images have alt text
- [ ] All forms have associated labels
- [ ] Keyboard navigation works throughout
- [ ] Focus indicators are visible
- [ ] Color contrast meets WCAG AA standards
- [ ] Text is resizable to 200%
- [ ] No time limits on interactions
- [ ] Skip navigation link included
- [ ] Page title is descriptive
- [ ] Language is specified (`<html lang="en">`)

### Pre-Release Testing

- [ ] Run automated accessibility tests
- [ ] Test with keyboard only (no mouse)
- [ ] Test with screen reader (NVDA/VoiceOver)
- [ ] Test at 200% zoom
- [ ] Test on mobile device
- [ ] Validate HTML
- [ ] Check color contrast
- [ ] Test with color blindness simulator
- [ ] Test with browser extensions disabled
- [ ] Review ARIA usage

### Ongoing Maintenance

- [ ] Include accessibility in code reviews
- [ ] Run automated tests in CI/CD
- [ ] Collect user feedback on accessibility
- [ ] Update documentation as patterns evolve
- [ ] Stay current with WCAG updates
- [ ] Regular accessibility audits

---

## Implementation Priority

### Phase 1: Foundation (Must Have)

1. Semantic HTML structure
2. Form labels and ARIA attributes
3. Keyboard navigation
4. Alt text for images
5. Color contrast compliance
6. Skip navigation link

### Phase 2: Enhancement (Should Have)

1. Screen reader testing
2. Focus management for dynamic content
3. Error message handling
4. Live regions for updates
5. Mobile accessibility
6. Comprehensive ARIA labels

### Phase 3: Optimization (Nice to Have)

1. Advanced screen reader features
2. Keyboard shortcuts
3. High contrast mode
4. Reduced motion support
5. Custom focus styles
6. Accessibility documentation for users

---

## Contact and Support

**Questions about accessibility?**
- Open an issue on GitHub
- Tag with `accessibility` label
- Reference WCAG guideline if applicable

**Found an accessibility issue?**
- Report as a bug
- Include: browser, assistive technology (if any), steps to reproduce
- We prioritize accessibility bugs

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-31 | Team | Initial accessibility guidelines |

