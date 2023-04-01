const startStreamBtn = document.querySelector('#start-stream-btn');
const captureImageBtn = document.querySelector('#capture-image-btn');
const cameraStream = document.querySelector('#camera-stream');
const imageDataInput = document.querySelector('#image-data');

let stream;

// startStreamBtn.addEventListener('click', () => {
    // Get access to the camera hardware
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(newStream => {
            // Save the stream to a variable
            stream = newStream;
            // Display the stream on the video element
            cameraStream.srcObject = stream;
            cameraStream.play();
            // Show the capture image button
            captureImageBtn.style.display = 'inline-block';
        })
        .catch(error => {
            console.error('Error accessing camera:', error);
        });
// });

captureImageBtn.addEventListener('click', () => {
    // Create a canvas element to capture the image
    const canvas = document.createElement('canvas');
    canvas.width = cameraStream.videoWidth;
    canvas.height = cameraStream.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(cameraStream, 0, 0, canvas.width, canvas.height);
    // Convert the image to a base64-encoded string
    const imageData = canvas.toDataURL('image/jpeg');
    // Store the image data in the input field
    imageDataInput.value = imageData;
    // Submit the form to process the image
    const submitButton = document.querySelector('form button[type="submit"]');
    submitButton.click();
});