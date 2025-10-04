// トークンの取得
function getToken() {
    return localStorage.getItem('token');
}

// 日時フォーマット関数
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('ja-JP', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

// ステータスの日本語表示
const statusMapping = {
    'PENDING': '保留中',
    'PREPARING': '準備中',
    'READY': '準備完了',
    'DELIVERING': '配達中',
    'DELIVERED': '配達完了',
    'CANCELLED': 'キャンセル'
};

// 注文一覧の取得
async function fetchOrders() {
    try {
        const token = getToken();
        if (!token) {
            window.location.href = '/login';
            return;
        }

        const response = await fetch('/api/v1/admin/orders/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            window.location.href = '/login';
            return;
        }

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const orders = await response.json();
        return orders;
    } catch (error) {
        console.error('注文の取得に失敗しました:', error);
        showError('注文の取得に失敗しました。');
    }
}

// 注文ステータスの更新
async function updateOrderStatus(orderId, newStatus) {
    try {
        const token = getToken();
        if (!token) {
            window.location.href = '/login';
            return;
        }

        const response = await fetch(`/api/v1/admin/orders/${orderId}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        });

        if (response.status === 401) {
            window.location.href = '/login';
            return;
        }

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        await refreshOrders();
        showSuccess('注文ステータスを更新しました。');
    } catch (error) {
        console.error('ステータスの更新に失敗しました:', error);
        showError('ステータスの更新に失敗しました。');
    }
}

// 注文テーブルの更新
function updateOrderTable(orders) {
    const tableBody = document.getElementById('orderTableBody');
    const statusFilter = document.getElementById('statusFilter').value;

    // フィルタリング
    const filteredOrders = statusFilter
        ? orders.filter(order => order.status === statusFilter)
        : orders;

    // テーブル内容のクリア
    tableBody.innerHTML = '';

    // 注文の表示
    filteredOrders.forEach(order => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${order.id}</td>
            <td>${formatDateTime(order.created_at)}</td>
            <td>${order.delivery_address}</td>
            <td>${statusMapping[order.status] || order.status}</td>
            <td>¥${order.total_amount.toLocaleString()}</td>
            <td>
                <div class="btn-group">
                    <button class="btn btn-info btn-sm" onclick="showOrderDetail(${order.id})">
                        詳細
                    </button>
                    <button class="btn btn-primary btn-sm dropdown-toggle" data-bs-toggle="dropdown">
                        ステータス変更
                    </button>
                    <ul class="dropdown-menu">
                        ${Object.entries(statusMapping)
                .filter(([status]) => status !== order.status)
                .map(([status, label]) => `
                                <li><a class="dropdown-item" href="#" 
                                    onclick="updateOrderStatus(${order.id}, '${status}')">
                                    ${label}
                                </a></li>
                            `).join('')}
                    </ul>
                </div>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// 注文一覧の更新
async function refreshOrders() {
    const orders = await fetchOrders();
    if (orders) {
        updateOrderTable(orders);
    }
}

// 注文の詳細表示
async function showOrderDetail(orderId) {
    try {
        const token = getToken();
        if (!token) {
            window.location.href = '/login';
            return;
        }

        const response = await fetch(`/api/v1/admin/orders/${orderId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            window.location.href = '/login';
            return;
        }

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const order = await response.json();

        // モーダル内容の更新
        const modalContent = document.getElementById('orderDetailContent');
        modalContent.innerHTML = `
            <div class="order-detail">
                <h4>注文情報</h4>
                <p><strong>注文ID:</strong> ${order.id}</p>
                <p><strong>注文日時:</strong> ${formatDateTime(order.created_at)}</p>
                <p><strong>ステータス:</strong> ${statusMapping[order.status] || order.status}</p>
                <p><strong>お届け先:</strong> ${order.delivery_address}</p>
                <p><strong>お届け希望時間:</strong> ${order.delivery_time ? formatDateTime(order.delivery_time) : '指定なし'}</p>
                
                <h4 class="mt-4">注文内容</h4>
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>商品名</th>
                            <th>数量</th>
                            <th>単価</th>
                            <th>小計</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${order.items.map(item => `
                            <tr>
                                <td>${item.menu_item.name}</td>
                                <td>${item.quantity}</td>
                                <td>¥${item.menu_item.price.toLocaleString()}</td>
                                <td>¥${(item.quantity * item.menu_item.price).toLocaleString()}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                
                <div class="text-end mt-3">
                    <h5>合計金額: ¥${order.total_amount.toLocaleString()}</h5>
                </div>
            </div>
        `;

        // モーダルの表示
        const modal = new bootstrap.Modal(document.getElementById('orderDetailModal'));
        modal.show();
    } catch (error) {
        console.error('注文詳細の取得に失敗しました:', error);
        showError('注文詳細の取得に失敗しました。');
    }
}

// エラーメッセージの表示
function showError(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.container').firstChild);
}

// 成功メッセージの表示
function showSuccess(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.container').firstChild);
}

// フィルター適用
function filterOrders() {
    refreshOrders();
}

// ページ読み込み時に注文一覧を取得
document.addEventListener('DOMContentLoaded', () => {
    refreshOrders();
});