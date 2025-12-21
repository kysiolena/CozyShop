/**
 * Display value of '[class$="fieldName"] input[type="file"]' by 'img' tag placed into '.field-preview' container.
 * Two tags connected by 'data-name' attribute of container tag.
 */
const displayImagePreview = () => {
    const fieldPreviewContainers = document.querySelectorAll(".field-preview")

    fieldPreviewContainers.forEach((fieldPreviewContainer) => {
        const img = fieldPreviewContainer.querySelector("img")
        const fieldName = fieldPreviewContainer.dataset.name

        if (img && fieldName) {
            const parentModule = fieldPreviewContainer.closest('.module')
            const inputField = parentModule.querySelector(`.field-${fieldName} input[type='file']`)

            if (inputField) {
                inputField.addEventListener("change", (evt) => {
                    const file = evt.target.files[0];
                    const reader = new FileReader();

                    reader.addEventListener("load", (evt) => {
                        img.src = evt.target.result;
                        img.style.display = "block";
                    });

                    if (file) {
                        reader.readAsDataURL(file);
                    } else {
                        img.style.display = "none";
                    }
                })
            }
        }

    })
}

document.addEventListener("DOMContentLoaded", () => {
    displayImagePreview()
})

