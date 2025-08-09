let isInteractionsBlocked = false;
let tooltip = null;
let blurStylesInjected = false;
let containerElements = []; // Array to store multiple containers

// Inject CSS for blur effect
function injectBlurStyles() {
    if (blurStylesInjected) return;
    
    const style = document.createElement('style');
    style.textContent = `
        .interaction-blocked-blur {
            filter: blur(2px);
            transition: filter 0.3s ease;
        }
        .interaction-blocked-blur:hover {
            filter: blur(2px);
        }
    `;
    document.head.appendChild(style);
    blurStylesInjected = true;
}

// Create the tooltip element
function createTooltip() {
    tooltip = document.createElement('div');
    tooltip.textContent = 'You cannot interact with the page right now';
    tooltip.style.cssText = `
        position: fixed;
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 14px;
        pointer-events: none;
        z-index: 10000;
        display: none;
        transition: opacity 0.3s;
    `;
    document.body.appendChild(tooltip);
}

// Show tooltip at position
function showTooltip(x, y) {
    if (!tooltip) createTooltip();
    
    tooltip.style.left = `${x}px`;
    tooltip.style.top = `${y}px`;
    tooltip.style.display = 'block';
    
    // Hide after 2 seconds
    setTimeout(() => {
        tooltip.style.display = 'none';
    }, 2000);
}

// Check if element is within any of our containers
function isWithinContainer(element) {
    if (containerElements.length === 0) return false;
    
    for (const container of containerElements) {
        // If container is a string selector
        if (typeof container === 'string') {
            if (element.closest(container) !== null) return true;
        } 
        // If container is a DOM element
        else if (container.contains(element) || element === container) {
            return true;
        }
    }
    
    return false;
}

// In your block-interactions.js file, update the selectors in handleInteraction and handleKeydown functions:

// Handle interaction attempts with blur effect
function handleInteraction(event) {
    if (!isInteractionsBlocked) return;
    
    // Check if target is an interactive element - UPDATED SELECTOR
    const interactiveElement = event.target.closest(
        'button, input, select, textarea, a, [role="button"], [tabindex]:not([tabindex="-1"]), [onclick]'
    );
    
    // Only block if element is within any of our containers
    if (interactiveElement && isWithinContainer(interactiveElement)) {
        event.preventDefault();
        event.stopPropagation();
        
        // Add blur effect
        interactiveElement.classList.add('interaction-blocked-blur');
        
        // Remove blur effect after animation
        setTimeout(() => {
            interactiveElement.classList.remove('interaction-blocked-blur');
        }, 500);
        
        // Show tooltip at cursor position
        showTooltip(event.clientX, event.clientY);
    }
}

// Handle keyboard interactions
function handleKeydown(event) {
    if (!isInteractionsBlocked) return;
    
    // Check if target is an interactive element - UPDATED SELECTOR
    const interactiveElement = event.target.closest(
        'button, input, select, textarea, a, [role="button"], [tabindex]:not([tabindex="-1"]), [onclick]'
    );
    
    // Only block if element is within any of our containers
    if (interactiveElement && isWithinContainer(interactiveElement)) {
        // Allow navigation keys
        const allowedKeys = ['Tab', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Escape'];
        if (!allowedKeys.includes(event.key)) {
            event.preventDefault();
            
            // Add blur effect
            interactiveElement.classList.add('interaction-blocked-blur');
            
            // Remove blur effect after animation
            setTimeout(() => {
                interactiveElement.classList.remove('interaction-blocked-blur');
            }, 500);
            
            // Show tooltip near element
            const rect = interactiveElement.getBoundingClientRect();
            showTooltip(rect.left + rect.width / 2, rect.top + rect.height / 2);
        }
    }
}

// Block all interactions within specific containers
function blockInteractions(containers) {
    // If this is the first call, set up the blocking
    if (!isInteractionsBlocked) {
        isInteractionsBlocked = true;
        
        // Inject blur styles
        injectBlurStyles();
        
        // Create tooltip if needed
        if (!tooltip) createTooltip();
        
        // Add event listeners
        document.addEventListener('mousedown', handleInteraction, true);
        document.addEventListener('click', handleInteraction, true);
        document.addEventListener('touchstart', handleInteraction, true);
        document.addEventListener('keydown', handleKeydown, true);
        document.addEventListener('submit', (e) => {
            if (isWithinContainer(e.target)) {
                e.preventDefault();
            }
        }, true);
    }
    
    // Add containers to our array
    if (Array.isArray(containers)) {
        containers.forEach(container => {
            if (!containerElements.includes(container)) {
                containerElements.push(container);
            }
        });
    } else {
        if (!containerElements.includes(containers)) {
            containerElements.push(containers);
        }
    }
    
    // Add visual cue to all containers
    containerElements.forEach(container => {
        if (typeof container === 'string') {
            document.querySelectorAll(container).forEach(el => {
                el.style.cursor = 'not-allowed';
            });
        } else if (container) {
            container.style.cursor = 'not-allowed';
        }
    });
}

// Restore interactions
function restoreInteractions() {
    if (!isInteractionsBlocked) return;
    isInteractionsBlocked = false;
    
    // Remove event listeners
    document.removeEventListener('mousedown', handleInteraction, true);
    document.removeEventListener('click', handleInteraction, true);
    document.removeEventListener('touchstart', handleInteraction, true);
    document.removeEventListener('keydown', handleKeydown, true);
    
    // Remove visual cue from all containers
    containerElements.forEach(container => {
        if (typeof container === 'string') {
            document.querySelectorAll(container).forEach(el => {
                el.style.cursor = '';
            });
        } else if (container) {
            container.style.cursor = '';
        }
    });
    
    // Remove any remaining blur effects
    document.querySelectorAll('.interaction-blocked-blur').forEach(el => {
        el.classList.remove('interaction-blocked-blur');
    });
    
    // Clear container references
    containerElements = [];
}

// Usage in Django template:
// <script>
//   // Block interactions within multiple containers
//   blockInteractions(['#first', '#second', '#third']);
//   
//   // Or add containers one by one
//   blockInteractions('#first');
//   blockInteractions('#second');
//   
//   // Later, when ready to restore interactions
//   restoreInteractions();
// </script>