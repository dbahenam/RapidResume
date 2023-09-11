document.addEventListener('DOMContentLoaded', function () {

    const container = document.getElementById('form-container');

    container.addEventListener('click', function (event) {
        if (event.target.id === 'add-button') {
            const lastForm = container.querySelector('.django-formset-form:last-of-type'); // last-of-type is CSS Selector
            const clonedForm = lastForm.cloneNode(true); // clone form and all of its subtree elements

            // Find the current form count
            const formCountInput = document.querySelector('#id_form-TOTAL_FORMS');
            let prevFormCount = parseInt(formCountInput.value);

            // Update form count
            let updatedFormCount = prevFormCount + 1;

            // Clean cloned form from previous inputs
            clonedForm.querySelectorAll('input, select, textarea').forEach(input => {
                input.name = input.name.replace('-' + prevFormCount + '-', '-' + updatedFormCount + '-');
                input.id = input.id.replace('-' + prevFormCount + '-', '-' + updatedFormCount + '-');

                if (input.tagName === 'INPUT' || input.tagName === 'TEXTAREA') {
                    input.value = ''; // clear input values
                }
            });

            const generateDescriptionButton = clonedForm.querySelector('[data-form-index]');
            if (generateDescriptionButton) {
                generateDescriptionButton.setAttribute('data-form-index', updatedFormCount);
            }
            
            container.appendChild(clonedForm);

            const removeButton = clonedForm.querySelector('.remove-form-button');
            if (removeButton.classList.contains('inactive')) {
                removeButton.classList.remove('inactive');
            }

            // Increment form count in management form
            formCountInput.value = updatedFormCount;

        } else if (event.target.classList.contains('remove-form-button')) {
            const parentForm = event.target.closest('.django-formset-form');
            if (parentForm) {
                parentForm.remove();

                const formCountInput = document.querySelector('#id_form-TOTAL_FORMS');
                let formCount = parseInt(formCountInput.value);
                formCountInput.value = formCount - 1;
            }
        }
    });
});