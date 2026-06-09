import re
from typing import Optional, Tuple, Dict


class AddressParser:
    """한국 주소 파싱 (도로명/지번 주소)"""

    # 시/도
    PROVINCES = [
        '서울', '부산', '대구', '인천', '광주', '대전', '울산',
        '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주'
    ]

    def __init__(self):
        self.province_pattern = '|'.join(self.PROVINCES)

    def parse_korean_address(self, text: str) -> Optional[str]:
        """
        텍스트에서 한국 주소 추출 및 정규화
        도로명 주소와 지번 주소 모두 지원
        """
        text = text.strip()

        # 공백 정규화
        text = re.sub(r'\s+', ' ', text)

        # 우편번호는 보존 (별도로 추출하므로 제거하지 않음)
        # 우편번호 제거
        # text = re.sub(r'[0-9]{5}(?:\s|-)?[0-9]{4}', '', text)
        # text = re.sub(r'\([0-9]{5}\)', '', text)

        # 도로명 주소 형식: 서울시 강남구 테헤란로 123
        roadname_pattern = (
            f'({self.province_pattern})[시도]\\s+'
            r'[가-힣]+[구시군]\\s+'
            r'[가-힣0-9]+(?:로|길|가)\\s+'
            r'[0-9]+(?:-[0-9]+)?'
        )

        # 지번 주소 형식: 서울시 강남구 역삼동 123-4
        jibun_pattern = (
            f'({self.province_pattern})[시도]\\s+'
            r'[가-힣]+[구시군]\\s+'
            r'[가-힣]+[동읍면]\\s+'
            r'[0-9]+(?:-[0-9]+)?'
        )

        # 도로명 주소 매칭
        match = re.search(roadname_pattern, text)
        if match:
            address = match.group(0)
            return self._normalize_address(address)

        # 지번 주소 매칭
        match = re.search(jibun_pattern, text)
        if match:
            address = match.group(0)
            return self._normalize_address(address)

        return None

    def _normalize_address(self, address: str) -> str:
        """주소 정규화 (공백 정리, 띄어쓰기 통일)"""
        address = address.strip()
        address = re.sub(r'\s+', ' ', address)
        return address

    def extract_addresses_from_text(self, text: str) -> list[str]:
        """한 텍스트에서 여러 주소 추출"""
        addresses = []
        lines = text.split('\n')

        for line in lines:
            addr = self.parse_korean_address(line)
            if addr and addr not in addresses:
                addresses.append(addr)

        return addresses
