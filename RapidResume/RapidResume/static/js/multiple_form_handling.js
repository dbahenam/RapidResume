document.addEventListener('DOMContentLoaded', function () {

    const container = document.getElementById('form-container');

    container.addEventListener('click', function (event) {
        if (event.target.id === 'add-button') {
            const lastForm = container.querySelector('.django-formset-form:last-of-type'); // last-of-type is CSS Selector
            const clonedForm = lastForm.cloneNode(true); // clone form and all of its subtree elements

            // Find the current form count
            const formCountInput = document.querySelector('#id_form-TOTAL_FORMS');
            let prevFormCount = parseInt(formCountInput.value);
            if (prevFormCount !== 0) { prevFormCount--;}
            console.log(prevFormCount)

            // Update form count
            let updatedFormCount = prevFormCount + 1;

            // Clean cloned form from previous inputs
            clonedForm.querySelectorAll('input, select, textarea').forEach(input => {
                console.log(input)
                input.name = input.name.replace('-' + prevFormCount + '-', '-' + updatedFormCount + '-');
                input.id = input.id.replace('-' + prevFormCount + '-', '-' + updatedFormCount + '-');

                if (input.tagName === 'INPUT' || input.tagName === 'TEXTAREA') {
                    input.value = ''; // clear input values
                }
            });

            clonedForm.querySelectorAll('label').forEach(label => {
                label.htmlFor = label.htmlFor.replace('-' + prevFormCount + '-', '-' + updatedFormCount + '-');
            });

            // After cloning the form, remove the id input field from the cloned form
            const idInput = clonedForm.querySelector('input[name*="-id"]');
            if (idInput) {
                idInput.remove();
            }


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