// Global state
let allProperties = [];
let filteredProperties = [];
let currentSuburb = '';
let currentFilter = 'all';

// DOM Elements
const suburbInput = document.getElementById('suburbInput');
const propertyTypeSelect = document.getElementById('propertyTypeSelect');
const searchBtn = document.getElementById('searchBtn');
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');
const dashboardSection = document.getElementById('dashboardSection');
const propertiesGrid = document.getElementById('propertiesGrid');
const noResults = document.getElementById('noResults');
const retryBtn = document.getElementById('retryBtn');
const sortSelect = document.getElementById('sortSelect');
const filterBtns = document.querySelectorAll('.filter-btn');
const quickSearchBtns = document.querySelectorAll('.chip');
const propertyModal = document.getElementById('propertyModal');
const modalBody = document.getElementById('modalBody');
const modalClose = document.querySelector('.modal-close');
const modalOverlay = document.querySelector('.modal-overlay');

// Event Listeners
searchBtn.addEventListener('click', handleSearch);
retryBtn.addEventListener('click', handleSearch);
sortSelect.addEventListener('change', handleSort);
suburbInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSearch();
});

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter;
        applyFilters();
    });
});

quickSearchBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        suburbInput.value = btn.dataset.suburb;
        handleSearch();
    });
});

modalClose.addEventListener('click', closeModal);
modalOverlay.addEventListener('click', closeModal);

// Main search function
async function handleSearch() {
    const suburb = suburbInput.value.trim();
    const propertyType = propertyTypeSelect.value;

    if (!suburb) {
        showError('Please enter a suburb name');
        return;
    }

    currentSuburb = suburb;
    showLoading();

    try {
        const params = new URLSearchParams({ suburb });
        if (propertyType) {
            params.append('property_type', propertyType);
        }

        const response = await fetch(`/api/properties?${params}`);
        const result = await response.json();

        if (!response.ok) {
            // Handle unauthorized error with helpful message
            if (response.status === 401 && result.hint) {
                throw new Error(result.message + '|' + result.hint);
            }
            throw new Error(result.message || result.error || 'Failed to fetch properties');
        }

        if (result.success) {
            allProperties = result.data || [];
            filteredProperties = [...allProperties];
            
            if (allProperties.length === 0) {
                showNoResults();
            } else {
                displayDashboard(result);
            }
        } else {
            throw new Error(result.message || 'Failed to load properties');
        }
    } catch (error) {
        console.error('Error fetching properties:', error);
        
        // Parse error message for hint
        const errorParts = error.message.split('|');
        const message = errorParts[0];
        const hint = errorParts[1] || '';
        
        showError(message, hint);
    }
}

// Display functions
function showLoading() {
    hideAllStates();
    loadingState.classList.remove('hidden');
}

function showError(message, hint = '') {
    hideAllStates();
    
    // Create error message with hint if available
    let errorHTML = `<p>${message}</p>`;
    
    if (hint) {
        errorHTML += `
            <div class="error-hint">
                <i class="fas fa-lightbulb"></i>
                <strong>Suggestion:</strong> ${hint}
            </div>
        `;
    }
    
    errorMessage.innerHTML = errorHTML;
    errorState.classList.remove('hidden');
}

function showNoResults() {
    hideAllStates();
    dashboardSection.classList.remove('hidden');
    propertiesGrid.innerHTML = '';
    noResults.classList.remove('hidden');
    
    // Update stats to show zero
    updateStatistics({ total: 0, average_price: 0, average_bedrooms: 0, min_price: 0, max_price: 0 });
}

function hideAllStates() {
    loadingState.classList.add('hidden');
    errorState.classList.add('hidden');
    dashboardSection.classList.add('hidden');
    noResults.classList.add('hidden');
}

function displayDashboard(result) {
    hideAllStates();
    dashboardSection.classList.remove('hidden');
    
    // Update suburb name
    document.getElementById('suburbName').textContent = currentSuburb;
    
    // Update statistics
    updateStatistics(result.statistics);
    
    // Display properties
    displayProperties(filteredProperties);
}

