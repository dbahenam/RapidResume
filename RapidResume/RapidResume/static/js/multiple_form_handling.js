document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('form-container');

    container.addEventListener('click', function (event) {
        if (event.target.id === 'add-button') {
            const lastForm = container.querySelector('.django-formset-form:last-of-type');
            const clonedForm = lastForm.cloneNode(true);

            // Find the current form count
            const formCountInput = document.querySelector('#id_form-TOTAL_FORMS');
            let formCount = parseInt(formCountInput.value);

            // Clean cloned form from previous inputs
            clonedForm.querySelectorAll('input, select, textarea').forEach(input => {
                input.name = input.name.replace('-' + (formCount - 1) + '-', '-' + formCount + '-');
                input.id = input.id.replace('-' + (formCount - 1) + '-', '-' + formCount + '-');
                if (input.tagName === 'INPUT' || input.tagName === 'TEXTAREA') {
                    input.value = ''; // clear input values
                }
            });

            container.appendChild(clonedForm);

            const removeButton = clonedForm.querySelector('.remove-form-button');
            if (removeButton.classList.contains('inactive')) {
                removeButton.classList.remove('inactive');
            }

            // Increment form count in management form
            formCountInput.value = formCount + 1;

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