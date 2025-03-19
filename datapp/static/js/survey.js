// 将原来的JS代码提取到这个文件中

function addQuestion() {
    const container = document.getElementById('questions-container');
    const newQuestionHTML = `
        <div class="question-item border p-3 mb-2" style="background-color: #f8f9fa;">
            <input type="hidden" name="kept_question_ids[]" value="">
            <input type="text" name="question_text[]" class="form-control mb-2" placeholder="Enter question content">
            <select name="question_type[]" class="form-select mb-2" onchange="toggleOptionsInput(this)">
                <option value="0">Single Choice</option>
                <option value="1">Multiple Choice</option>
                <option value="2">Text Question</option>
            </select>
            <select name="is_required[]" class="form-select mb-2">
                <option value="0">Optional</option>
                <option value="1">Required</option>
            </select>
            <input type="text" name="options[]" class="form-control mb-2 options-input" placeholder="Options separated by | (for single/multiple choice only)" required>
            <button type="button" class="btn btn-danger" onclick="removeQuestion(this)">Delete Question</button>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', newQuestionHTML);
}

function removeQuestion(button) {
    button.closest('.question-item').remove();
}

function toggleOptionsInput(selectElement) {
    const optionsInput = selectElement.closest('.question-item').querySelector('.options-input');
    if (selectElement.value === '2') {
        optionsInput.style.display = 'none';
        optionsInput.removeAttribute('required');
    } else {
        optionsInput.style.display = 'block';
        optionsInput.setAttribute('required', 'required');
    }
}
