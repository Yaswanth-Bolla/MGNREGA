import sqlite3
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

class DistrictPerformance:
    def __init__(self, id: str, district: str, state: str, year: int, month: int,
                 person_days_generated: float, total_expenditure: float,
                 avg_days_of_employment: float, work_completion_rate: float,
                 total_households_completed_100_days: int, female_participation_rate: float):
        self.id = id
        self.district = district
        self.state = state
        self.year = year
        self.month = month
        self.person_days_generated = person_days_generated
        self.total_expenditure = total_expenditure
        self.avg_days_of_employment = avg_days_of_employment
        self.work_completion_rate = work_completion_rate
        self.total_households_completed_100_days = total_households_completed_100_days
        self.female_participation_rate = female_participation_rate

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'district': self.district,
            'state': self.state,
            'year': self.year,
            'month': self.month,
            'person_days_generated': self.person_days_generated,
            'total_expenditure': self.total_expenditure,
            'avg_days_of_employment': self.avg_days_of_employment,
            'work_completion_rate': self.work_completion_rate,
            'total_households_completed_100_days': self.total_households_completed_100_days,
            'female_participation_rate': self.female_participation_rate,
        }

class MGNREGADatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database and create tables if they don't exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS district_performance (
                    id TEXT PRIMARY KEY,
                    district TEXT NOT NULL,
                    state TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    person_days_generated REAL,
                    total_expenditure REAL,
                    avg_days_of_employment REAL,
                    work_completion_rate REAL,
                    total_households_completed_100_days INTEGER,
                    female_participation_rate REAL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            ''')

            conn.execute('CREATE INDEX IF NOT EXISTS idx_district_year_month ON district_performance(district, year, month);')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_state_year ON district_performance(state, year);')

    def insert_performance(self, data: DistrictPerformance):
        """Insert or replace performance data."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO district_performance
                (id, district, state, year, month, person_days_generated, total_expenditure,
                 avg_days_of_employment, work_completion_rate, total_households_completed_100_days,
                 female_participation_rate, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.id,
                data.district,
                data.state,
                data.year,
                data.month,
                data.person_days_generated,
                data.total_expenditure,
                data.avg_days_of_employment,
                data.work_completion_rate,
                data.total_households_completed_100_days,
                data.female_participation_rate,
                datetime.now()
            ))

    def get_all_performance(self) -> List[DistrictPerformance]:
        """Get all performance data."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute('SELECT id, district, state, year, month, person_days_generated, total_expenditure, avg_days_of_employment, work_completion_rate, total_households_completed_100_days, female_participation_rate FROM district_performance ORDER BY district, year, month').fetchall()

        return [DistrictPerformance(*row) for row in rows]

    def get_performance_by_district(self, district: str) -> List[DistrictPerformance]:
        """Get performance data for a specific district."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                'SELECT id, district, state, year, month, person_days_generated, total_expenditure, avg_days_of_employment, work_completion_rate, total_households_completed_100_days, female_participation_rate FROM district_performance WHERE district = ? ORDER BY year, month',
                (district,)
            ).fetchall()

        return [DistrictPerformance(*row) for row in rows]

    def get_performance_by_state(self, state: str) -> List[DistrictPerformance]:
        """Get performance data for a specific state."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                'SELECT id, district, state, year, month, person_days_generated, total_expenditure, avg_days_of_employment, work_completion_rate, total_households_completed_100_days, female_participation_rate FROM district_performance WHERE state = ? ORDER BY district, year, month',
                (state,)
            ).fetchall()

        return [DistrictPerformance(*row) for row in rows]

    def get_districts(self) -> List[str]:
        """Get list of all districts."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute('SELECT DISTINCT district FROM district_performance ORDER BY district').fetchall()

        return [row[0] for row in rows]

    def close(self):
        """Close database connection (SQLite handles this automatically, but kept for compatibility)."""
        pass
