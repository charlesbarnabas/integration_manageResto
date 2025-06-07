// Menangani pesan flash
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 3 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 500);
        }, 3000);
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error');
                } else {
                    input.classList.remove('error');
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    });

    // Password strength indicator - hanya untuk halaman register
    const passwordInput = document.querySelector('input[type="password"]');
    const isRegisterPage = document.querySelector('form').action.includes('register');
    
    if (passwordInput && isRegisterPage) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            
            if (password.length >= 8) strength++;
            if (password.match(/[a-z]/)) strength++;
            if (password.match(/[A-Z]/)) strength++;
            if (password.match(/[0-9]/)) strength++;
            if (password.match(/[^a-zA-Z0-9]/)) strength++;

            const strengthIndicator = document.createElement('div');
            strengthIndicator.className = 'password-strength';
            
            let strengthText = '';
            let strengthClass = '';
            
            switch(strength) {
                case 0:
                case 1:
                    strengthText = 'Very Weak';
                    strengthClass = 'very-weak';
                    break;
                case 2:
                    strengthText = 'Weak';
                    strengthClass = 'weak';
                    break;
                case 3:
                    strengthText = 'Medium';
                    strengthClass = 'medium';
                    break;
                case 4:
                    strengthText = 'Strong';
                    strengthClass = 'strong';
                    break;
                case 5:
                    strengthText = 'Very Strong';
                    strengthClass = 'very-strong';
                    break;
            }

            strengthIndicator.textContent = strengthText;
            strengthIndicator.className = `password-strength ${strengthClass}`;

            const existingIndicator = document.querySelector('.password-strength');
            if (existingIndicator) {
                existingIndicator.remove();
            }
            
            if (password.length > 0) {
                this.parentNode.appendChild(strengthIndicator);
            }
        });
    }
}); 