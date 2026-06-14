#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
택배 주소 스캔 시스템 - 사용자 매뉴얼 PDF 생성
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

def create_user_manual():
    """사용자 매뉴얼 PDF 생성"""

    # PDF 생성
    filename = "택배주소스캔시스템_사용자매뉴얼.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm,
        title="택배 주소 스캔 시스템 사용자 매뉴얼",
        author="Claude AI"
    )

    # 스타일 정의
    styles = getSampleStyleSheet()

    # 한글 폰트를 지원하는 커스텀 스타일
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#1f4788'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=HexColor('#1f4788'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=HexColor('#2e5c8a'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )

    # 문서 내용
    story = []

    # ===== 제목 페이지 =====
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("📦 택배 주소 스캔 시스템", title_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("사용자 매뉴얼 v2.0", title_style))
    story.append(Spacer(1, 1*cm))

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=6,
        textColor=HexColor('#666666')
    )

    story.append(Paragraph("PHASE 1 & 2 완료", subtitle_style))
    story.append(Paragraph(f"최종 수정: {datetime.now().strftime('%Y년 %m월 %d일')}", subtitle_style))
    story.append(Spacer(1, 2*cm))

    story.append(Paragraph("주요 기능", heading2_style))
    features = [
        "✓ 카메라로 택배 주소 실시간 스캔",
        "✓ AI 자동 인식 (우편번호/수취인/전화번호)",
        "✓ SQLite 데이터베이스 저장",
        "✓ QR코드 & 바코드 자동 생성",
        "✓ Xprinter 라벨프린터 연동",
    ]

    for feature in features:
        story.append(Paragraph(feature, normal_style))

    story.append(PageBreak())

    # ===== 목차 =====
    story.append(Paragraph("목차", heading1_style))
    story.append(Spacer(1, 0.5*cm))

    toc_items = [
        "1. 시스템 요구사항",
        "2. 설치 방법",
        "3. 프로그램 시작",
        "4. 각 탭별 사용 방법",
        "5. 데이터 관리",
        "6. 문제 해결",
        "7. FAQ",
        "8. 기술 지원",
    ]

    for item in toc_items:
        story.append(Paragraph(item, normal_style))

    story.append(PageBreak())

    # ===== 1. 시스템 요구사항 =====
    story.append(Paragraph("1. 시스템 요구사항", heading1_style))

    story.append(Paragraph("하드웨어 요구사항", heading2_style))
    hw_data = [
        ["항목", "최소 사양"],
        ["CPU", "Intel Core i5 이상"],
        ["RAM", "4GB 이상"],
        ["저장공간", "500MB 이상 여유공간"],
        ["카메라", "USB 웹캠 (선택사항)"],
        ["프린터", "Xprinter (선택사항)"],
    ]

    hw_table = Table(hw_data, colWidths=[2*cm, 10*cm])
    hw_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), ['white', HexColor('#f9f9f9')]),
    ]))
    story.append(hw_table)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("소프트웨어 요구사항", heading2_style))
    story.append(Paragraph("• Windows 10/11 이상 (다른 OS도 지원 가능)", normal_style))
    story.append(Paragraph("• Python 3.8 이상 (exe 버전 사용 시 불필요)", normal_style))
    story.append(Paragraph("• 카메라 사용 시 웹캠 드라이버", normal_style))

    story.append(PageBreak())

    # ===== 2. 설치 방법 =====
    story.append(Paragraph("2. 설치 방법", heading1_style))

    story.append(Paragraph("Windows EXE 버전 (권장)", heading2_style))
    story.append(Paragraph("가장 간단한 방법입니다.", normal_style))
    story.append(Spacer(1, 0.3*cm))

    exe_steps = [
        "1. 다운로드: GitHub에서 '택배주소스캔시스템.exe' 파일을 다운로드합니다.",
        "2. 실행: 다운로드한 exe 파일을 더블클릭하면 자동으로 시작됩니다.",
        "3. 설정: 첫 실행 시 카메라와 프린터 권한을 설정합니다.",
    ]

    for step in exe_steps:
        story.append(Paragraph(step, normal_style))

    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("Python 소스 버전", heading2_style))
    story.append(Paragraph("개발자나 고급 사용자용입니다.", normal_style))
    story.append(Spacer(1, 0.3*cm))

    python_steps = [
        "1. Python 설치: Python 3.8 이상을 설치합니다.",
        "2. Git Clone: git clone https://github.com/...parcel-address-scanner.git",
        "3. 의존성 설치: pip install -r requirements.txt",
        "4. 실행: python main.py",
    ]

    for step in python_steps:
        story.append(Paragraph(step, normal_style))

    story.append(PageBreak())

    # ===== 3. 프로그램 시작 =====
    story.append(Paragraph("3. 프로그램 시작", heading1_style))

    story.append(Paragraph("프로그램 실행", heading2_style))
    story.append(Paragraph("exe 파일 또는 python main.py 명령으로 프로그램을 시작합니다.", normal_style))
    story.append(Paragraph("프로그램이 시작되면 아래와 같은 초기 화면이 나타납니다:", normal_style))
    story.append(Spacer(1, 0.3*cm))

    init_features = [
        "• 6개 탭이 있는 메인 윈도우",
        "• 하단의 상태바 (현재 상태 표시)",
        "• 탭 1: 카메라 스캔 (기본 탭)",
    ]

    for feature in init_features:
        story.append(Paragraph(feature, normal_style))

    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("카메라 권한 설정", heading2_style))
    story.append(Paragraph("Windows에서 처음 실행할 때 카메라 권한을 요청받습니다.", normal_style))
    story.append(Paragraph("'허용'을 클릭하면 카메라에 접근할 수 있습니다.", normal_style))

    story.append(PageBreak())

    # ===== 4. 각 탭별 사용 방법 =====
    story.append(Paragraph("4. 각 탭별 사용 방법", heading1_style))

    # Tab 1
    story.append(Paragraph("탭 1: 카메라 스캔 📷", heading2_style))
    story.append(Paragraph("택배 주소를 카메라로 스캔하는 기본 기능입니다.", normal_style))
    story.append(Spacer(1, 0.3*cm))

    tab1_steps = [
        "1. [카메라 시작] 버튼 클릭 → 웹캠이 활성화됩니다.",
        "2. 택배 상자의 주소 라벨을 카메라에 맞춥니다.",
        "3. [스캔] 버튼 클릭 → AI가 텍스트를 자동으로 인식합니다.",
        "4. 인식된 정보 확인:",
        "   - 우편번호 (XXXXX-XXXX)",
        "   - 수취인명",
        "   - 전화번호",
        "   - 주소",
        "5. [DB에 저장] 또는 [Excel에 저장] 선택",
    ]

    for step in tab1_steps:
        story.append(Paragraph(step, normal_style))

    story.append(Spacer(1, 0.5*cm))

    # Tab 2
    story.append(Paragraph("탭 2: 주소록 관리 📋", heading2_style))
    story.append(Paragraph("저장된 주소들을 관리합니다.", normal_style))
    story.append(Spacer(1, 0.3*cm))

    tab2_features = [
        "• 모든 저장된 주소 목록 표시",
        "• 주소 선택하여 삭제 가능",
        "• 배치 삭제 (여러 개 동시 삭제)",
        "• CSV로 내보내기",
    ]

    for feature in tab2_features:
        story.append(Paragraph(feature, normal_style))

    story.append(Spacer(1, 0.5*cm))

    # Tab 3
    story.append(Paragraph("탭 3: 주소 검색 🔍", heading2_style))
    story.append(Paragraph("저장된 주소를 검색합니다.", normal_style))
    story.append(Spacer(1, 0.3*cm))

    tab3_features = [
        "• 수취인명으로 검색 (예: 홍길동)",
        "• 전화번호로 검색 (예: 010-1234-5678)",
        "• 주소로 검색 (예: 서울시 강남구)",
        "• 실시간 검색 결과 표시",
    ]

    for feature in tab3_features:
        story.append(Paragraph(feature, normal_style))

    story.append(PageBreak())

    # Tab 4
    story.append(Paragraph("탭 4: 통계 📊", heading2_style))
    story.append(Paragraph("저장된 데이터의 통계 정보를 표시합니다.", normal_style))
    story.append(Spacer(1, 0.3*cm))

    tab4_stats = [
        "• 총 주소 개수",
        "• 총 송장 개수",
        "• 총 LOT 개수",
    ]

    for stat in tab4_stats:
        story.append(Paragraph(stat, normal_style))

    story.append(Spacer(1, 0.5*cm))

    # Tab 5
    story.append(Paragraph("탭 5: 바코드/QR 생성 📊", heading2_style))
    story.append(Paragraph("선택한 주소에 대한 바코드와 QR코드를 생성합니다.", normal_style))
    story.append(Spacer(1, 0.3*cm))

    tab5_features = [
        "• QR코드 생성 (송장 정보 인코딩)",
        "• Code128 바코드 생성",
        "• 라벨 이미지 자동 생성",
        "• 미리보기 제공",
    ]

    for feature in tab5_features:
        story.append(Paragraph(feature, normal_style))

    story.append(Spacer(1, 0.5*cm))

    # Tab 6
    story.append(Paragraph("탭 6: 라벨 프린터 🖨️", heading2_style))
    story.append(Paragraph("Xprinter를 사용하여 라벨을 인쇄합니다.", normal_style))
    story.append(Spacer(1, 0.3*cm))

    tab6_features = [
        "• 프린터 자동 검색",
        "• 프린터 상태 확인",
        "• 테스트 인쇄",
        "• 라벨 인쇄",
        "• 용지 자동 절단",
    ]

    for feature in tab6_features:
        story.append(Paragraph(feature, normal_style))

    story.append(PageBreak())

    # ===== 5. 데이터 관리 =====
    story.append(Paragraph("5. 데이터 관리", heading1_style))

    story.append(Paragraph("데이터 저장 방식", heading2_style))

    storage_data = [
        ["방식", "설명"],
        ["SQLite", "프로그램이 자동으로 관리하는 데이터베이스"],
        ["Excel", "Excel 파일로 자동 생성 (주소록.xlsx)"],
        ["CSV", "주소록 탭에서 내보낼 수 있음"],
    ]

    storage_table = Table(storage_data, colWidths=[3*cm, 9*cm])
    storage_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), ['white', HexColor('#f9f9f9')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(storage_table)

    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("데이터 위치", heading2_style))
    story.append(Paragraph("프로그램 실행 폴더에 자동으로 생성됩니다:", normal_style))

    file_locations = [
        "• parcel_database.db → SQLite 데이터베이스",
        "• 주소록.xlsx → Excel 파일",
        "• barcodes/ → 생성된 바코드/QR 이미지",
    ]

    for loc in file_locations:
        story.append(Paragraph(loc, normal_style))

    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("백업 방법", heading2_style))
    story.append(Paragraph("중요한 데이터는 정기적으로 백업하세요:", normal_style))

    backup_steps = [
        "1. parcel_database.db 파일 복사",
        "2. 주소록.xlsx 파일 복사",
        "3. 안전한 장소에 저장",
    ]

    for step in backup_steps:
        story.append(Paragraph(step, normal_style))

    story.append(PageBreak())

    # ===== 6. 문제 해결 =====
    story.append(Paragraph("6. 문제 해결", heading1_style))

    story.append(Paragraph("카메라가 작동하지 않음", heading2_style))

    camera_solutions = [
        "1. Windows 설정에서 카메라 권한 확인",
        "   설정 > 개인정보 및 보안 > 카메라",
        "2. 다른 프로그램에서 카메라를 사용하지 않는지 확인",
        "3. 웹캠 드라이버 업데이트",
        "4. 프로그램 재시작",
    ]

    for solution in camera_solutions:
        story.append(Paragraph(solution, normal_style))

    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("한글이 깨짐", heading2_style))
    story.append(Paragraph("• 이는 시스템 폰트 설정 문제입니다.", normal_style))
    story.append(Paragraph("• exe 버전을 사용하면 자동으로 해결됩니다.", normal_style))
    story.append(Paragraph("• Python 버전에서는 맑은 고딕 폰트가 설치되어 있는지 확인하세요.", normal_style))

    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("OCR 인식 실패", heading2_style))

    ocr_solutions = [
        "1. 밝은 환경에서 스캔하세요",
        "2. 택배 라벨이 명확하게 보이도록 조정",
        "3. 카메라를 30cm 거리에서 촬영",
        "4. 라벨에 그림자가 지지 않도록 주의",
    ]

    for solution in ocr_solutions:
        story.append(Paragraph(solution, normal_style))

    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("프린터가 인식되지 않음", heading2_style))

    printer_solutions = [
        "1. Xprinter가 USB로 연결되어 있는지 확인",
        "2. 프린터 드라이버가 설치되어 있는지 확인",
        "3. 프로그램 재시작 후 [프린터 검색] 클릭",
        "4. Windows 장치 관리자에서 프린터 확인",
    ]

    for solution in printer_solutions:
        story.append(Paragraph(solution, normal_style))

    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("데이터베이스 오류", heading2_style))

    db_solutions = [
        "1. 프로그램을 완전히 종료합니다.",
        "2. parcel_database.db 파일을 삭제합니다.",
        "3. 프로그램을 다시 시작하면 자동으로 재생성됩니다.",
    ]

    for solution in db_solutions:
        story.append(Paragraph(solution, normal_style))

    story.append(PageBreak())

    # ===== 7. FAQ =====
    story.append(Paragraph("7. FAQ (자주 묻는 질문)", heading1_style))

    faqs = [
        ("Q: 프로그램을 여러 번 실행해도 되나요?",
         "A: 네, 각 실행은 독립적입니다. 다만 동시에 2개 이상 실행하지 않는 것이 좋습니다."),

        ("Q: 주소를 수정할 수 있나요?",
         "A: 현재 버전에서는 수정 기능이 없습니다. 삭제 후 다시 입력하세요."),

        ("Q: 택배사별로 다른 바코드를 만들 수 있나요?",
         "A: 현재는 표준 Code128 바코드만 생성합니다. PHASE 3에서 확대될 예정입니다."),

        ("Q: 인식율을 높일 수 있나요?",
         "A: 카메라 각도, 조명, 거리를 조정하면 인식율이 높아집니다."),

        ("Q: 데이터를 다른 프로그램으로 옮길 수 있나요?",
         "A: 네, Excel 파일 또는 CSV로 내보낼 수 있습니다."),

        ("Q: 인터넷이 필요한가요?",
         "A: 아니요, 완전히 오프라인에서 작동합니다."),
    ]

    for q, a in faqs:
        story.append(Paragraph(q, ParagraphStyle(
            'FAQ_Q',
            parent=styles['Normal'],
            fontSize=11,
            textColor=HexColor('#1f4788'),
            spaceAfter=3,
            fontName='Helvetica-Bold'
        )))
        story.append(Paragraph(a, normal_style))
        story.append(Spacer(1, 0.3*cm))

    story.append(PageBreak())

    # ===== 8. 기술 지원 =====
    story.append(Paragraph("8. 기술 지원", heading1_style))

    story.append(Paragraph("버전 정보", heading2_style))

    version_data = [
        ["항목", "정보"],
        ["프로그램명", "택배 주소 스캔 시스템"],
        ["버전", "v2.0"],
        ["PHASE", "1 & 2 완료"],
        ["개발자", "Claude AI"],
        ["라이선스", "MIT"],
    ]

    version_table = Table(version_data, colWidths=[4*cm, 8*cm])
    version_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), ['white', HexColor('#f9f9f9')]),
    ]))
    story.append(version_table)

    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("지원 방법", heading2_style))

    support_methods = [
        "• 버그 리포트: GitHub Issues에 등록",
        "• 기능 요청: GitHub Discussions에서 논의",
        "• 소스코드: https://github.com/...parcel-address-scanner",
    ]

    for method in support_methods:
        story.append(Paragraph(method, normal_style))

    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("향후 계획", heading2_style))

    future_plans = [
        "• PHASE 3: 이미지 업로드 & PDF 송장 생성",
        "• PHASE 4: LOT 추적 & 택배사 API 연동",
    ]

    for plan in future_plans:
        story.append(Paragraph(plan, normal_style))

    story.append(Spacer(1, 1*cm))

    story.append(Paragraph("감사합니다!", heading2_style))
    story.append(Paragraph("이 프로그램을 사용해주셔서 감사합니다.", normal_style))

    # PDF 생성
    doc.build(story)
    print(f"✅ 사용자 매뉴얼이 생성되었습니다: {filename}")

if __name__ == "__main__":
    create_user_manual()
