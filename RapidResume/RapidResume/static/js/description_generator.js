// Global variable to hold the current form index
let currentFormIndex;

document.addEventListener('DOMContentLoaded', function () {

    document.getElementById('form-container').addEventListener('click', function(event) {
        let button = event.target.closest('[data-form-index]');
        if (button) {
            setCurrentFormIndex(button);
        }
    });

    // Event listener for the "Generate" button inside the modal
    document.getElementById('generateDescription').addEventListener('click', function (event) {
        // With bootstrap settings, once this button is clicked the modal asking for user input will display
        makeDescriptionRequest(event);
    });
});

function setCurrentFormIndex(button) {
    currentFormIndex = button.getAttribute('data-form-index');
    console.log(currentFormIndex);
}

function makeDescriptionRequest(event) {
    console.log('Generate Description button clicked!'); // Debugging line

    var descriptionField = document.querySelector(`[name="form-${currentFormIndex}-description"]`);
    if (!descriptionField) {
        console.error(`Description field with index ${currentFormIndex} not found.`);
        console.log(`Current form index: ${currentFormIndex}`);
        return;
    }

    // Get the values from the modal's input fields
    var firstInput = document.getElementById('firstInput').value;
    var secondInput = document.getElementById('secondInput').value;
    console.log(firstInput, secondInput)

    var csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    fetch('/generate_description_endpoint/' + dataEndpointSlug, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            'first_input': firstInput,
            'second_input': secondInput,
        })
    })
    .then(response => response.json())
    .then(data => {
        descriptionField.innerHTML = '';
        const descriptions = data.description;

        createAndShowModal(descriptions);

    })
    .catch(error => {
        console.error('Error:', error);
    });
}

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
                            ${descriptions.map((description, index) => `
                                <li class="list-group-item d-flex justify-content-between align-items-center my-2">
                                    ${description}
                                    <div class="d-flex">
                                        <button class="btn btn-outline-primary btn-sm mx-2 add-btn" data-index="${index}">Add</button>
                                        <button class="btn btn-outline-danger btn-sm erase-btn" data-index="${index}">Erase</button>
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

    // Append the modal to the body
    document.body.insertAdjacentHTML('beforeend', modalHtml);

    // Display newly formed modal
    let descriptionListModal = new bootstrap.Modal(document.getElementById('descriptionListModal'));
    descriptionListModal.show();

    // List of descriptions
    let descriptionsMap = new Map();

    // For the add, erase buttons in the description list modal
    document.querySelectorAll('.add-btn').forEach((btn, index) => {
        btn.addEventListener('click', function() {
            const descriptionField = document.querySelector(`[name="form-${currentFormIndex}-description"]`);
            
            const bullet = "• ";

            descriptionsMap.set(index, bullet + descriptions[index] + '\n');

            descriptionField.value = [...descriptionsMap.values()].join('');

            btn.disabled = true;
        });
    });

    document.querySelectorAll('.erase-btn').forEach((btn, index) => {
        btn.addEventListener('click', function () {
            if (descriptionsMap.has(index)) {
                descriptionsMap.delete(index);

                const descriptionField = document.querySelector(`[name="form-${currentFormIndex}-description"]`);
                descriptionField.value = [...descriptionsMap.values()].join('');
                
                document.querySelector(`.add-btn[data-index="${index}"]`).disabled = false;
            }   
        });
    });

    document.getElementById('doneButton').addEventListener('click', function () {
        const modalListElement = document.getElementById('descriptionListModal');
        modalListElement.remove();
    });
    
    // Close the modal
    var descriptionModal = document.getElementById('descriptionGeneratorModal');
    descriptionModal.querySelector('.close').click();
}