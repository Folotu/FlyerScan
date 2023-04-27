// const video = document.querySelector('.player');
// // const canvas = document.querySelector('.photo');
// // const ctx = canvas.getContext('2d');
// const strip = document.querySelector('.strip');
// const snap = document.querySelector('.snap');

// // Fix for iOS Safari from https://leemartin.dev/hello-webrtc-on-safari-11-e8bcb5335295
// video.setAttribute('autoplay', '');
// video.setAttribute('muted', '');
// video.setAttribute('playsinline', '')

// const constraints = {
//   audio: false,
//   video: {
//     facingMode: 'environment'
//   }
// }

// function getVideo() {
//   navigator.mediaDevices.getUserMedia(constraints)
//     .then(localMediaStream => {
//       console.log(localMediaStream);
    
// //  DEPRECIATION : 
// //       The following has been depreceated by major browsers as of Chrome and Firefox.
// //       video.src = window.URL.createObjectURL(localMediaStream);
// //       Please refer to these:
// //       Deprecated  - https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL
// //       Newer Syntax - https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/srcObject
//       console.dir(video);
//       if ('srcObject' in video) {
//         video.srcObject = localMediaStream;
//       } else {
//         video.src = URL.createObjectURL(localMediaStream);
//       }
//       // video.src = window.URL.createObjectURL(localMediaStream);
//       video.play();
//     })
//     .catch(err => {
//       console.error(`OH NO!!!!`, err);
//     });
// }



// const captureImageBtn = document.querySelector('#capture-image-btn');
// const cameraStream = document.querySelector('#camera-stream');
// const imageDataInput = document.querySelector('#image-data');

// captureImageBtn.addEventListener('click', () => {
//   // Create a canvas element to capture the image
//   const canvas = document.createElement('canvas');
//   canvas.width = cameraStream.videoWidth;
//   canvas.height = cameraStream.videoHeight;
//   const context = canvas.getContext('2d');
//   context.drawImage(cameraStream, 0, 0, canvas.width, canvas.height);
//   // Convert the image to a base64-encoded string
//   const imageData = canvas.toDataURL('image/jpeg');
//   // Store the image data in the input field
//   imageDataInput.value = imageData;
//   // Show the loading message or spinner
//   const overlay = document.querySelector('#overlay');
//   overlay.style.display = 'flex';
//   // Submit the form to process the image
//   const submitButton = document.querySelector('form button[type="submit"]');
//   submitButton.click();
// });

// function redEffect(pixels) {
//   for (let i = 0; i < pixels.data.length; i+=4) {
//     pixels.data[i + 0] = pixels.data[i + 0] + 200; // RED
//     pixels.data[i + 1] = pixels.data[i + 1] - 50; // GREEN
//     pixels.data[i + 2] = pixels.data[i + 2] * 0.5; // Blue
//   }
//   return pixels;
// }

// function rgbSplit(pixels) {
//   for (let i = 0; i < pixels.data.length; i+=4) {
//     pixels.data[i - 150] = pixels.data[i + 0]; // RED
//     pixels.data[i + 500] = pixels.data[i + 1]; // GREEN
//     pixels.data[i - 550] = pixels.data[i + 2]; // Blue
//   }
//   return pixels;
// }

// function greenScreen(pixels) {
//   const levels = {};

//   document.querySelectorAll('.rgb input').forEach((input) => {
//     levels[input.name] = input.value;
//   });

//   for (i = 0; i < pixels.data.length; i = i + 4) {
//     red = pixels.data[i + 0];
//     green = pixels.data[i + 1];
//     blue = pixels.data[i + 2];
//     alpha = pixels.data[i + 3];

//     if (red >= levels.rmin
//       && green >= levels.gmin
//       && blue >= levels.bmin
//       && red <= levels.rmax
//       && green <= levels.gmax
//       && blue <= levels.bmax) {
//       // take it out!
//       pixels.data[i + 3] = 0;
//     }
//   }

//   return pixels;
// }

// getVideo();

// video.addEventListener('canplay', paintToCanvas);