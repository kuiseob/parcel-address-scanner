# 🔨 빌드 및 배포 가이드

## Windows EXE 생성

### 방법 1: 자동 빌드 스크립트 (권장)

1. **PowerShell 또는 Command Prompt 열기**
   - Windows 검색에서 "PowerShell" 검색
   - 또는 "cmd" 입력

2. **프로젝트 폴더로 이동**
   ```powershell
   cd C:\path\to\parcel-address-scanner
   ```

3. **빌드 스크립트 실행**
   ```batch
   build_exe.bat
   ```

4. **완료!**
   - 생성된 EXE: `dist\택배주소스캔시스템.exe`

### 방법 2: 수동 빌드

1. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

2. **PyInstaller 설치**
   ```bash
   pip install pyinstaller
   ```

3. **EXE 생성**
   ```bash
   pyinstaller --onefile --windowed --name "택배주소스캔시스템" main.py
   ```

4. **결과**
   - `dist` 폴더에 `택배주소스캔시스템.exe` 생성

---

## macOS / Linux 바이너리 생성

### macOS

```bash
chmod +x build_exe.sh
./build_exe.sh
```

### Linux

```bash
chmod +x build_exe.sh
./build_exe.sh
```

---

## GitHub 리포지토리 설정

### 1단계: GitHub 계정 확인
- https://github.com 가입 확인

### 2단계: 새 리포지토리 생성
1. GitHub.com 로그인
2. 우측 상단 "+" 아이콘 → "New repository"
3. Repository name: `parcel-address-scanner`
4. Description: `택배 주소 자동 스캔 및 배송 시스템`
5. Public 선택
6. "Create repository" 클릭

### 3단계: Git 초기화 (macOS/Linux 기준)

```bash
cd /Users/kuiseob/parcel-address-scanner

# Git 초기화
git init

# GitHub 원격 저장소 연결
git remote add origin https://github.com/YOUR_USERNAME/parcel-address-scanner.git

# 기본 브랜치를 main으로 설정
git branch -M main

# 모든 파일 스테이징
git add .

# 커밋
git commit -m "Initial commit: PHASE 1-2 완료 (OCR, DB, 바코드, 프린터)"

# 푸시
git push -u origin main
```

---

## ⚙️ PyInstaller 옵션 설명

| 옵션 | 설명 |
|------|------|
| `--onefile` | 모든 파일을 하나의 EXE로 패킹 |
| `--windowed` | 콘솔 창 숨기기 (GUI 앱용) |
| `--name` | EXE 파일명 지정 |
| `--icon` | 아이콘 지정 (ICO 파일) |
| `--add-data` | 추가 데이터 폴더 포함 |
| `--hidden-import` | 숨겨진 import 지정 |

---

## 📦 배포 시 필요 파일

### 최소 필요 파일
```
택배주소스캔시스템.exe     (메인 프로그램)
```

### 선택사항
```
requirements.txt           (개발자용)
README.md                  (사용 설명서)
QUICK_START.md            (빠른 시작)
```

---

## 🚀 배포 옵션

### 옵션 1: 단순 EXE 배포
- 장점: 간단, 빠름, 파일 크기 작음
- 단점: 사용자가 Python 설치 필요 없음 ✓
- **추천**: GitHub Releases에서 제공

### 옵션 2: Installer 생성
```bash
pip install pyinstaller-windows-runtime
```

### 옵션 3: Windows Store
- 장점: 자동 업데이트
- 단점: 복잡한 심사 과정

---

## 📊 빌드 결과 예상

### 파일 크기
```
택배주소스캔시스템.exe : ~250-300MB
(Python + OpenCV + EasyOCR 포함)
```

### 실행 시간
```
첫 실행: ~5초 (EasyOCR 모델 로드)
이후: ~1초
```

---

## 🐛 트러블슈팅

### Q: "PyInstaller를 찾을 수 없음" 오류
```bash
pip install pyinstaller
```

### Q: "cv2 모듈을 찾을 수 없음" 오류
```bash
pip install opencv-python
```

### Q: EXE 파일이 너무 큼 (>300MB)
- 정상입니다. EasyOCR과 OpenCV 때문에 큽니다.
- 최적화: `--onedir` 옵션 사용

### Q: EXE 실행 시 "DLL을 찾을 수 없음"
- 시스템에 Visual C++ Redistributable 설치
- https://support.microsoft.com/ko-kr/help/2977003

---

## 📈 배포 체크리스트

- [ ] 로컬에서 EXE 테스트 완료
- [ ] 모든 기능 작동 확인
- [ ] 에러 메시지 처리 확인
- [ ] GitHub 리포지토리 생성
- [ ] EXE 파일 업로드
- [ ] README 작성
- [ ] Releases 페이지에 EXE 등록
- [ ] 다운로드 링크 확인

---

## 📝 GitHub Releases 등록

1. GitHub 리포지토리 페이지 접속
2. 우측 "Releases" 클릭
3. "Create a new release"
4. Tag version: `v2.1` (또는 원하는 버전)
5. Release title: `v2.1 - PHASE 1-2 완료`
6. Description: 
   ```
   ## 주요 기능
   - ✅ 우편번호 자동 추출
   - ✅ 수취인/전화/주소 분리
   - ✅ SQLite 데이터베이스
   - ✅ QR/바코드 생성
   - ✅ Xprinter 라벨 인쇄
   
   ## 다운로드
   - Windows: 택배주소스캔시스템.exe
   ```
7. "Choose Files to upload" → EXE 파일 선택
8. "Publish release"

---

## 🔗 유용한 링크

- **PyInstaller 문서**: https://pyinstaller.org
- **GitHub**: https://github.com
- **Python.org**: https://python.org

---

**최종 수정**: 2026-06-09
**버전**: v2.1
