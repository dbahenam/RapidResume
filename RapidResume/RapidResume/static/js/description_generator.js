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
            console.log(data.description)
            descriptionField.innerHTML = '';
            const descriptions = data.description;

            createAndShowModal(descriptions);
            
    })
    .catch(error => {
        console.error('Error:', error);
    });

    function createAndShowModal(descriptions) {
        const modalHtml = `
            <div class="modal fade" id="descriptionListModal" tabindex="-1" role="dialog" aria-labelledby="descriptionGeneratorModalLabel" aria-hidden="true">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="descriptionListLabel">Descriptions</h5>
                        </div>
                        <div class="modal-body">
                            <ul class="list-group">
                                ${descriptions.map(description => `
                                    <li class="list-group-item d-flex justify-content-between align-items-center my-2">
                                        ${description}
                                        <div class="d-flex">
                                            <button class="btn btn-outline-primary btn-sm mx-2 add-btn">Add</button>
                                            <button class="btn btn-outline-danger btn-sm erase-btn">Erase</button>
                                        </div>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                        <div class="modal-footer">
                            <button id="doneButton" type="button" class="btn btn-outline-primary" data-bs-dismiss="modal">Done</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Append the modal to the body or a specific container
        document.body.insertAdjacentHTML('beforeend', modalHtml);

        let descriptionListModal = new bootstrap.Modal(document.getElementById('descriptionListModal'));
        descriptionListModal.show();

        // Add event listeners
        document.querySelectorAll('.add-btn').forEach((btn, index) => {
            btn.addEventListener('click', function() {
                const descriptionField = document.querySelector('[name="description"]');
                const bullet = "• ";
                descriptionField.value += "\n" + bullet + descriptions[index] + "\n\n";
                // You can disable the button or hide the list item after adding
                btn.disabled = true;
            });
        });

        document.querySelectorAll('.erase-btn').forEach((btn, index) => {
            btn.addEventListener('click', function() {
                // Implement the logic to remove a specific description from the descriptionField
                // You can enable the corresponding "Add" button or show the list item again
            });
        });

        document.getElementById('doneButton').addEventListener('click', function () {
            const modalListElement = document.getElementById('descriptionListModal');
            modalListElement.remove();
        })

        // // Close modal event
        // document.querySelector('.modal-close-btn').addEventListener('click', function() {
        //     const modal = document.getElementById('descriptionModal');
        //     modal.parentElement.removeChild(modal);
        // });

        
    }

    // Close the modal
    var descriptionModal = document.getElementById('descriptionGeneratorModal');
    descriptionModal.querySelector('.close').click();
});