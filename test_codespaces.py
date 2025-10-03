#!/usr/bin/env python3
"""
Codespaces環境テストスクリプト
ワークスペースとPython環境が正常に動作するかチェック
"""

import os
import sys
from pathlib import Path

def test_workspace():
    """ワークスペース環境をテスト"""
    print("🔍 Codespaces環境テスト")
    print("=" * 40)
    
    # 現在の作業ディレクトリ
    cwd = Path.cwd()
    print(f"📂 現在のディレクトリ: {cwd}")
    
    # プロジェクトファイルの確認
    expected_files = [
        "app",
        "static", 
        "templates",
        "requirements.txt",
        "docker-compose.yml",
        "README.md"
    ]
    
    print("\n📋 プロジェクトファイル確認:")
    all_exist = True
    for file_name in expected_files:
        file_path = cwd / file_name
        exists = file_path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {file_name}")
        if not exists:
            all_exist = False
    
    # Python環境確認
    print(f"\n🐍 Python環境:")
    print(f"  - バージョン: {sys.version}")
    print(f"  - 実行パス: {sys.executable}")
    print(f"  - PYTHONPATH: {sys.path[:3]}...")
    
    # 依存関係の確認
    print(f"\n📦 重要な依存関係:")
    packages = ["fastapi", "sqlalchemy", "alembic", "uvicorn"]
    for package in packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (未インストール)")
            all_exist = False
    
    # 結果
    print("\n" + "=" * 40)
    if all_exist:
        print("🎉 環境テスト成功！Task A開発を開始できます。")
        print("\n🚀 開発開始コマンド:")
        print("  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("⚠️ 環境に問題があります。依存関係をインストールしてください:")
        print("  pip install -r requirements.txt")
    
    return all_exist

if __name__ == "__main__":
    test_workspace()