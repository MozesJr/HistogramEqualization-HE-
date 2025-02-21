function uploadImage() {
    let fileInput = document.getElementById('fileInput').files[0];
    let method = document.getElementById('method').value;
    let formData = new FormData();
    formData.append('file', fileInput);
    formData.append('method', method);

    fetch('/process', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('originalImg').src = data.original;
                document.getElementById('processedImg').src = data.processed;
                document.getElementById('histogramImg').src = data.histogram; // Tambahkan ini untuk histogram
            }
        })
        .catch(error => console.error('Error:', error));
}

function fetchImages() {
    fetch('/images')
        .then(response => response.json())
        .then(data => {
            let table = document.getElementById("imageTable");
            table.innerHTML = "";
            data.forEach(image => {
                let row = `<tr>
                <td><img src="${image.original_path}" style="max-width: 300px;"></td>
                <td><img src="${image.processed_path}" style="max-width: 300px;"></td>
                <td><img src="${image.histogram_path}" style="max-width: 300px;"></td>
                <td><button onclick="deleteImage('${image.filename}')">Delete</button></td>
            </tr>`;
                table.innerHTML += row;
            });
        })
        .catch(error => console.error('Error:', error));
}

function deleteImage(filename) {
    fetch('/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filename: filename
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            fetchImages(); // Refresh data
        })
        .catch(error => console.error('Error:', error));
}

// Panggil fetchImages() saat halaman dimuat
document.addEventListener("DOMContentLoaded", fetchImages);