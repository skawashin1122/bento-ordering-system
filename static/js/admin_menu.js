/**
 * 管理者メニュー管理画面のJavaScript
 * ダミーロジック：JS配列データ操作
 */

// ダミーデータ（実際の実装ではAPIから取得）
let menuData = [
    {
        id: 1,
        name: "和風ハンバーグ弁当",
        description: "ふっくらジューシーなハンバーグと野菜がたっぷり入った人気の弁当",
        price: 680,
        category: "main",
        image_url: "https://example.com/images/hamburger.jpg",
        is_available: true,
        created_at: "2024-01-15T10:30:00Z",
        updated_at: "2024-01-15T10:30:00Z"
    },
    {
        id: 2,
        name: "鶏のから揚げ弁当",
        description: "サクサクジューシーな鶏のから揚げが自慢の定番弁当",
        price: 750,
        category: "main",
        image_url: "https://example.com/images/karaage.jpg",
        is_available: true,
        created_at: "2024-01-16T11:00:00Z",
        updated_at: "2024-01-16T11:00:00Z"
    },
    {
        id: 3,
        name: "海老フライ弁当",
        description: "プリプリの海老を使った贅沢なフライ弁当",
        price: 890,
        category: "main",
        image_url: "https://example.com/images/ebi_fry.jpg",
        is_available: false,
        created_at: "2024-01-17T09:15:00Z",
        updated_at: "2024-01-20T14:30:00Z"
    },
    {
        id: 4,
        name: "ポテトサラダ",
        description: "クリーミーでまろやかなポテトサラダ",
        price: 280,
        category: "side",
        image_url: "https://example.com/images/potato_salad.jpg",
        is_available: true,
        created_at: "2024-01-18T13:45:00Z",
        updated_at: "2024-01-18T13:45:00Z"
    },
    {
        id: 5,
        name: "緑茶",
        description: "香り豊かな緑茶",
        price: 150,
        category: "drink",
        image_url: "https://example.com/images/green_tea.jpg",
        is_available: true,
        created_at: "2024-01-19T08:20:00Z",
        updated_at: "2024-01-19T08:20:00Z"
    },
    {
        id: 6,
        name: "チョコレートケーキ",
        description: "濃厚なチョコレートの味わいが楽しめるケーキ",
        price: 420,
        category: "dessert",
        image_url: "https://example.com/images/chocolate_cake.jpg",
        is_available: true,
        created_at: "2024-01-20T16:10:00Z",
        updated_at: "2024-01-20T16:10:00Z"
    }
];

// フィルタ条件
let currentFilters = {
    category: '',
    availability: '',
    page: 1,
    limit: 10
};

// 編集中のメニューID
let editingMenuId = null;

// カテゴリ名のマッピング
const categoryNames = {
    'main': 'メイン弁当',
    'side': 'サイドメニュー',
    'drink': 'ドリンク',
    'dessert': 'デザート'
};

/**
 * ページ読み込み時の初期化
 */
document.addEventListener('DOMContentLoaded', function () {
    loadMenuList();
    setupEventListeners();
});

/**
 * イベントリスナーの設定
 */
function setupEventListeners() {
    // フィルタの変更監視
    document.getElementById('categoryFilter').addEventListener('change', function () {
        currentFilters.category = this.value;
    });

    document.getElementById('availabilityFilter').addEventListener('change', function () {
        currentFilters.availability = this.value;
    });

    // モーダルが閉じられた時の処理
    document.getElementById('menuModal').addEventListener('hidden.bs.modal', function () {
        resetMenuForm();
    });
}

/**
 * メニュー一覧の読み込み
 */
function loadMenuList() {
    const filteredData = filterMenuData();
    const paginatedData = paginateData(filteredData);

    renderMenuTable(paginatedData.items);
    renderPagination(paginatedData.totalPages, currentFilters.page);
}

/**
 * データのフィルタリング
 */
function filterMenuData() {
    return menuData.filter(menu => {
        // カテゴリフィルタ
        if (currentFilters.category && menu.category !== currentFilters.category) {
            return false;
        }

        // 販売状況フィルタ
        if (currentFilters.availability !== '') {
            const isAvailable = currentFilters.availability === 'true';
            if (menu.is_available !== isAvailable) {
                return false;
            }
        }

        return true;
    });
}

/**
 * データのページネーション
 */
function paginateData(data) {
    const totalItems = data.length;
    const totalPages = Math.ceil(totalItems / currentFilters.limit);
    const startIndex = (currentFilters.page - 1) * currentFilters.limit;
    const endIndex = startIndex + currentFilters.limit;
    const items = data.slice(startIndex, endIndex);

    return {
        items,
        totalPages,
        totalItems,
        currentPage: currentFilters.page
    };
}

/**
 * メニューテーブルの描画
 */
