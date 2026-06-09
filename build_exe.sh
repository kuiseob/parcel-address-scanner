#!/bin/bash

# ============================================
#  택배 주소 스캔 시스템 - macOS/Linux 빌드
# ============================================

echo ""
echo "=========================================="
echo "  EXE 파일 생성 중..."
echo "=========================================="
echo ""

# Python 버전 확인
python3 --version

# 의존성 설치
echo "의존성 설치 중..."
pip3 install -r requirements.txt

# 기존 빌드 폴더 정리
rm -rf build dist *.spec

# PyInstaller 실행
echo ""
echo "EXE 생성 중... (약 2-3분 소요)"
echo ""

pyinstaller --onefile \
    --windowed \
    --name "택배주소스캔시스템" \
    --icon=NONE \
    --add-data "barcodes:barcodes" \
    --hidden-import=cv2 \
    --hidden-import=easyocr \
    --hidden-import=qrcode \
    --hidden-import=barcode \
    --hidden-import=pyusb \
    main.py

echo ""
echo "=========================================="
echo "  EXE 파일 생성 완료!"
echo "=========================================="
echo ""
echo "생성 위치: dist/택배주소스캔시스템"
echo ""