function updateStatistics(stats) {
    document.getElementById('totalProperties').textContent = stats.total.toLocaleString();
    document.getElementById('avgPrice').textContent = stats.average_price > 0 
        ? `$${stats.average_price.toLocaleString()}` 
        : 'N/A';
    document.getElementById('avgBedrooms').textContent = stats.average_bedrooms > 0 
        ? stats.average_bedrooms.toFixed(1) 
        : 'N/A';
    
    if (stats.min_price > 0 && stats.max_price > 0) {
        document.getElementById('priceRange').textContent = 
            `$${formatPrice(stats.min_price)} - $${formatPrice(stats.max_price)}`;
    } else {
        document.getElementById('priceRange').textContent = 'N/A';
    }
}

function displayProperties(properties) {
    propertiesGrid.innerHTML = '';
    
    if (properties.length === 0) {
        noResults.classList.remove('hidden');
        return;
    }
    
    noResults.classList.add('hidden');
    
    properties.forEach((property, index) => {
        const card = createPropertyCard(property, index);
        propertiesGrid.appendChild(card);
    });
}

function createPropertyCard(property, index) {
    const card = document.createElement('div');
    card.className = 'property-card';
    card.style.animationDelay = `${index * 0.05}s`;
    
    // Extract property data
    const address = getPropertyField(property, ['address', 'street_address', 'location']) || 'Address not available';
    const price = getPropertyField(property, ['price', 'listing_price', 'sale_price', 'asking_price']);
    const bedrooms = getPropertyField(property, ['bedrooms', 'beds', 'bedroom_count']);
    const bathrooms = getPropertyField(property, ['bathrooms', 'baths', 'bathroom_count']);
    const parking = getPropertyField(property, ['parking', 'car_spaces', 'garage']);
    const propertyType = getPropertyField(property, ['property_type', 'type', 'category']) || 'Property';
    const landSize = getPropertyField(property, ['land_size', 'lot_size', 'land_area']);
    
    // Format price
    const priceDisplay = price ? `$${formatPrice(price)}` : 'Price on application';
    
    card.innerHTML = `
        <div class="property-image">
            <div class="property-image-placeholder">
                <i class="fas fa-home"></i>
            </div>
            <div class="property-badge">${capitalizeFirst(propertyType)}</div>
        </div>
        <div class="property-details">
            <div class="property-price">${priceDisplay}</div>
            <div class="property-address">${address}</div>
            
            <div class="property-features">
                ${bedrooms ? `
                    <div class="feature">
                        <i class="fas fa-bed"></i>
                        <span>${bedrooms}</span>
                    </div>
                ` : ''}
                ${bathrooms ? `
                    <div class="feature">
                        <i class="fas fa-bath"></i>
                        <span>${bathrooms}</span>
                    </div>
                ` : ''}
                ${parking ? `
                    <div class="feature">
                        <i class="fas fa-car"></i>
                        <span>${parking}</span>
                    </div>
                ` : ''}
                ${landSize ? `
                    <div class="feature">
                        <i class="fas fa-ruler-combined"></i>
                        <span>${landSize} m²</span>
                    </div>
                ` : ''}
            </div>
            
            <button class="btn-view-details" onclick="viewPropertyDetails(${index})">
                View Details <i class="fas fa-arrow-right"></i>
            </button>
        </div>
    `;
    
    return card;
}

