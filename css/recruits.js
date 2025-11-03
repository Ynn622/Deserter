// ===== Topic Content Data =====
const topicContent = {
    terminology: {
        title: '新訓常用名詞解釋',
        content: `
            <h4>軍中暗語大解密</h4>
            <p>剛入伍最怕聽不懂長官在說什麼，這裡整理了最常用的軍中用語：</p>
            <ul>
                <li><strong>阿凱過（OK啦）：</strong>表示同意、沒問題</li>
                <li><strong>長官辛苦：</strong>萬用問候語，見到長官就對了</li>
                <li><strong>了解：</strong>表示收到指令，不是真的了解</li>
                <li><strong>報告：</strong>任何對話前都要先說這個</li>
                <li><strong>收操：</strong>結束訓練，可以休息了</li>
                <li><strong>集合：</strong>要快速整隊，動作要快</li>
                <li><strong>打飯班：</strong>負責分配伙食的人</li>
                <li><strong>公差：</strong>額外的工作任務</li>
                <li><strong>站哨：</strong>輪值站崗</li>
                <li><strong>禁足：</strong>不能外出，要留在營區</li>
            </ul>
            <h4>生存小技巧</h4>
            <p>記住這些用語，配合正確的態度和反應速度，就能在新訓中活得更輕鬆！</p>
        `
    },
    checklist: {
        title: '入伍前後注意事項',
        content: `
            <h4>入伍前準備清單</h4>
            <ul>
                <li>身分證、健保卡（必帶）</li>
                <li>入營通知書</li>
                <li>印章（建議帶）</li>
                <li>零錢約500-1000元</li>
                <li>個人盥洗用具（牙刷、牙膏、毛巾）</li>
                <li>內衣褲數套（會發但自己的比較舒服）</li>
                <li>眼鏡（如有近視，建議帶備用）</li>
            </ul>
            <h4>手機與3C產品</h4>
            <p><strong>新訓期間：</strong>手機通常可以帶，但使用時間有限制，通常是晚上或假日才能使用。</p>
            <p><strong>下部隊後：</strong>依各單位規定，大部分晚上可自由使用。</p>
            <h4>入伍當天注意事項</h4>
            <ul>
                <li>提早到達集合地點</li>
                <li>不要遲到（會被記住）</li>
                <li>保持低調，不要太突出</li>
                <li>聽從指示，不要亂問問題</li>
                <li>貴重物品不要帶太多</li>
            </ul>
            <h4>禁止攜帶物品</h4>
            <ul>
                <li>違禁品（刀械、毒品等）</li>
                <li>易燃易爆物品</li>
                <li>過多現金</li>
                <li>遊戲機、平板等娛樂用品</li>
            </ul>
        `
    },
    classes: {
        title: '部隊中常見的班級類型',
        content: `
            <h4>認識你的戰友們</h4>
            <p>在部隊裡，你會遇到各式各樣的人，以下是最常見的幾種類型：</p>
            
            <h4>💪 全能戰士型</h4>
            <p>體能好、反應快、做事積極，常被選為班長或值星。優點是能帶動團隊，缺點是容易被長官盯上做更多事。</p>
            
            <h4>😴 擺爛躺平型</h4>
            <p>能躲就躲、能睡就睡，公差永遠找不到人。雖然讓人頭痛，但有時也是生存智慧的展現。</p>
            
            <h4>🤓 理論派學霸型</h4>
            <p>背條文、記規定樣樣精通，考試第一名但實作可能不太行。適合當教育班長或文書兵。</p>
            
            <h4>😂 搞笑氣氛組</h4>
            <p>專門講幹話、逗大家開心，是營區的開心果。雖然常被唸，但大家都喜歡他。</p>
            
            <h4>😇 乖乖牌聽話型</h4>
            <p>長官說什麼就做什麼，不多問不抱怨。雖然不突出，但也不會出錯，是最安全的類型。</p>
            
            <h4>🎯 關係戶特權型</h4>
            <p>家裡有背景或認識長官，可能有特殊待遇。不用羨慕，做好自己的事就好。</p>
            
            <h4>你是哪一型？</h4>
            <p>每個人都有自己的生存方式，重要的是找到適合自己的位置，和大家和平相處！</p>
        `
    },
    survival: {
        title: '不被班長盯上的五大心法',
        content: `
            <h4>軍中生存黃金法則</h4>
            <p>想要平安退伍？記住這五大心法，讓你在軍中如魚得水：</p>
            
            <h4>🤐 第一心法：沉默是金</h4>
            <p>不要當第一個發問的人，也不要當最後一個完成任務的人。保持中庸之道，不突出也不落後。</p>
            <ul>
                <li>長官問「有沒有問題」時，不要真的問問題</li>
                <li>不要主動表達意見</li>
                <li>少說話多做事</li>
            </ul>
            
            <h4>⚡ 第二心法：動作要快</h4>
            <p>軍中最重視效率，動作慢就等著被盯上。</p>
            <ul>
                <li>集合速度要快</li>
                <li>聽到指令立刻反應</li>
                <li>公差搶著做（表現積極但不要太突出）</li>
            </ul>
            
            <h4>🙊 第三心法：少講幹話</h4>
            <p>幽默可以，但要看時機和對象。</p>
            <ul>
                <li>不要在長官面前耍嘴皮子</li>
                <li>不要取笑其他同袍</li>
                <li>抱怨可以但私底下說</li>
            </ul>
            
            <h4>👏 第四心法：多捧場</h4>
            <p>適時的讚美和認同很重要。</p>
            <ul>
                <li>長官講話要點頭</li>
                <li>「了解」、「收到」、「是」要大聲</li>
                <li>班長辛苦了要常說</li>
            </ul>
            
            <h4>🎯 第五心法：服從第一</h4>
            <p>軍中最重要的就是服從命令。</p>
            <ul>
                <li>不要質疑命令</li>
                <li>不要找理由推託</li>
                <li>就算不合理也先做再說</li>
            </ul>
            
            <h4>💡 額外加分項</h4>
            <ul>
                <li>主動幫忙整理環境</li>
                <li>對同袍友善</li>
                <li>保持儀容整潔</li>
                <li>不要抱怨伙食（很重要！）</li>
            </ul>
            
            <p><strong>記住：</strong>當兵就是一場表演，演好你的角色，時間很快就過去了！</p>
        `
    }
};

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

