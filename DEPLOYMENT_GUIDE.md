# 🚀 배포 및 GitHub 가이드

이 문서는 **택배 주소 스캔 시스템**을 Windows EXE로 빌드하고 GitHub에 배포하는 완전한 가이드입니다.

---

## 📋 목차

1. [Windows EXE 생성](#windows-exe-생성)
2. [GitHub 리포지토리 설정](#github-리포지토리-설정)
3. [GitHub에 푸시](#github에-푸시)
4. [배포 및 공유](#배포-및-공유)
5. [트러블슈팅](#트러블슈팅)

---

## Windows EXE 생성

### 필수 요구사항

- ✅ Windows 10/11
- ✅ Python 3.8+ (설치 필요)
- ✅ pip (Python 패키지 관리자)

### 단계별 가이드

#### 1단계: Python 설치 확인

```powershell
# PowerShell 또는 Command Prompt에서
python --version
pip --version
```

설치되지 않았다면: https://python.org 에서 다운로드

#### 2단계: 프로젝트 다운로드

```powershell
# GitHub에서 클론 (나중에 푸시한 후)
git clone https://github.com/YOUR_USERNAME/parcel-address-scanner.git
cd parcel-address-scanner
```

또는 처음부터 생성하는 경우, 이 폴더 사용.

#### 3단계: 자동 빌드 (권장)

```powershell
# 현재 폴더에서
build_exe.bat
```

**자동으로 수행됨:**
- ✅ 의존성 설치
- ✅ PyInstaller 실행
- ✅ EXE 생성

**결과:**
```
dist\택배주소스캔시스템.exe
```

#### 4단계: EXE 테스트

```powershell
# 생성된 EXE 실행
.\dist\택배주소스캔시스템.exe
```

---

## GitHub 리포지토리 설정

### GitHub 계정 준비

1. https://github.com 방문
2. 아직 계정이 없다면 **Sign up** 클릭
3. 이메일, 사용자명, 비밀번호 입력
4. 이메일 인증 완료

### 리포지토리 생성

1. GitHub.com 로그인
2. 우측 상단 **"+"** 아이콘 → **New repository**
3. 설정:
   ```
   Repository name: parcel-address-scanner
   Description: 택배 주소 자동 스캔 및 배송 자동화 시스템
   Visibility: Public
   ☐ Add a README file (체크 해제)
   ☐ Add .gitignore (체크 해제)
   ☐ Choose a license (체크 해제)
   ```
4. **Create repository** 클릭

생성된 리포지토리 주소:
```
https://github.com/YOUR_USERNAME/parcel-address-scanner
```

---

## GitHub에 푸시

### 방법 1: 개인 액세스 토큰 (Windows)

#### 토큰 생성

1. GitHub.com 로그인
2. 우측 상단 프로필 → **Settings**
3. **Developer settings** → **Personal access tokens**
4. **Tokens (classic)** → **Generate new token (classic)**
5. 설정:
   ```
   Token name: parcel-scanner-token
   Expiration: 90 days
   Scopes: repo (전체 선택)
   ```
6. **Generate token** 클릭
7. **토큰 복사** (다시 보이지 않으니 저장해두기!)

#### 푸시 명령어

```powershell
cd /Users/kuiseob/parcel-address-scanner

# 원격 저장소 추가
git remote add origin https://github.com/YOUR_USERNAME/parcel-address-scanner.git

# 푸시
git push -u origin main

# 입력 프롬프트:
# Username: YOUR_USERNAME
# Password: (위에서 복사한 토큰)
```

### 방법 2: SSH 키 (macOS/Linux)

```bash
# SSH 키 생성 (처음 한 번만)
ssh-keygen -t ed25519 -C "your.email@example.com"

# 공개 키 복사
cat ~/.ssh/id_ed25519.pub

# GitHub에 등록:
# Settings → SSH and GPG keys → New SSH key
# (복사한 공개 키 붙여넣기)

# 원격 저장소 추가
git remote add origin git@github.com:YOUR_USERNAME/parcel-address-scanner.git

# 푸시
git push -u origin main
```

### 푸시 확인

GitHub 리포지토리 페이지 새로고침:
```
✅ 모든 파일 표시됨
✅ README.md 자동 표시
✅ 코드 미리보기 가능
```

---

## 배포 및 공유

### 1단계: Windows EXE 업로드

#### GitHub Releases에서 배포

1. 리포지토리 페이지 → **Releases** 탭
2. **Create a new release**
3. 설정:
   ```
   Tag version: v2.1
   Release title: v2.1 - PHASE 1-2 완료
   Release notes:
   
   ## 주요 기능
   - ✅ 우편번호 자동 추출
   - ✅ 수취인/전화/주소 분리
   - ✅ SQLite 데이터베이스
   - ✅ QR/바코드 자동 생성
   - ✅ Xprinter 라벨 인쇄
   
   ## 설치 방법
   1. 택배주소스캔시스템.exe 다운로드
   2. 더블클릭하여 실행
   
   ## 시스템 요구사항
   - Windows 10/11
   - USB 카메라 (선택사항)
   - 2GB RAM 이상
   ```
4. **Choose Files** → `dist\택배주소스캔시스템.exe` 선택
5. **Publish release** 클릭

#### 직접 다운로드 링크

```
https://github.com/YOUR_USERNAME/parcel-address-scanner/releases/download/v2.1/택배주소스캔시스템.exe
```

### 2단계: 문서 정리

#### 필수 문서 확인

```
✅ README.md          - 프로젝트 설명
✅ INSTALL.md         - 설치 가이드
✅ QUICK_START.md     - 빠른 시작
✅ BUILD_INSTRUCTIONS.md - 빌드 가이드
✅ GITHUB_PUSH_GUIDE.md  - GitHub 푸시 가이드
```

#### GitHub 저장소 최적화

1. **Topics 추가**
   - Settings → Topics
   - 추가: `python`, `ocr`, `automation`, `barcode`, `shipping`

2. **Description 추가**
   - 리포지토리 상단 Edit
   - "택배 주소 자동 스캔 및 배송 자동화 시스템"

3. **Website 링크** (선택사항)
   - 공식 웹사이트가 있으면 추가

### 3단계: 공유하기

#### 방법 1: GitHub 링크 공유
```
https://github.com/YOUR_USERNAME/parcel-address-scanner
```

#### 방법 2: 다운로드 링크 공유
```
직접 다운로드: https://github.com/YOUR_USERNAME/parcel-address-scanner/releases/download/v2.1/택배주소스캔시스템.exe
```

#### 방법 3: README 링크
```markdown
# 택배 주소 스캔 시스템

[GitHub 저장소](https://github.com/YOUR_USERNAME/parcel-address-scanner)
[최신 버전 다운로드](https://github.com/YOUR_USERNAME/parcel-address-scanner/releases/latest)
```

---

## 트러블슈팅

### EXE 생성 문제

#### Q: "build_exe.bat를 찾을 수 없습니다"
- 파일이 프로젝트 루트 폴더에 있는지 확인
- 폴더 탐색기에서 이동 후 우클릭 → "PowerShell 여기서 열기"

#### Q: "PyInstaller를 찾을 수 없음"
```powershell
pip install pyinstaller
build_exe.bat
```

#### Q: EXE 파일이 너무 큼 (200MB+)
- 정상입니다. EasyOCR과 OpenCV 때문
- 최적화 불가능 (필수 라이브러리)

### GitHub 푸시 문제

#### Q: "fatal: 'origin' does not appear..."
```powershell
git remote add origin https://github.com/YOUR_USERNAME/parcel-address-scanner.git
git push -u origin main
```

#### Q: "authentication failed"
1. 토큰 만료 여부 확인
2. GitHub Settings에서 새 토큰 생성
3. 토큰 복사 후 다시 시도

#### Q: "SSL certificate problem"
```powershell
git config --global http.sslVerify false
git push origin main
```

---

## 📊 완료 체크리스트

### 로컬 준비
- [ ] Windows 10/11 환경
- [ ] Python 3.8+ 설치
- [ ] 프로젝트 폴더 준비
- [ ] `build_exe.bat` 실행
- [ ] EXE 파일 생성 확인

### GitHub 설정
- [ ] GitHub 계정 생성
- [ ] 새 리포지토리 생성
- [ ] 개인 액세스 토큰 생성 (또는 SSH 키)
- [ ] Git 원격 저장소 연결
- [ ] 첫 푸시 완료

### 배포
- [ ] EXE 파일 업로드
- [ ] Releases 페이지 작성
- [ ] README 및 문서 확인
- [ ] 다운로드 링크 테스트
- [ ] 친구/동료와 공유

---

## 🎉 완료!

축하합니다! 😊

이제 당신의 프로젝트는:
- ✅ **GitHub에 공개됨**
- ✅ **Windows EXE로 배포 가능**
- ✅ **누구나 다운로드 가능**
- ✅ **사용자가 쉽게 실행 가능**

---

## 📞 다음 단계

1. **PHASE 3 개발** (2주)
   - 이미지 업로드 기능
   - PDF 송장 양식

2. **PHASE 4 개발** (2주)
   - LOT 추적 시스템
   - 택배사 API 연동

3. **커뮤니티 피드백**
   - GitHub Issues로 버그 보고
   - Pull Requests로 기여 받기
   - 사용자 피드백 수집

---

**최종 수정**: 2026-06-09
**버전**: v2.1
**상태**: 배포 준비 완료 ✅
