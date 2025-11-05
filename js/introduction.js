// ===== Tab Switching Animation =====
document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.intro-nav-tabs .nav-link');
    
    tabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function (e) {
            const targetPane = document.querySelector(e.target.getAttribute('data-bs-target'));
            
            // Add fade-in animation to the content
            if (targetPane) {
                targetPane.style.animation = 'none';
                setTimeout(() => {
                    targetPane.style.animation = 'fadeIn 0.5s ease-in';
                }, 10);
            }
        });
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

// ===== Aspect Cards Click Handlers =====
const aspectCards = document.querySelectorAll('.aspect-card');

aspectCards.forEach(card => {
    const button = card.querySelector('.btn-aspect');
    
    button.addEventListener('click', function(e) {
        e.stopPropagation();
        const cardTitle = card.querySelector('.aspect-card-title').textContent;
        showAspectModal(cardTitle);
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
        ripple.style.zIndex = '10';
        
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

// ===== Modal Function for Aspect Details =====
function showAspectModal(aspectName) {
    const messages = {
        '國軍歷史': '國軍歷史詳細資訊即將推出！\n將包含從北伐到現代化的完整歷程。',
        '兵力調整規劃': '兵力調整規劃詳細資訊即將推出！\n將介紹精實案、精進案等重要改革。',
        '薪資行情': '薪資行情詳細資訊即將推出！\n將提供志願役與義務役的完整薪資資訊。'
    };
    
    alert(`${aspectName}\n\n${messages[aspectName] || '更多資訊即將推出！'}`);
}

// ===== Intersection Observer for Cards Animation =====
const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.style.opacity = '1';
                entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
            }, index * 150); // Stagger animation
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all aspect cards
aspectCards.forEach(card => {
    card.style.opacity = '0';
    observer.observe(card);
});

// ===== Smooth Scroll to Top =====
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add scroll to top button dynamically
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            cursor: pointer;
            box-shadow: 0 0.25rem 1rem rgba(0, 0, 0, 0.2);
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

// ===== Tab Content Counter Animation =====
function animateTabSwitch() {
    const tabPanes = document.querySelectorAll('.tab-pane');
    tabPanes.forEach(pane => {
        pane.addEventListener('shown.bs.tab', function() {
            console.log('Tab switched:', this.id);
        });
    });
}

animateTabSwitch();

// ===== Console Message =====
console.log('%c國軍簡介頁面', 'font-size: 24px; font-weight: bold; color: #667eea;');
console.log('%c深入了解中華民國國軍的歷史與現況', 'font-size: 14px; color: #666;');

// ===== Load Animation Complete =====
window.addEventListener('load', function() {
    console.log('✅ 國軍簡介頁面載入完成！');
});
