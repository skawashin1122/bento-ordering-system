/**
 * メニュー表示とカート機能のJavaScript
 * Phase 1: モックデータ、Phase 2: 実API連携
 */

// ========================================
// モックデータ（Phase 1）
// ========================================
const MOCK_MENUS = [
    {
        id: 1,
        name: "から揚げ弁当",
        description: "ジューシーなから揚げがメイン。ご飯と野菜のバランスも◎",
        price: 580,
        category: "meat",
        image_url: "https://via.placeholder.com/300x200/3498db/ffffff?text=から揚げ弁当",
        is_available: true,
        created_at: "2024-01-01T12:00:00",
        updated_at: "2024-01-01T12:00:00"
    },
    {
        id: 2,
        name: "鮭弁当",
        description: "焼き鮭がメインの和風弁当。栄養バランス抜群です。",
        price: 520,
        category: "fish",
        image_url: "https://via.placeholder.com/300x200/e74c3c/ffffff?text=鮭弁当",
        is_available: true,
        created_at: "2024-01-01T12:00:00",
        updated_at: "2024-01-01T12:00:00"
    },
    {
        id: 3,
        name: "豚の生姜焼き弁当",
        description: "甘辛い生姜焼きでご飯が進む！ボリューム満点です。",
        price: 600,
        category: "meat",
        image_url: "https://via.placeholder.com/300x200/27ae60/ffffff?text=生姜焼き弁当",
        is_available: true,
        created_at: "2024-01-01T12:00:00",
        updated_at: "2024-01-01T12:00:00"
    },
    {
        id: 4,
        name: "野菜炒め弁当",
        description: "色とりどりの野菜をたっぷり使用。ヘルシー志向の方にオススメ。",
        price: 480,
        category: "vegetable",
        image_url: "https://via.placeholder.com/300x200/f39c12/ffffff?text=野菜炒め弁当",
        is_available: true,
        created_at: "2024-01-01T12:00:00",
        updated_at: "2024-01-01T12:00:00"
    },
    {
        id: 5,
        name: "ハンバーグ弁当",
        description: "ジューシーなハンバーグにデミグラスソース。お子様にも大人気！",
        price: 650,
        category: "meat",
        image_url: "https://via.placeholder.com/300x200/9b59b6/ffffff?text=ハンバーグ弁当",
        is_available: true,
        created_at: "2024-01-01T12:00:00",
        updated_at: "2024-01-01T12:00:00"
    },
    {
        id: 6,
        name: "海老フライ弁当",
        description: "プリプリの海老をサクサクの衣で包みました。タルタルソース付き。",
        price: 750,
        category: "fish",
        image_url: "https://via.placeholder.com/300x200/e67e22/ffffff?text=海老フライ弁当",
        is_available: true,
        created_at: "2024-01-01T12:00:00",
        updated_at: "2024-01-01T12:00:00"
    }
];

// ========================================
// 状態管理
// ========================================
let currentCategory = "";
let currentPage = 1;
const itemsPerPage = 6;

// カート管理（ローカルストレージと同期）
const CART_STORAGE_KEY = 'bentoCart';
let cart = [];

// ========================================
// ユーティリティ関数
// ========================================

/**
 * カテゴリ名を日本語に変換
 */
function getCategoryDisplayName(category) {
    const categoryNames = {
        meat: "肉類",
        fish: "魚類",
        vegetable: "野菜",
        other: "その他"
    };
    return categoryNames[category] || category;
}

/**
 * 価格を円表記にフォーマット
 */
function formatPrice(price) {
    return `¥${price.toLocaleString()}`;
}

/**
 * ローディング表示の制御
 */
function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('menu-grid').classList.add('hidden');
    document.getElementById('error-message').classList.add('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('menu-grid').classList.remove('hidden');
}

/**
 * エラー表示
 */
function showError() {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('menu-grid').classList.add('hidden');
    document.getElementById('error-message').classList.remove('hidden');
}

// ========================================
// カート関連関数
// ========================================

/**
 * ローカルストレージからカートを読み込み
 */
function loadCartFromStorage() {
    try {
        const savedCart = localStorage.getItem(CART_STORAGE_KEY);
        if (savedCart) {
            cart = JSON.parse(savedCart);
        }
    } catch (error) {
        console.error('カートデータの読み込みに失敗:', error);
        cart = [];
    }
}

