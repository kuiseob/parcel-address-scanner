# 📦 택배 주소 스캔 시스템 - Release Guide

## 🚀 다운로드 방법

### Windows EXE 파일 (권장 - 설치 불필요)

#### 방법 1: GitHub Releases에서 다운로드
1. GitHub 저장소 방문: https://github.com/kuiseob/parcel-address-scanner
2. **Releases** 탭 클릭
3. 최신 Release에서 `택배주소스캔시스템.exe` 다운로드
4. 파일을 더블클릭하여 실행

#### 방법 2: 최신 Release 직접 링크
```
https://github.com/kuiseob/parcel-address-scanner/releases/latest
```

---

## 📋 설치 및 실행

### EXE 파일 (Windows)

**최소 요구사항:**
- Windows 10/11 (또는 그 이상)
- 500MB 여유 공간
- USB 웹캠 (선택사항)

**실행 방법:**
1. `택배주소스캔시스템.exe` 파일 다운로드
2. 원하는 위치에 저장 (예: Desktop, Documents)
3. 파일을 더블클릭하여 실행
4. 첫 실행 시 카메라/프린터 권한 설정
5. 준비 완료!

**참고:**
- EXE 파일 크기: 약 200-300MB (모든 의존성 포함)
- 설치 과정 없음 (standalone executable)
- Python 설치 불필요

---

### Python 소스 코드로 실행

Python 개발자 또는 커스터마이징이 필요한 경우:

#### 1. Python 설치
- Python 3.8 이상 필요
- https://www.python.org/downloads/ 에서 다운로드

#### 2. 프로젝트 다운로드
```bash
# Git 사용
git clone https://github.com/kuiseob/parcel-address-scanner.git
cd parcel-address-scanner

# 또는 ZIP 다운로드
# GitHub에서 Code → Download ZIP
```

#### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

#### 4. 프로그램 실행
```bash
python main.py
```

---

## 🔧 EXE 파일 직접 빌드 (선택사항)

Windows 환경에서 직접 EXE를 빌드하려면:

#### 1. 준비
```bash
# Python 3.8+ 확인
python --version

# 저장소 클론
git clone https://github.com/kuiseob/parcel-address-scanner.git
cd parcel-address-scanner
```

#### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

#### 3. EXE 생성
```bash
python build_windows_exe.py
```

#### 4. 완료
- EXE 파일 위치: `dist\택배주소스캔시스템.exe`
- 파일 크기: 약 200-300MB

---

## 📚 사용자 매뉴얼

**PDF 매뉴얼**: `택배주소스캔시스템_사용자매뉴얼.pdf`

주요 내용:
- ✅ 시스템 요구사항
- ✅ 상세 설치 가이드
- ✅ 각 탭별 사용법
- ✅ 데이터 관리 방법
- ✅ 문제 해결 (FAQ)
- ✅ 기술 지원

---

## 🐛 문제 해결

### EXE 실행이 안 됨
```
→ Windows Defender가 차단했을 수 있습니다.
→ 설정 > 보안 및 개인정보 > 바이러스 및 위협 방지
→ 차단된 앱 관리 > "실행 안 함" 제거
```

### 한글이 깨짐
```
→ EXE 버전을 사용하면 자동으로 해결됩니다
→ Python 버전에서는 맑은 고딕 폰트 필요
```

### 카메라가 작동 안 함
```
→ 설정 > 프라이버시 > 카메라 권한 확인
→ 다른 프로그램이 카메라를 사용하지 않는지 확인
→ 웹캠 드라이버 업데이트
```

---

## 📊 버전 정보

### 최신 버전: v2.0.2

| 버전 | 날짜 | 변경사항 |
|------|------|---------|
| v2.0.2 | 2026-06-14 | 의존성 수정, EXE 빌드 안정화 |
| v2.0.1 | 2026-06-14 | GitHub Actions 업데이트 |
| v2.0.0 | 2026-06-14 | 첫 공개 릴리스 |

---

## 🔄 업데이트 확인

새 버전이 있으면 GitHub Releases 페이지에 공지됩니다.

**릴리스 확인:**
- https://github.com/kuiseob/parcel-address-scanner/releases

---

## 💬 피드백 & 지원

### 버그 리포트
- GitHub Issues: https://github.com/kuiseob/parcel-address-scanner/issues

### 기능 요청
- GitHub Discussions에서 논의

### 소스 코드
- https://github.com/kuiseob/parcel-address-scanner

---

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

## 🎓 기술 정보

### 포함된 기능
- ✅ 카메라 실시간 스캔
- ✅ AI 자동 인식 (EasyOCR)
- ✅ SQLite 데이터베이스
- ✅ QR코드 & 바코드 생성
- ✅ Xprinter 라벨 인쇄

### 기술 스택
- **언어**: Python 3.8+
- **GUI**: tkinter
- **OCR**: EasyOCR
- **데이터베이스**: SQLite3
- **이미지 처리**: Pillow, OpenCV
- **바코드**: qrcode, python-barcode

---

## 🗂️ 데이터 저장 위치

EXE 실행 폴더에 자동으로 생성됩니다:

```
프로그램 폴더/
├── parcel_database.db     (SQLite 데이터베이스)
├── 주소록.xlsx             (Excel 파일)
└── barcodes/              (생성된 바코드/QR 이미지)
```

---

## ⏱️ 성능 지표

| 작업 | 소요 시간 |
|------|----------|
| 카메라 스캔 | 2-3초 |
| 정보 분석 | <100ms |
| DB 저장 | <50ms |
| QR/바코드 생성 | 400ms |
| 라벨 프린트 | 5초 |
| **전체 처리** | **~7초** |

---

## 📞 연락처

개발자: Claude AI (Anthropic)

---

**행운을 빕니다! 📦✨**
