/**
 * SecureBank - Main JavaScript File
 * Contains client-side functionality for the banking system application
 */

// Execute when DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize popovers
    initializePopovers();
    
    // Initialize session timeout warning
    initializeSessionTimeout();
    
    // Initialize transaction data table (if present)
    initializeDataTables();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize card copy functionality
    initializeCardCopy();
    
    // Handle alert dismissal
    initializeAlertDismissal();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize Bootstrap popovers
 */
function initializePopovers() {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Initialize alert dismissal with fade out
 */
function initializeAlertDismissal() {
    // Auto-dismiss success alerts after 5 seconds
    setTimeout(function() {
        var successAlerts = document.querySelectorAll('.alert-success');
        successAlerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            setTimeout(function() {
                bsAlert.close();
            }, 5000);
        });
    }, 500);

    // Handle manual alert dismissal
    document.querySelectorAll('.alert .btn-close').forEach(function(button) {
        button.addEventListener('click', function() {
            var alert = this.closest('.alert');
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 300);
        });
    });
}

/**
 * Initialize datatable functionality if table exists
 */
function initializeDataTables() {
    var transactionTable = document.getElementById('transactionTable');
    if (transactionTable) {
        // Add simple search functionality to transaction table
        var searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.classList.add('form-control', 'mb-3');
        searchInput.placeholder = 'Search transactions...';
        transactionTable.parentNode.insertBefore(searchInput, transactionTable);
        
        searchInput.addEventListener('keyup', function() {
            var searchTerm = this.value.toLowerCase();
            var rows = transactionTable.querySelectorAll('tbody tr');
            
            rows.forEach(function(row) {
                var text = row.textContent.toLowerCase();
                if (text.indexOf(searchTerm) > -1) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
}

/**
 * Initialize session timeout warning
 * Shows a warning before the session expires
 */
function initializeSessionTimeout() {
    // Check if user is logged in by looking for logout link
    var logoutLink = document.querySelector('a[href*="logout"]');
    if (!logoutLink) {
        return; // User not logged in, no need for timeout warning
    }
    
    // Session timeout warning (13 minutes, with 2 minutes warning before 15-minute server timeout)
    var warningTime = 13 * 60 * 1000; // 13 minutes
    
    var timeoutWarning = setTimeout(function() {
        // Create modal if it doesn't exist
        var modalId = 'sessionTimeoutModal';
        var modal = document.getElementById(modalId);
        
        if (!modal) {
            // Create the modal
            modal = document.createElement('div');
            modal.id = modalId;
            modal.className = 'modal fade';
            modal.tabIndex = '-1';
            modal.setAttribute('aria-labelledby', 'sessionTimeoutModalLabel');
            modal.setAttribute('aria-hidden', 'true');
            
            modal.innerHTML = `
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header bg-warning text-dark">
                            <h5 class="modal-title" id="sessionTimeoutModalLabel">
                                <i class="fas fa-exclamation-triangle me-2"></i>Session Timeout Warning
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <p>Your session is about to expire due to inactivity. You will be logged out in <span id="sessionCountdown">120</span> seconds.</p>
                            <p>Do you want to continue your session?</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Log Out Now</button>
                            <button type="button" class="btn btn-primary" id="extendSession">Continue Session</button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // Add event listener to the extend session button
            document.getElementById('extendSession').addEventListener('click', function() {
                refreshSession();
                var bsModal = bootstrap.Modal.getInstance(modal);
                bsModal.hide();
            });
        }
        
        // Show the modal
        var bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        // Start countdown
        var secondsLeft = 120;
        var countdownEl = document.getElementById('sessionCountdown');
        
        var countdownInterval = setInterval(function() {
            secondsLeft--;
            if (countdownEl) {
                countdownEl.textContent = secondsLeft;
            }
            
            if (secondsLeft <= 0) {
                clearInterval(countdownInterval);
                window.location.href = logoutLink.href; // Redirect to logout
            }
        }, 1000);
        
        // Clear interval if modal is closed
        modal.addEventListener('hidden.bs.modal', function() {
            clearInterval(countdownInterval);
        });
        
    }, warningTime);
    
    // Reset timeout warning on user activity
    var events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];
    
    events.forEach(function(event) {
        document.addEventListener(event, function() {
            clearTimeout(timeoutWarning);
            timeoutWarning = setTimeout(function() {
                // Show warning modal
                var modal = document.getElementById('sessionTimeoutModal');
                if (modal) {
                    var bsModal = new bootstrap.Modal(modal);
                    bsModal.show();
                }
            }, warningTime);
        }, false);
    });
}

/**
 * Refresh the user session by making a request to the server
 */
function refreshSession() {
    // Make AJAX request to refresh CSRF token
    fetch(window.location.href, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    }).then(function(response) {
        if (response.ok) {
            console.log('Session refreshed successfully');
        }
    }).catch(function(error) {
        console.error('Error refreshing session:', error);
    });
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    var forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        // Add submit event listener
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            // Mark all fields as validated
            form.classList.add('was-validated');
        }, false);
        
        // Check password fields for match
        var password1 = form.querySelector('input[name="password1"]');
        var password2 = form.querySelector('input[name="password2"]');
        
        if (password1 && password2) {
            password2.addEventListener('input', function() {
                if (password1.value !== password2.value) {
                    password2.setCustomValidity('Passwords do not match');
                } else {
                    password2.setCustomValidity('');
                }
            });
            
            password1.addEventListener('input', function() {
                if (password2.value && password1.value !== password2.value) {
                    password2.setCustomValidity('Passwords do not match');
                } else {
                    password2.setCustomValidity('');
                }
            });
        }
        
        // PIN validation
        var pinInputs = form.querySelectorAll('input[name$="pin"]');
        pinInputs.forEach(function(input) {
            input.addEventListener('input', function() {
                var value = this.value;
                
                // Clean input - only digits allowed
                if (/[^0-9]/.test(value)) {
                    this.value = value.replace(/[^0-9]/g, '');
                }
                
                // Check length
                if (value.length !== 4) {
                    this.setCustomValidity('PIN must be exactly 4 digits');
                } else {
                    this.setCustomValidity('');
                }
            });
        });
        
        // Amount validation
        var amountInputs = form.querySelectorAll('input[name="amount"]');
        amountInputs.forEach(function(input) {
            input.addEventListener('input', function() {
                var value = parseFloat(this.value);
                
                if (isNaN(value) || value <= 0) {
                    this.setCustomValidity('Amount must be greater than zero');
                } else {
                    this.setCustomValidity('');
                }
            });
        });
    });
}

/**
 * Initialize copy functionality for card details
 */
function initializeCardCopy() {
    var copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var textToCopy = this.getAttribute('data-copy');
            var originalText = this.innerHTML;
            
            // Create temporary input element
            var tempInput = document.createElement('input');
            tempInput.value = textToCopy;
            document.body.appendChild(tempInput);
            
            // Select and copy text
            tempInput.select();
            document.execCommand('copy');
            
            // Remove temporary element
            document.body.removeChild(tempInput);
            
            // Update button text
            this.innerHTML = '<i class="fas fa-check"></i> Copied';
            
            // Reset button text after 2 seconds
            setTimeout(function() {
                button.innerHTML = originalText;
            }, 2000);
        });
    });
}

/**
 * Toggle password/PIN visibility
 * @param {string} inputId - ID of the input element
 * @param {string} toggleId - ID of the toggle button
 */
function togglePasswordVisibility(inputId, toggleId) {
    var input = document.getElementById(inputId);
    var toggle = document.getElementById(toggleId);
    
    if (input && toggle) {
        if (input.type === 'password') {
            input.type = 'text';
            toggle.innerHTML = '<i class="fas fa-eye-slash"></i>';
        } else {
            input.type = 'password';
            toggle.innerHTML = '<i class="fas fa-eye"></i>';
        }
    }
}

/**
 * Format currency input to show proper decimal places
 * @param {object} input - Input element
 */
function formatCurrency(input) {
    var value = input.value.replace(/[^\d.]/g, '');
    
    // Ensure only one decimal point
    var parts = value.split('.');
    if (parts.length > 2) {
        value = parts[0] + '.' + parts.slice(1).join('');
    }
    
    // Format to 2 decimal places if there's a decimal point
    if (value.includes('.')) {
        var decimalPart = parts[1] || '';
        if (decimalPart.length > 2) {
            value = parts[0] + '.' + decimalPart.substring(0, 2);
        }
    }
    
    input.value = value;
}

/**
 * Show a confirmation dialog before proceeding with an action
 * @param {string} message - Confirmation message to show
 * @returns {boolean} - True if confirmed, false otherwise
 */
function confirmAction(message) {
    return confirm(message || 'Are you sure you want to proceed?');
}
