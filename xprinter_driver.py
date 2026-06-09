import usb.core
import usb.util
import struct
from typing import Optional, List, Tuple
from PIL import Image
import io


class XprinterDriver:
    """Xprinter 열전사 라벨 프린터 드라이버 (ESC/POS)"""

    # Xprinter 제품 ID
    XPRINTER_VENDOR_ID = 0x0483  # STM32
    XPRINTER_PRODUCT_IDS = [0x110, 0x111, 0x115, 0x120]  # 다양한 모델

    # ESC/POS 명령어
    ESC = b'\x1b'  # Escape
    GS = b'\x1d'   # Group Separator

    def __init__(self):
        self.device = None
        self.endpoint_out = None
        self.endpoint_in = None
        self.paper_width = 32  # 기본 100mm (32 dot = 1mm, 약)
        self.paper_height = 48  # 기본 150mm

    def find_printers(self) -> List[dict]:
        """연결된 모든 Xprinter 프린터 찾기"""
        printers = []

        try:
            devices = usb.core.find(
                find_all=True,
                idVendor=self.XPRINTER_VENDOR_ID
            )

            for device in devices:
                try:
                    device.set_configuration()
                    printer_info = {
                        'vendor_id': device.idVendor,
                        'product_id': device.idProduct,
                        'manufacturer': device.manufacturer,
                        'product': device.product,
                        'device': device,
                        'bus': device.bus,
                        'address': device.address
                    }
                    printers.append(printer_info)
                except:
                    pass

        except usb.core.USBError as e:
            print(f"USB 스캔 오류: {e}")

        return printers

    def connect(self, device_index: int = 0) -> bool:
        """프린터 연결"""
        try:
            printers = self.find_printers()

            if not printers:
                print("연결된 Xprinter를 찾을 수 없습니다")
                return False

            if device_index >= len(printers):
                print(f"프린터 인덱스 범위 초과: {device_index}")
                return False

            self.device = printers[device_index]['device']
            self.device.set_configuration()

            # 엔드포인트 설정
            intf = self.device.get_active_configuration()[(0, 0)]

            # OUT 엔드포인트 찾기
            self.endpoint_out = usb.util.find_descriptor(
                intf,
                custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
            )

            # IN 엔드포인트 찾기
            self.endpoint_in = usb.util.find_descriptor(
                intf,
                custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
            )

            print(f"프린터 연결 성공: {printers[device_index]['product']}")
            return True

        except Exception as e:
            print(f"프린터 연결 오류: {e}")
            return False

    def disconnect(self):
        """프린터 연결 해제"""
        try:
            if self.device:
                usb.core.dispose(self.device)
                self.device = None
        except:
            pass

    def _send_command(self, command: bytes) -> bool:
        """프린터에 명령어 전송"""
        try:
            if not self.device or not self.endpoint_out:
                return False

            self.endpoint_out.write(command)
            return True

        except usb.core.USBError as e:
            print(f"전송 오류: {e}")
            return False

    def _read_response(self, length: int = 32) -> bytes:
        """프린터 응답 읽기"""
        try:
            if not self.device or not self.endpoint_in:
                return b''

            return self.endpoint_in.read(length, timeout=1000)

        except usb.core.USBTimeoutError:
            return b''
        except Exception as e:
            print(f"응답 읽기 오류: {e}")
            return b''

    def initialize(self) -> bool:
        """프린터 초기화"""
        # ESC @ (프린터 초기화)
        command = self.ESC + b'@'
        return self._send_command(command)

    def reset(self) -> bool:
        """프린터 리셋"""
        # ESC ! (리셋)
        command = self.ESC + b'!' + b'\x00'
        return self._send_command(command)

    def print_text(self, text: str, bold: bool = False, size: int = 1) -> bool:
        """텍스트 인쇄"""
        command = b''

        # 크기 설정 (GS ! n)
        if size > 1:
            command += self.GS + b'!' + bytes([size - 1])

        # 텍스트 인쇄
        command += text.encode('utf-8')
        command += b'\n'

        return self._send_command(command)

    def print_barcode(self, barcode_data: str, barcode_type: int = 4) -> bool:
        """바코드 인쇄 (GS h, GS w, GS k)"""
        # barcode_type: 4 = Code128

        try:
            command = b''

            # 바코드 높이 설정 (GS h)
            command += self.GS + b'h' + b'\x64'  # 100 dot (약 13mm)

            # 바코드 너비 설정 (GS w)
            command += self.GS + b'w' + b'\x02'

            # 바코드 데이터 (GS k)
            barcode_bytes = barcode_data.encode('ascii')
            command += self.GS + b'k' + bytes([barcode_type]) + bytes([len(barcode_bytes)]) + barcode_bytes

            return self._send_command(command)

        except Exception as e:
            print(f"바코드 인쇄 오류: {e}")
            return False

    def print_image(self, image_path: str, width: int = 384, height: int = 100) -> bool:
        """이미지 인쇄 (GS v 0)"""
        try:
            # 이미지 로드
            image = Image.open(image_path)
            image = image.convert('L')  # 그레이스케일
            image = image.resize((width, height), Image.Resampling.LANCZOS)

            # 이미지를 바이너리로 변환
            pixels = image.tobytes()

            # 이미지 데이터 전송
            command = self.GS + b'v' + b'0'
            command += bytes([width % 256, width // 256])  # 너비 (리틀 엔디안)
            command += bytes([height % 256, height // 256])  # 높이
            command += pixels

            return self._send_command(command)

        except Exception as e:
            print(f"이미지 인쇄 오류: {e}")
            return False

    def feed_paper(self, lines: int = 1) -> bool:
        """용지 공급 (개행)"""
        command = b'\n' * lines
        return self._send_command(command)

    def cut_paper(self) -> bool:
        """용지 절단"""
        # ESC m (부분 절단)
        command = self.ESC + b'm'
        return self._send_command(command)

    def get_printer_status(self) -> Optional[dict]:
        """프린터 상태 확인"""
        # GS r (실시간 상태 요청)
        command = self.GS + b'r' + b'\x01'

        if self._send_command(command):
            response = self._read_response()

            if len(response) > 0:
                status = response[0]

                return {
                    'ready': (status & 0x01) == 0,
                    'paper_low': (status & 0x02) != 0,
                    'paper_out': (status & 0x04) != 0,
                    'temp_error': (status & 0x08) != 0,
                    'offline': (status & 0x10) != 0,
                    'raw': status
                }

        return None

    def test_print(self) -> bool:
        """테스트 인쇄"""
        command = b''
        command += self.ESC + b'@'  # 초기화

        # 테스트 텍스트
        test_text = "XPRINTER TEST\n"
        command += test_text.encode('utf-8')

        # 라인 피드
        command += b'\n' * 5

        # 용지 절단
        command += self.ESC + b'm'

        return self._send_command(command)

    def print_label(self, label_data: dict) -> bool:
        """라벨 전체 인쇄"""
        try:
            command = b''

            # 초기화
            command += self.ESC + b'@'

            # 제목
            if 'title' in label_data:
                command += label_data['title'].encode('utf-8')
                command += b'\n\n'

            # 정보 (우편번호, 수취인, 주소 등)
            for key, value in label_data.items():
                if key not in ['title', 'barcode', 'qrcode']:
                    command += f"{key}: {value}\n".encode('utf-8')

            # 이미지 인쇄
            if 'barcode' in label_data:
                # 바코드 인쇄
                command += self.GS + b'h' + b'\x64'
                barcode_bytes = label_data['barcode'].encode('ascii')
                command += self.GS + b'k' + b'\x04' + bytes([len(barcode_bytes)]) + barcode_bytes
                command += b'\n'

            # 피드 및 절단
            command += b'\n' * 5
            command += self.ESC + b'm'

            return self._send_command(command)

        except Exception as e:
            print(f"라벨 인쇄 오류: {e}")
            return False


class XprinterLabelTemplate:
    """Xprinter 라벨 템플릿"""

    @staticmethod
    def get_label_template(carrier: str = 'default') -> dict:
        """택배사별 라벨 템플릿 반환"""

        templates = {
            'CJ': {
                'title': 'CJ LOGISTICS',
                'fields': [
                    ('우편번호', 'postal_code'),
                    ('수취인', 'receiver_name'),
                    ('전화', 'phone_number'),
                    ('주소', 'address'),
                ],
                'barcode_type': 4,  # Code128
                'font_size': 1,
                'paper_size': (100, 150)  # mm
            },
            'LOGEN': {
                'title': 'LOGEN EXPRESS',
                'fields': [
                    ('우편번호', 'postal_code'),
                    ('수취인', 'receiver_name'),
                    ('전화', 'phone_number'),
                    ('주소', 'address'),
                ],
                'barcode_type': 4,
                'font_size': 1,
                'paper_size': (100, 150)
            },
            'default': {
                'title': 'PARCEL LABEL',
                'fields': [
                    ('우편번호', 'postal_code'),
                    ('수취인', 'receiver_name'),
                    ('전화', 'phone_number'),
                    ('주소', 'address'),
                ],
                'barcode_type': 4,
                'font_size': 1,
                'paper_size': (100, 150)
            }
        }

        return templates.get(carrier, templates['default'])

    @staticmethod
    def format_label_data(parcel_info, carrier: str = 'default') -> dict:
        """ParcelInfo를 라벨 데이터로 포맷"""

        template = XprinterLabelTemplate.get_label_template(carrier)

        label_data = {'title': template['title']}

        for display_name, field_name in template['fields']:
            value = getattr(parcel_info, field_name, '')
            if value:
                label_data[display_name] = str(value)

        return label_data
