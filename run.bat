@echo off
chcp 65001 >nul
echo.
echo ==========================================
echo   택배 주소 스캔 시스템 시작
echo ==========================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ==========================================
    echo   오류가 발생했습니다.
    echo   아래 명령어로 의존성을 설치하세요:
    echo   pip install -r requirements.txt
    echo ==========================================
    pause
)
