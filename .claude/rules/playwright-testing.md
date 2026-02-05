# Visual Testing with Playwright

## When to Use

Use Playwright for visual verification when:
- Fixing UI bugs or layout issues
- Testing responsive design across breakpoints
- Verifying modal/dialog behavior
- Testing interactive elements (buttons, forms, dropdowns)
- Confirming CSS changes render correctly

## Workflow

### 1. Start Dev Server (if not running)

```bash
# Check if server is running
listProcesses

# If not running, start as background process
controlPwshProcess action="start" command="uv run python manage.py runserver"
```

### 2. Navigate and Take Snapshots

```javascript
// Navigate to the page
mcp_playwright_browser_navigate url="http://127.0.0.1:8000/your-page/"

// Get accessibility snapshot (preferred for understanding structure)
mcp_playwright_browser_snapshot

// Take screenshot for visual verification
mcp_playwright_browser_take_screenshot filename="descriptive_name.png" type="png"
```

### 3. Test Interactions

```javascript
// Click elements using ref from snapshot
mcp_playwright_browser_click ref="e123" element="Button description"

// Type into inputs
mcp_playwright_browser_type ref="e456" text="input value"

// Fill forms
mcp_playwright_browser_fill_form fields=[{name: "field", type: "textbox", ref: "e789", value: "value"}]
```

### 4. Test Responsive Design

```javascript
// Resize to mobile
mcp_playwright_browser_resize width=375 height=812

// Resize to tablet
mcp_playwright_browser_resize width=768 height=1024

// Resize back to desktop
mcp_playwright_browser_resize width=1280 height=800
```

### 5. Debug Alpine.js Issues

```javascript
// Check Alpine data state
mcp_playwright_browser_evaluate function="() => {
    const el = document.querySelector('[x-data]');
    return Alpine.$data(el);
}"

// Check element visibility
mcp_playwright_browser_evaluate function="() => {
    const el = document.querySelector('.my-element');
    return {
        display: window.getComputedStyle(el).display,
        visibility: window.getComputedStyle(el).visibility
    };
}"

// Manually dispatch events for testing
mcp_playwright_browser_evaluate function="() => {
    window.dispatchEvent(new CustomEvent('my-event', { detail: { id: '123' } }));
}"
```

### 6. Check Console for Errors

```javascript
mcp_playwright_browser_console_messages level="error"
```

### 7. Clean Up

```javascript
mcp_playwright_browser_close
```

## Common Patterns

### Testing Modals

1. Navigate to page
2. Take snapshot to find trigger button ref
3. Click trigger button
4. Take snapshot/screenshot to verify modal opened
5. Test modal interactions
6. Close modal and verify it closed

### Testing Mobile Responsiveness

1. Start at desktop size
2. Test functionality
3. Resize to mobile (375x812)
4. Verify layout adapts correctly
5. Test same functionality on mobile
6. Take screenshots at each breakpoint

### Debugging Hidden Elements

If an element should be visible but isn't:

1. Check if element exists in DOM
2. Check computed display/visibility styles
3. Check if Alpine x-show condition is true
4. Check if element is inside correct x-data scope
5. Check for CSS conflicts (z-index, overflow, position)

## Tips

- Use `mcp_playwright_browser_snapshot` over screenshots when you need to interact with elements
- Screenshots are better for visual verification of styling
- Always check both desktop and mobile views before committing UI changes
- Use descriptive filenames for screenshots
- Check console for JavaScript errors if interactions don't work
