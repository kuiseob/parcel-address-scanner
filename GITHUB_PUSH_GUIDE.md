# 🚀 GitHub 푸시 가이드

로컬 저장소를 GitHub에 푸시하는 방법을 단계별로 설명합니다.

---

## 준비물

- GitHub 계정 (https://github.com/signup)
- Git 설치 (이미 완료됨)
- 개인 액세스 토큰 또는 SSH 키

---

## 방법 1: 개인 액세스 토큰으로 푸시 (권장 - Windows)

### Step 1: GitHub 개인 액세스 토큰 생성

1. GitHub.com 로그인
2. 우측 상단 프로필 → **Settings**
3. 좌측 메뉴 → **Developer settings**
4. **Personal access tokens** → **Tokens (classic)**
5. **Generate new token (classic)** 클릭
6. 설정:
   - Token name: `parcel-scanner-token`
   - Expiration: `90 days` (또는 원하는 기간)
   - Scopes: `repo` (전체 선택)
7. **Generate token** 클릭
8. **토큰 복사 후 저장** (다시 볼 수 없음!)

### Step 2: 새 GitHub 리포지토리 생성

1. GitHub.com 로그인
2. 우측 상단 "+" → **New repository**
3. Repository 설정:
   - **Repository name**: `parcel-address-scanner`
   - **Description**: `택배 주소 자동 스캔 및 배송 자동화 시스템`
   - **Visibility**: `Public`
   - ✅ Add a README file - **체크 해제** (이미 있음)
   - ✅ Add .gitignore - **체크 해제** (이미 있음)
4. **Create repository** 클릭

### Step 3: 리모트 저장소 연결

```bash
cd /Users/kuiseob/parcel-address-scanner

# 원격 저장소 추가 (YOUR_USERNAME을 자신의 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/parcel-address-scanner.git

# 원격 저장소 확인
git remote -v
```

### Step 4: 푸시하기

```bash
# main 브랜치 푸시
git push -u origin main

# 프롬프트에서 GitHub 사용자명 입력
# Username: YOUR_USERNAME

# 프롬프트에서 토큰 입력 (비밀번호로 사용)
# Password: (생성한 토큰 붙여넣기)
```

---

## 방법 2: SSH 키로 푸시 (권장 - macOS/Linux)

### Step 1: SSH 키 생성 (처음 한 번만)

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"

# 또는 (구형 시스템)
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"
```

프롬프트:
```
> Enter file in which to save the key: [Press enter]
> Enter passphrase: [암호 입력 (선택사항)]
> Enter same passphrase again: [다시 입력]
```

### Step 2: GitHub에 공개 키 등록

1. SSH 공개 키 복사:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. GitHub 등록:
   - GitHub.com → Settings → **SSH and GPG keys**
   - **New SSH key** 클릭
   - Title: `MacBook` (또는 컴퓨터명)
   - Key: (위에서 복사한 공개 키 붙여넣기)
   - **Add SSH key** 클릭

### Step 3: SSH 연결 테스트

```bash
ssh -T git@github.com
```

성공 메시지:
```
Hi YOUR_USERNAME! You've successfully authenticated...
```

### Step 4: SSH를 사용하여 원격 저장소 연결

```bash
git remote add origin git@github.com:YOUR_USERNAME/parcel-address-scanner.git
```

### Step 5: 푸시하기

```bash
git push -u origin main
```

---

## 완전한 단계별 예시

### 시나리오: GitHub 계정이 `john-doe`, 토큰이 `ghp_ABC123...`

```bash
# 1. 디렉토리 이동
cd /Users/kuiseob/parcel-address-scanner

# 2. Git 상태 확인
git status
# Output: On branch main, nothing to commit

# 3. 원격 저장소 추가
git remote add origin https://github.com/john-doe/parcel-address-scanner.git

# 4. 푸시
git push -u origin main

# 프롬프트에서 입력:
# Username for 'https://github.com': john-doe
# Password for 'https://john-doe@github.com': ghp_ABC123...
```

완료! 🎉

---

## 업데이트 푸시하기

코드를 수정한 후:

```bash
# 변경 사항 확인
git status

# 모든 파일 스테이징
git add .

# 커밋
git commit -m "설명: 어떤 변경을 했는지"

# 푸시
git push origin main
```

---

## 💡 팁

### Credential 자동 저장

Windows에서 매번 입력 없이 자동으로 저장:

```bash
git config --global credential.helper wincred
```

macOS:

```bash
git config --global credential.helper osxkeychain
```

### 토큰 관리

토큰이 유출되었다면 즉시 GitHub에서 revoke:
- Settings → Developer settings → Personal access tokens → Delete

---

## 🆘 문제 해결

### Q: "fatal: 'origin' does not appear to be a git repository"

해결:
```bash
git remote -v

# 만약 아무 것도 출력되지 않으면:
git remote add origin https://github.com/YOUR_USERNAME/parcel-address-scanner.git
```

### Q: "fatal: The current branch main has no upstream branch"

해결:
```bash
git push -u origin main
```

### Q: "authentication failed"

해결:
1. 토큰/SSH 키 확인
2. 토큰 만료되었다면 새 토큰 생성
3. SSH 키 권한 확인:
   ```bash
   chmod 600 ~/.ssh/id_ed25519
   ```

### Q: "Please tell me who you are"

해결:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 📊 GitHub 저장소 완성 후

### 1. README 확인
- GitHub 리포지토리 페이지에서 자동으로 표시됨

### 2. Releases 등록
- "Releases" 탭 → "Create a new release"
- Windows EXE 파일 업로드
- 설명 작성

### 3. Topics 추가
- Settings → Topics
- 추가: `python`, `ocr`, `barcode`, `shipping`, `automation`

### 4. Stars 받기
- 친구/동료에게 공유
- 유용하면 ⭐ 클릭하도록 권유

---

## ✅ 완료 체크리스트

- [ ] GitHub 계정 생성
- [ ] 개인 액세스 토큰 또는 SSH 키 생성
- [ ] 새 GitHub 리포지토리 생성
- [ ] 원격 저장소 연결 (`git remote add origin`)
- [ ] 첫 푸시 완료 (`git push -u origin main`)
- [ ] GitHub 리포지토리 확인
- [ ] README 및 문서 표시 확인
- [ ] Windows EXE 생성 및 업로드
- [ ] Releases 페이지 작성

---

## 🔗 유용한 링크

- [GitHub 개인 액세스 토큰 가이드](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub SSH 설정 가이드](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Git 설명서](https://git-scm.com/doc)
- [GitHub 시작 가이드](https://guides.github.com/activities/hello-world/)

---

**최종 수정**: 2026-06-09
**버전**: v2.1
