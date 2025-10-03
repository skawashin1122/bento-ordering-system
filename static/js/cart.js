/**
 * カート機能のJavaScript
 * Phase 1: モック注文処理、Phase 2: 実API連携
 */

// グローバル状態管理
let cart = [];

// DOM要素の取得
const cartContent = document.getElementById('cart-content');
const emptyCart = document.getElementById('empty-cart');
const cartCheckout = document.getElementById('cart-checkout');
const cartCount = document.getElementById('cart-count');
const subtotalEl = document.getElementById('subtotal');
const totalEl = document.getElementById('total');
const orderForm = document.getElementById('order-form');
const orderBtn = document.getElementById('order-btn');
const orderSuccessModal = document.getElementById('order-success-modal');

// ローカルストレージキー
const CART_STORAGE_KEY = 'bentoCart';

/**
 * ページ初期化
 */
document.addEventListener('DOMContentLoaded', function() {
    loadCartFromStorage();
    updateCartDisplay();
    initializeOrderForm();
    
    console.log('カートページが初期化されました');
});

/**
 * ローカルストレージからカートデータを読み込み
 */
function loadCartFromStorage() {
    try {
        const savedCart = localStorage.getItem(CART_STORAGE_KEY);
        if (savedCart) {
            cart = JSON.parse(savedCart);
            console.log('カートデータを読み込みました:', cart);
        }
    } catch (error) {
        console.error('カートデータの読み込みに失敗:', error);
        cart = [];
    }
}

/**
 * カートデータをローカルストレージに保存
 */
function saveCartToStorage() {
    try {
        localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
    } catch (error) {
        console.error('カートデータの保存に失敗:', error);
    }
}

/**
 * カート表示を更新
 */
function updateCartDisplay() {
    updateCartCount();
    
    if (cart.length === 0) {
        showEmptyCart();
    } else {
        showCartItems();
        updateCartSummary();
    }
}

/**
 * カートアイテム数の更新
 */
function updateCartCount() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
}

/**
 * 空のカート表示
 */
function showEmptyCart() {
    cartContent.style.display = 'none';
    cartCheckout.style.display = 'none';
    emptyCart.style.display = 'block';
}

/**
 * カートアイテム表示
 */
function showCartItems() {
    emptyCart.style.display = 'none';
    cartContent.style.display = 'block';
    cartCheckout.style.display = 'block';
    
    const cartItemsHTML = cart.map(item => `
        <div class="cart-items">
            <div class="cart-item" data-menu-id="${item.menu_id}">
                <img src="${item.image}" alt="${item.name}" class="item-image" 
                     onerror="this.src='/static/images/default-bento.jpg'">
                <div class="item-info">
                    <div class="item-name">${item.name}</div>
                    <div class="item-price">¥${item.price.toLocaleString()}</div>
                </div>
                <div class="quantity-controls">
                    <button class="quantity-btn" onclick="updateQuantity(${item.menu_id}, ${item.quantity - 1})"
                            ${item.quantity <= 1 ? 'disabled' : ''}>
                        −
                    </button>
                    <span class="quantity">${item.quantity}</span>
                    <button class="quantity-btn" onclick="updateQuantity(${item.menu_id}, ${item.quantity + 1})">
                        ＋
                    </button>
                </div>
                <button class="remove-btn" onclick="removeFromCart(${item.menu_id})">
                    削除
                </button>
            </div>
        </div>
    `).join('');
    
    cartContent.innerHTML = cartItemsHTML;
}

/**
 * カートサマリーの更新
 */
function updateCartSummary() {
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const total = subtotal; // 配送料無料
    
    subtotalEl.textContent = `¥${subtotal.toLocaleString()}`;
    totalEl.textContent = `¥${total.toLocaleString()}`;
}

/**
 * アイテム数量の更新
 */
function updateQuantity(menuId, newQuantity) {
    if (newQuantity <= 0) {
        removeFromCart(menuId);
        return;
    }
    
    const itemIndex = cart.findIndex(item => item.menu_id === menuId);
    if (itemIndex !== -1) {
        cart[itemIndex].quantity = newQuantity;
        saveCartToStorage();
        updateCartDisplay();
        
        console.log(`メニューID ${menuId} の数量を ${newQuantity} に更新`);
    }
}

/**
 * カートからアイテムを削除
 */
function removeFromCart(menuId) {
    cart = cart.filter(item => item.menu_id !== menuId);
    saveCartToStorage();
    updateCartDisplay();
    
    console.log(`メニューID ${menuId} をカートから削除`);
}

/**
 * 注文フォームの初期化
 */
