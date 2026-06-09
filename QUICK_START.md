# 🚀 빠른 시작 가이드

## Windows
```bash
# 1. 의존성 설치 (처음 한 번만)
pip install -r requirements.txt

# 2. 프로그램 실행
run.bat
```
또는 `python main.py`

---

## macOS / Linux
```bash
# 1. 의존성 설치 (처음 한 번만)
pip3 install -r requirements.txt

# 2. 프로그램 실행
python3 main.py
```

---

## 사용 방법 (3단계)

### 1️⃣ 카메라 시작
`[카메라 시작]` 버튼 클릭 → 웹캠 영상 보임

### 2️⃣ 택배 주소 스캔
카메라에 택배를 대고 `[스캔]` 버튼 클릭
- AI가 자동으로 주소를 인식합니다
- 인식된 주소 목록이 나타납니다

### 3️⃣ 주소 저장
원하는 주소를 선택 후 `[주소 추가]` 버튼
- 자동으로 Excel에 저장됩니다
- `[주소록 열기]`로 확인 가능

---

## 특징

✅ **실시간 카메라** - 웹캠으로 직접 스캔
✅ **AI 인식** - EasyOCR + 한글 자동 인식
✅ **중복 방지** - 이미 있는 주소는 자동 제외
✅ **Excel 저장** - 자동 번호, 등록 날짜 기록
✅ **크로스 플랫폼** - Windows, macOS, Linux 모두 지원

---

## 첫 실행 시 주의

⚠️ **첫 실행 때 모델 다운로드 시간 (1-5분)**
- EasyOCR이 한글 인식 모델(100MB) 다운로드
- 이후 실행은 빠릅니다

---

## 문제 해결

**Q: 카메라가 안 보임**
- Windows: 설정 > 프라이버시 > 카메라 권한 확인
- Mac: 시스템 환경설정 > 보안 및 개인정보 > 카메라 권한 확인

**Q: 글자가 깨짐**
- Windows: 이미 설치됨
- Linux: `sudo apt-get install fonts-noto-cjk` 설치

**Q: "ModuleNotFoundError" 나옴**
```bash
pip install -r requirements.txt --upgrade
```

더 자세한 설명은 [INSTALL.md](INSTALL.md)를 보세요.
