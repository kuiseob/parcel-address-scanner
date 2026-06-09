import re
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict
from postal_code_extractor import PostalCodeExtractor


@dataclass
class ParcelInfo:
    """택배 정보 데이터 클래스"""
    postal_code: Optional[str] = None      # 우편번호 (05000-1234)
    receiver_name: Optional[str] = None    # 수취인명
    phone_number: Optional[str] = None     # 전화번호
    address: Optional[str] = None          # 기본 주소 (도로명/지번)
    detail_address: Optional[str] = None   # 상세 주소 (호/건물명)
    full_address: Optional[str] = None     # 전체 주소
    confidence: Dict[str, float] = None    # 신뢰도 점수
    raw_text: Optional[str] = None         # 원본 텍스트

    def __post_init__(self):
        if self.confidence is None:
            self.confidence = {
                'postal_code': 0.0,
                'receiver_name': 0.0,
                'phone_number': 0.0,
                'address': 0.0,
                'detail_address': 0.0
            }

    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return asdict(self)

    def to_csv_row(self) -> tuple:
        """CSV 행으로 변환"""
        return (
            self.postal_code or '',
            self.receiver_name or '',
            self.phone_number or '',
            self.address or '',
            self.detail_address or '',
            self.full_address or ''
        )


class ParcelInfoParser:
    """택배 정보 파싱 (수취인, 전화번호, 주소 자동 분리)"""

    def __init__(self):
        self.postal_code_extractor = PostalCodeExtractor()

        # 정규식 패턴 정의
        self.phone_pattern = self._compile_phone_patterns()
        self.receiver_pattern = self._compile_receiver_pattern()

    def _compile_phone_patterns(self) -> List[re.Pattern]:
        """전화번호 정규식 패턴"""
        return [
            re.compile(r'0\d{1,2}-\d{3,4}-\d{4}'),           # 010-1234-5678
            re.compile(r'0\d{1,2}\d{3,4}\d{4}'),             # 01012345678
            re.compile(r'0\d{1,2} \d{3,4} \d{4}'),           # 010 1234 5678
            re.compile(r'\(\d{3,4}\) \d{3,4}-\d{4}'),        # (02) 1234-5678
        ]

    def _compile_receiver_pattern(self) -> re.Pattern:
        """수취인명 정규식 (2-4자 한글)"""
        return re.compile(r'[가-힣]{2,4}(?=\s|$|[0-9]|\(|\[|「|「|[,.])')

    def parse(self, text: str) -> ParcelInfo:
        """
        전체 택배 정보 파싱
        """
        info = ParcelInfo(raw_text=text)

        # 1. 우편번호 추출
        info.postal_code = self.postal_code_extractor.extract_postal_code(text)
        if info.postal_code:
            info.confidence['postal_code'] = 0.95  # 높은 신뢰도

        # 2. 전화번호 추출
        phone = self._extract_phone_number(text)
        if phone:
            info.phone_number = phone
            info.confidence['phone_number'] = 0.9

        # 3. 수취인명 추출
        receiver = self._extract_receiver_name(text)
        if receiver:
            info.receiver_name = receiver
            info.confidence['receiver_name'] = 0.85

        # 4. 주소 추출 및 분리
        address_info = self._extract_and_split_address(text, info)
        info.address = address_info.get('basic_address')
        info.detail_address = address_info.get('detail_address')
        info.full_address = address_info.get('full_address')
        info.confidence.update(address_info.get('confidence', {}))

        return info

    def _extract_phone_number(self, text: str) -> Optional[str]:
        """전화번호 추출"""
        for pattern in self.phone_pattern:
            match = pattern.search(text)
            if match:
                phone = match.group(0)
                # 표준 형식으로 변환
                return self._normalize_phone_number(phone)
        return None

    def _normalize_phone_number(self, phone: str) -> str:
        """전화번호 표준화 (010-1234-5678)"""
        # 숫자만 추출
        digits = re.sub(r'[^0-9]', '', phone)

        # 길이에 따라 포맷
        if len(digits) == 10:
            return f"{digits[:2]}-{digits[2:6]}-{digits[6:]}"  # 02-1234-5678
        elif len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"  # 010-1234-5678

        return phone

    def _extract_receiver_name(self, text: str) -> Optional[str]:
        """
        수취인명 추출 (2-4자 한글)
        우편번호나 전화번호 앞에 있는 경우가 많음
        """
        # 전화번호 앞의 한글 이름
        pattern = r'([가-힣]{2,4})\s*0\d'
        match = re.search(pattern, text)
        if match:
            return match.group(1)

        # 우편번호 앞의 한글 이름
        pattern = r'([가-힣]{2,4})\s*\(?[0-9]{5}'
        match = re.search(pattern, text)
        if match:
            return match.group(1)

        # 일반적인 한글 2-4자 (라인 시작)
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            match = self.receiver_pattern.search(line)
            if match:
                return match.group(0)

        return None

    def _extract_and_split_address(self, text: str, info: ParcelInfo) -> Dict:
        """
        주소 추출 및 기본/상세 주소 분리
        기본: 도로명/지번 주소
        상세: 호/건물명/층수
        """
        result = {
            'basic_address': None,
            'detail_address': None,
            'full_address': None,
            'confidence': {
                'address': 0.0,
                'detail_address': 0.0
            }
        }

        # 주소 영역 추출 (우편번호 이후 부분)
        if info.postal_code:
            # 우편번호 이후의 텍스트
            idx = text.find(info.postal_code)
            if idx >= 0:
                text = text[idx + len(info.postal_code):]

        # 기본 주소와 상세 주소 분리
        lines = text.split('\n')

        for i, line in enumerate(lines):
            line = line.strip()

            # 기본 주소 패턴 (도로명/지번)
            if self._is_basic_address(line):
                result['basic_address'] = line
                result['confidence']['address'] = 0.9

                # 다음 라인이 상세 주소일 가능성
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if self._is_detail_address(next_line):
                        result['detail_address'] = next_line
                        result['confidence']['detail_address'] = 0.85
                        result['full_address'] = f"{line} {next_line}"
                    else:
                        result['full_address'] = line
                else:
                    result['full_address'] = line

                break

        # 기본 주소를 찾지 못한 경우, 전체 텍스트 사용
        if not result['basic_address']:
            # 숫자와 한글이 섞인 가장 긴 라인 찾기
            longest_line = max(
                [line.strip() for line in lines if len(line.strip()) > 5],
                key=len,
                default=None
            )
            if longest_line:
                result['basic_address'] = longest_line
                result['full_address'] = longest_line
                result['confidence']['address'] = 0.6

        return result

    def _is_basic_address(self, text: str) -> bool:
        """
        기본 주소 판별
        - 시/도로 시작
        - 도로명 또는 지번 포함
        """
        provinces = ['서울', '부산', '대구', '인천', '광주', '대전', '울산',
                     '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']

        # 시/도로 시작
        for prov in provinces:
            if text.startswith(prov):
                return True

        return False

    def _is_detail_address(self, text: str) -> bool:
        """
        상세 주소 판별
        - 숫자로 시작 (호/층수)
        - 특수 문자 포함 (호, 층, 동, 호선 등)
        """
        if re.match(r'^\d+', text):
            return True

        if re.search(r'[호층동건물]', text):
            return True

        return False

    def parse_multiple(self, texts: List[str]) -> List[ParcelInfo]:
        """여러 텍스트 일괄 파싱"""
        results = []
        for text in texts:
            info = self.parse(text)
            results.append(info)
        return results
