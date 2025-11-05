// ===== Navbar Background Change on Scroll =====
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.backgroundColor = 'rgba(45, 55, 72, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
    } else {
        navbar.style.backgroundColor = 'var(--secondary-color)';
        navbar.style.backdropFilter = 'none';
    }
});

// ===== Deserter Cards Click Handler =====
const deserterCards = document.querySelectorAll('.deserter-card');
const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
const modalImage = document.getElementById('modalImage');
const modalPersonName = document.getElementById('modalPersonName');
const modalTitle = document.getElementById('imageModalLabel');

deserterCards.forEach(card => {
    card.addEventListener('click', function() {
        const img = this.querySelector('.deserter-image');
        const name = this.getAttribute('data-name');
        
        // Set modal content
        modalImage.src = img.src;
        modalImage.alt = name;
        modalPersonName.textContent = name;
        modalTitle.textContent = `${name} - 閃兵傳奇`;
        
        // Show modal
        imageModal.show();
    });

    // Add hover scale effect
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-0.5rem)';
        this.style.boxShadow = '0 1rem 2rem rgba(0, 0, 0, 0.2)';
    });

    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 0.25rem 1rem rgba(0, 0, 0, 0.1)';
    });
});

// ===== Image Loading Handler =====
const deserterImages = document.querySelectorAll('.deserter-image');

deserterImages.forEach(img => {
    const wrapper = img.closest('.deserter-image-wrapper');
    
    // Add loading state
    wrapper.classList.add('loading');
    
    // Remove loading state when image loads
    img.addEventListener('load', function() {
        wrapper.classList.remove('loading');
    });
    
    // Handle error
    img.addEventListener('error', function() {
        wrapper.classList.remove('loading');
        this.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"%3E%3Crect fill="%23ddd" width="400" height="400"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="monospace" font-size="24" fill="%23999"%3E無圖片%3C/text%3E%3C/svg%3E';
    });
});

// ===== Scroll to Top Button =====
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

window.addEventListener('scroll', function() {
    let scrollBtn = document.getElementById('scrollTopBtn');
    
    if (!scrollBtn) {
        scrollBtn = document.createElement('button');
        scrollBtn.id = 'scrollTopBtn';
        scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
        scrollBtn.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 3rem;
            height: 3rem;
            border-radius: 50%;
            background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
            color: white;
            border: none;
            cursor: pointer;
            box-shadow: 0 0.25rem 1rem rgba(0, 0, 0, 0.3);
            z-index: 1000;
            display: none;
            transition: all 0.3s ease;
        `;
        scrollBtn.addEventListener('click', scrollToTop);
        scrollBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
        });
        scrollBtn.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
        document.body.appendChild(scrollBtn);
    }
    
    if (window.scrollY > 300) {
        scrollBtn.style.display = 'block';
    } else {
        scrollBtn.style.display = 'none';
    }
});

// ===== Keyboard Navigation for Modal =====
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        imageModal.hide();
    }
});

// ===== Lazy Loading Images (Optional Enhancement) =====
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                // Image is already loaded, just observe for analytics
                imageObserver.unobserve(img);
            }
        });
    });

    deserterImages.forEach(img => {
        imageObserver.observe(img);
    });
}

// ===== Console Messages =====
console.log('%c閃兵傳奇', 'font-size: 24px; font-weight: bold; color: #2d3748;');
console.log('%c這些藝人都服過兵役！', 'font-size: 14px; color: #666;');

// ===== Easter Egg =====
let clickCount = 0;
const heroTitle = document.querySelector('.deserter-hero-title');

if (heroTitle) {
    heroTitle.addEventListener('click', function() {
        clickCount++;
        if (clickCount === 3) {
            this.style.animation = 'rainbow 2s infinite';
            setTimeout(() => {
                this.style.animation = '';
                alert('🎉 恭喜發現彩蛋！\n\n這些都是完成兵役的藝人，\n他們都是好榜樣！💪');
                clickCount = 0;
            }, 2000);
        }
    });
}

// Add rainbow animation
const rainbowStyle = document.createElement('style');
rainbowStyle.textContent = `
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
`;
document.head.appendChild(rainbowStyle);

// ===== Card Enter Animation (Optional) =====
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }, index * 50);
            observer.unobserve(entry.target);
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
});

// Uncomment below to enable enter animation
// deserterCards.forEach(card => {
//     card.style.opacity = '0';
//     card.style.transform = 'translateY(2rem)';
//     card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
//     observer.observe(card);
// });

// ===== Load Complete =====
window.addEventListener('load', function() {
    console.log('✅ 閃兵傳奇頁面載入完成！');
    console.log('💡 提示：點擊標題3次有驚喜！');
});