/**
 * カートをローカルストレージに保存
 */
function saveCartToStorage() {
    try {
        localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
    } catch (error) {
        console.error('カートデータの保存に失敗:', error);
    }
}

/**
 * カート数量を更新
 */
function updateCartCount() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const cartCountEl = document.getElementById('cart-count');
    if (cartCountEl) {
        cartCountEl.textContent = totalItems;
    }
}

/**
 * カートにアイテムを追加
 */
function addToCart(menuId) {
    const menu = MOCK_MENUS.find(m => m.id === menuId);
    if (!menu) {
        alert('メニューが見つかりません');
        return;
    }
    
    if (!menu.is_available) {
        alert('このメニューは現在販売されていません');
        return;
    }
    
    const existingItem = cart.find(item => item.menu_id === menuId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            menu_id: menuId,
            name: menu.name,
            price: menu.price,
            image: menu.image_url,
            quantity: 1
        });
    }
    
    saveCartToStorage();
    updateCartCount();
    
    console.log(`メニュー「${menu.name}」をカートに追加`);
    showAddToCartNotification(menu.name);
}

/**
 * カート追加通知を表示
 */
function showAddToCartNotification(itemName) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #28a745;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 4px;
        z-index: 1000;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        font-weight: bold;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = `「${itemName}」をカートに追加しました`;
    
    // アニメーションスタイルを追加
    if (!document.getElementById('cart-animation-style')) {
        const style = document.createElement('style');
        style.id = 'cart-animation-style';
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => notification.remove(), 300);
    }, 2500);
}

// ========================================
// API通信関数（Phase 1はダミー、Phase 2で実装）
// ========================================

/**
 * メニュー一覧を取得（ダミー実装）
 */
async function fetchMenus(category = "", offset = 0, limit = itemsPerPage) {
    console.log('API通信中...（ダミー）');
    
    // ネットワーク遅延を模倣
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // カテゴリフィルタリング
    let filteredMenus = MOCK_MENUS;
    if (category) {
        filteredMenus = MOCK_MENUS.filter(menu => menu.category === category);
    }
    
    // ページネーション
    const total = filteredMenus.length;
    const items = filteredMenus.slice(offset, offset + limit);
    
    return {
        items,
        total,
        limit,
        offset
    };
}

/**
 * メニュー詳細を取得（ダミー実装）
 */
async function fetchMenuDetail(menuId) {
    console.log(`メニュー詳細取得中... ID: ${menuId}（ダミー）`);
    
    // ネットワーク遅延を模倣
    await new Promise(resolve => setTimeout(resolve, 300));
    
    const menu = MOCK_MENUS.find(m => m.id === menuId);
    if (!menu) {
        throw new Error('メニューが見つかりません');
    }
    
    return menu;
}

// ========================================
// メニュー表示関数
// ========================================

/**
 * メニューカードのHTML生成
 */
function createMenuCard(menu) {
    return `
        <div class="menu-card" onclick="showMenuDetail(${menu.id})">
            <div class="menu-image" style="background-image: url('${menu.image_url}')">
                ${menu.image_url ? '' : '🍱'}
            </div>
            <div class="menu-content">
                <h3 class="menu-name">${menu.name}</h3>
                <p class="menu-description">${menu.description}</p>
                <div class="menu-category">${getCategoryDisplayName(menu.category)}</div>
                <div class="menu-price">${formatPrice(menu.price)}</div>
                <button class="btn btn-primary add-to-cart" onclick="event.stopPropagation(); addToCart(${menu.id})">
                    カートに追加
                </button>
            </div>
        </div>
    `;
}

/**
 * メニュー一覧を表示
 */
async function displayMenus() {
    showLoading();
    
    try {
        const offset = (currentPage - 1) * itemsPerPage;
        const data = await fetchMenus(currentCategory, offset, itemsPerPage);
        
        const menuGrid = document.getElementById('menu-grid');
        
        if (data.items.length === 0) {
            menuGrid.innerHTML = '<p class="text-center">メニューが見つかりませんでした。</p>';
        } else {
            menuGrid.innerHTML = data.items.map(createMenuCard).join('');
        }
        
        updatePagination(data.total);
        hideLoading();
        
    } catch (error) {
        console.error('メニュー取得エラー:', error);
        showError();
    }
}

