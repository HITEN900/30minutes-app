// ============================================
// 30 MINUTES - MAIN JAVASCRIPT
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    loadServices();
    setupThemeToggle();
    setupForms();
    setupBookingForm();
    checkAuthStatus();
});

// ============================================
// LOAD SERVICES
// ============================================
function loadServices() {
    const services = [
        { name: 'Plumber', icon: 'bi-wrench', color: 'primary', count: 25, desc: 'Pipe repairs & installations' },
        { name: 'Electrician', icon: 'bi-lightning-fill', color: 'warning', count: 18, desc: 'Wiring & installations' },
        { name: 'Carpenter', icon: 'bi-hammer', color: 'success', count: 15, desc: 'Furniture & cabinets' },
        { name: 'Mechanic', icon: 'bi-gear', color: 'danger', count: 20, desc: 'Repairs & servicing' },
        { name: 'Painter', icon: 'bi-palette-fill', color: 'info', count: 12, desc: 'Interior & exterior' },
        { name: 'Cleaner', icon: 'bi-brush', color: 'secondary', count: 10, desc: 'Home & office cleaning' }
    ];

    const grid = document.getElementById('servicesGrid');
    if (grid) {
        grid.innerHTML = services.map(service => 
            <div class="col-lg-4 col-md-6">
                <div class="service-card">
                    <div class="service-icon" style="color: var(--);">
                        <i class="bi "></i>
                    </div>
                    <h5 class="fw-bold"></h5>
                    <p class="text-muted small mb-2"></p>
                    <span class="badge bg-light text-dark mb-2"> available</span>
                    <br>
                    <button class="btn btn-primary btn-sm rounded-pill px-3" onclick="showBookingModal('')">
                        Book Now
                    </button>
                </div>
            </div>
        ).join('');
    }
}

// ============================================
// BOOKING MODAL
// ============================================
function showBookingModal(service) {
    const modal = new bootstrap.Modal(document.getElementById('bookingModal'));
    modal.show();
    
    if (service) {
        const select = document.querySelector('#bookingForm select');
        if (select) {
            for (let option of select.options) {
                if (option.value.toLowerCase() === service.toLowerCase()) {
                    option.selected = true;
                    break;
                }
            }
        }
    }
}

// ============================================
// THEME TOGGLE
// ============================================
function setupThemeToggle() {
    const toggle = document.getElementById('themeToggle');
    if (toggle) {
        toggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const icon = this.querySelector('i');
            if (document.body.classList.contains('dark-mode')) {
                icon.className = 'bi bi-sun-fill';
                localStorage.setItem('darkMode', 'true');
            } else {
                icon.className = 'bi bi-moon-fill';
                localStorage.setItem('darkMode', 'false');
            }
        });
    }

    const saved = localStorage.getItem('darkMode');
    if (saved === 'true') {
        document.body.classList.add('dark-mode');
        const toggle = document.getElementById('themeToggle');
        if (toggle) {
            const icon = toggle.querySelector('i');
            if (icon) icon.className = 'bi bi-sun-fill';
        }
    }
}

// ============================================
AUTH STATUS
// ============================================
function checkAuthStatus() {
    const user = localStorage.getItem('user');
    if (user) {
        const userData = JSON.parse(user);
        updateNavForLoggedInUser(userData);
    }
}

function updateNavForLoggedInUser(userData) {
    const nav = document.querySelector('.navbar-nav');
    if (nav) {
        const loginBtn = nav.querySelector('[data-bs-toggle="modal"][data-bs-target="#loginModal"]');
        const registerBtn = nav.querySelector('.btn-primary');
        if (loginBtn) loginBtn.closest('.nav-item').style.display = 'none';
        if (registerBtn) registerBtn.closest('.nav-item').style.display = 'none';
        
        const profileItem = document.createElement('li');
        profileItem.className = 'nav-item dropdown';
        profileItem.innerHTML = 
            <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                <i class="bi bi-person-circle"></i> 
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
                <li><a class="dropdown-item" href="#"><i class="bi bi-person"></i> Profile</a></li>
                <li><a class="dropdown-item" href="#"><i class="bi bi-clock-history"></i> My Bookings</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item text-danger" href="#" onclick="logout()"><i class="bi bi-box-arrow-right"></i> Logout</a></li>
            </ul>
        ;
        nav.appendChild(profileItem);
    }
}

function logout() {
    localStorage.removeItem('user');
    location.reload();
}

// ============================================
// FORMS
// ============================================
function setupForms() {
    // Login form
    document.getElementById('loginForm')?.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('✅ Login successful! Welcome to 30 Minutes.');
    });

    // OTP form
    document.getElementById('otpForm')?.addEventListener('submit', function(e) {
        e.preventDefault();
        document.getElementById('otpVerifySection').style.display = 'block';
        alert('📱 OTP sent to your phone!');
    });

    // Verify OTP
    document.querySelector('#otpModal .btn-success')?.addEventListener('click', function() {
        alert('✅ OTP Verified! Login successful.');
        const userData = { firstName: 'Demo', lastName: 'User', phone: '9876543210' };
        localStorage.setItem('user', JSON.stringify(userData));
        location.reload();
    });
}

// ============================================
// BOOKING FORM
// ============================================
function setupBookingForm() {
    document.getElementById('bookingForm')?.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('✅ Service booked successfully! A technician will be with you within 30 minutes.');
        bootstrap.Modal.getInstance(document.getElementById('bookingModal'))?.hide();
    });
}

// ============================================
// SMOOTH SCROLL
// ============================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href && href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    });
});

console.log('🚀 30 Minutes App loaded successfully!');
