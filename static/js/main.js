// main.js - Client-side logic for the Todo app
/**
 * Enable inline editing for a todo item.
 * @param {number} todoId - The ID of the todo to edit.
 */
function enableEdit(todoId) {
    const todoItem = document.getElementById(`todo-${todoId}`);
    todoItem.classList.add('edit-active');

    const input = todoItem.querySelector('.edit-form input');
    input.focus();
    input.setSelectionRange(input.value.length, input.value.length);
}

// Close edit mode on Escape key
// Event listener for global keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const activeItems = document.querySelectorAll('.edit-active');
        activeItems.forEach(item => item.classList.remove('edit-active'));
    }
});
