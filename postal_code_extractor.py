import re
from typing import Optional, List, Dict, Tuple


class PostalCodeExtractor:
    """한국 우편번호 추출 및 검증"""

    # 우편번호 정규식 패턴
    POSTAL_CODE_PATTERNS = [
        r'\b([0-9]{5})\s*[-–−]\s*([0-9]{4})\b',  # XXXXX-XXXX (하이픈 포함)
        r'\b\(([0-9]{5})\)',                      # (XXXXX)
        r'\b([0-9]{5})\b(?=[\s\)])',               # XXXXX (공백/괄호 앞)
    ]

    def __init__(self):
        self.postal_code_db = self._load_postal_code_db()

    def _load_postal_code_db(self) -> Dict[str, str]:
        """
        한국 우편번호 데이터 로드
        (실제 구현에서는 외부 CSV/API 로드)
        """
        # 기본 우편번호 샘플 (실제로는 공공데이터포털에서 다운로드)
        return {
            '06000': '서울시 강남구 테헤란로',
            '06001': '서울시 강남구 강남대로',
            '03153': '서울시 종로구 인사동',
            # ... 더 많은 우편번호 데이터
        }

    def extract_postal_code(self, text: str) -> Optional[str]:
        """
        텍스트에서 우편번호 추출
        반환: "05000-1234" 형식의 우편번호 또는 None
        """
        text = text.strip()

        # 각 패턴으로 매칭 시도
        for pattern in self.POSTAL_CODE_PATTERNS:
            matches = re.finditer(pattern, text)
            for match in matches:
                if len(match.groups()) == 2:
                    # XXXXX-XXXX 형식
                    code = f"{match.group(1)}-{match.group(2)}"
                else:
                    # XXXXX 형식
                    code = match.group(1) if match.group(1) else match.group(0)
                    # 4자리를 뒤에 붙이려고 하면 추가 처리 필요
                    if len(code) == 5:
                        code = code  # 5자리만 반환

                if self._validate_postal_code(code):
                    return code

        return None

    def extract_all_postal_codes(self, text: str) -> List[str]:
        """
        텍스트에서 모든 우편번호 추출
        """
        codes = []
        for pattern in self.POSTAL_CODE_PATTERNS:
            matches = re.finditer(pattern, text)
            for match in matches:
                if len(match.groups()) == 2:
                    code = f"{match.group(1)}-{match.group(2)}"
                else:
                    code = match.group(1) if match.group(1) else match.group(0)

                if self._validate_postal_code(code) and code not in codes:
                    codes.append(code)

        return codes

    def _validate_postal_code(self, code: str) -> bool:
        """
        우편번호 검증
        - 5자리 또는 5자리-4자리 형식
        - 숫자만 포함
        """
        # XXXXX 형식
        if re.match(r'^\d{5}$', code):
            return True

        # XXXXX-XXXX 형식
        if re.match(r'^\d{5}-\d{4}$', code):
            return True

        # (XXXXX) 형식
        if re.match(r'^\(\d{5}\)$', code):
            return True

        return False

    def get_address_from_postal_code(self, postal_code: str) -> Optional[str]:
        """
        우편번호로부터 기본 주소 조회
        """
        # 기본 형식으로 변환 (5자리만)
        base_code = postal_code.split('-')[0] if '-' in postal_code else postal_code
        base_code = base_code.strip('()')

        return self.postal_code_db.get(base_code)

    def clean_postal_code(self, postal_code: str) -> str:
        """
        우편번호 정리 (표준 형식으로 변환)
        XXXXX-XXXX 형식으로 통일
        """
        # 괄호 제거
        code = postal_code.strip('() ')

        # 이미 XXXXX-XXXX 형식
        if '-' in code:
            parts = code.split('-')
            if len(parts) == 2:
                return f"{parts[0]}-{parts[1]}"

        # XXXXX 형식
        if len(code) == 5:
            return code

        return None


class PostalCodeCache:
    """우편번호 캐시 (성능 최적화)"""

    def __init__(self):
        self.cache = {}

    def get(self, postal_code: str) -> Optional[str]:
        """캐시에서 조회"""
        return self.cache.get(postal_code)

    def set(self, postal_code: str, address: str):
        """캐시에 저장"""
        self.cache[postal_code] = address

    def clear(self):
        """캐시 초기화"""
        self.cache.clear()

    def size(self) -> int:
        """캐시 크기"""
        return len(self.cache)
