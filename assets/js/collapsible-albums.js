document.addEventListener('DOMContentLoaded', function() {
    const collapsibleButtons = document.querySelectorAll('.collapse-button');
  
    collapsibleButtons.forEach(button => {
      button.addEventListener('click', function() {
        const expanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', !expanded);
        const content = document.getElementById(this.getAttribute('aria-controls'));
        content.classList.toggle('collapsed', expanded);
      });
    });
  });