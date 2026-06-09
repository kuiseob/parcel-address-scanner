import easyocr
import cv2
import numpy as np
from typing import Optional, Tuple


class OCRProcessor:
    """EasyOCR을 이용한 한글 주소 인식"""

    def __init__(self):
        self.reader = easyocr.Reader(['ko', 'en'], gpu=False)

    def extract_text_from_frame(self, frame: np.ndarray) -> str:
        """프레임에서 텍스트 추출"""
        # 이미지 전처리
        processed = self._preprocess_image(frame)

        # OCR 실행
        results = self.reader.readtext(processed, detail=0)

        # 텍스트 정렬 (위에서 아래로)
        text = '\n'.join(results)
        return text

    def _preprocess_image(self, frame: np.ndarray) -> np.ndarray:
        """이미지 전처리 (대비 향상, 노이즈 제거)"""
        # 그레이스케일 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 대비 향상 (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # 노이즈 제거
        denoised = cv2.fastNlMeansDenoising(enhanced)

        return denoised

    def draw_detection_box(
        self, frame: np.ndarray, results: list
    ) -> Tuple[np.ndarray, list[str]]:
        """인식된 텍스트에 박스 그리기"""
        texts = []

        for (bbox, text, confidence) in results:
            # 좌표 변환
            bbox_points = np.array(bbox, dtype=np.int32)

            # 신뢰도 0.5 이상만 표시
            if confidence > 0.5:
                color = (0, 255, 0)  # 초록색
                thickness = 2
                texts.append(text)
            else:
                color = (0, 0, 255)  # 빨간색
                thickness = 1

            # 박스 그리기
            cv2.polylines(frame, [bbox_points], True, color, thickness)

            # 텍스트 표시
            x, y = int(bbox[0][0]), int(bbox[0][1])
            cv2.putText(
                frame, f"{text}({confidence:.2f})",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1
            )

        return frame, texts