function initializeOrderForm() {
    // 最小配送時間を設定（現在時刻から1時間後）
    const now = new Date();
    now.setHours(now.getHours() + 1);
    const minDateTime = now.toISOString().slice(0, 16);
    document.getElementById('delivery-time').min = minDateTime;
    
    // フォーム送信イベント
    orderForm.addEventListener('submit', handleOrderSubmit);
}

/**
 * 注文送信処理
 */
async function handleOrderSubmit(event) {
    event.preventDefault();
    
    if (cart.length === 0) {
        alert('カートが空です。商品を追加してください。');
        return;
    }
    
    // ボタンを無効化
    orderBtn.disabled = true;
    orderBtn.textContent = '注文処理中...';
    
    try {
        const formData = new FormData(orderForm);
        const orderData = {
            items: cart.map(item => ({
                menu_id: item.menu_id,
                quantity: item.quantity
            })),
            delivery_address: formData.get('delivery_address'),
            delivery_time: formData.get('delivery_time'),
            notes: formData.get('notes') || null
        };
        
        console.log('注文データ:', orderData);
        
        // Phase 1: モック注文処理
        const result = await mockOrderSubmit(orderData);
        
        // Phase 2で実装予定: 実API呼び出し
        // const result = await submitOrder(orderData);
        
        if (result.success) {
            showOrderSuccess(result.order_id);
            clearCart();
        } else {
            throw new Error(result.error);
        }
        
    } catch (error) {
        console.error('注文処理エラー:', error);
        alert('注文の処理中にエラーが発生しました。もう一度お試しください。');
    } finally {
        // ボタンを有効化
        orderBtn.disabled = false;
        orderBtn.textContent = '注文を確定する';
    }
}

/**
 * Phase 1: モック注文処理
 */
async function mockOrderSubmit(orderData) {
    // 実際のAPI呼び出しをシミュレート
    return new Promise((resolve) => {
        setTimeout(() => {
            const orderId = `ORD${Date.now()}`;
            console.log('モック注文完了:', { orderId, orderData });
            
            resolve({
                success: true,
                order_id: orderId,
                message: '注文が正常に処理されました'
            });
        }, 1500); // 1.5秒の遅延でAPIを模擬
    });
}

/**
 * Phase 2で実装予定: 実際のAPI注文送信
 */
async function submitOrder(orderData) {
    try {
        const response = await fetch('/api/v1/orders/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // 'Authorization': `Bearer ${getAuthToken()}` // 認証実装後に追加
            },
            body: JSON.stringify(orderData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || '注文の送信に失敗しました');
        }
        
        const result = await response.json();
        return {
            success: true,
            order_id: result.id,
            result: result
        };
        
    } catch (error) {
        console.error('API注文送信エラー:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * 注文完了表示
 */
function showOrderSuccess(orderId) {
    document.getElementById('order-number').textContent = orderId;
    orderSuccessModal.style.display = 'flex';
    
    // 3秒後に自動でモーダルを閉じる
    setTimeout(() => {
        orderSuccessModal.style.display = 'none';
    }, 3000);
}

/**
 * カートをクリア
 */
function clearCart() {
    cart = [];
    saveCartToStorage();
    updateCartDisplay();
    orderForm.reset();
    
    console.log('カートをクリアしました');
}

/**
 * メニューページからカートに追加された際のハンドラー
 * menu.jsから呼び出される
 */
window.addToCart = function(menuId, name, price, image) {
    const existingItem = cart.find(item => item.menu_id === menuId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            menu_id: menuId,
            name: name,
            price: price,
            image: image,
            quantity: 1
        });
    }
    
    saveCartToStorage();
    updateCartCount();
    
    console.log(`メニュー「${name}」をカートに追加`);
    
    // メニューページでの成功表示
    showAddToCartSuccess(name);
};

/**
 * カート追加成功メッセージの表示
 */
function showAddToCartSuccess(itemName) {
    // 簡単な通知表示（実装は簡略化）
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #28a745;
        color: white;
        padding: 1rem;
        border-radius: 4px;
        z-index: 1000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    `;
    notification.textContent = `「${itemName}」をカートに追加しました`;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

/**
 * 外部からカート情報を取得するためのAPI
 */
window.getCartInfo = function() {
    return {
        items: cart,
        count: cart.reduce((sum, item) => sum + item.quantity, 0),
        total: cart.reduce((sum, item) => sum + (item.price * item.quantity), 0)
    };
};

// モーダルのクリックイベント（背景クリックで閉じる）
window.onclick = function(event) {
    if (event.target === orderSuccessModal) {
        orderSuccessModal.style.display = 'none';
    }
};