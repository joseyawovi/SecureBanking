/**
 * SecureBank - Main JavaScript
 * A comprehensive set of functions for the banking application
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeTooltips();
    setupTransactionFilters();
    setupPinInputs();
    setupCharts();
    setupCardFlip();
    setupSessionTimeout();
    setupMobileNavigation();
});

/**
 * Initialize tooltips for enhanced UI
 */
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltipEl = document.createElement('div');
            tooltipEl.classList.add('tooltip');
            tooltipEl.textContent = tooltipText;
            tooltipEl.style.position = 'absolute';
            tooltipEl.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
            tooltipEl.style.color = 'white';
            tooltipEl.style.padding = '5px 10px';
            tooltipEl.style.borderRadius = '4px';
            tooltipEl.style.fontSize = '14px';
            tooltipEl.style.zIndex = '1000';
            
            document.body.appendChild(tooltipEl);
            
            const rect = this.getBoundingClientRect();
            tooltipEl.style.top = (rect.bottom + 10) + 'px';
            tooltipEl.style.left = (rect.left + rect.width / 2 - tooltipEl.offsetWidth / 2) + 'px';
        });
        
        tooltip.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
}

/**
 * Setup transaction filtering functionality
 */
function setupTransactionFilters() {
    const filterToggle = document.getElementById('filter-toggle');
    const filterForm = document.getElementById('transaction-filters');
    
    if (filterToggle && filterForm) {
        filterToggle.addEventListener('click', function() {
            filterForm.classList.toggle('collapsed');
            const isCollapsed = filterForm.classList.contains('collapsed');
            filterToggle.innerHTML = isCollapsed 
                ? '<i class="fas fa-filter"></i> Show Filters' 
                : '<i class="fas fa-filter"></i> Hide Filters';
        });
    }
    
    // Date range picker for transaction filters
    const dateRangeStart = document.getElementById('date-range-start');
    const dateRangeEnd = document.getElementById('date-range-end');
    
    if (dateRangeStart && dateRangeEnd) {
        dateRangeStart.addEventListener('change', function() {
            dateRangeEnd.min = this.value;
        });
        
        dateRangeEnd.addEventListener('change', function() {
            dateRangeStart.max = this.value;
        });
    }
}

/**
 * Setup PIN input behavior for secure entry
 */
function setupPinInputs() {
    const pinInputs = document.querySelectorAll('.pin-input');
    
    pinInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Replace any character that's not a digit
            this.value = this.value.replace(/\D/g, '');
            
            // Limit to 4 digits
            if (this.value.length > 4) {
                this.value = this.value.slice(0, 4);
            }
        });
        
        // Auto-focus next input
        input.addEventListener('keyup', function(e) {
            if (this.value.length >= 4 && e.key !== 'Backspace' && e.key !== 'Delete') {
                const nextInput = this.nextElementSibling;
                if (nextInput && nextInput.tagName === 'INPUT') {
                    nextInput.focus();
                } else {
                    // If it's the last input, focus on the submit button
                    const submitButton = this.form.querySelector('button[type="submit"]');
                    if (submitButton) {
                        submitButton.focus();
                    }
                }
            }
        });
    });
}

/**
 * Setup charts for data visualization
 */
function setupCharts() {
    // Balance trend chart
    const balanceTrendCtx = document.getElementById('balance-trend-chart');
    
    if (balanceTrendCtx) {
        // This is a placeholder - in a real application, we'd use a charting library
        // such as Chart.js to create the actual chart.
        const chartContainer = balanceTrendCtx.parentElement;
        chartContainer.innerHTML = '<div class="flex justify-center items-center h-full text-gray-500">Chart data loading...</div>';
        
        // Simulate loading chart data
        setTimeout(() => {
            chartContainer.innerHTML = '<div class="flex justify-center items-center h-full text-green-600"><i class="fas fa-chart-line text-5xl"></i></div>';
        }, 1000);
    }
    
    // Spending categories chart
    const spendingCategoriesCtx = document.getElementById('spending-categories-chart');
    
    if (spendingCategoriesCtx) {
        // This is a placeholder - in a real application, we'd use a charting library
        const chartContainer = spendingCategoriesCtx.parentElement;
        chartContainer.innerHTML = '<div class="flex justify-center items-center h-full text-gray-500">Chart data loading...</div>';
        
        // Simulate loading chart data
        setTimeout(() => {
            chartContainer.innerHTML = '<div class="flex justify-center items-center h-full text-green-600"><i class="fas fa-chart-pie text-5xl"></i></div>';
        }, 1000);
    }
}

/**
 * Setup card flipping effect for card details
 */
