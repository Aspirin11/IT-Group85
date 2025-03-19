// Function to add a new question
function addQuestion() {
    const container = document.getElementById('questions-container');
    const newQuestionHTML = `
        <div class="question-item">
            <input type="hidden" name="kept_question_ids[]" value="">
            <input type="text" name="question_text[]" value="">

            <select name="question_type[]">
                <option value="0">Single Choice</option>
                <option value="1">Multiple Choice</option>
                <option value="2">Text Question</option>
            </select>

            <select name="is_required[]">
                <option value="0">Optional</option>
                <option value="1">Required</option>
            </select>

            <input type="text" name="options[]" placeholder="Options separated by | (for single/multiple choice only)">

            <button type="button" onclick="removeQuestion(this)" class="btn btn-danger" style="margin-bottom: 10px;">Delete Question</button>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', newQuestionHTML);
}


function removeQuestion(button) {
    button.closest('.question-item').remove();
}