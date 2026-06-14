#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows EXE 빌드 스크립트
이 파일을 Windows에서 실행하면 택배주소스캔시스템.exe 파일을 생성합니다.

사용 방법:
1. pip install -r requirements.txt  (PyInstaller 포함)
2. python build_windows_exe.py
3. dist 폴더에서 택배주소스캔시스템.exe 찾기
"""

import PyInstaller.__main__
import os
import sys
import shutil

def build_exe():
    """Windows EXE 빌드"""

    print("=" * 60)
    print("택배 주소 스캔 시스템 - Windows EXE 빌드")
    print("=" * 60)
    print()

    # 기존 빌드 폴더 정리
    print("[1/4] 기존 빌드 폴더 정리 중...")
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  ✓ {folder}/ 제거됨")

    spec_file = "택배주소스캔시스템.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"  ✓ {spec_file} 제거됨")
    print()

    # PyInstaller 실행
    print("[2/4] PyInstaller 실행 중... (약 3-5분 소요)")
    print()

    try:
        PyInstaller.__main__.run([
            '--onefile',
            '--windowed',
            '--name=택배주소스캔시스템',
            '--icon=NONE',
            '--add-data=barcodes:barcodes',
            '--hidden-import=cv2',
            '--hidden-import=easyocr',
            '--hidden-import=qrcode',
            '--hidden-import=barcode',
            '--hidden-import=pyusb',
            '--hidden-import=openpyxl',
            '--hidden-import=PIL',
            'main.py'
        ])
        print()
        print("[3/4] EXE 파일 생성 완료!")
        print()

    except Exception as e:
        print(f"❌ 빌드 실패: {e}")
        sys.exit(1)

    # 생성된 파일 확인
    print("[4/4] 생성된 파일 확인 중...")
    exe_path = os.path.join('dist', '택배주소스캔시스템.exe')

    if os.path.exists(exe_path):
        exe_size = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"  ✓ {exe_path}")
        print(f"  ✓ 파일 크기: {exe_size:.1f} MB")
        print()
        print("=" * 60)
        print("✅ 빌드 완료!")
        print("=" * 60)
        print()
        print(f"생성 위치: {os.path.abspath(exe_path)}")
        print()
        print("다음 단계:")
        print("1. dist\\택배주소스캔시스템.exe 파일을 실행하세요")
        print("2. GitHub에 업로드하거나 배포하세요")
        print()

    else:
        print(f"❌ EXE 파일을 찾을 수 없습니다: {exe_path}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
