import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import cv2
import threading
import platform
import subprocess
import os
from PIL import Image, ImageTk
from address_parser import AddressParser
from address_book import AddressBook
from ocr_processor import OCRProcessor
from parcel_info_parser import ParcelInfoParser
from database_manager import DatabaseManager
from barcode_generator import BarcodeGenerator
from xprinter_driver import XprinterDriver, XprinterLabelTemplate


class ParcelAddressScannerApp:
    """택배 주소 스캔 및 주소록 관리 GUI (PHASE 1 업그레이드)"""

    def __init__(self, root):
        self.root = root
        self.root.title("택배 주소 스캔 시스템 v2.0")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # 플랫폼 감지
        self.platform = platform.system()

        # 초기화
        self.camera = None
        self.is_running = False
        self.ocr = OCRProcessor()
        self.address_parser = AddressParser()
        self.parcel_parser = ParcelInfoParser()
        self.address_book = AddressBook()
        self.db = DatabaseManager()  # SQLite 데이터베이스
        self.barcode_gen = BarcodeGenerator()  # 바코드 생성기
        self.xprinter = XprinterDriver()  # Xprinter 드라이버
        self.current_text = ""
        self.photo_image = None
        self.current_parcel_info = None
        self.last_generated_barcode = None

        self._setup_ui()
        self._update_statistics()

    def _get_fonts(self):
        """플랫폼별 폰트 설정"""
        if self.platform == 'Windows':
            return {
                'title': ("맑은 고딕", 12, "bold"),
                'text': ("굴림", 10),
                'mono': ("Courier New", 9)
            }
        elif self.platform == 'Darwin':
            return {
                'title': ("Apple SD Gothic Neo", 12, "bold"),
                'text': ("Apple SD Gothic Neo", 10),
                'mono': ("Monaco", 9)
            }
        else:
            return {
                'title': ("DejaVu Sans", 12, "bold"),
                'text': ("DejaVu Sans", 10),
                'mono': ("DejaVu Sans Mono", 9)
            }

    def _setup_ui(self):
        """메인 UI 설정"""
        fonts = self._get_fonts()

        # 노트북 (탭)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 탭 1: 카메라 스캔
        self._setup_camera_tab(notebook, fonts)

        # 탭 2: 주소록 관리
        self._setup_addressbook_tab(notebook, fonts)

        # 탭 3: 주소 검색
        self._setup_search_tab(notebook, fonts)

        # 탭 4: 통계
        self._setup_statistics_tab(notebook, fonts)

        # 탭 5: 바코드/QR & 라벨 인쇄 (PHASE 2)
        self._setup_barcode_tab(notebook, fonts)

        # 상태바
        self.status_var = tk.StringVar(value="준비됨")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    def _setup_camera_tab(self, notebook, fonts):
        """탭 1: 카메라 스캔"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="카메라 스캔")

        # 좌측: 카메라 영상
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(left_frame, text="카메라 입력", font=fonts['title']).pack()
        self.canvas = tk.Canvas(left_frame, bg="black", width=480, height=480)
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=5)

        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=5)
        self.start_btn = ttk.Button(button_frame, text="카메라 시작", command=self._start_camera)
        self.start_btn.pack(side=tk.LEFT, padx=2)
        self.stop_btn = ttk.Button(button_frame, text="카메라 중지", command=self._stop_camera, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        self.capture_btn = ttk.Button(button_frame, text="[스캔]", command=self._capture_frame, state=tk.DISABLED)
        self.capture_btn.pack(side=tk.LEFT, padx=2)

        # 우측: 인식 결과
        right_frame = ttk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 인식된 텍스트
        ttk.Label(right_frame, text="인식된 텍스트", font=fonts['title']).pack()
        self.text_widget = scrolledtext.ScrolledText(right_frame, height=8, width=40, font=fonts['mono'])
        self.text_widget.pack(fill=tk.BOTH, expand=True, pady=3)

        # 추출된 정보 (우편번호, 수취인, 전화번호, 주소)
        ttk.Label(right_frame, text="추출된 배송 정보", font=fonts['title']).pack(pady=(10, 0))
        info_frame = ttk.LabelFrame(right_frame, text="정보 상세", padding=5)
        info_frame.pack(fill=tk.X, pady=3)

        info_data = [
            ('우편번호:', 'postal_code'),
            ('수취인:', 'receiver_name'),
            ('전화번호:', 'phone_number'),
            ('기본주소:', 'address'),
            ('상세주소:', 'detail_address'),
        ]

        self.info_labels = {}
        for label_text, key in info_data:
            row = ttk.Frame(info_frame)
            row.pack(fill=tk.X, pady=2)
            ttk.Label(row, text=label_text, width=10, font=fonts['text']).pack(side=tk.LEFT)
            value_label = ttk.Label(row, text="", foreground="#333333", font=fonts['text'])
            value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.info_labels[key] = value_label

        # 버튼
        control_frame = ttk.Frame(right_frame)
        control_frame.pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="저장 (DB)", command=self._save_to_database).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="저장 (Excel)", command=self._save_to_excel).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="초기화", command=self._clear_all).pack(side=tk.LEFT, padx=2)

    def _setup_addressbook_tab(self, notebook, fonts):
        """탭 2: 주소록 관리"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="주소록 관리")

        # 상단: 버튼
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame, text="Excel 열기", command=self._open_excel).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="DB 내보내기 (CSV)", command=self._export_csv).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="통계 갱신", command=self._update_statistics).pack(side=tk.LEFT, padx=2)

        # 주소 리스트 (테이블)
        ttk.Label(frame, text="저장된 주소록", font=fonts['title']).pack(anchor=tk.W, padx=5, pady=3)

        # 스크롤 가능한 테이블
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', '우편번호', '수취인', '전화번호', '주소'),
            height=20,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.W, width=30)
        self.tree.column('우편번호', anchor=tk.W, width=100)
        self.tree.column('수취인', anchor=tk.W, width=80)
        self.tree.column('전화번호', anchor=tk.W, width=120)
        self.tree.column('주소', anchor=tk.W, width=300)

        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('ID', text='ID', anchor=tk.W)
        self.tree.heading('우편번호', text='우편번호', anchor=tk.W)
        self.tree.heading('수취인', text='수취인', anchor=tk.W)
        self.tree.heading('전화번호', text='전화번호', anchor=tk.W)
        self.tree.heading('주소', text='주소', anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # 하단: 삭제 버튼
        delete_frame = ttk.Frame(frame)
        delete_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(delete_frame, text="선택 삭제", command=self._delete_selected_address).pack(side=tk.LEFT)

        # 주소록 로드
        self._refresh_addressbook_list()

    def _setup_search_tab(self, notebook, fonts):
        """탭 3: 주소 검색"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="주소 검색")

        # 검색 입력
        search_frame = ttk.LabelFrame(frame, text="검색 조건", padding=5)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(search_frame, text="검색어:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_input = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_input.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Label(search_frame, text="검색 유형:").pack(side=tk.LEFT, padx=5)
        self.search_type_var = tk.StringVar(value='all')
        search_type = ttk.Combobox(
            search_frame,
            textvariable=self.search_type_var,
            values=['전체', '수취인', '전화번호', '주소'],
            state='readonly',
            width=15
        )
        search_type.pack(side=tk.LEFT, padx=5)

        ttk.Button(search_frame, text="검색", command=self._search_addresses).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="초기화", command=self._reset_search).pack(side=tk.LEFT, padx=5)

        # 결과 표시
        ttk.Label(frame, text="검색 결과", font=fonts['title']).pack(anchor=tk.W, padx=5, pady=3)

        result_frame = ttk.Frame(frame)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)

        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.search_tree = ttk.Treeview(
            result_frame,
            columns=('ID', '우편번호', '수취인', '전화번호', '주소'),
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.search_tree.yview)

        self.search_tree.column('#0', width=0, stretch=tk.NO)
        self.search_tree.column('ID', anchor=tk.W, width=30)
        self.search_tree.column('우편번호', anchor=tk.W, width=100)
        self.search_tree.column('수취인', anchor=tk.W, width=80)
        self.search_tree.column('전화번호', anchor=tk.W, width=120)
        self.search_tree.column('주소', anchor=tk.W, width=300)

        self.search_tree.heading('ID', text='ID', anchor=tk.W)
        self.search_tree.heading('우편번호', text='우편번호', anchor=tk.W)
        self.search_tree.heading('수취인', text='수취인', anchor=tk.W)
        self.search_tree.heading('전화번호', text='전화번호', anchor=tk.W)
        self.search_tree.heading('주소', text='주소', anchor=tk.W)

        self.search_tree.pack(fill=tk.BOTH, expand=True)

    def _setup_statistics_tab(self, notebook, fonts):
        """탭 4: 통계"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="통계")

        # 통계 표시
        self.stat_frame = ttk.LabelFrame(frame, text="데이터베이스 통계", padding=10)
        self.stat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.stat_labels = {}
        stats = [
            ('총 주소 개수', 'total_addresses'),
            ('총 송장 개수', 'total_parcels'),
            ('총 LOT 개수', 'total_lots'),
        ]

        for label_text, key in stats:
            row = ttk.Frame(self.stat_frame)
            row.pack(fill=tk.X, pady=10)
            ttk.Label(row, text=label_text, font=fonts['title'], width=20).pack(side=tk.LEFT)
            stat_label = ttk.Label(row, text="0", font=("Arial", 20, "bold"), foreground="#0066CC")
            stat_label.pack(side=tk.LEFT, padx=20)
            self.stat_labels[key] = stat_label

    # ============ 카메라 기능 ============

    def _start_camera(self):
        """카메라 시작"""
        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            messagebox.showerror("에러", "카메라를 열 수 없습니다")
            return

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.capture_btn.config(state=tk.NORMAL)
        self.status_var.set("카메라 실행 중...")

        thread = threading.Thread(target=self._camera_loop, daemon=True)
        thread.start()

    def _camera_loop(self):
        """카메라 루프"""
        while self.is_running and self.camera:
            ret, frame = self.camera.read()
            if not ret:
                break

            frame = cv2.resize(frame, (480, 480))
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            self.photo_image = ImageTk.PhotoImage(image)

            self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
            self.root.update()

    def _stop_camera(self):
        """카메라 중지"""
        self.is_running = False
        if self.camera:
            self.camera.release()
            self.camera = None

        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.capture_btn.config(state=tk.DISABLED)
        self.status_var.set("카메라 중지됨")

    def _capture_frame(self):
        """프레임 캡처 및 OCR 처리"""
        if not self.camera or not self.camera.isOpened():
            messagebox.showwarning("경고", "카메라가 실행 중이 아닙니다")
            return

        ret, frame = self.camera.read()
        if not ret:
            messagebox.showerror("에러", "프레임을 캡처할 수 없습니다")
            return

        self.status_var.set("텍스트 인식 중...")
        self.root.update()

        # OCR 처리
        text = self.ocr.extract_text_from_frame(frame)
        self.current_text = text

        # UI 업데이트
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(1.0, text)

        # 배송 정보 파싱 (우편번호, 수취인, 전화번호, 주소)
        self.current_parcel_info = self.parcel_parser.parse(text)
        self._update_info_display()

        self.status_var.set(f"인식 완료")

    def _update_info_display(self):
        """추출된 정보 표시"""
        if not self.current_parcel_info:
            return

        info = self.current_parcel_info

        display_data = {
            'postal_code': info.postal_code or '미감지',
            'receiver_name': info.receiver_name or '미감지',
            'phone_number': info.phone_number or '미감지',
            'address': info.address or '미감지',
            'detail_address': info.detail_address or '-',
        }

        for key, label in self.info_labels.items():
            label.config(text=display_data[key])

    def _save_to_database(self):
        """데이터베이스에 저장"""
        if not self.current_parcel_info:
            messagebox.showwarning("경고", "저장할 정보가 없습니다")
            return

        if not self.current_parcel_info.receiver_name or not self.current_parcel_info.address:
            messagebox.showwarning("경고", "수취인과 주소 정보가 필요합니다")
            return

        result = self.db.add_address(self.current_parcel_info, source='camera')

        if result:
            messagebox.showinfo("성공", f"주소가 데이터베이스에 저장되었습니다 (ID: {result})")
            self._refresh_addressbook_list()
            self._update_statistics()
            self.status_var.set(f"저장됨: {self.current_parcel_info.receiver_name} ({self.current_parcel_info.address})")
        else:
            messagebox.showwarning("경고", "이미 등록된 주소입니다 (중복)")

    def _save_to_excel(self):
        """Excel에 저장"""
        if not self.current_parcel_info:
            messagebox.showwarning("경고", "저장할 정보가 없습니다")
            return

        # address_book은 여전히 Excel 저장 담당
        # ParcelInfo를 임시로 변환
        if self.address_book.add_address(self.current_parcel_info.full_address or self.current_parcel_info.address):
            messagebox.showinfo("성공", f"주소가 Excel에 저장되었습니다")
            self.status_var.set(f"Excel 저장됨")
        else:
            messagebox.showwarning("경고", "이미 등록된 주소입니다")

    def _clear_all(self):
        """화면 초기화"""
        self.text_widget.delete(1.0, tk.END)
        for label in self.info_labels.values():
            label.config(text='')
        self.current_text = ""
        self.current_parcel_info = None
        self.status_var.set("초기화됨")

    # ============ 주소록 관리 ============

    def _refresh_addressbook_list(self):
        """주소록 목록 새로 고침"""
        # 기존 항목 삭제
        for item in self.tree.get_children():
            self.tree.delete(item)

        # DB에서 주소 조회
        addresses = self.db.get_all_addresses(limit=100)
        for addr in addresses:
            self.tree.insert('', 'end', values=(
                addr['id'],
                addr['postal_code'] or '',
                addr['receiver_name'],
                addr['phone_number'] or '',
                addr['full_address'] or addr['basic_address']
            ))

    def _delete_selected_address(self):
        """선택된 주소 삭제"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("경고", "삭제할 주소를 선택하세요")
            return

        if messagebox.askyesno("확인", f"{len(selection)}개 주소를 삭제하시겠습니까?"):
            for item in selection:
                values = self.tree.item(item)['values']
                address_id = values[0]
                self.db.delete_address(address_id)

            self._refresh_addressbook_list()
            self._update_statistics()
            messagebox.showinfo("성공", "주소가 삭제되었습니다")

    def _open_excel(self):
        """Excel 파일 열기"""
        if not os.path.exists(self.address_book.filename):
            messagebox.showwarning("경고", "주소록 파일이 없습니다")
            return

        try:
            if self.platform == 'Windows':
                os.startfile(self.address_book.filename)
            elif self.platform == 'Darwin':
                subprocess.Popen(['open', self.address_book.filename])
            else:
                subprocess.Popen(['xdg-open', self.address_book.filename])
            self.status_var.set("Excel 열기 완료")
        except Exception as e:
            messagebox.showerror("에러", f"파일을 열 수 없습니다: {e}")

    def _export_csv(self):
        """CSV로 내보내기"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filepath:
            if self.db.export_to_csv(filepath):
                messagebox.showinfo("성공", f"CSV로 내보내기 완료: {filepath}")
                self.status_var.set(f"CSV 내보내기: {filepath}")
            else:
                messagebox.showerror("에러", "CSV 내보내기 실패")

    # ============ 검색 기능 ============

    def _search_addresses(self):
        """주소 검색"""
        keyword = self.search_var.get().strip()
        if not keyword:
            messagebox.showwarning("경고", "검색어를 입력하세요")
            return

        # 검색 유형 매핑
        search_type_map = {
            '전체': 'all',
            '수취인': 'name',
            '전화번호': 'phone',
            '주소': 'address'
        }
        search_type = search_type_map.get(self.search_type_var.get(), 'all')

        # 검색 실행
        results = self.db.search_addresses(keyword, search_type)

        # 결과 표시
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)

        for addr in results:
            self.search_tree.insert('', 'end', values=(
                addr['id'],
                addr['postal_code'] or '',
                addr['receiver_name'],
                addr['phone_number'] or '',
                addr['full_address'] or addr['basic_address']
            ))

        self.status_var.set(f"검색 완료: {len(results)}개 결과")

    def _reset_search(self):
        """검색 초기화"""
        self.search_var.set('')
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)

    # ============ 통계 ============

    def _update_statistics(self):
        """통계 업데이트"""
        stats = self.db.get_statistics()

        self.stat_labels['total_addresses'].config(text=str(stats['total_addresses']))
        self.stat_labels['total_parcels'].config(text=str(stats['total_parcels']))
        self.stat_labels['total_lots'].config(text=str(stats['total_lots']))

    # ============ PHASE 2: 바코드/QR & 라벨 인쇄 ============

    def _setup_barcode_tab(self, notebook, fonts):
        """탭 5: 바코드/QR 코드 생성 & 라벨 인쇄"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="바코드/QR (PHASE 2)")

        # 상단: 송장번호 입력
        input_frame = ttk.LabelFrame(frame, text="송장 정보", padding=5)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(input_frame, text="송장번호:").pack(side=tk.LEFT, padx=5)
        self.tracking_var = tk.StringVar()
        tracking_input = ttk.Entry(input_frame, textvariable=self.tracking_var, width=30)
        tracking_input.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Label(input_frame, text="택배사:").pack(side=tk.LEFT, padx=5)
        self.carrier_var = tk.StringVar(value="CJ")
        carrier_combo = ttk.Combobox(
            input_frame,
            textvariable=self.carrier_var,
            values=["CJ", "LOGEN", "HANJIN", "EPOST", "DHL"],
            state='readonly',
            width=15
        )
        carrier_combo.pack(side=tk.LEFT, padx=5)

        # 중앙: 바코드 생성 버튼
        button_frame = ttk.LabelFrame(frame, text="생성 옵션", padding=5)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            button_frame,
            text="QR코드 생성",
            command=self._generate_qr_code
        ).pack(side=tk.LEFT, padx=5, pady=3)

        ttk.Button(
            button_frame,
            text="바코드 생성",
            command=self._generate_barcode
        ).pack(side=tk.LEFT, padx=5, pady=3)

        ttk.Button(
            button_frame,
            text="라벨 생성",
            command=self._generate_label
        ).pack(side=tk.LEFT, padx=5, pady=3)

        ttk.Button(
            button_frame,
            text="프린터 테스트",
            command=self._test_printer
        ).pack(side=tk.LEFT, padx=5, pady=3)

        # 프린터 상태
        ttk.Label(button_frame, text="프린터:", font=fonts['text']).pack(side=tk.LEFT, padx=10)
        self.printer_status_var = tk.StringVar(value="연결 안 됨")
        ttk.Label(
            button_frame,
            textvariable=self.printer_status_var,
            foreground="#CC0000"
        ).pack(side=tk.LEFT, padx=5)

        # 하단: 미리보기
        ttk.Label(frame, text="생성된 이미지 미리보기", font=fonts['title']).pack(anchor=tk.W, padx=5, pady=3)

        preview_frame = ttk.Frame(frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)

        self.barcode_canvas = tk.Canvas(preview_frame, bg="white", width=400, height=300)
        self.barcode_canvas.pack(fill=tk.BOTH, expand=True)

    def _generate_qr_code(self):
        """QR코드 생성"""
        if not self.current_parcel_info:
            messagebox.showwarning("경고", "먼저 주소 정보를 스캔하세요")
            return

        try:
            self.status_var.set("QR코드 생성 중...")
            self.root.update()

            # QR코드 생성
            qr_path = self.barcode_gen.generate_qr_code(self.current_parcel_info)

            # 미리보기
            qr_image = Image.open(qr_path)
            qr_image.thumbnail((300, 300))
            self.qr_photo = ImageTk.PhotoImage(qr_image)
            self.barcode_canvas.create_image(0, 0, image=self.qr_photo, anchor=tk.NW)

            messagebox.showinfo("성공", f"QR코드 생성 완료:\n{qr_path}")
            self.status_var.set(f"QR코드 생성됨: {qr_path}")

        except Exception as e:
            messagebox.showerror("에러", f"QR코드 생성 실패: {e}")
            self.status_var.set("QR코드 생성 실패")

    def _generate_barcode(self):
        """바코드 생성"""
        tracking_number = self.tracking_var.get().strip()

        if not tracking_number:
            messagebox.showwarning("경고", "송장번호를 입력하세요")
            return

        try:
            self.status_var.set("바코드 생성 중...")
            self.root.update()

            # 바코드 생성
            barcode_path = self.barcode_gen.generate_code128_barcode(tracking_number)

            if barcode_path and os.path.exists(barcode_path):
                # 미리보기
                barcode_image = Image.open(barcode_path)
                barcode_image.thumbnail((400, 100))
                self.barcode_photo = ImageTk.PhotoImage(barcode_image)
                self.barcode_canvas.create_image(0, 0, image=self.barcode_photo, anchor=tk.NW)

                self.last_generated_barcode = barcode_path
                messagebox.showinfo("성공", f"바코드 생성 완료:\n{barcode_path}")
                self.status_var.set(f"바코드 생성됨: {barcode_path}")
            else:
                messagebox.showerror("에러", "바코드 생성 실패")

        except Exception as e:
            messagebox.showerror("에러", f"바코드 생성 실패: {e}")
            self.status_var.set("바코드 생성 실패")

    def _generate_label(self):
        """라벨 생성"""
        if not self.current_parcel_info:
            messagebox.showwarning("경고", "먼저 주소 정보를 스캔하세요")
            return

        try:
            self.status_var.set("라벨 생성 중...")
            self.root.update()

            # QR코드 생성
            qr_path = self.barcode_gen.generate_qr_code(self.current_parcel_info)

            # 바코드 생성
            tracking_number = self.tracking_var.get().strip() or "000000000000"
            barcode_path = self.barcode_gen.generate_code128_barcode(tracking_number)

            # 라벨 생성
            label_path = self.barcode_gen.generate_label_image(
                self.current_parcel_info,
                barcode_path,
                qr_path
            )

            # 미리보기
            label_image = Image.open(label_path)
            label_image.thumbnail((300, 400))
            self.label_photo = ImageTk.PhotoImage(label_image)
            self.barcode_canvas.create_image(0, 0, image=self.label_photo, anchor=tk.NW)

            messagebox.showinfo("성공", f"라벨 생성 완료:\n{label_path}")
            self.status_var.set(f"라벨 생성됨: {label_path}")

        except Exception as e:
            messagebox.showerror("에러", f"라벨 생성 실패: {e}")
            self.status_var.set("라벨 생성 실패")

    def _test_printer(self):
        """프린터 테스트"""
        try:
            self.status_var.set("프린터 검색 중...")
            self.root.update()

            # 프린터 검색
            printers = self.xprinter.find_printers()

            if not printers:
                messagebox.showwarning("경고", "연결된 Xprinter를 찾을 수 없습니다")
                self.printer_status_var.set("연결 안 됨")
                return

            # 프린터 연결
            if self.xprinter.connect(0):
                self.printer_status_var.set("연결됨 ✓")
                self.printer_status_var.config(foreground="#00AA00")

                # 초기화
                self.xprinter.initialize()

                # 테스트 인쇄
                if self.xprinter.test_print():
                    messagebox.showinfo("성공", "프린터 테스트 인쇄 완료")
                    self.status_var.set("프린터 테스트 완료")
                else:
                    messagebox.showerror("에러", "프린터 인쇄 실패")

                self.xprinter.disconnect()
            else:
                messagebox.showerror("에러", "프린터 연결 실패")
                self.printer_status_var.set("연결 실패")
                self.printer_status_var.config(foreground="#CC0000")

        except Exception as e:
            messagebox.showerror("에러", f"프린터 테스트 실패: {e}")
            self.status_var.set("프린터 테스트 실패")


if __name__ == "__main__":
    root = tk.Tk()
    app = ParcelAddressScannerApp(root)
    root.mainloop()
