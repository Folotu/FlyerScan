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
const links = document.querySelectorAll('.nav__link', '.nav__link2');

let lastActiveLink = null;

if (links.length) {
  links.forEach((link) => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      links.forEach((link) => {
        link.classList.remove('nav__link--active', 'nav__link2--active');
      });
      link.classList.add('nav__link--active', 'nav__link2--active');

      // Remove active class from last active link
      if (lastActiveLink) {
        lastActiveLink.classList.remove('nav__link--active', 'nav__link2--active');
      }
      lastActiveLink = link;

      // Redirect to the "/camera" URL if the link is the "Scan" link
      if (link.href.includes('/camera')) {
        window.location.href = '/camera';
      }
      else if (link.href.includes('/history')) {
        window.location.href = '/history';
      }
      else if (link.href.includes('/account')) {
        window.location.href = '/account';
      }
      else if (link.href.includes('/home')) {
        window.location.href = '/';
      }
    });
    // Set active class for current page
    const path = window.location.pathname;
    const linkPath = link.pathname;
    if (path.startsWith(linkPath) || (path == '/' && linkPath == '/home')) {
      link.classList.add('nav__link--active', 'nav__link2--active');
      lastActiveLink = link;
    }
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

