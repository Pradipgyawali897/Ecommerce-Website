// Modern Product Form JavaScript for Django
document.addEventListener('DOMContentLoaded', function() {
    // Initialize form functionality
    initializeForm();
    setupFileUpload();
    setupFormValidation();
    setupFormSubmission();
});

function initializeForm() {
    // Add floating label effect for all form inputs
    const inputs = document.querySelectorAll('.form-group input, .form-group select, .form-group textarea');
    inputs.forEach(input => {
        // Add focus/blur effects
        input.addEventListener('focus', function() {
            this.closest('.form-group').classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.closest('.form-group').classList.remove('focused');
            }
        });
        
        // Check if input has value on load
        if (input.value) {
            input.closest('.form-group').classList.add('focused');
        }
    });
    
    // Auto-generate SKU based on product name (if SKU field exists)
    const productNameInput = document.querySelector('input[name*="product_name"], input[name*="name"]');
    const skuInput = document.querySelector('input[name*="sku"]');
    
    if (productNameInput && skuInput) {
        productNameInput.addEventListener('input', function() {
            if (!skuInput.value || skuInput.dataset.autoGenerated === 'true') {
                const sku = generateSKU(this.value);
                skuInput.value = sku;
                skuInput.dataset.autoGenerated = 'true';
            }
        });
        
        skuInput.addEventListener('input', function() {
            this.dataset.autoGenerated = 'false';
        });
    }
    
    // Enhanced select styling
    const selects = document.querySelectorAll('select');
    selects.forEach(select => {
        select.addEventListener('change', function() {
            if (this.value) {
                this.classList.add('has-value');
            } else {
                this.classList.remove('has-value');
            }
        });
        
        // Check initial value
        if (select.value) {
            select.classList.add('has-value');
        }
    });
}

function generateSKU(productName) {
    if (!productName) return '';
    
    // Create SKU from product name
    const cleanName = productName
        .replace(/[^a-zA-Z0-9\s]/g, '')
        .trim()
        .toUpperCase()
        .split(' ')
        .slice(0, 3)
        .map(word => word.substring(0, 3))
        .join('');
    
    // Add random number
    const randomNum = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
    
    return `${cleanName}-${randomNum}`;
}

function setupFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(fileInput => {
        const formGroup = fileInput.closest('.form-group');
        if (!formGroup) return;
        
        // Create preview container
        const previewContainer = document.createElement('div');
        previewContainer.className = 'file-preview-container';
        formGroup.appendChild(previewContainer);

        // Handle file selection
        fileInput.addEventListener('change', function() {
            previewContainer.innerHTML = ''; // Clear previous previews
            const files = this.files;

            if (files.length > 0) {
                Array.from(files).forEach(file => {
                    if (file.type.startsWith('image/')) {
                        // Create image preview
                        const img = document.createElement('img');
                        img.className = 'file-preview';
                        img.src = URL.createObjectURL(file);
                        previewContainer.appendChild(img);
                    } else {
                        // Create file name display
                        const fileName = document.createElement('span');
                        fileName.className = 'file-name';
                        fileName.textContent = file.name;
                        previewContainer.appendChild(fileName);
                    }
                });
                formGroup.classList.add('has-files');
            } else {
                formGroup.classList.remove('has-files');
            }
        });

        // Drag and drop support
        formGroup.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });

        formGroup.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
        });

        formGroup.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            fileInput.files = e.dataTransfer.files;
            fileInput.dispatchEvent(new Event('change'));
        });
    });
}

function setupFormValidation() {
    const form = document.querySelector('form');
    if (!form) return;

    // Real-time validation
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            validateField(this);
        });
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });

    // Custom validation patterns
    const patterns = {
        price: /^\d+(\.\d{1,2})?$/,
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        number: /^\d+$/,
    };

    function validateField(field) {
        const formGroup = field.closest('.form-group');
        if (!formGroup) return;

        let isValid = true;
        const errorMessage = formGroup.querySelector('.error-message') || document.createElement('div');
        errorMessage.className = 'error-message';

        // Check required
        if (field.required && !field.value.trim()) {
            isValid = false;
            errorMessage.textContent = 'This field is required';
        }

        // Check pattern
        if (isValid && field.dataset.pattern && patterns[field.dataset.pattern]) {
            isValid = patterns[field.dataset.pattern].test(field.value);
            errorMessage.textContent = `Please enter a valid ${field.dataset.pattern}`;
        }

        // Update UI
        if (!isValid) {
            formGroup.classList.add('has-error');
            if (!formGroup.querySelector('.error-message')) {
                formGroup.appendChild(errorMessage);
            }
        } else {
            formGroup.classList.remove('has-error');
            if (formGroup.querySelector('.error-message')) {
                formGroup.removeChild(errorMessage);
            }
        }

        return isValid;
    }

    // Validate entire form
    form.validate = function() {
        let isValid = true;
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });
        return isValid;
    };
}

function setupFormSubmission() {
    const form = document.querySelector('form');
    if (!form) return;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Validate form
        if (!form.validate()) {
            const firstError = form.querySelector('.has-error');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth' });
            }
            return;
        }

        // Show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.classList.add('loading');
        }

        try {
            // Create form data
            const formData = new FormData(form);

            // Handle CSRF for Django
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
            if (csrfToken) {
                formData.append('csrfmiddlewaretoken', csrfToken.value);
            }

            // Submit form
            const response = await fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // For Django AJAX detection
                }
            });

            const result = await response.json();

            // Handle response
            if (response.ok) {
                // Success handling
                showSuccessMessage(result.message || 'Form submitted successfully!');
                form.reset();
                document.querySelectorAll('.form-group').forEach(group => {
                    group.classList.remove('focused', 'has-files', 'has-error');
                });
            } else {
                // Error handling
                showErrorMessage(result.error || 'An error occurred. Please try again.');
            }
        } catch (error) {
            showErrorMessage('Network error. Please try again.');
        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.classList.remove('loading');
            }
        }
    });
}

function showSuccessMessage(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

function showErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 3000);
}