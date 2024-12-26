// Function to update the date and time in the header
function updateDateTime() {
    const dateElement = document.getElementById('date');
    const timeElement = document.getElementById('time');

    const now = new Date();
    const date = now.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    });
    const time = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
    });

    dateElement.textContent = date;
    timeElement.textContent = time;
}

// Update the date and time every second
setInterval(updateDateTime, 1000);
updateDateTime(); // Initial call

// Handle image upload and display preview
document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const previewImage = document.getElementById('previewImage');
    const fileFeedback = document.getElementById('fileFeedback');
    const resultDiv = document.getElementById('result');
    const file = fileInput.files[0];

    // Validate image file
    if (file && file.type.startsWith('image/')) {
        fileFeedback.style.display = 'none';

        const reader = new FileReader();
        reader.onload = function () {
            previewImage.src = reader.result;
            previewImage.style.display = 'block';
        };
        reader.readAsDataURL(file);

        // Show a placeholder classification result
        resultDiv.innerHTML = '<p>Classifying image...</p>';

        // Simulate classification result
        setTimeout(function () {
            const classifications = ['Good', 'Bad', 'Neutral'];
            const randomIndex = Math.floor(Math.random() * classifications.length);
            resultDiv.innerHTML = `<p>Classification: <strong>${classifications[randomIndex]}</strong></p>`;
        }, 2000);
    } else {
        fileFeedback.style.display = 'inline';
        previewImage.style.display = 'none';
        resultDiv.innerHTML = '';
    }
});
