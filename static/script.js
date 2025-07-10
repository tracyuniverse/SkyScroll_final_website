function uploadImage() {
    const input = document.getElementById('imageUpload');
    const file = input.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('image', file);

    // Show preview
    const reader = new FileReader();
    reader.onload = function (e) {
        const preview = document.getElementById('uploadedImagePreview');
        preview.innerHTML = `<img src="${e.target.result}" width="200" />`;
    };
    reader.readAsDataURL(file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        const seal = document.getElementById('sealImage');
        seal.className = ''; // Reset

        switch (data.gesture) {
            case 'swipe_right':
                seal.classList.add('animate__animated', 'animate__slideInRight');
                break;
            case 'swipe_down':
                seal.classList.add('animate__animated', 'animate__slideInDown');
                break;
            case 'zoom_in':
                seal.classList.add('animate__animated', 'animate__zoomIn');
                break;
            case 'zoom_out':
                seal.classList.add('animate__animated', 'animate__zoomOut');
                break;
            case 'swipe_up':
                seal.classList.add('animate__animated', 'animate__slideInUp');
                break;
            case 'swipe_up_down':
                seal.classList.add('animate__animated', 'animate__bounce');
                break;
        }
    })
    .catch(err => console.error(err));
}