function renderMenuTable(menus) {
    const tbody = document.getElementById('menuTableBody');

    if (menus.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-muted py-4">
                    <i class="fas fa-box-open me-2"></i>該当する商品がありません
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = menus.map(menu => {
        const statusBadge = menu.is_available
            ? '<span class="badge bg-success">販売中</span>'
            : '<span class="badge bg-secondary">販売停止</span>';

        const formattedDate = new Date(menu.created_at).toLocaleDateString('ja-JP');

        return `
            <tr>
                <td>${menu.id}</td>
                <td>
                    <div class="fw-bold">${escapeHtml(menu.name)}</div>
                    ${menu.description ? `<small class="text-muted">${escapeHtml(menu.description.substring(0, 50))}${menu.description.length > 50 ? '...' : ''}</small>` : ''}
                </td>
                <td>${categoryNames[menu.category] || menu.category}</td>
                <td>¥${menu.price.toLocaleString()}</td>
                <td>${statusBadge}</td>
                <td>${formattedDate}</td>
                <td>
                    <div class="btn-group btn-group-sm" role="group">
                        <button type="button" class="btn btn-outline-primary" onclick="editMenu(${menu.id})" title="編集">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button type="button" class="btn btn-outline-danger" onclick="deleteMenu(${menu.id})" title="削除">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

/**
 * ページネーションの描画
 */
function renderPagination(totalPages, currentPage) {
    const pagination = document.getElementById('pagination');

    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }

    let paginationHtml = '';

    // 前ページボタン
    const prevDisabled = currentPage === 1 ? 'disabled' : '';
    paginationHtml += `
        <li class="page-item ${prevDisabled}">
            <a class="page-link" href="#" onclick="changePage(${currentPage - 1})">前へ</a>
        </li>
    `;

    // ページ番号ボタン
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);

    if (startPage > 1) {
        paginationHtml += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="changePage(1)">1</a>
            </li>
        `;
        if (startPage > 2) {
            paginationHtml += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        const active = i === currentPage ? 'active' : '';
        paginationHtml += `
            <li class="page-item ${active}">
                <a class="page-link" href="#" onclick="changePage(${i})">${i}</a>
            </li>
        `;
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            paginationHtml += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
        paginationHtml += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="changePage(${totalPages})">${totalPages}</a>
            </li>
        `;
    }

    // 次ページボタン
    const nextDisabled = currentPage === totalPages ? 'disabled' : '';
    paginationHtml += `
        <li class="page-item ${nextDisabled}">
            <a class="page-link" href="#" onclick="changePage(${currentPage + 1})">次へ</a>
        </li>
    `;

    pagination.innerHTML = paginationHtml;
}

/**
 * フィルタの適用
 */
function applyFilters() {
    currentFilters.page = 1; // ページを最初に戻す
    loadMenuList();
}

/**
 * フィルタのクリア
 */
function clearFilters() {
    document.getElementById('categoryFilter').value = '';
    document.getElementById('availabilityFilter').value = '';
    currentFilters = {
        category: '',
        availability: '',
        page: 1,
        limit: 10
    };
    loadMenuList();
}

/**
 * ページ変更
 */
function changePage(page) {
    if (page < 1) return;
    currentFilters.page = page;
    loadMenuList();
}

/**
 * 新規メニュー作成モーダルを開く
 */
function openMenuModal() {
    editingMenuId = null;
    document.getElementById('menuModalLabel').textContent = '新規商品追加';
    resetMenuForm();
}

/**
 * メニュー編集
 */
function editMenu(menuId) {
    const menu = menuData.find(m => m.id === menuId);
    if (!menu) {
        showAlert('エラー', 'メニューが見つかりません', 'danger');
        return;
    }

    editingMenuId = menuId;
    document.getElementById('menuModalLabel').textContent = '商品編集';

    // フォームにデータを設定
    document.getElementById('menuId').value = menu.id;
    document.getElementById('menuName').value = menu.name;
    document.getElementById('menuCategory').value = menu.category;
    document.getElementById('menuPrice').value = menu.price;
    document.getElementById('menuImageUrl').value = menu.image_url || '';
    document.getElementById('menuDescription').value = menu.description || '';
    document.getElementById('menuIsAvailable').checked = menu.is_available;

    // モーダルを表示
    const modal = new bootstrap.Modal(document.getElementById('menuModal'));
    modal.show();
}

/**
 * メニュー削除
 */
function deleteMenu(menuId) {
    const menu = menuData.find(m => m.id === menuId);
    if (!menu) {
        showAlert('エラー', 'メニューが見つかりません', 'danger');
        return;
    }

    editingMenuId = menuId;
    document.getElementById('deleteMenuName').textContent = menu.name;

    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}

/**
 * 削除確認
 */
function confirmDelete() {
    if (!editingMenuId) return;

    // データから削除
    const index = menuData.findIndex(m => m.id === editingMenuId);
    if (index !== -1) {
        const deletedMenu = menuData.splice(index, 1)[0];
        showAlert('成功', `「${deletedMenu.name}」を削除しました`, 'success');
        loadMenuList();
    }

    // モーダルを閉じる
    const modal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
    modal.hide();
    editingMenuId = null;
}

/**
 * メニュー保存
 */
function saveMenu() {
    const form = document.getElementById('menuForm');
    const formData = new FormData(form);

    // バリデーション
    if (!formData.get('name').trim()) {
        showAlert('エラー', '商品名を入力してください', 'danger');
        return;
    }

    if (!formData.get('category')) {
        showAlert('エラー', 'カテゴリを選択してください', 'danger');
        return;
    }

    const price = parseFloat(formData.get('price'));
    if (isNaN(price) || price < 0) {
        showAlert('エラー', '正しい価格を入力してください', 'danger');
        return;
    }

    // メニューデータの作成
    const menuItem = {
        name: formData.get('name').trim(),
        description: formData.get('description').trim(),
        price: price,
        category: formData.get('category'),
        image_url: formData.get('image_url').trim(),
        is_available: formData.has('is_available'),
        updated_at: new Date().toISOString()
    };

    if (editingMenuId) {
        // 編集
        const index = menuData.findIndex(m => m.id === editingMenuId);
        if (index !== -1) {
            menuData[index] = { ...menuData[index], ...menuItem };
            showAlert('成功', '商品を更新しました', 'success');
        }
    } else {
        // 新規作成
        const newId = Math.max(...menuData.map(m => m.id)) + 1;
        menuItem.id = newId;
        menuItem.created_at = new Date().toISOString();
        menuData.push(menuItem);
        showAlert('成功', '新しい商品を追加しました', 'success');
    }

    // 一覧を更新
    loadMenuList();

    // モーダルを閉じる
    const modal = bootstrap.Modal.getInstance(document.getElementById('menuModal'));
    modal.hide();
}

/**
 * フォームをリセット
 */
function resetMenuForm() {
    const form = document.getElementById('menuForm');
    form.reset();
    document.getElementById('menuIsAvailable').checked = true;
    editingMenuId = null;
}

/**
 * アラート表示
 */
function showAlert(title, message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    const alertId = 'alert-' + Date.now();

    const alertHtml = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
            <strong>${title}:</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;

    alertContainer.insertAdjacentHTML('beforeend', alertHtml);

    // 5秒後に自動で消す
    setTimeout(() => {
        const alertElement = document.getElementById(alertId);
        if (alertElement) {
            const alert = bootstrap.Alert.getInstance(alertElement);
            if (alert) {
                alert.close();
            }
        }
    }, 5000);
}

/**
 * HTMLエスケープ
 */
function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function (m) { return map[m]; });
}

/**
 * 実際のAPI実装時に使用する関数群
 * 現在はダミーロジックのため、コメントアウト
 */

/*
// 実際のAPI呼び出し版

async function loadMenuListFromAPI() {
    try {
        const params = new URLSearchParams({
            limit: currentFilters.limit,
            offset: (currentFilters.page - 1) * currentFilters.limit,
            available_only: false  // 管理者は全商品を表示
        });

        if (currentFilters.category) {
            params.append('category', currentFilters.category);
        }

        const response = await fetch(`/api/v1/admin/menus/?${params}`);
        const data = await response.json();

        if (response.ok) {
            renderMenuTable(data.items);
            renderPagination(Math.ceil(data.total / currentFilters.limit), currentFilters.page);
        } else {
            showAlert('エラー', 'メニュー一覧の取得に失敗しました', 'danger');
        }
    } catch (error) {
        console.error('API Error:', error);
        showAlert('エラー', 'サーバーとの通信に失敗しました', 'danger');
    }
}

async function saveMenuToAPI() {
    const form = document.getElementById('menuForm');
    const formData = new FormData(form);

    const menuData = {
        name: formData.get('name').trim(),
        description: formData.get('description').trim() || null,
        price: parseFloat(formData.get('price')),
        category: formData.get('category'),
        image_url: formData.get('image_url').trim() || null,
        is_available: formData.has('is_available')
    };

    try {
        let response;
        if (editingMenuId) {
            // 編集
            response = await fetch(`/api/v1/admin/menus/${editingMenuId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(menuData)
            });
        } else {
            // 新規作成
            response = await fetch('/api/v1/admin/menus/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(menuData)
            });
        }

        if (response.ok) {
            const savedMenu = await response.json();
            showAlert('成功', editingMenuId ? '商品を更新しました' : '新しい商品を追加しました', 'success');
            loadMenuListFromAPI();
            
            const modal = bootstrap.Modal.getInstance(document.getElementById('menuModal'));
            modal.hide();
        } else {
            const errorData = await response.json();
            showAlert('エラー', errorData.detail || '保存に失敗しました', 'danger');
        }
    } catch (error) {
        console.error('API Error:', error);
        showAlert('エラー', 'サーバーとの通信に失敗しました', 'danger');
    }
}

async function deleteMenuFromAPI() {
    if (!editingMenuId) return;

    try {
        const response = await fetch(`/api/v1/admin/menus/${editingMenuId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showAlert('成功', '商品を削除しました', 'success');
            loadMenuListFromAPI();
        } else {
            const errorData = await response.json();
            showAlert('エラー', errorData.detail || '削除に失敗しました', 'danger');
        }
    } catch (error) {
        console.error('API Error:', error);
        showAlert('エラー', 'サーバーとの通信に失敗しました', 'danger');
    }

    const modal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
    modal.hide();
    editingMenuId = null;
}
*/