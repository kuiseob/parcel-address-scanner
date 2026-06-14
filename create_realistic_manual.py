#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
실제 주소 예제를 포함한 상세 사용자 매뉴얼
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, Color
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from datetime import datetime

def create_realistic_manual():
    """실제 주소 예제를 포함한 상세 매뉴얼"""

    filename = "실제예제_상세매뉴얼.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=1*cm,
        leftMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm,
        title="택배 주소 스캔 시스템 - 실제 예제 매뉴얼",
        author="Claude AI"
    )

    styles = getSampleStyleSheet()

    # 커스텀 스타일
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#0052CC'),
        spaceAfter=4,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=HexColor('#0052CC'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=HexColor('#1f4788'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )

    h3_style = ParagraphStyle(
        'H3',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=HexColor('#2d5aa8'),
        spaceAfter=6,
        spaceBefore=6,
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        leading=14,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )

    example_style = ParagraphStyle(
        'Example',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor('#FFFFFF'),
        spaceAfter=4,
        leftIndent=10,
        rightIndent=10,
        backColor=HexColor('#0052CC'),
        borderColor=HexColor('#0052CC'),
        borderWidth=1,
        borderPadding=8,
        fontName='Courier'
    )

    box_style = ParagraphStyle(
        'Box',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=6,
        leftIndent=15,
        rightIndent=15,
        backColor=HexColor('#F0F5FF'),
        borderColor=HexColor('#0052CC'),
        borderWidth=2,
        borderPadding=10,
        fontName='Helvetica'
    )

    tip_style = ParagraphStyle(
        'Tip',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor('#006400'),
        spaceAfter=8,
        leftIndent=15,
        rightIndent=15,
        backColor=HexColor('#F0FFF0'),
        borderColor=HexColor('#90EE90'),
        borderWidth=1,
        borderPadding=8,
        fontName='Helvetica'
    )

    story = []

    # ===== 제목 페이지 =====
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("📦 택배 주소 스캔 시스템", title_style))
    story.append(Paragraph("실제 예제로 배우는 사용 가이드", title_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("예제 주소: 인천 연수구 해돋이로 107, 2동 1906호",
                          ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=11,
                                       alignment=TA_CENTER, textColor=HexColor('#666666'))))

    story.append(PageBreak())

    # ===== 실제 예제 소개 =====
    story.append(Paragraph("📍 오늘의 예제 주소", h1_style))

    story.append(Paragraph("이 매뉴얼에서 사용할 실제 주소", h2_style))

    real_address_content = (
        "<b>수취인:</b> 홍길동<br/>"
        "<b>기본주소:</b> 인천 연수구 해돋이로 107<br/>"
        "<b>상세주소:</b> 2동 1906호<br/>"
        "<b>우편번호:</b> 21931<br/>"
        "<b>전화번호:</b> 010-1234-5678"
    )
    story.append(Paragraph(real_address_content, box_style))

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("주소 설명", h2_style))
    explanation = (
        "<b>인천 연수구</b>: 경기도 인천광역시 연수구 (도시 및 지역)<br/>"
        "<b>해돋이로 107</b>: 도로명 주소의 도로명과 번호<br/>"
        "<b>2동</b>: 건물의 동(棟) 번호<br/>"
        "<b>1906호</b>: 아파트 또는 오피스텔의 호수<br/>"
        "<b>우편번호 21931</b>: 배송을 위한 지역 코드<br/>"
        "<b>010-1234-5678</b>: 수취인의 휴대폰 번호"
    )
    story.append(Paragraph(explanation, normal_style))

    story.append(PageBreak())

    # ===== 택배 라벨 예제 =====
    story.append(Paragraph("📮 실제 택배 라벨 예제", h1_style))

    story.append(Paragraph("택배 라벨의 모습", h2_style))
    story.append(Paragraph(
        "다음은 우리가 스캔할 실제 택배 라벨의 예제입니다. "
        "대부분의 한국 택배 라벨은 이와 유사한 형식을 가지고 있습니다.",
        normal_style
    ))

    story.append(Spacer(1, 0.2*cm))

    # 라벨 시뮬레이션
    label_data = [
        ["수취인정보", ""],
        ["홍길동", "010-1234-5678"],
        ["인천 연수구 해돋이로 107", ""],
        ["2동 1906호", ""],
        ["우편번호: 21931", ""],
        ["", ""],
        ["배송정보", ""],
        ["송장번호: 1234567890123", "배송사: CJ대한통운"],
        ["상품: 의류", "무게: 2.5kg"],
    ]

    label_table = Table(label_data, colWidths=[8*cm, 4*cm])
    label_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), ['white', HexColor('#F9F9F9')]),
        ('BOX', (0, 0), (-1, -1), 2, HexColor('#000000')),
    ]))
    story.append(label_table)

    story.append(PageBreak())

    # ===== 단계별 스캔 가이드 =====
    story.append(Paragraph("🚀 단계별 스캔 가이드", h1_style))

    story.append(Paragraph("Step 1: 프로그램 시작", h2_style))
    step1 = (
        "parcel_scanner.exe 파일을 더블클릭하여 프로그램을 시작합니다.<br/>"
        "프로그램이 로드되면 카메라 스캔 탭이 기본으로 표시됩니다."
    )
    story.append(Paragraph(step1, normal_style))

    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("Step 2: 카메라 활성화", h2_style))
    step2 = (
        "메인 화면 왼쪽 상단의 [카메라 시작] 버튼을 클릭합니다.<br/>"
        "웹캠이 활성화되면 화면에 실시간 영상이 나타납니다."
    )
    story.append(Paragraph(step2, normal_style))

    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("Step 3: 택배 라벨 준비", h2_style))
    step3 = (
        "<b>올바른 위치:</b><br/>"
        "• 택배 라벨이 화면 중앙에 오도록 배치<br/>"
        "• 카메라에서 약 30cm 거리<br/>"
        "• 라벨이 펴져있고 구겨지지 않은 상태<br/><br/>"
        "<b>우리 예제의 경우:</b><br/>"
        "인천 연수구 해돋이로 107 주소가 명확하게 보이도록 조정"
    )
    story.append(Paragraph(step3, normal_style))

    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("Step 4: 스캔 실행", h2_style))
    step4 = (
        "[스캔] 버튼을 클릭하면 AI가 화면의 텍스트를 인식합니다.<br/>"
        "처리 시간: 약 2-3초"
    )
    story.append(Paragraph(step4, normal_style))

    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("Step 5: 인식 결과 확인", h2_style))
    story.append(Paragraph("스캔 후 다음과 같은 결과가 나타납니다:", normal_style))

    result_data = [
        ["필드", "인식 결과", "상태"],
        ["우편번호", "21931", "✓"],
        ["수취인", "홍길동", "✓"],
        ["전화번호", "010-1234-5678", "✓"],
        ["기본주소", "인천 연수구 해돋이로 107", "✓"],
        ["상세주소", "2동 1906호", "✓"],
    ]

    result_table = Table(result_data, colWidths=[3*cm, 5*cm, 1.5*cm])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#0052CC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), ['white', HexColor('#F9F9F9')]),
    ]))
    story.append(result_table)

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("💡 주의사항", tip_style))
    story.append(Paragraph(
        "• 우편번호는 5자리 + 하이픈 + 4자리(예: 21931-0001) 형식<br/>"
        "• 동 번호와 호수는 상세주소 필드에 저장<br/>"
        "• 모든 정보가 올바르게 인식되었는지 확인 후 저장"
    , normal_style))

    story.append(PageBreak())

    # ===== Step 6: 저장 =====
    story.append(Paragraph("Step 6: 데이터 저장", h2_style))

    story.append(Paragraph("저장 옵션", h3_style))
    save_options = (
        "<b>Option 1: DB에 저장 (권장)</b><br/>"
        "• SQLite 데이터베이스에 저장<br/>"
        "• 나중에 검색 및 관리 가능<br/>"
        "• 중복 자동 방지<br/><br/>"
        "<b>Option 2: Excel에 저장</b><br/>"
        "• Excel 파일(주소록.xlsx)에 저장<br/>"
        "• 다른 프로그램에서 바로 열기 가능"
    )
    story.append(Paragraph(save_options, normal_style))

    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("우리 예제에서는:", h3_style))
    example_save = (
        "[DB에 저장] 버튼을 클릭하면<br/>"
        "인천 연수구 해돋이로 107, 2동 1906호 주소가<br/>"
        "데이터베이스에 저장됩니다."
    )
    story.append(Paragraph(example_save, example_style))

    story.append(PageBreak())

    # ===== 저장된 데이터 확인 =====
    story.append(Paragraph("📋 저장된 데이터 확인", h1_style))

    story.append(Paragraph("주소록 탭에서 확인하기", h2_style))

    story.append(Paragraph("저장 후 [주소록] 탭으로 이동하면 다음과 같이 표시됩니다:", normal_style))

    data_view = [
        ["번호", "수취인", "전화번호", "주소"],
        ["1", "홍길동", "010-1234-5678", "인천 연수구 해돋이로 107, 2동 1906호"],
    ]

    data_table = Table(data_view, colWidths=[1*cm, 2*cm, 3*cm, 6*cm])
    data_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#0052CC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), ['white', HexColor('#F9F9F9')]),
    ]))
    story.append(data_table)

    story.append(PageBreak())

    # ===== 검색 예제 =====
    story.append(Paragraph("🔍 검색 기능 사용하기", h1_style))

    story.append(Paragraph("검색 탭에서 주소 찾기", h2_style))

    story.append(Paragraph("검색 방법 1: 수취인으로 검색", h3_style))
    search1 = (
        "검색창에 '홍길동' 입력<br/>"
        "결과: 인천 연수구 해돋이로 107, 2동 1906호 주소가 표시됨"
    )
    story.append(Paragraph(search1, normal_style))

    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("검색 방법 2: 전화번호로 검색", h3_style))
    search2 = (
        "검색창에 '010-1234' 입력<br/>"
        "결과: 홍길동의 주소가 자동으로 표시됨"
    )
    story.append(Paragraph(search2, normal_style))

    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("검색 방법 3: 주소로 검색", h3_style))
    search3 = (
        "검색창에 '연수구' 또는 '해돋이로' 입력<br/>"
        "결과: 해당 지역의 모든 주소가 표시됨"
    )
    story.append(Paragraph(search3, normal_style))

    story.append(PageBreak())

    # ===== 실제 업무 시나리오 =====
    story.append(Paragraph("💼 실제 업무 시나리오", h1_style))

    story.append(Paragraph("아침에 10개 택배가 도착했을 때", h2_style))

    scenario = (
        "아침 8:00 - 택배 10개 도착 (인천 연수구 해돋이로 107 건물)<br/>"
        "8:05 - 프로그램 시작, 카메라 활성화<br/>"
        "8:10 - 택배 1-5개 스캔 및 저장 (약 35초)<br/>"
        "8:15 - 택배 6-10개 스캔 및 저장 (약 35초)<br/>"
        "8:20 - 전체 주소록 확인<br/>"
        "8:25 - 필요시 CSV 내보내기<br/>"
        "8:30 - 완료 (기존 수동 작업 30분 → 30초 단축!)"
    )
    story.append(Paragraph(scenario, example_style))

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("예상 결과", h3_style))

    result_summary = (
        "<b>저장된 주소 중 일부:</b><br/>"
        "1. 홍길동 / 010-1234-5678 / 인천 연수구 해돋이로 107, 2동 1906호<br/>"
        "2. 김영희 / 010-9876-5432 / 인천 연수구 해돋이로 107, 3동 2001호<br/>"
        "3. 이순신 / 010-5555-6666 / 인천 연수구 해돋이로 109, 1동 1501호<br/>"
        "...<br/>"
        "총 10개 주소 저장 완료"
    )
    story.append(Paragraph(result_summary, box_style))

    story.append(PageBreak())

    # ===== 팁 및 주의사항 =====
    story.append(Paragraph("⚡ 팁 & 주의사항", h1_style))

    story.append(Paragraph("성공적인 스캔을 위한 팁", h2_style))

    tips = [
        ("카메라 거리", "약 30cm 거리에서 라벨 중앙에 초점 맞추기"),
        ("조명", "밝은 환경(창가, 스탠드 옆)에서 스캔하기"),
        ("라벨 상태", "구겨지거나 손상된 라벨은 펴서 스캔하기"),
        ("속도", "급할수록 정확도가 떨어지므로 천천히 스캔하기"),
        ("확인", "저장 전 인식 결과를 반드시 확인하기"),
    ]

    for title, tip in tips:
        story.append(Paragraph(f"<b>{title}:</b> {tip}", normal_style))

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("자주 하는 실수", h2_style))

    mistakes = [
        ("카메라가 너무 가깝다",
         "→ 30cm 정도 떨어져서 전체 라벨이 보이도록 조정"),
        ("어두운 환경에서 스캔",
         "→ 밝은 환경에서 스캔하면 인식률 95% 이상"),
        ("라벨 각도가 비스듬하다",
         "→ 라벨을 수평으로 맞추고 스캔"),
        ("인식 후 확인하지 않고 저장",
         "→ 항상 정보를 확인한 후 저장하기"),
    ]

    for mistake, solution in mistakes:
        story.append(Paragraph(f"❌ {mistake}", normal_style))
        story.append(Paragraph(f"✓ {solution}", tip_style))
        story.append(Spacer(1, 0.15*cm))

    story.append(PageBreak())

    # ===== 요약 =====
    story.append(Paragraph("📌 정리하기", h1_style))

    summary_text = (
        "우리는 인천 연수구 해돋이로 107, 2동 1906호 주소를 예제로<br/>"
        "택배 스캔 시스템의 기본 사용법을 배웠습니다.<br/><br/>"
        "<b>주요 단계 정리:</b><br/>"
        "1️⃣ 프로그램 시작<br/>"
        "2️⃣ 카메라 활성화<br/>"
        "3️⃣ 택배 라벨 준비<br/>"
        "4️⃣ 스캔 실행<br/>"
        "5️⃣ 인식 결과 확인<br/>"
        "6️⃣ 데이터 저장<br/>"
        "7️⃣ 주소록에서 확인<br/><br/>"
        "이제 여러분도 실제 택배를 스캔해볼 준비가 되었습니다!"
    )
    story.append(Paragraph(summary_text, box_style))

    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("행운을 빕니다! 🎊",
                          ParagraphStyle('Closing', parent=styles['Normal'],
                                       fontSize=12, alignment=TA_CENTER,
                                       textColor=HexColor('#0052CC'),
                                       fontName='Helvetica-Bold')))

    # PDF 생성
    doc.build(story)
    print(f"✅ 실제 예제 기반 매뉴얼이 생성되었습니다: {filename}")
    print(f"   (파일명: 실제예제_상세매뉴얼.pdf)")

if __name__ == "__main__":
    create_realistic_manual()
