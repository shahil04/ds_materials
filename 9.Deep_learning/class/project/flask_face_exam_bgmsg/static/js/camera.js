const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.srcObject = stream; });

setInterval(() => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    let image_data = canvas.toDataURL('image/jpeg');

    fetch('/monitor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: image_data })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            Swal.fire({
                icon: 'warning',
                text: data.message,
                timer: 2000,
                showConfirmButton: false
            });
        }
        if (data.status === 'submit') {
            document.getElementById('examForm').submit();
        }
    });
}, 3000);
