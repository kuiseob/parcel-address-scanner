#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 요약 사용자 매뉴얼 생성
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def create_simple_manual():
    """간단한 요약 매뉴얼"""

    filename = "사용자매뉴얼_간단버전.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=1.2*cm,
        leftMargin=1.2*cm,
        topMargin=1.2*cm,
        bottomMargin=1.2*cm,
        title="택배 주소 스캔 시스템 - 간단 사용 가이드",
        author="Claude AI"
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=HexColor('#0052CC'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=HexColor('#666666'),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=HexColor('#0052CC'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=HexColor('#1f4788'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8,
        leading=14,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )

    box_style = ParagraphStyle(
        'Box',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=6,
        leftIndent=12,
        rightIndent=12,
        backColor=HexColor('#F0F5FF'),
        borderColor=HexColor('#0052CC'),
        borderWidth=1,
        borderPadding=8,
        fontName='Helvetica'
    )

    story = []

    # ===== 페이지 1: 제목 =====
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("📦 택배 주소 스캔 시스템", title_style))
    story.append(Paragraph("간단 사용 가이드", h2_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("v2.0.6", subtitle_style))

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("핵심 기능", h1_style))
    features = (
        "• 카메라로 택배 라벨 스캔<br/>"
        "• AI가 자동으로 정보 인식<br/>"
        "• 데이터베이스에 자동 저장<br/>"
        "• 라벨 프린트 및 통계 조회"
    )
    story.append(Paragraph(features, normal_style))

    story.append(PageBreak())

    # ===== 페이지 2: 설치 및 시작 =====
    story.append(Paragraph("1️⃣ 시작하기", h1_style))

    story.append(Paragraph("설치", h2_style))
    install_text = (
        "<b>단계 1:</b> GitHub Release에서 parcel_scanner.exe 다운로드<br/>"
        "<b>단계 2:</b> 더블클릭해서 실행<br/>"
        "<b>단계 3:</b> 카메라/프린터 권한 허락 (필요시)<br/>"
        "<b>단계 4:</b> 완료! 프로그램 사용 시작"
    )
    story.append(Paragraph(install_text, normal_style))

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("화면 구성", h2_style))

    screen_data = [
        ["탭 이름", "기능"],
        ["📷 카메라 스캔", "라벨 촬영 및 정보 인식"],
        ["📚 주소록", "저장된 데이터 조회"],
        ["🔍 검색", "이름/전화/주소로 검색"],
        ["🖨️ 프린트", "라벨 프린트"],
        ["📊 통계", "저장 현황 확인"],
        ["⚙️ 설정", "프로그램 설정"],
    ]

    screen_table = Table(screen_data, colWidths=[3.5*cm, 6*cm])
    screen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#0052CC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), ['white', HexColor('#F9F9F9')]),
    ]))
    story.append(screen_table)

    story.append(PageBreak())

    # ===== 페이지 3: 기본 사용법 =====
    story.append(Paragraph("2️⃣ 기본 사용법", h1_style))

    story.append(Paragraph("카메라로 스캔하기", h2_style))
    scan_steps = (
        "<b>1단계:</b> '📷 카메라 스캔' 탭 클릭<br/>"
        "<b>2단계:</b> [카메라 시작] 버튼 클릭<br/>"
        "<b>3단계:</b> 택배 라벨을 카메라에 보임<br/>"
        "<b>4단계:</b> AI가 자동으로 정보 인식<br/>"
        "<b>5단계:</b> 정보 확인 후 [DB에 저장] 클릭"
    )
    story.append(Paragraph(scan_steps, normal_style))

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("인식되는 정보", h2_style))
    info_box = (
        "<b>• 수취인:</b> 받는 사람 이름<br/>"
        "<b>• 주소:</b> 배송지 도로명 주소<br/>"
        "<b>• 상세주소:</b> 건물 동/호수<br/>"
        "<b>• 우편번호:</b> 5자리 지역 코드<br/>"
        "<b>• 전화:</b> 수취인 휴대폰 번호"
    )
    story.append(Paragraph(info_box, box_style))

    story.append(PageBreak())

    # ===== 페이지 4: 추가 기능 =====
    story.append(Paragraph("3️⃣ 추가 기능", h1_style))

    story.append(Paragraph("라벨 프린트", h2_style))
    print_text = (
        "1. 프린트할 데이터 선택<br/>"
        "2. '🖨️ 프린트' 탭 클릭<br/>"
        "3. [라벨 프린트] 버튼 클릭<br/>"
        "4. 라벨프린터(Xprinter)에서 자동 출력"
    )
    story.append(Paragraph(print_text, normal_style))

    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("데이터 검색", h2_style))
    search_text = (
        "1. '🔍 검색' 탭 클릭<br/>"
        "2. 검색 조건 선택 (이름/전화/주소)<br/>"
        "3. 검색어 입력<br/>"
        "4. [검색] 버튼 클릭"
    )
    story.append(Paragraph(search_text, normal_style))

    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("통계 확인", h2_style))
    stats_text = (
        "'📊 통계' 탭에서 오늘 저장한 데이터 건수, "
        "이번 달 통계, 가장 많이 배송된 지역 등을 볼 수 있습니다."
    )
    story.append(Paragraph(stats_text, normal_style))

    story.append(PageBreak())

    # ===== 페이지 5: 문제 해결 =====
    story.append(Paragraph("4️⃣ 자주 묻는 질문", h1_style))

    story.append(Paragraph("Q: 프로그램이 시작되지 않습니다", h2_style))
    q1 = "A: Windows 10/11인지 확인하세요. 문제 해결: 프로그램 재설치 또는 antivirus 설정 확인"
    story.append(Paragraph(q1, normal_style))

    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("Q: 카메라가 인식되지 않습니다", h2_style))
    q2 = "A: 웹캠이 USB에 제대로 연결되었는지 확인하세요. 필요시 '⚙️ 설정' 탭에서 카메라 재선택"
    story.append(Paragraph(q2, normal_style))

    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("Q: 정보가 잘못 인식됩니다", h2_style))
    q3 = "A: 라벨이 밝고 선명한지 확인하세요. 수동으로 수정 후 저장 가능합니다."
    story.append(Paragraph(q3, normal_style))

    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("Q: 데이터는 어디에 저장됩니다?", h2_style))
    q4 = "A: SQLite 데이터베이스(parcel_database.db)와 Excel 파일(주소록.xlsx)에 저장됩니다."
    story.append(Paragraph(q4, normal_style))

    story.append(Spacer(1, 0.4*cm))

    footer = (
        "<b>더 많은 정보:</b> 상세 매뉴얼 'realistic_example_manual.pdf' 참조 또는 "
        "GitHub Issues에 문의 (github.com/kuiseob/parcel-address-scanner/issues)"
    )
    story.append(Paragraph(footer, normal_style))

    # PDF 생성
    doc.build(story)
    print(f"✅ 간단한 사용자 매뉴얼이 생성되었습니다: {filename}")

if __name__ == "__main__":
    create_simple_manual()
