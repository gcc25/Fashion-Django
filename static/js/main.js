// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
  // Header scroll effect
  const header = document.querySelector('.site-header');
  const handleScroll = () => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };
  
  window.addEventListener('scroll', handleScroll);
  handleScroll(); // Initialize on page load
  
  // Mobile menu toggle
  const menuToggle = document.querySelector('.nav-toggle');
  const mainNav = document.querySelector('.main-nav');
  
  if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', function() {
      mainNav.classList.toggle('active');
      menuToggle.setAttribute('aria-expanded', 
        menuToggle.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'
      );
    });
  }
  
  // Product thumbnails
  const thumbnails = document.querySelectorAll('.product-thumbnail');
  const mainImage = document.querySelector('.product-main-image img');
  
  if (thumbnails.length && mainImage) {
    thumbnails.forEach(thumbnail => {
      thumbnail.addEventListener('click', function() {
        // Update main image
        mainImage.src = this.querySelector('img').getAttribute('data-full-img') || this.querySelector('img').src;
        
        // Update active state
        thumbnails.forEach(t => t.classList.remove('active'));
        this.classList.add('active');
      });
    });
  }
  
  // Product options
  const colorOptions = document.querySelectorAll('.color-option');
  const sizeOptions = document.querySelectorAll('.size-option');
  const colorInput = document.querySelector('input[name="color"]');
  const sizeInput = document.querySelector('input[name="size"]');
  
  if (colorOptions.length && colorInput) {
    colorOptions.forEach(option => {
      option.addEventListener('click', function() {
        if (this.classList.contains('out-of-stock')) return;
        
        colorOptions.forEach(o => o.classList.remove('active'));
        this.classList.add('active');
        colorInput.value = this.getAttribute('data-color');
      });
    });
  }
  
  if (sizeOptions.length && sizeInput) {
    sizeOptions.forEach(option => {
      option.addEventListener('click', function() {
        if (this.classList.contains('out-of-stock')) return;
        
        sizeOptions.forEach(o => o.classList.remove('active'));
        this.classList.add('active');
        sizeInput.value = this.getAttribute('data-size');
      });
    });
  }
  
  // Accordion
  const accordionHeaders = document.querySelectorAll('.accordion-header');
  
  if (accordionHeaders.length) {
    accordionHeaders.forEach(header => {
      header.addEventListener('click', function() {
        const content = this.nextElementSibling;
        
        this.classList.toggle('active');
        content.classList.toggle('active');
      });
    });
  }
  
  // Quantity buttons
  const quantityInputs = document.querySelectorAll('.quantity-input');
  
  if (quantityInputs.length) {
    quantityInputs.forEach(input => {
      const decrementBtn = input.previousElementSibling;
      const incrementBtn = input.nextElementSibling;
      
      if (decrementBtn && decrementBtn.classList.contains('quantity-btn-decrement')) {
        decrementBtn.addEventListener('click', function() {
          const currentValue = parseInt(input.value, 10);
          if (currentValue > 1) {
            input.value = currentValue - 1;
          }
        });
      }
      
      if (incrementBtn && incrementBtn.classList.contains('quantity-btn-increment')) {
        incrementBtn.addEventListener('click', function() {
          const currentValue = parseInt(input.value, 10);
          input.value = currentValue + 1;
        });
      }
    });
  }
  
  // Wishlist button
  const wishlistButtons = document.querySelectorAll('.wishlist-btn, .wishlist-btn-detail');
  
  if (wishlistButtons.length) {
    wishlistButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        const productId = this.getAttribute('data-product-id');
        const isAuthenticated = this.getAttribute('data-authenticated') === 'true';
        
        if (!isAuthenticated) {
          window.location.href = '/accounts/login/?next=' + window.location.pathname;
          return;
        }
        
        // Add your AJAX logic to add/remove from wishlist
        fetch(`/users/wishlist/add/${productId}/`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
          }
        })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            // Update UI based on response
            const icon = this.querySelector('i');
            if (icon) {
              icon.classList.toggle('far');
              icon.classList.toggle('fas');
            }
          }
        });
        
        e.preventDefault();
      });
    });
  }
  
  // Messages auto-dismiss
  const messages = document.querySelectorAll('.message');
  
  if (messages.length) {
    messages.forEach(message => {
      setTimeout(() => {
        message.style.opacity = '0';
        setTimeout(() => {
          message.style.display = 'none';
        }, 300);
      }, 5000);
    });
  }
  
  // Initialize animations for elements
  const animateElements = document.querySelectorAll('.animate-fade-in');
  
  if (animateElements.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    
    animateElements.forEach(element => {
      element.style.opacity = '0';
      element.style.transform = 'translateY(20px)';
      element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      observer.observe(element);
    });
  }
});