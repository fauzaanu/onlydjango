/**
 * Kandy - Generic HTMX Loading States & Animations
 * 
 * Automatically handles loading states for HTMX requests using data attributes:
 * - kandy-loading: Elements that show during loading
 * - kandy-content: Elements that hide during loading
 * + Adds smooth animations to content swaps
 */

document.addEventListener('DOMContentLoaded', function () {

    // X Clock Mechanism - Allow loading UI after JS initializes
    document.body.classList.add('js-loaded');

    // Initialize all loading states to be hidden by default
    document.querySelectorAll('[kandy-loading]').forEach(el => {
        el.style.display = 'none';
    });

    // Initialize all content states to be visible by default + add transitions
    document.querySelectorAll('[kandy-content]').forEach(el => {
        el.style.display = 'block';
        el.style.transition = 'opacity 600ms cubic-bezier(0.4, 0, 0.2, 1)';
    });

    // Generic HTMX loading state handler
    document.addEventListener('htmx:beforeRequest', function (evt) {
        // Find the target container
        const target = evt.detail.target;

        // Look for loading state elements within the target
        const loadingElements = target.querySelectorAll('[kandy-loading]');
        const contentElements = target.querySelectorAll('[kandy-content]');

        // Hide content, show loading
        contentElements.forEach(el => el.style.display = 'none');
        loadingElements.forEach(el => el.style.display = 'flex');
    });

    document.addEventListener('htmx:afterRequest', function (evt) {
        // Find the target container
        const target = evt.detail.target;

        // Look for loading state elements within the target
        const loadingElements = target.querySelectorAll('[kandy-loading]');
        const contentElements = target.querySelectorAll('[kandy-content]');

        // Show content, hide loading
        contentElements.forEach(el => el.style.display = 'block');
        loadingElements.forEach(el => el.style.display = 'none');
    });

    // Add animations after HTMX swaps new content in
    document.addEventListener('htmx:afterSwap', function (evt) {
        const target = evt.detail.target;

        // Find content elements in the new swapped content
        const contentElements = target.querySelectorAll('[kandy-content]');

        contentElements.forEach(el => {
            // Ensure smooth transition is set
            el.style.transition = 'opacity 600ms cubic-bezier(0.4, 0, 0.2, 1)';

            // Start with invisible
            el.style.opacity = '0';

            // Animate to visible after a small delay
            setTimeout(() => {
                el.style.opacity = '1';
            }, 50);
        });
    });

});