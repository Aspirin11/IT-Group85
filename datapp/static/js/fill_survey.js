document.getElementById('survey-form').addEventListener('submit', function(event) {
    let isValid = true;
    const requiredQuestions = document.querySelectorAll('[data-required="1"]');

    requiredQuestions.forEach(question => {
        const inputs = question.querySelectorAll('input, textarea');
        const isAnswered = Array.from(inputs).some(input => {
            if (input.type === 'radio' || input.type === 'checkbox') {
                return input.checked;
            } else {
                return input.value.trim() !== '';
            }
        });

        const errorMessage = question.querySelector('.error-message');

        if (!isAnswered) {
            isValid = false;
            question.classList.add('border', 'border-danger');
            if (errorMessage) {
                errorMessage.style.visibility = 'visible';
            }
        } else {
            question.classList.remove('border', 'border-danger');
            if (errorMessage) {
                errorMessage.style.visibility = 'hidden';
            }
        }
    });

    if (!isValid) {
        event.preventDefault();
    }
});