function viewPropertyDetails(index) {
    const property = filteredProperties[index];
    
    modalBody.innerHTML = `
        <div class="modal-header">
            <h2>${getPropertyField(property, ['address', 'street_address']) || 'Property Details'}</h2>
            <div class="property-type-badge">${capitalizeFirst(getPropertyField(property, ['property_type', 'type']) || 'Property')}</div>
        </div>
        
        <div class="modal-price">
            ${getPropertyField(property, ['price', 'listing_price']) 
                ? `$${formatPrice(getPropertyField(property, ['price', 'listing_price']))}` 
                : 'Price on application'}
        </div>
        
        <div class="modal-features-grid">
            ${getPropertyField(property, ['bedrooms', 'beds']) ? `
                <div class="modal-feature">
                    <i class="fas fa-bed"></i>
                    <div>
                        <strong>${getPropertyField(property, ['bedrooms', 'beds'])}</strong>
                        <span>Bedrooms</span>
                    </div>
                </div>
            ` : ''}
            
            ${getPropertyField(property, ['bathrooms', 'baths']) ? `
                <div class="modal-feature">
                    <i class="fas fa-bath"></i>
                    <div>
                        <strong>${getPropertyField(property, ['bathrooms', 'baths'])}</strong>
                        <span>Bathrooms</span>
                    </div>
                </div>
            ` : ''}
            
            ${getPropertyField(property, ['parking', 'car_spaces']) ? `
                <div class="modal-feature">
                    <i class="fas fa-car"></i>
                    <div>
                        <strong>${getPropertyField(property, ['parking', 'car_spaces'])}</strong>
                        <span>Parking</span>
                    </div>
                </div>
            ` : ''}
            
            ${getPropertyField(property, ['land_size', 'lot_size']) ? `
                <div class="modal-feature">
                    <i class="fas fa-ruler-combined"></i>
                    <div>
                        <strong>${getPropertyField(property, ['land_size', 'lot_size'])}</strong>
                        <span>Land Size (m²)</span>
                    </div>
                </div>
            ` : ''}
        </div>
        
        <div class="modal-section">
            <h3>All Property Information</h3>
            <div class="property-data">
                <pre>${JSON.stringify(property, null, 2)}</pre>
            </div>
        </div>
    `;
    
    propertyModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    propertyModal.classList.add('hidden');
    document.body.style.overflow = '';
}

// Filter and sort functions
function applyFilters() {
    if (currentFilter === 'all') {
        filteredProperties = [...allProperties];
    } else {
        filteredProperties = allProperties.filter(property => {
            const type = getPropertyField(property, ['property_type', 'type', 'category']);
            return type && type.toLowerCase().includes(currentFilter.toLowerCase());
        });
    }
    
    handleSort();
}

function handleSort() {
    const sortValue = sortSelect.value;
    
    switch (sortValue) {
        case 'price-asc':
            filteredProperties.sort((a, b) => {
                const priceA = getPropertyField(a, ['price', 'listing_price']) || 0;
                const priceB = getPropertyField(b, ['price', 'listing_price']) || 0;
                return priceA - priceB;
            });
            break;
        case 'price-desc':
            filteredProperties.sort((a, b) => {
                const priceA = getPropertyField(a, ['price', 'listing_price']) || 0;
                const priceB = getPropertyField(b, ['price', 'listing_price']) || 0;
                return priceB - priceA;
            });
            break;
        case 'bedrooms-asc':
            filteredProperties.sort((a, b) => {
                const bedsA = getPropertyField(a, ['bedrooms', 'beds']) || 0;
                const bedsB = getPropertyField(b, ['bedrooms', 'beds']) || 0;
                return bedsA - bedsB;
            });
            break;
        case 'bedrooms-desc':
            filteredProperties.sort((a, b) => {
                const bedsA = getPropertyField(a, ['bedrooms', 'beds']) || 0;
                const bedsB = getPropertyField(b, ['bedrooms', 'beds']) || 0;
                return bedsB - bedsA;
            });
            break;
    }
    
    displayProperties(filteredProperties);
}

// Utility functions
function getPropertyField(property, fields) {
    for (const field of fields) {
        if (property[field] !== undefined && property[field] !== null && property[field] !== '') {
            return property[field];
        }
    }
    return null;
}

function formatPrice(price) {
    if (typeof price === 'string') {
        price = parseInt(price.replace(/[^0-9]/g, ''));
    }
    
    if (price >= 1000000) {
        return (price / 1000000).toFixed(2) + 'M';
    } else if (price >= 1000) {
        return (price / 1000).toFixed(0) + 'K';
    }
    return price.toLocaleString();
}

function capitalizeFirst(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

// Initialize with default search on page load (optional)
window.addEventListener('DOMContentLoaded', () => {
    // Optionally auto-load Belmont North on page load
    // suburbInput.value = 'Belmont North';
    // handleSearch();
});