// ===== Topic Card Click Handlers =====
const topicButtons = document.querySelectorAll('.btn-topic');
const topicModal = new bootstrap.Modal(document.getElementById('topicModal'));
const modalTitle = document.getElementById('topicModalLabel');
const modalBody = document.getElementById('topicModalBody');

topicButtons.forEach(button => {
    button.addEventListener('click', function(e) {
        e.stopPropagation();
        const topic = this.getAttribute('data-topic');
        const content = topicContent[topic];
        
        if (content) {
            modalTitle.textContent = content.title;
            modalBody.innerHTML = content.content;
            topicModal.show();
        }
    });
});

// ===== Topic Cards Hover Effect =====
const topicCards = document.querySelectorAll('.topic-card');

topicCards.forEach(card => {
    // Add ripple effect on click
    card.addEventListener('click', function(e) {
        // Only trigger if not clicking on button
        if (e.target.classList.contains('btn-topic') || e.target.closest('.btn-topic')) {
            return;
        }
        
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
        ripple.style.background = 'rgba(102, 126, 234, 0.3)';
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

// ===== Initialize Cards (Animation Removed) =====
topicCards.forEach(card => {
    // Cards are visible by default, just add animated class for icon float
    card.classList.add('animated');
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

// ===== Console Messages =====
console.log('%c新兵入伍指南', 'font-size: 24px; font-weight: bold; color: #667eea;');
console.log('%c祝你順利退伍！💪', 'font-size: 14px; color: #666;');

// ===== Easter Egg =====
let clickCount = 0;
const introBox = document.querySelector('.intro-box');

if (introBox) {
    introBox.addEventListener('click', function() {
        clickCount++;
        if (clickCount === 5) {
            alert('🎉 恭喜發現彩蛋！\n\n記住：當兵最重要的是平安退伍！\n保持低調、做好自己、時間很快就過去了！\n\n加油，未來的老兵！💪');
            clickCount = 0;
        }
    });
}

// ===== Load Complete =====
window.addEventListener('load', function() {
    console.log('✅ 新兵入伍指南頁面載入完成！');
    console.log('💡 提示：點擊介紹框5次有驚喜！');
});
