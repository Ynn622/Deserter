// ===== Smooth Scrolling for Navigation Links =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        
        if (target) {
            const navbarHeight = document.querySelector('.navbar').offsetHeight;
            const targetPosition = target.offsetTop - navbarHeight - 20;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
            
            // Close mobile menu if open
            const navbarCollapse = document.querySelector('.navbar-collapse');
            if (navbarCollapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                    toggle: false
                });
                bsCollapse.hide();
            }
        }
    });
});

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

// ===== Category Card Click Handlers =====
const categoryCards = document.querySelectorAll('.category-card');

categoryCards.forEach(card => {
    const button = card.querySelector('.btn-card');
    
    button.addEventListener('click', function(e) {
        e.stopPropagation();
        const cardTitle = card.querySelector('.card-title').textContent;
        showCategoryModal(cardTitle);
    });
    
    // Add ripple effect on click
    card.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        ripple.style.position = 'absolute';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.style.width = '0';
        ripple.style.height = '0';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'rgba(255, 255, 255, 0.5)';
        ripple.style.transform = 'translate(-50%, -50%)';
        ripple.style.animation = 'ripple 0.6s ease-out';
        ripple.style.pointerEvents = 'none';
        
        card.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// Add ripple animation to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            width: 500px;
            height: 500px;
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ===== Modal Function for Category Details =====
function showCategoryModal(categoryName) {
    const messages = {
        '空軍': '空軍單位詳細資訊即將推出！',
        '陸軍': '陸軍單位詳細資訊即將推出！',
        '海軍': '海軍單位詳細資訊即將推出！',
        '閃兵傳奇': '閃兵傳奇故事即將推出！'
    };
    
    alert(`${categoryName}\n\n${messages[categoryName] || '更多資訊即將推出！'}`);
}

// ===== Intersection Observer for Animation on Scroll =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all category cards
categoryCards.forEach(card => {
    card.style.opacity = '0';
    observer.observe(card);
});

// ===== Dropdown Auto-Navigate =====
const dropdownItems = document.querySelectorAll('.dropdown-item');
dropdownItems.forEach(item => {
    item.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            e.preventDefault();
            const navbarHeight = document.querySelector('.navbar').offsetHeight;
            const targetPosition = targetElement.offsetTop - navbarHeight - 20;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ===== Easter Egg: Konami Code =====
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', function(e) {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        activateEasterEgg();
    }
});

function activateEasterEgg() {
    document.body.style.animation = 'rainbow 2s infinite';
    setTimeout(() => {
        document.body.style.animation = '';
        alert('🎉 恭喜你發現彩蛋！你是真正的逃兵大師！');
    }, 2000);
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

// ===== Performance: Lazy Loading Images =====
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                imageObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ===== Console Message =====
console.log('%c逃兵大陸', 'font-size: 30px; font-weight: bold; color: #667eea;');
console.log('%c歡迎來到逃兵大陸！請記得這只是娛樂性質的網站。', 'font-size: 14px; color: #666;');
console.log('%c提示：試試看輸入 Konami Code (↑↑↓↓←→←→BA)', 'font-size: 12px; color: #999; font-style: italic;');

// ===== Load Animation Complete =====
window.addEventListener('load', function() {
    document.body.style.opacity = '1';
    console.log('✅ 網站載入完成！');
});