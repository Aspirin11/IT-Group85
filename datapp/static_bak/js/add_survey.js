function addQuestion() {
    const container = document.getElementById('questions-container');
    const newQuestionHTML = `
        <div class="question-item border p-3 mb-2">
            <input type="hidden" name="kept_question_ids[]" value="">
            <input type="text" name="question_text[]" class="form-control mb-2" placeholder="Enter question content">
            <select name="question_type[]" class="form-select mb-2">
                <option value="0">Single Choice</option>
                <option value="1">Multiple Choice</option>
                <option value="2">Text Question</option>
            </select>
            <select name="is_required[]" class="form-select mb-2">
                <option value="0">Optional</option>
                <option value="1">Required</option>
            </select>
            <input type="text" name="options[]" class="form-control mb-2" placeholder="Options separated by | (for single/multiple choice only)">
            <button type="button" class="btn btn-danger" onclick="removeQuestion(this)">Delete Question</button>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', newQuestionHTML);
}

function removeQuestion(button) {
    button.closest('.question-item').remove();
}