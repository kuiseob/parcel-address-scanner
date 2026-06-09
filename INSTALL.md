# 설치 가이드

## Windows 설치 및 실행

### 1단계: Python 설치
- [Python 공식 사이트](https://www.python.org/downloads/)에서 Python 3.8 이상 다운로드
- 설치할 때 **"Add Python to PATH"** 반드시 체크

### 2단계: 프로젝트 다운로드
```bash
# 프로젝트 폴더로 이동
cd C:\Users\사용자이름\Documents  # 또는 원하는 폴더

# 여기에 parcel-address-scanner 폴더 복사
```

### 3단계: 의존성 설치

**Command Prompt (명령 프롬프트) 또는 PowerShell 열기:**

```bash
cd parcel-address-scanner
pip install -r requirements.txt
```

> **주의:** 첫 실행 시 EasyOCR이 한글 모델(약 100MB)을 자동 다운로드합니다. 시간이 걸릴 수 있습니다.

### 4단계: 프로그램 실행

```bash
python main.py
```

또는 **실행 파일 만들기:**

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

생성된 exe 파일은 `dist/main.exe` 에 있습니다.

---

## macOS 설치 및 실행

```bash
# Python 3.8+ 설치 (Homebrew)
brew install python3

# 의존성 설치
cd parcel-address-scanner
pip3 install -r requirements.txt

# 실행
python3 main.py
```

---

## Linux 설치 및 실행

```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip python3-tk

# 의존성 설치
cd parcel-address-scanner
pip3 install -r requirements.txt

# 실행
python3 main.py
```

---

## 문제 해결

### ❌ "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install opencv-python --upgrade
```

### ❌ "카메라를 열 수 없습니다"
- Windows: 설정 > 프라이버시 > 카메라 권한 확인
- Mac: 시스템 환경설정 > 보안 및 개인정보 > 카메라 권한 확인

### ❌ 한글 폰트가 깨짐
- Windows: 이미 설치됨 (맑은 고딕)
- Mac: 자동으로 Apple SD Gothic Neo 사용
- Linux: `sudo apt-get install fonts-noto-cjk` 설치

### ❌ EasyOCR이 느림
첫 실행은 모델 다운로드 때문에 시간이 걸립니다. (1-5분)
이후 실행은 빠릅니다.

---

## 간단한 실행 방법 (Windows)

**run.bat 파일 생성:**
```batch
@echo off
python main.py
pause
```

이 파일을 더블클릭하면 프로그램이 실행됩니다.