/**
 * メニュー詳細モーダルを表示
 */
async function showMenuDetail(menuId) {
    try {
        const menu = await fetchMenuDetail(menuId);
        const modal = document.getElementById('menu-modal');
        const modalBody = modal.querySelector('.modal-body');
        
        modalBody.innerHTML = `
            <div class="text-center">
                <div class="menu-image" style="background-image: url('${menu.image_url}'); width: 100%; height: 250px; margin-bottom: 1rem;">
                    ${menu.image_url ? '' : '🍱'}
                </div>
                <h2>${menu.name}</h2>
                <p class="menu-description" style="margin: 1rem 0;">${menu.description}</p>
                <div class="menu-category" style="margin: 1rem 0;">${getCategoryDisplayName(menu.category)}</div>
                <div class="menu-price" style="font-size: 2rem; margin: 1rem 0;">${formatPrice(menu.price)}</div>
                <button class="btn btn-primary btn-lg" onclick="addToCart(${menu.id}); closeModal()">
                    カートに追加
                </button>
            </div>
        `;
        
        modal.style.display = 'block';
        
    } catch (error) {
        console.error('メニュー詳細取得エラー:', error);
        alert('メニュー詳細を取得できませんでした。');
    }
}

/**
 * モーダルを閉じる
 */
function closeModal() {
    document.getElementById('menu-modal').style.display = 'none';
}

// ========================================
// イベントハンドラー
// ========================================

/**
 * カテゴリフィルター
 */
function handleCategoryFilter(category) {
    currentCategory = category;
    currentPage = 1;
    
    // フィルターボタンのアクティブ状態更新
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-category="${category}"]`).classList.add('active');
    
    // メニュー再読み込み
    displayMenus();
}

/**
 * ページネーション処理
 */
function updatePagination(total) {
    const totalPages = Math.ceil(total / itemsPerPage);
    
    // ページ情報更新
    document.getElementById('page-info').textContent = 
        `${currentPage} / ${totalPages} ページ (全 ${total} 件)`;
    
    // 前ページボタン
    document.getElementById('prev-page').disabled = currentPage <= 1;
    
    // 次ページボタン  
    document.getElementById('next-page').disabled = currentPage >= totalPages;
}

function handlePrevPage() {
    if (currentPage > 1) {
        currentPage--;
        displayMenus();
    }
}

function handleNextPage() {
    currentPage++;
    displayMenus();
}

// ========================================
// 初期化とイベントハンドラー
// ========================================

/**
 * ページ初期化
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('メニューページが読み込まれました');
    
    // カート初期化
    loadCartFromStorage();
    
    // フィルターボタンのイベント設定
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const category = this.dataset.category;
            handleCategoryFilter(category);
        });
    });
    
    // ページネーションボタン
    document.getElementById('prev-page').addEventListener('click', handlePrevPage);
    document.getElementById('next-page').addEventListener('click', handleNextPage);
    
    // モーダル閉じる
    document.querySelector('.modal-close').addEventListener('click', closeModal);
    document.getElementById('menu-modal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeModal();
        }
    });
    
    // 初期表示
    updateCartCount();
    displayMenus();
});

// ========================================
// API結合用の関数（Phase 2で実装予定）
// ========================================

/**
 * 実際のAPI呼び出し（Phase 2で実装予定）
 */
async function fetchMenusFromAPI(category = "", offset = 0, limit = itemsPerPage) {
    const params = new URLSearchParams({
        limit: limit.toString(),
        offset: offset.toString()
    });
    
    if (category) {
        params.append('category', category);
    }
    
    const response = await fetch(`/api/v1/menus/?${params}`);
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

async function fetchMenuDetailFromAPI(menuId) {
    const response = await fetch(`/api/v1/menus/${menuId}`);
    
    if (!response.ok) {
        if (response.status === 404) {
            throw new Error('メニューが見つかりません');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// Phase 2でダミー関数を実際のAPI関数に置き換える予定
// fetchMenus = fetchMenusFromAPI;
// fetchMenuDetail = fetchMenuDetailFromAPI;