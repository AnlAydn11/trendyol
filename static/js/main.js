// Initialize all interactive elements when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeProductImages();
    initializeFilters();
    initializeSortingOptions();
    initializeSearchSuggestions();
    initializeCart();
});

// Product Image Gallery
function initializeProductImages() {
    const mainImage = document.querySelector('.main-image img');
    const thumbnails = document.querySelectorAll('.thumbnail-grid img');
    
    if (!mainImage || !thumbnails.length) return;
    
    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function() {
            // Update main image
            mainImage.src = this.src;
            // Update active state
            thumbnails.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// Filter Handling
function initializeFilters() {
    const filterInputs = document.querySelectorAll('.filter-option input');
    
    filterInputs.forEach(input => {
        input.addEventListener('change', function() {
            updateProductList();
        });
    });
}

function updateProductList() {
    const selectedFilters = getSelectedFilters();
    // Here you would typically make an AJAX call to your backend
    // For now, we'll just console.log the selected filters
    console.log('Selected filters:', selectedFilters);
}

function getSelectedFilters() {
    const filters = {};
    document.querySelectorAll('.filter-option input:checked').forEach(input => {
        const filterType = input.name;
        if (!filters[filterType]) {
            filters[filterType] = [];
        }
        filters[filterType].push(input.value);
    });
    return filters;
}

// Sorting Options
function initializeSortingOptions() {
    const sortSelect = document.querySelector('#sort-select');
    if (!sortSelect) return;
    
    sortSelect.addEventListener('change', function() {
        const selectedSort = this.value;
        // Here you would typically make an AJAX call to your backend
        console.log('Sort option selected:', selectedSort);
    });
}

// Search Suggestions
function initializeSearchSuggestions() {
    const searchInput = document.querySelector('.search-wrapper input');
    if (!searchInput) return;
    
    let debounceTimer;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            const query = this.value;
            if (query.length >= 3) {
                fetchSearchSuggestions(query);
            }
        }, 300);
    });
}

function fetchSearchSuggestions(query) {
    // Here you would typically make an AJAX call to your backend
    console.log('Fetching suggestions for:', query);
}

// Shopping Cart
function initializeCart() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            addToCart(productId);
        });
    });
}

function addToCart(productId) {
    // Here you would typically make an AJAX call to your backend
    console.log('Adding to cart:', productId);
    
    // Show success message
    showNotification('Product added to cart successfully!');
}

// Utility Functions
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Lazy loading for images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}


// Initialize all interactive elements when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeProductImages();
    initializeSearchFilters();
    initializeSortingOptions();
    initializeSearchSuggestions();
    initializeCart();
});

// Product Image Gallery
function initializeProductImages() {
    const mainImage = document.querySelector('.main-image img');
    const thumbnails = document.querySelectorAll('.thumbnail-grid img');
    
    if (!mainImage || !thumbnails.length) return;
    
    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function() {
            mainImage.src = this.src;
            thumbnails.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// Search Page Specific Filter Handling
function initializeSearchFilters() {
    // Only initialize if we're on the search page
    if (!document.querySelector('.search-results-page')) return;

    const filterInputs = document.querySelectorAll('.filter-option input');
    const brandSearch = document.querySelector('#brandSearch');
    
    if (brandSearch) {
        brandSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const brandOptions = document.querySelectorAll('#brandOptions .filter-option');
            
            brandOptions.forEach(option => {
                const brandName = option.querySelector('span').textContent.toLowerCase();
                option.style.display = brandName.includes(searchTerm) ? '' : 'none';
            });
        });
    }
    
    filterInputs.forEach(input => {
        input.addEventListener('change', function() {
            updateProductList();
        });
    });
}

// Remove any existing dropdowns from main navigation
function removeMainNavDropdowns() {
    const mainNavLinks = document.querySelectorAll('.nav-link');
    mainNavLinks.forEach(link => {
        const existingDropdown = link.nextElementSibling;
        if (existingDropdown && existingDropdown.classList.contains('nav-dropdown')) {
            existingDropdown.remove();
        }
    });
}
