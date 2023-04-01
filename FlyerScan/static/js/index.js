window.addEventListener('load', () => {
    registerServiceWorker();

});


async function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
      try {
        await navigator.serviceWorker.register('/static/sw01.js');
      } catch (e) {
        console.log(`SW registration failed`);
      }
    }
  }


  // Function to highlight current tab on navbar
  const links = document.querySelectorAll('.nav__link');
    
  if (links.length) {
    links.forEach((link) => {
      link.addEventListener('click', (e) => {
        links.forEach((link) => {
            link.classList.remove('nav__link--active');
        });
        e.preventDefault();
        link.classList.add('nav__link--active');
      });
    });
  }


// Register Service Worker
// if ('serviceWorker' in navigator) {
//     navigator.serviceWorker
//     .register('/static/sw01.js')
//     .then(function(registration) {
//         console.log('Service Worker Registered');
//         return registration;
//     })
//     .catch(function(err) {
//         console.error('Unable to register service worker.', err);
//     });
// }




// let deferredPrompt;
// const addBtn = document.querySelector('.add-button');
// addBtn.style.display = 'none';



// window.addEventListener('beforeinstallprompt', (e) => {
//   e.preventDefault();
//   deferredPrompt = e;
//   addBtn.style.display = 'block';
//   addBtn.addEventListener('click', (e) => {
//     addBtn.style.display = 'none';
//     deferredPrompt.prompt();
//     deferredPrompt.userChoice.then((choiceResult) => {
//         if (choiceResult.outcome === 'accepted') {


//           console.log('User accepted the A2HS prompt');


//         } else {

//           console.log('User dismissed the A2HS prompt');

//         }
//         deferredPrompt = null;
//       });
//   });
// });




// window.addEventListener('online', function(e) {
//     console.log("You are online");
// }, false);

