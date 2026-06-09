import qrcode
import barcode
from barcode.writer import ImageWriter
from barcode.ean13 import EAN13
import json
import os
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
from parcel_info_parser import ParcelInfo


class BarcodeGenerator:
    """바코드 및 QR코드 생성"""

    def __init__(self, output_dir: str = "barcodes"):
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    def generate_qr_code(
        self, parcel_info: ParcelInfo, filename: Optional[str] = None
    ) -> str:
        """
        QR코드 생성
        파라미터: ParcelInfo 객체
        반환: 생성된 파일 경로
        """
        # QR코드 데이터 (JSON 형식)
        qr_data = {
            "postal_code": parcel_info.postal_code,
            "receiver_name": parcel_info.receiver_name,
            "phone_number": parcel_info.phone_number,
            "address": parcel_info.address,
            "detail_address": parcel_info.detail_address
        }

        qr_json = json.dumps(qr_data, ensure_ascii=False)

        # QR코드 생성
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(qr_json)
        qr.make(fit=True)

        # 이미지 생성
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # 파일 저장
        if not filename:
            filename = f"qr_{parcel_info.receiver_name}_{parcel_info.postal_code}.png"

        filepath = os.path.join(self.output_dir, filename)
        qr_image.save(filepath)

        return filepath

    def generate_code128_barcode(
        self, tracking_number: str, filename: Optional[str] = None
    ) -> str:
        """
        Code128 바코드 생성 (송장번호용)
        """
        # EAN13으로 변환하려면 13자리 숫자 필요
        # 실제로는 Code128 사용 (더 유연함)

        # Code128 바코드 생성
        try:
            from barcode.code128 import Code128

            code = Code128(tracking_number, writer=ImageWriter())

            if not filename:
                filename = f"barcode_{tracking_number}"

            filepath = os.path.join(self.output_dir, filename)
            code.save(filepath)

            return f"{filepath}.png"

        except Exception as e:
            print(f"바코드 생성 오류: {e}")
            return None

    def generate_label_image(
        self,
        parcel_info: ParcelInfo,
        barcode_path: Optional[str] = None,
        qrcode_path: Optional[str] = None,
        filename: Optional[str] = None
    ) -> str:
        """
        라벨 이미지 생성 (바코드 + QR 포함)
        크기: 100mm x 150mm (300dpi 기준 1181x1772px)
        """
        # 이미지 생성 (흰색 배경)
        width, height = 1000, 1200
        label_image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(label_image)

        # 폰트 설정
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttf", 30)
            text_font = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttf", 24)
            small_font = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttf", 16)
        except:
            # Windows/Linux 폰트
            try:
                title_font = ImageFont.truetype("C:\\Windows\\Fonts\\malgun.ttf", 30)
                text_font = ImageFont.truetype("C:\\Windows\\Fonts\\malgun.ttf", 24)
                small_font = ImageFont.truetype("C:\\Windows\\Fonts\\malgun.ttf", 16)
            except:
                # 기본 폰트
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                small_font = ImageFont.load_default()

        y_offset = 20

        # 제목
        draw.text((width // 2 - 100, y_offset), "배송 라벨", fill='black', font=title_font)
        y_offset += 60

        # 우편번호
        if parcel_info.postal_code:
            draw.text((20, y_offset), f"우편번호: {parcel_info.postal_code}", fill='black', font=text_font)
        y_offset += 50

        # 수취인
        if parcel_info.receiver_name:
            draw.text((20, y_offset), f"수취인: {parcel_info.receiver_name}", fill='black', font=text_font)
        y_offset += 50

        # 전화번호
        if parcel_info.phone_number:
            draw.text((20, y_offset), f"전화: {parcel_info.phone_number}", fill='black', font=text_font)
        y_offset += 50

        # 주소 (줄 바꿈)
        if parcel_info.address:
            address_text = parcel_info.address
            # 주소가 길면 여러 줄로 분할
            if len(address_text) > 30:
                address_lines = [address_text[i:i+30] for i in range(0, len(address_text), 30)]
            else:
                address_lines = [address_text]

            draw.text((20, y_offset), "주소:", fill='black', font=text_font)
            y_offset += 40

            for line in address_lines:
                draw.text((40, y_offset), line, fill='black', font=small_font)
                y_offset += 35

        y_offset += 40

        # QR코드 삽입
        if qrcode_path and os.path.exists(qrcode_path):
            qr_img = Image.open(qrcode_path)
            qr_img = qr_img.resize((200, 200))
            label_image.paste(qr_img, (width - 230, y_offset - 100))

        # 바코드 삽입
        if barcode_path and os.path.exists(barcode_path):
            try:
                barcode_img = Image.open(barcode_path)
                barcode_img = barcode_img.resize((400, 80))
                label_image.paste(barcode_img, (20, height - 120))
            except:
                pass

        # 파일 저장
        if not filename:
            filename = f"label_{parcel_info.receiver_name}_{parcel_info.postal_code}.png"

        filepath = os.path.join(self.output_dir, filename)
        label_image.save(filepath)

        return filepath

    def generate_full_label(
        self, parcel_info: ParcelInfo, tracking_number: str
    ) -> dict:
        """
        완전한 라벨 생성 (QR + 바코드 + 라벨 이미지)
        반환: {'qr': 경로, 'barcode': 경로, 'label': 경로}
        """
        result = {}

        # QR코드 생성
        qr_path = self.generate_qr_code(parcel_info)
        result['qr'] = qr_path

        # 바코드 생성
        barcode_path = self.generate_code128_barcode(tracking_number)
        result['barcode'] = barcode_path

        # 라벨 이미지 생성
        label_path = self.generate_label_image(parcel_info, barcode_path, qr_path)
        result['label'] = label_path

        return result


class QRCodeAdvanced:
    """고급 QR코드 생성 (커스터마이징)"""

    @staticmethod
    def create_qr_with_logo(qr_path: str, logo_path: str, output_path: str) -> bool:
        """
        로고가 있는 QR코드 생성
        """
        try:
            qr_image = Image.open(qr_path)
            logo = Image.open(logo_path)

            # 로고 크기 조정 (QR의 약 1/5)
            qr_width, qr_height = qr_image.size
            logo_size = qr_width // 5
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            # 로고 위치 (중앙)
            logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_image.paste(logo, logo_pos)

            qr_image.save(output_path)
            return True

        except Exception as e:
            print(f"로고 삽입 오류: {e}")
            return False

    @staticmethod
    def create_qr_with_text(qr_path: str, text: str, output_path: str) -> bool:
        """
        QR코드 아래 텍스트 추가
        """
        try:
            qr_image = Image.open(qr_path)
            qr_width, qr_height = qr_image.size

            # 새 이미지 (QR + 텍스트 공간)
            new_height = qr_height + 100
            new_image = Image.new('RGB', (qr_width, new_height), color='white')

            # QR코드 붙여넣기
            new_image.paste(qr_image, (0, 0))

            # 텍스트 추가
            draw = ImageDraw.Draw(new_image)
            try:
                font = ImageFont.truetype("C:\\Windows\\Fonts\\malgun.ttf", 20)
            except:
                font = ImageFont.load_default()

            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (qr_width - text_width) // 2
            text_y = qr_height + 20

            draw.text((text_x, text_y), text, fill='black', font=font)

            new_image.save(output_path)
            return True

        except Exception as e:
            print(f"텍스트 추가 오류: {e}")
            return False
