/**
 * SecureBank - Main JavaScript file
 * This file contains custom JavaScript for the banking application
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Add event listeners for transaction filters
    setupTransactionFilters();
    
    // Setup PIN input behavior
    setupPinInputs();
    
    // Setup chart visualizations if present
    setupCharts();
    
    // Setup card flipping effect
    setupCardFlip();
    
    // Setup session timeout warning
    setupSessionTimeout();
    
    // Setup responsive navigation
    setupMobileNavigation();
});

/**
 * Initialize tooltips for enhanced UI
 */
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function(e) {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltipEl = document.createElement('div');
            tooltipEl.className = 'tooltip bg-gray-800 text-white px-2 py-1 rounded text-sm absolute z-50';
            tooltipEl.textContent = tooltipText;
            document.body.appendChild(tooltipEl);
            
            const rect = this.getBoundingClientRect();
            tooltipEl.style.top = rect.bottom + 10 + 'px';
            tooltipEl.style.left = rect.left + (rect.width / 2) - (tooltipEl.offsetWidth / 2) + 'px';
            
            this.addEventListener('mouseleave', function() {
                document.body.removeChild(tooltipEl);
            }, { once: true });
        });
    });
}

/**
 * Setup transaction filtering functionality
 */
function setupTransactionFilters() {
    const filterForm = document.getElementById('transaction-filter-form');
    if (!filterForm) return;
    
    const filterInputs = filterForm.querySelectorAll('input, select');
    filterInputs.forEach(input => {
        input.addEventListener('change', function() {
            filterForm.submit();
        });
    });
    
    const dateRangeSelect = document.getElementById('date-range');
    const customDateFields = document.getElementById('custom-date-fields');
    
    if (dateRangeSelect && customDateFields) {
        dateRangeSelect.addEventListener('change', function() {
            if (this.value === 'custom') {
                customDateFields.classList.remove('hidden');
            } else {
                customDateFields.classList.add('hidden');
            }
        });
    }
}

/**
 * Setup PIN input behavior for secure entry
 */
function setupPinInputs() {
    const pinInputs = document.querySelectorAll('.pin-input');
    
    pinInputs.forEach(input => {
        // Only allow numbers
        input.addEventListener('keypress', function(e) {
            if (!/\d/.test(e.key)) {
                e.preventDefault();
            }
        });
        
        // Auto-focus next input
        input.addEventListener('input', function() {
            if (this.value.length >= this.maxLength) {
                const nextInput = this.nextElementSibling;
                if (nextInput && nextInput.classList.contains('pin-input')) {
                    nextInput.focus();
                }
            }
        });
        
        // Handle backspace
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Backspace' && this.value.length === 0) {
                const prevInput = this.previousElementSibling;
                if (prevInput && prevInput.classList.contains('pin-input')) {
                    prevInput.focus();
                }
            }
        });
    });
}

/**
 * Setup charts for data visualization
 */
function setupCharts() {
    const transactionChartElement = document.getElementById('transaction-chart');
    if (!transactionChartElement) return;
    
    // This is a placeholder function that would typically use a charting library like Chart.js
    // In a production environment, you would include Chart.js and implement proper charts
    console.log('Chart visualization would be initialized here');
}

/**
 * Setup card flipping effect for card details
 */
function setupCardFlip() {
    const cardElements = document.querySelectorAll('.card-flip');
    
    cardElements.forEach(card => {
        card.addEventListener('click', function() {
            this.classList.toggle('is-flipped');
        });
    });
}

/**
 * Setup session timeout warning for security
 */
function setupSessionTimeout() {
    // Session timeout in seconds (14 minutes = 840 seconds)
    const sessionTimeout = 840;
    const warningTime = 60; // Show warning 1 minute before timeout
    
    let timeoutWarningShown = false;
    let timeoutTimer = null;
    
    function resetTimer() {
        clearTimeout(timeoutTimer);
        timeoutWarningShown = false;
        
        timeoutTimer = setTimeout(function() {
            showTimeoutWarning();
        }, (sessionTimeout - warningTime) * 1000);
    }
    
    function showTimeoutWarning() {
        if (timeoutWarningShown) return;
        timeoutWarningShown = true;
        
        const warningEl = document.createElement('div');
        warningEl.className = 'fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50';
        warningEl.innerHTML = `
            <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
                <h3 class="text-xl font-bold mb-4">Session Timeout Warning</h3>
                <p class="mb-4">Your session will expire in less than a minute due to inactivity.</p>
                <div class="flex justify-end space-x-3">
                    <button id="logout-btn" class="px-4 py-2 bg-gray-200 rounded">Logout</button>
                    <button id="continue-btn" class="px-4 py-2 bg-primary-600 text-white rounded">Continue Session</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(warningEl);
        
        document.getElementById('logout-btn').addEventListener('click', function() {
            window.location.href = '/users/logout/';
        });
        
        document.getElementById('continue-btn').addEventListener('click', function() {
            document.body.removeChild(warningEl);
            resetTimer();
            
            // Send a request to keep session alive
            fetch('/api/keep-alive/', { method: 'POST', credentials: 'same-origin' });
        });
    }
    
    // Events that reset the timer
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];
    events.forEach(event => {
        document.addEventListener(event, resetTimer, true);
    });
    
    // Initialize the timer
    resetTimer();
}

/**
 * Setup mobile navigation for responsive design
 */
function setupMobileNavigation() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (!mobileMenuButton || !mobileMenu) return;
    
    mobileMenuButton.addEventListener('click', function() {
        mobileMenu.classList.toggle('hidden');
    });
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
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(date);
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
    const errorElement = field.nextElementSibling;
    
    if (!isValid) {
        field.classList.add('border-red-500');
        if (errorElement && errorElement.classList.contains('error-message')) {
            errorElement.textContent = errorMessage;
            errorElement.classList.remove('hidden');
        }
    } else {
        field.classList.remove('border-red-500');
        if (errorElement && errorElement.classList.contains('error-message')) {
            errorElement.classList.add('hidden');
        }
    }
    
    return isValid;
}