// 認証関連の状態管理
let authToken = localStorage.getItem('authToken');

// APIエンドポイント
const API_URL = '/api/v1';

// ダミーの認証処理（本番環境では実際のAPIを使用）
async function login(email, password) {
    console.log('API通信中...');
    await new Promise(r => setTimeout(r, 500)); // ネットワーク遅延を模倣
    if (email === 'test@example.com' && password === 'password') {
        const token = 'dummy-jwt-token-string';
        localStorage.setItem('authToken', token);
        return { access_token: token };
    } else {
        throw new Error('メールアドレスまたはパスワードが違います');
    }
}

async function register(email, password) {
    console.log('API通信中...');
    await new Promise(r => setTimeout(r, 500)); // ネットワーク遅延を模倣
    if (email && password) {
        const token = 'dummy-jwt-token-string';
        localStorage.setItem('authToken', token);
        return { access_token: token };
    } else {
        throw new Error('登録に失敗しました');
    }
}

// UI関連の処理
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const showRegisterLink = document.getElementById('showRegister');
    const showLoginLink = document.getElementById('showLogin');
    const registerFormDiv = document.getElementById('registerForm');

    // ログインフォームの送信処理
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const result = await login(email, password);
            console.log('ログイン成功:', result);
            window.location.href = '/'; // ログイン成功後はトップページへ
        } catch (error) {
            alert(error.message);
        }
    });

    // 新規登録フォームの送信処理
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;

        try {
            const result = await register(email, password);
            console.log('登録成功:', result);
            window.location.href = '/'; // 登録成功後はトップページへ
        } catch (error) {
            alert(error.message);
        }
    });

    // フォーム切り替え処理
    showRegisterLink.addEventListener('click', (e) => {
        e.preventDefault();
        loginForm.parentElement.style.display = 'none';
        registerFormDiv.style.display = 'block';
    });

    showLoginLink.addEventListener('click', (e) => {
        e.preventDefault();
        loginForm.parentElement.style.display = 'block';
        registerFormDiv.style.display = 'none';
    });
});