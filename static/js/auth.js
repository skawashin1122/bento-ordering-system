// 認証関連の状態管理
let authToken = localStorage.getItem('authToken');

// APIエンドポイント
const API_URL = '/api/v1';

// 本番環境の認証処理
async function login(email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                username: email,
                password: password,
                grant_type: 'password'
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'ログインに失敗しました');
        }

        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        return data;
    } catch (error) {
        console.error('ログインエラー:', error);
        throw error;
    }
}

async function register(email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '登録に失敗しました');
        }

        return await login(email, password);
    } catch (error) {
        console.error('登録エラー:', error);
        throw error;
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