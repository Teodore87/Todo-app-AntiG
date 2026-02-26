// main.js - Client-side logic for the Todo app

/**
 * Enable inline editing for a todo item.
 * @param {number} todoId - The ID of the todo to edit.
 */
function enableEdit(todoId) {
    const todoItem = document.getElementById(`todo-${todoId}`);
    todoItem.classList.add('edit-active');

    const input = todoItem.querySelector('.edit-title');
    input.focus();
    input.setSelectionRange(input.value.length, input.value.length);
}

/**
 * Save todo via form submission. Triggered on blur.
 * @param {number} todoId 
 */
function saveTodo(todoId) {
    const todoItem = document.getElementById(`todo-${todoId}`);
    const form = document.getElementById(`edit-form-${todoId}`);

    // Check if we are still focusing something within the form
    // Short delay to allow new focus to land
    setTimeout(() => {
        if (!form.contains(document.activeElement)) {
            form.submit();
        }
    }, 100);
}

// Close edit mode on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const activeItems = document.querySelectorAll('.edit-active');
        activeItems.forEach(item => item.classList.remove('edit-active'));
    }
});
