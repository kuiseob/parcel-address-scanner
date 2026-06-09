@echo off
REM ============================================
REM  택배 주소 스캔 시스템 - Windows EXE 빌드
REM ============================================

chcp 65001 >nul
echo.
echo ==========================================
echo   EXE 파일 생성 중...
echo ==========================================
echo.

REM Python 버전 확인
python --version

REM 의존성 설치
echo 의존성 설치 중...
pip install -r requirements.txt

REM 기존 빌드 폴더 정리
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "택배 주소 스캔 시스템.spec" del "택배 주소 스캔 시스템.spec"

REM PyInstaller 실행
echo.
echo EXE 생성 중... (약 2-3분 소요)
echo.

pyinstaller --onefile ^
    --windowed ^
    --name "택배주소스캔시스템" ^
    --icon=NONE ^
    --add-data "barcodes:barcodes" ^
    --hidden-import=cv2 ^
    --hidden-import=easyocr ^
    --hidden-import=qrcode ^
    --hidden-import=barcode ^
    --hidden-import=pyusb ^
    main.py

echo.
echo ==========================================
echo   EXE 파일 생성 완료!
echo ==========================================
echo.
echo 생성 위치: dist\택배주소스캔시스템.exe
echo.
pause
