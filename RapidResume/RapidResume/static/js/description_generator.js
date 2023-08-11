document.getElementById('generateDescription').addEventListener('click', function() {
    // Get the values from the modal's input fields
    var firstInput = document.getElementById('firstInput').value;
    var secondInput = document.getElementById('secondInput').value;
    var descriptionField = document.querySelector('[name="description"]');
    var csrfToken = document.getElementById('descriptionButton').getAttribute('data-csrf');
    
    // TODO: Send an AJAX request to your backend with these values, get the generated description, and populate your form's description field.
    fetch('/generate_description_endpoint/' + dataEndpointSlug, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            'first_input' : firstInput,
            'second_input' : secondInput,
        })
    })
    .then(response => response.json())
    .then(data => {
        descriptionField.value = data.description; // Assuming the response has a "description" key.
    })
    .catch(error => {
        console.error('Error:', error);
    });

    // Close the modal
    var descriptionModal = document.getElementById('descriptionGeneratorModal');
    descriptionModal.querySelector('.close').click();
});