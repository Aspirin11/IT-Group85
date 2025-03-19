document.getElementById('survey-form').addEventListener('submit', function(event) {
    let isValid = true; // 标志表单是否有效
    const requiredQuestions = document.querySelectorAll('[data-required="1"]'); // 查找所有必填项

    requiredQuestions.forEach(question => {
        const inputs = question.querySelectorAll('input, textarea'); // 查找输入项
        const isAnswered = Array.from(inputs).some(input => {
            if (input.type === 'radio' || input.type === 'checkbox') {
                return input.checked;
            } else {
                return input.value.trim() !== '';
            }
        });

        const errorMessage = question.querySelector('.error-message'); // 获取错误信息元素

        if (!isAnswered) {
            isValid = false;
            question.classList.add('border', 'border-danger'); // 高亮未填写的问题
            if (errorMessage) {
                errorMessage.style.visibility = 'visible'; // 显示错误消息
            }
        } else {
            question.classList.remove('border', 'border-danger'); // 移除高亮
            if (errorMessage) {
                errorMessage.style.visibility = 'hidden'; // 隐藏错误消息
            }
        }
    });

    if (!isValid) {
        event.preventDefault(); // 阻止表单提交
    }
});