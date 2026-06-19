#!/usr/bin/env python3
"""
통합 테스트 스크립트
백엔드와 프론트엔드 전체 시스템 테스트
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def run_command(cmd, cwd=None):
    """명령어 실행"""
    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, cwd=cwd)
    return result.returncode

def test_backend():
    """백엔드 테스트"""
    print("\n🧪 BACKEND TESTS")
    print("="*60)

    backend_dir = Path("backend")

    # 1. 의존성 확인
    print("\n1️⃣ Checking Python dependencies...")
    if not (backend_dir / "venv").exists():
        print("   Creating virtual environment...")
        run_command(["python3", "-m", "venv", "venv"], cwd=backend_dir)

    # 2. 테스트 실행
    print("\n2️⃣ Running backend tests...")
    result = run_command(
        ["python3", "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd=backend_dir
    )

    if result != 0:
        print("❌ Backend tests failed!")
        return False

    print("✅ Backend tests passed!")
    return True

def test_frontend():
    """프론트엔드 테스트"""
    print("\n🧪 FRONTEND TESTS")
    print("="*60)

    frontend_dir = Path("frontend")

    # 1. 의존성 확인
    print("\n1️⃣ Checking Node dependencies...")
    if not (frontend_dir / "node_modules").exists():
        print("   Installing dependencies...")
        run_command(["npm", "install"], cwd=frontend_dir)

    # 2. 테스트 실행
    print("\n2️⃣ Running frontend tests...")
    result = run_command(["npm", "test"], cwd=frontend_dir)

    if result != 0:
        print("❌ Frontend tests failed!")
        return False

    print("✅ Frontend tests passed!")
    return True

def build_frontend():
    """프론트엔드 빌드"""
    print("\n🏗️ FRONTEND BUILD")
    print("="*60)

    frontend_dir = Path("frontend")

    print("\n1️⃣ Building frontend...")
    result = run_command(["npm", "run", "build"], cwd=frontend_dir)

    if result != 0:
        print("❌ Frontend build failed!")
        return False

    print("✅ Frontend build successful!")
    return True

def lint_backend():
    """백엔드 린트"""
    print("\n🔍 BACKEND LINTING")
    print("="*60)

    backend_dir = Path("backend")

    print("\n1️⃣ Checking code quality with flake8...")
    result = run_command(
        ["python3", "-m", "flake8", "app.py", "services/", "models/", "api/", "--max-line-length=120"],
        cwd=backend_dir
    )

    if result != 0:
        print("⚠️  Linting issues found (non-blocking)")
    else:
        print("✅ Code quality check passed!")

    return True

def check_imports():
    """임포트 확인"""
    print("\n📦 CHECKING IMPORTS")
    print("="*60)

    backend_dir = Path("backend")

    print("\n1️⃣ Checking Python imports...")
    result = run_command(
        ["python3", "-c", "from app import app; print('✅ Backend imports OK')"],
        cwd=backend_dir
    )

    if result != 0:
        print("❌ Backend import check failed!")
        return False

    return True

def main():
    """메인 테스트 실행"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  US Power Grid Dashboard - Integration Tests".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")

    results = {
        "Backend Imports": check_imports(),
        "Backend Tests": test_backend(),
        "Backend Linting": lint_backend(),
        "Frontend Tests": test_frontend(),
        "Frontend Build": build_frontend(),
    }

    # 결과 요약
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + "  TEST SUMMARY".center(58) + "║")
    print("║" + "="*58 + "║")

    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"║ {test_name:<40} {status:>16} ║")

    print("╚" + "="*58 + "╝")

    all_passed = all(results.values())

    if all_passed:
        print("\n🎉 All tests passed successfully!\n")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the output above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
