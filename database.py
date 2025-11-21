import sqlite3
import os
from datetime import datetime

DB_PATH = 'class_log.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Students Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number INTEGER,
        name TEXT NOT NULL,
        gender TEXT,
        memo TEXT
    )
    ''')
    
    # Counsel Logs Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS counsel_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        category TEXT,
        content TEXT,
        is_important INTEGER DEFAULT 0,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    ''')
    
    conn.commit()
    conn.close()

# --- Student CRUD ---
def add_student(number, name, gender='', memo=''):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (number, name, gender, memo) VALUES (?, ?, ?, ?)', 
                   (number, name, gender, memo))
    conn.commit()
    conn.close()

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students ORDER BY number ASC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def search_students(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE name LIKE ? ORDER BY number ASC', (f'%{keyword}%',))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_student(student_id, number, name, gender, memo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE students 
        SET number = ?, name = ?, gender = ?, memo = ?
        WHERE id = ?
    ''', (number, name, gender, memo, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM counsel_logs WHERE student_id = ?', (student_id,))
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()

# --- Log CRUD ---
def add_log(student_id, date, category, content, is_important):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO counsel_logs (student_id, date, category, content, is_important) 
        VALUES (?, ?, ?, ?, ?)
    ''', (student_id, date, category, content, 1 if is_important else 0))
    conn.commit()
    conn.close()

def get_logs_by_student(student_id, start_date=None, end_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT * FROM counsel_logs 
        WHERE student_id = ?
    '''
    params = [student_id]
    
    if start_date:
        query += ' AND date >= ?'
        params.append(start_date)
    
    if end_date:
        query += ' AND date <= ?'
        params.append(end_date)
    
    query += ' ORDER BY date DESC, id DESC'
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_log(log_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM counsel_logs WHERE id = ?', (log_id,))
    conn.commit()
    conn.close()

def search_logs_global(student_name=None, start_date=None, end_date=None, keyword=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    # 학생 이름으로 먼저 필터링된 학생 ID 목록을 가져옴
    student_ids = None
    if student_name:
        cursor.execute('SELECT id FROM students WHERE name LIKE ?', (f'%{student_name}%',))
        student_ids = [row[0] for row in cursor.fetchall()]
        if not student_ids:
            # 해당 이름의 학생이 없으면 빈 결과 반환
            conn.close()
            return []
    
    query = '''
        SELECT l.*, s.name as student_name, s.number as student_number
        FROM counsel_logs l
        INNER JOIN students s ON l.student_id = s.id
        WHERE 1=1
    '''
    params = []
    
    # 학생 이름 필터링 (정확한 학생 ID로 필터링)
    if student_ids:
        placeholders = ','.join(['?'] * len(student_ids))
        query += f' AND l.student_id IN ({placeholders})'
        params.extend(student_ids)
        
    if start_date:
        query += ' AND l.date >= ?'
        params.append(start_date)
        
    if end_date:
        query += ' AND l.date <= ?'
        params.append(end_date)
        
    # 키워드는 내용에서만 검색 (학생 이름과 혼동 방지)
    if keyword:
        query += ' AND l.content LIKE ?'
        params.append(f'%{keyword}%')
        
    query += ' ORDER BY l.date DESC, l.id DESC'
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_statistics(start_date=None, end_date=None):
    """상담 통계 데이터 가져오기"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            l.category,
            COUNT(*) as count,
            SUM(CASE WHEN l.is_important = 1 THEN 1 ELSE 0 END) as important_count
        FROM counsel_logs l
        WHERE 1=1
    '''
    params = []
    
    if start_date:
        query += ' AND l.date >= ?'
        params.append(start_date)
        
    if end_date:
        query += ' AND l.date <= ?'
        params.append(end_date)
    
    query += ' GROUP BY l.category ORDER BY count DESC'
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    # 학생별 통계
    query_student = '''
        SELECT 
            s.name,
            s.number,
            COUNT(l.id) as log_count
        FROM students s
        LEFT JOIN counsel_logs l ON s.id = l.student_id
    '''
    params_student = []
    where_clauses = []
    
    if start_date:
        where_clauses.append('l.date >= ?')
        params_student.append(start_date)
    if end_date:
        where_clauses.append('l.date <= ?')
        params_student.append(end_date)
    
    if where_clauses:
        query_student += ' WHERE ' + ' AND '.join(where_clauses)
    
    query_student += ' GROUP BY s.id, s.name, s.number HAVING COUNT(l.id) > 0 ORDER BY log_count DESC LIMIT 10'
    
    cursor.execute(query_student, params_student)
    student_rows = cursor.fetchall()
    
    conn.close()
    
    return {
        'by_category': [dict(row) for row in rows],
        'by_student': [dict(row) for row in student_rows]
    }

# Initialize DB on module load (or explicit call)
if __name__ == '__main__':
    init_db()
    print("Database initialized.")
