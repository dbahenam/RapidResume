let saveTitleButton = document.getElementById('resumeTitleButton');
let userInput = document.getElementById('resumeTitle');
let resumeTitleModal = document.getElementById('resumeTitleModal');
let csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

function saveAndCloseModal() {
    let resumeTitle = userInput.value;
    let modal = new bootstrap.Modal(resumeTitleModal);
    modal.hide();
    sendTitleToBackend(resumeTitle);
}

function sendTitleToBackend(title) {
    fetch('/new-resume', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ resumeTitle: title }),
      })
      .then(response => response.json())
      .then(data => {
          console.log('Success:', data.redirect_url);
          window.location.href = data.redirect_url
      })
      .catch((error) => {
        console.error('Error:', error);
      });
}

saveTitleButton.addEventListener('click', saveAndCloseModal);