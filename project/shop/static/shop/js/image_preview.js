const imagePreview = (staticUrl, imgSelector = '.preview-img', inputFieldName = 'image') => {
    const img = document.querySelector(imgSelector);
    const inputField = document.querySelector(`input[name=${inputFieldName}]`);

    if (inputField && img) {
        inputField.addEventListener("change", (evt) => {
            const file = evt.target.files[0];
            const reader = new FileReader();

            reader.addEventListener("load", (evt) => {
                img.src = evt.target.result;
            });

            if (file) {
                reader.readAsDataURL(file);
            } else {
                img.src = `${staticUrl}shop/images/image-not-found.png`;
            }
        });
    }
};