function setupCardFlip() {
    const cards = document.querySelectorAll('.credit-card-container');
    
    cards.forEach(cardContainer => {
        const flipButton = cardContainer.querySelector('.flip-card');
        const card = cardContainer.querySelector('.credit-card');
        
        if (flipButton && card) {
            flipButton.addEventListener('click', function(e) {
                e.preventDefault();
                card.classList.toggle('is-flipped');
                
                // Change the button text based on the current state
                const isFlipped = card.classList.contains('is-flipped');
                flipButton.innerHTML = isFlipped 
                    ? '<i class="fas fa-undo"></i> Show Front' 
                    : '<i class="fas fa-sync"></i> Show Details';
            });
        }
    });
}

/**
 * Setup session timeout warning for security
 */
function setupSessionTimeout() {
    let idleTime = 0;
    const idleInterval = 60000; // 1 minute
    const timeoutWarning = 15; // Warning after 15 minutes of inactivity
    const timeoutLimit = 20; // Logout after 20 minutes of inactivity
    
    // Reset the idle timer on user activity
    const resetEvents = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];
    resetEvents.forEach(event => {
        document.addEventListener(event, resetTimer, true);
    });
    
    // Check idle time every minute
    setInterval(function() {
        idleTime += 1;
        
        if (idleTime >= timeoutWarning && idleTime < timeoutLimit) {
            showTimeoutWarning();
        } else if (idleTime >= timeoutLimit) {
            // Redirect to logout
            window.location.href = '/users/logout/';
        }
    }, idleInterval);
    
    function resetTimer() {
        idleTime = 0;
        
        // Hide the timeout warning if it's visible
        const timeoutWarningEl = document.getElementById('session-timeout-warning');
        if (timeoutWarningEl) {
            timeoutWarningEl.classList.add('hidden');
        }
    }
    
    function showTimeoutWarning() {
        let timeoutWarningEl = document.getElementById('session-timeout-warning');
        
        // Create the warning element if it doesn't exist
        if (!timeoutWarningEl) {
            timeoutWarningEl = document.createElement('div');
            timeoutWarningEl.id = 'session-timeout-warning';
            timeoutWarningEl.classList.add(
                'fixed', 'bottom-4', 'right-4', 'bg-yellow-100', 
                'border-l-4', 'border-yellow-500', 'text-yellow-700', 
                'p-4', 'shadow-lg', 'rounded', 'z-50'
            );
            
            timeoutWarningEl.innerHTML = `
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i class="fas fa-exclamation-triangle text-yellow-600"></i>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium">
                            Your session is about to expire due to inactivity.
                        </p>
                        <p class="text-xs mt-1">
                            You will be logged out in ${timeoutLimit - timeoutWarning} minutes.
                        </p>
                        <div class="mt-2">
                            <button type="button" id="extend-session" class="text-sm font-medium text-yellow-700 hover:text-yellow-600">
                                Click here to stay logged in
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(timeoutWarningEl);
            
            // Add event listener to the "stay logged in" button
            document.getElementById('extend-session').addEventListener('click', function() {
                resetTimer();
                timeoutWarningEl.classList.add('hidden');
            });
        } else {
            timeoutWarningEl.classList.remove('hidden');
        }
    }
}

/**
 * Setup mobile navigation for responsive design
 */
function setupMobileNavigation() {
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

/**
 * Show a confirmation dialog
 * @param {string} message - The confirmation message to display
 * @param {function} callback - The callback function to execute if confirmed
 */
function confirmAction(message, callback) {
    if (window.confirm(message)) {
        callback();
    }
}

/**
 * Format currency for display
 * @param {number} amount - The amount to format
 * @param {string} currency - The currency code (default: USD)
 * @return {string} The formatted currency string
 */
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

/**
 * Format date for display
 * @param {string} dateString - The date string to format
 * @return {string} The formatted date string
 */
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    
    return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Validate a form field
 * @param {HTMLElement} field - The field to validate
 * @param {function} validator - The validation function
 * @param {string} errorMessage - The error message to display
 * @return {boolean} Whether the field is valid
 */
function validateField(field, validator, errorMessage) {
    const isValid = validator(field.value);
    
    if (!isValid) {
        // Create or update error message
        let errorElement = field.nextElementSibling;
        
        if (!errorElement || !errorElement.classList.contains('error-message')) {
            errorElement = document.createElement('p');
            errorElement.classList.add('error-message', 'text-red-500', 'text-xs', 'mt-1');
            field.parentNode.insertBefore(errorElement, field.nextSibling);
        }
        
        errorElement.textContent = errorMessage;
        field.classList.add('border-red-500');
    } else {
        // Remove error message if it exists
        const errorElement = field.nextElementSibling;
        
        if (errorElement && errorElement.classList.contains('error-message')) {
            errorElement.remove();
        }
        
        field.classList.remove('border-red-500');
    }
    
    return isValid;
}