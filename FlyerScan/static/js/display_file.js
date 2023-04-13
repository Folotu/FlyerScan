      // Hide the spinner when the page has finished loading
      window.addEventListener('load', () => {
        const overlay = document.querySelector('#overlay');
        overlay.style.display = 'none';
        });