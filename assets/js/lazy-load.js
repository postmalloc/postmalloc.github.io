document.addEventListener('DOMContentLoaded', function() {
    // Create IntersectionObserver to watch for elements entering viewport
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        // If the image is in the viewport
        if (entry.isIntersecting) {
          const img = entry.target;
          const src = img.getAttribute('data-src');
          
          // Load the image
          if (src) {
            // Create a new image element to preload the image
            const preloadImg = new Image();
            preloadImg.onload = function() {
              // Once the image is loaded, set the src and add the loaded class
              img.src = src;
              img.classList.add('loaded');
            };
            preloadImg.src = src;
            
            // Set data-src to null to prevent reloading
            img.removeAttribute('data-src');
          }
          
          // Stop observing the image after it's loaded
          observer.unobserve(img);
        }
      });
    }, {
      // Options for the observer
      rootMargin: '50px 0px', // Load images when they are within 50px of the viewport
      threshold: 0.01
    });
    
    // Observe all images with the photo-img class
    document.querySelectorAll('.photo-img').forEach(img => {
      imageObserver.observe(img);
    });
  });