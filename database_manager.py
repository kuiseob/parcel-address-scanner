import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Tuple
from pathlib import Path
from parcel_info_parser import ParcelInfo


class DatabaseManager:
    """SQLite 데이터베이스 관리"""

    def __init__(self, db_path: str = "parcel_database.db"):
        self.db_path = db_path
        self.connection = None
        self._init_database()

    def _init_database(self):
        """데이터베이스 초기화"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        """테이블 생성"""
        cursor = self.connection.cursor()

        # 주소록 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS addresses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                postal_code TEXT,
                receiver_name TEXT NOT NULL,
                phone_number TEXT,
                basic_address TEXT NOT NULL,
                detail_address TEXT,
                full_address TEXT,
                source TEXT DEFAULT 'camera',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(postal_code, receiver_name, basic_address)
            )
        ''')

        # 송장 정보 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parcels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_number TEXT UNIQUE NOT NULL,
                address_id INTEGER,
                carrier TEXT,
                status TEXT DEFAULT 'pending',
                barcode_url TEXT,
                qrcode_url TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(address_id) REFERENCES addresses(id)
            )
        ''')

        # LOT 추적 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lot_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lot_number TEXT UNIQUE NOT NULL,
                total_count INTEGER DEFAULT 0,
                sent_count INTEGER DEFAULT 0,
                delivered_count INTEGER DEFAULT 0,
                failed_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # LOT-송장 매핑 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lot_parcels (
                lot_id INTEGER,
                parcel_id INTEGER,
                PRIMARY KEY(lot_id, parcel_id),
                FOREIGN KEY(lot_id) REFERENCES lot_tracking(id),
                FOREIGN KEY(parcel_id) REFERENCES parcels(id)
            )
        ''')

        # 인덱스 생성 (성능 향상)
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_receiver_name ON addresses(receiver_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_phone ON addresses(phone_number)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tracking ON parcels(tracking_number)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_lot ON lot_tracking(lot_number)')

        self.connection.commit()

    def add_address(self, parcel_info: ParcelInfo, source: str = 'camera') -> Optional[int]:
        """
        주소 추가 (중복 방지)
        반환: 추가된 행의 ID 또는 None
        """
        try:
            cursor = self.connection.cursor()

            cursor.execute('''
                INSERT INTO addresses (
                    postal_code, receiver_name, phone_number,
                    basic_address, detail_address, full_address, source
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                parcel_info.postal_code,
                parcel_info.receiver_name,
                parcel_info.phone_number,
                parcel_info.address,
                parcel_info.detail_address,
                parcel_info.full_address,
                source
            ))

            self.connection.commit()
            return cursor.lastrowid

        except sqlite3.IntegrityError:
            # 중복 주소
            return None
        except Exception as e:
            print(f"주소 추가 오류: {e}")
            return None

    def get_address(self, address_id: int) -> Optional[Dict]:
        """ID로 주소 조회"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM addresses WHERE id = ?', (address_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_addresses(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """모든 주소 조회 (페이지네이션)"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT * FROM addresses
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        return [dict(row) for row in cursor.fetchall()]

    def search_addresses(self, keyword: str, search_type: str = 'all') -> List[Dict]:
        """
        주소 검색
        search_type: 'all', 'name', 'phone', 'address'
        """
        cursor = self.connection.cursor()
        keyword = f"%{keyword}%"

        if search_type == 'name':
            cursor.execute(
                'SELECT * FROM addresses WHERE receiver_name LIKE ? ORDER BY created_at DESC',
                (keyword,)
            )
        elif search_type == 'phone':
            cursor.execute(
                'SELECT * FROM addresses WHERE phone_number LIKE ? ORDER BY created_at DESC',
                (keyword,)
            )
        elif search_type == 'address':
            cursor.execute(
                'SELECT * FROM addresses WHERE full_address LIKE ? ORDER BY created_at DESC',
                (keyword,)
            )
        else:  # all
            cursor.execute('''
                SELECT * FROM addresses WHERE
                receiver_name LIKE ? OR phone_number LIKE ? OR full_address LIKE ?
                ORDER BY created_at DESC
            ''', (keyword, keyword, keyword))

        return [dict(row) for row in cursor.fetchall()]

    def update_address(self, address_id: int, parcel_info: ParcelInfo) -> bool:
        """주소 업데이트"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE addresses SET
                    postal_code = ?,
                    receiver_name = ?,
                    phone_number = ?,
                    basic_address = ?,
                    detail_address = ?,
                    full_address = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (
                parcel_info.postal_code,
                parcel_info.receiver_name,
                parcel_info.phone_number,
                parcel_info.address,
                parcel_info.detail_address,
                parcel_info.full_address,
                address_id
            ))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"주소 업데이트 오류: {e}")
            return False

    def delete_address(self, address_id: int) -> bool:
        """주소 삭제"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM addresses WHERE id = ?', (address_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"주소 삭제 오류: {e}")
            return False

    def get_address_count(self) -> int:
        """전체 주소 개수"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM addresses')
        return cursor.fetchone()[0]

    # ============ 송장 관리 ============

    def add_parcel(self, tracking_number: str, address_id: int,
                   carrier: str = 'unknown') -> Optional[int]:
        """송장 추가"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO parcels (tracking_number, address_id, carrier)
                VALUES (?, ?, ?)
            ''', (tracking_number, address_id, carrier))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        except Exception as e:
            print(f"송장 추가 오류: {e}")
            return None

    def get_parcel(self, parcel_id: int) -> Optional[Dict]:
        """송장 조회"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM parcels WHERE id = ?', (parcel_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_parcel_status(self, parcel_id: int, status: str) -> bool:
        """송장 상태 업데이트"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE parcels SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, parcel_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"송장 상태 업데이트 오류: {e}")
            return False

    # ============ LOT 추적 ============

    def create_lot(self, lot_number: str) -> Optional[int]:
        """새 LOT 생성"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO lot_tracking (lot_number)
                VALUES (?)
            ''', (lot_number,))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def add_parcel_to_lot(self, lot_id: int, parcel_id: int) -> bool:
        """LOT에 송장 추가"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO lot_parcels (lot_id, parcel_id)
                VALUES (?, ?)
            ''', (lot_id, parcel_id))

            # LOT 개수 업데이트
            cursor.execute('''
                UPDATE lot_tracking SET
                    total_count = total_count + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (lot_id,))

            self.connection.commit()
            return True
        except Exception as e:
            print(f"LOT 송장 추가 오류: {e}")
            return False

    def get_lot(self, lot_id: int) -> Optional[Dict]:
        """LOT 정보 조회"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM lot_tracking WHERE id = ?', (lot_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_lots(self) -> List[Dict]:
        """모든 LOT 조회"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM lot_tracking ORDER BY created_at DESC')
        return [dict(row) for row in cursor.fetchall()]

    def get_lot_parcels(self, lot_id: int) -> List[Dict]:
        """LOT의 모든 송장 조회"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT p.* FROM parcels p
            JOIN lot_parcels lp ON p.id = lp.parcel_id
            WHERE lp.lot_id = ?
        ''', (lot_id,))
        return [dict(row) for row in cursor.fetchall()]

    def update_lot_status(self, lot_id: int, status: str) -> bool:
        """LOT 상태 업데이트"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE lot_tracking SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, lot_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"LOT 상태 업데이트 오류: {e}")
            return False

    # ============ 통계 ============

    def get_statistics(self) -> Dict:
        """통계 조회"""
        cursor = self.connection.cursor()

        # 주소 통계
        cursor.execute('SELECT COUNT(*) FROM addresses')
        total_addresses = cursor.fetchone()[0]

        # 송장 통계
        cursor.execute('SELECT COUNT(*) FROM parcels')
        total_parcels = cursor.fetchone()[0]

        cursor.execute('''
            SELECT status, COUNT(*) as count FROM parcels
            GROUP BY status
        ''')
        parcel_by_status = {row['status']: row['count'] for row in cursor.fetchall()}

        # LOT 통계
        cursor.execute('SELECT COUNT(*) FROM lot_tracking')
        total_lots = cursor.fetchone()[0]

        cursor.execute('''
            SELECT status, COUNT(*) as count FROM lot_tracking
            GROUP BY status
        ''')
        lot_by_status = {row['status']: row['count'] for row in cursor.fetchall()}

        return {
            'total_addresses': total_addresses,
            'total_parcels': total_parcels,
            'parcel_by_status': parcel_by_status,
            'total_lots': total_lots,
            'lot_by_status': lot_by_status
        }

    # ============ 유틸리티 ============

    def export_to_csv(self, filepath: str) -> bool:
        """주소록을 CSV로 내보내기"""
        try:
            import csv
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM addresses ORDER BY created_at DESC')

            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    '우편번호', '수취인', '전화번호',
                    '기본주소', '상세주소', '전체주소', '등록일시'
                ])

                for row in cursor.fetchall():
                    writer.writerow([
                        row['postal_code'],
                        row['receiver_name'],
                        row['phone_number'],
                        row['basic_address'],
                        row['detail_address'],
                        row['full_address'],
                        row['created_at']
                    ])

            return True
        except Exception as e:
            print(f"CSV 내보내기 오류: {e}")
            return False

    def close(self):
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()

    def __del__(self):
        """소멸자"""
        self.close()
