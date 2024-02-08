document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('fileInput').addEventListener('change', handleFileSelect, false);
})

function openFileInput() {
    document.getElementById('fileInput').click();
}
function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file) {
    console.log('Выбранный файл:', file);

    const formData = new FormData();
    formData.append('avatar', file);

    const csrfToken = getCookie('csrftoken');

    const options = {
        method: 'PUT',
        body: formData,
        headers: {
          // 'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
      },
    };
    fetch(`accounts/update`, options)
    .catch(error => console.error('Error fetching chat list:', error));
  }
}
