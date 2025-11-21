from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMainWindow, QWidget, QHBoxLayout, QSplitter, QListWidget, 
    QFormLayout, QTextEdit, QCheckBox, QDateEdit, QComboBox,
    QScrollArea, QFrame, QMessageBox, QListWidgetItem, QFileDialog,
    QGraphicsDropShadowEffect, QTabWidget
)
from PyQt6.QtCore import Qt, QDate, QSize
from PyQt6.QtGui import QFont, QIcon, QColor
import database
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Class Log - Login")
        self.setFixedSize(350, 200)
        self.setStyleSheet("background-color: #ffffff;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        title = QLabel("🔒 로그인")
        title.setFont(QFont("Malgun Gothic", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("비밀번호를 입력하세요")
        layout.addWidget(self.password_input)
        
        self.login_btn = QPushButton("로그인")
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.clicked.connect(self.check_password)
        layout.addWidget(self.login_btn)
        
        self.setLayout(layout)
        
        # Default password for demo
        self.correct_password = "1234" 

    def check_password(self):
        if self.password_input.text() == self.correct_password:
            self.accept()
        else:
            QMessageBox.warning(self, "오류", "비밀번호가 틀렸습니다.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Class Log")
        self.resize(1100, 750)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(2)
        
        # Left Panel: Student List
        self.student_panel = StudentListPanel(self)
        splitter.addWidget(self.student_panel)
        
        # Right Panel: Log Area
        self.log_panel = LogPanel(self)
        splitter.addWidget(self.log_panel)
        
        splitter.setSizes([350, 750])
        main_layout.addWidget(splitter)
        
        # Signals
        self.student_panel.student_selected.connect(self.log_panel.load_student)
        self.log_panel.log_added.connect(self.log_panel.refresh_history)

class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("학생 추가")
        self.setFixedSize(350, 300)
        self.setStyleSheet("background-color: #ffffff;")
        
        layout = QFormLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        self.number_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.gender_edit = QComboBox()
        self.gender_edit.addItems(["남", "여"])
        self.memo_edit = QLineEdit()
        
        layout.addRow("번호:", self.number_edit)
        layout.addRow("이름:", self.name_edit)
        layout.addRow("성별:", self.gender_edit)
        layout.addRow("특이사항:", self.memo_edit)
        
        self.save_btn = QPushButton("저장")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_student)
        layout.addRow("", self.save_btn)
        
        self.setLayout(layout)

    def save_student(self):
        try:
            number_text = self.number_edit.text()
            if not number_text:
                 QMessageBox.warning(self, "경고", "번호를 입력해주세요.")
                 return
            number = int(number_text)
            
            name = self.name_edit.text()
            gender = self.gender_edit.currentText()
            memo = self.memo_edit.text()
            
            if not name:
                QMessageBox.warning(self, "경고", "이름을 입력해주세요.")
                return
                
            database.add_student(number, name, gender, memo)
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "오류", "번호는 숫자여야 합니다.")

class LogSearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("상담 기록 검색")
        self.resize(700, 600)
        self.setStyleSheet("background-color: #ffffff;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🔍 상담 기록 검색")
        title.setFont(QFont("Malgun Gothic", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Filter Area
        filter_group = QFrame()
        filter_group.setObjectName("white_bg")
        filter_group.setStyleSheet("#white_bg { border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; }")
        filter_layout = QFormLayout(filter_group)
        filter_layout.setSpacing(12)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("학생 이름을 입력하세요 (부분 검색 가능)")
        
        date_layout = QHBoxLayout()
        self.start_date = QDateEdit(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)
        self.start_date.setMaximumWidth(150)
        self.end_date = QDateEdit(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.setMaximumWidth(150)
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(QLabel("~"))
        date_layout.addWidget(self.end_date)
        date_layout.addStretch()
        
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("상담 내용 키워드 (부분 검색 가능)")
        
        btn_layout = QHBoxLayout()
        self.search_btn = QPushButton("🔍 검색")
        self.search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_btn.setMinimumHeight(35)
        self.search_btn.clicked.connect(self.do_search)
        
        self.clear_btn = QPushButton("초기화")
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.setMinimumHeight(35)
        self.clear_btn.setStyleSheet("background-color: #64748b; color: white;")
        self.clear_btn.clicked.connect(self.clear_filters)
        
        btn_layout.addWidget(self.search_btn)
        btn_layout.addWidget(self.clear_btn)
        
        filter_layout.addRow("👤 학생 이름:", self.name_input)
        filter_layout.addRow("📅 날짜 범위:", date_layout)
        filter_layout.addRow("🔑 내용 키워드:", self.keyword_input)
        filter_layout.addRow("", btn_layout)
        
        layout.addWidget(filter_group)
        
        # Result Count Label
        self.result_count_label = QLabel("검색 결과: 0건")
        self.result_count_label.setFont(QFont("Malgun Gothic", 10))
        self.result_count_label.setStyleSheet("color: #64748b;")
        layout.addWidget(self.result_count_label)
        
        # Result Area
        self.result_list = QListWidget()
        self.result_list.setAlternatingRowColors(True)
        layout.addWidget(self.result_list)
        
        self.setLayout(layout)
        
        # Enter key to search
        self.name_input.returnPressed.connect(self.do_search)
        self.keyword_input.returnPressed.connect(self.do_search)

    def clear_filters(self):
        self.name_input.clear()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.end_date.setDate(QDate.currentDate())
        self.keyword_input.clear()
        self.result_list.clear()
        self.result_count_label.setText("검색 결과: 0건")

    def do_search(self):
        name = self.name_input.text().strip()
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.end_date.date().toString("yyyy-MM-dd")
        keyword = self.keyword_input.text().strip()
        
        # If all filters are empty, show warning
        if not name and not keyword:
            QMessageBox.information(self, "안내", "이름 또는 키워드를 입력해주세요.")
            return
        
        results = database.search_logs_global(name if name else None, start, end, keyword if keyword else None)
        
        self.result_list.clear()
        self.result_count_label.setText(f"검색 결과: {len(results)}건")
        
        if not results:
            item = QListWidgetItem("검색 결과가 없습니다.")
            item.setFlags(Qt.ItemFlag.NoItemFlags)  # Make it non-selectable
            self.result_list.addItem(item)
            return
            
        for log in results:
            important_mark = " ★" if log.get('is_important') else ""
            item_text = f"[{log['date']}] {log['student_name']} ({log.get('student_number', 'N/A')}번) - {log['category']}{important_mark}\n{log['content'][:80]}{'...' if len(log['content']) > 80 else ''}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, log)  # Store full log data
            self.result_list.addItem(item)

class StatisticsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("상담 결과 통계")
        self.resize(900, 700)
        self.setStyleSheet("background-color: #ffffff;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("📊 상담 결과 통계")
        title.setFont(QFont("Malgun Gothic", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Date Filter
        filter_group = QFrame()
        filter_group.setObjectName("white_bg")
        filter_group.setStyleSheet("#white_bg { border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; }")
        filter_layout = QHBoxLayout(filter_group)
        
        filter_layout.addWidget(QLabel("기간:"))
        self.start_date = QDateEdit(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)
        self.start_date.setMaximumWidth(150)
        self.end_date = QDateEdit(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.setMaximumWidth(150)
        
        self.refresh_btn = QPushButton("새로고침")
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.clicked.connect(self.update_statistics)
        
        filter_layout.addWidget(self.start_date)
        filter_layout.addWidget(QLabel("~"))
        filter_layout.addWidget(self.end_date)
        filter_layout.addWidget(self.refresh_btn)
        filter_layout.addStretch()
        
        layout.addWidget(filter_group)
        
        # Tab Widget for different charts
        self.tab_widget = QTabWidget()
        
        # Category Statistics Tab
        self.category_tab = QWidget()
        category_layout = QVBoxLayout(self.category_tab)
        self.category_canvas = FigureCanvas(Figure(figsize=(8, 5)))
        category_layout.addWidget(self.category_canvas)
        self.tab_widget.addTab(self.category_tab, "구분별 통계")
        
        # Student Statistics Tab
        self.student_tab = QWidget()
        student_layout = QVBoxLayout(self.student_tab)
        self.student_canvas = FigureCanvas(Figure(figsize=(8, 5)))
        student_layout.addWidget(self.student_canvas)
        self.tab_widget.addTab(self.student_tab, "학생별 통계")
        
        layout.addWidget(self.tab_widget)
        
        self.setLayout(layout)
        
        # Initial load
        self.update_statistics()
    
    def update_statistics(self):
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.end_date.date().toString("yyyy-MM-dd")
        
        stats = database.get_statistics(start, end)
        
        # Category Statistics
        self.draw_category_chart(stats['by_category'])
        
        # Student Statistics
        self.draw_student_chart(stats['by_student'])
    
    def draw_category_chart(self, data):
        self.category_canvas.figure.clear()
        ax = self.category_canvas.figure.add_subplot(111)
        
        # 한글 폰트 설정
        try:
            plt.rcParams['font.family'] = 'Malgun Gothic'
        except:
            try:
                plt.rcParams['font.family'] = 'NanumGothic'
            except:
                plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.unicode_minus'] = False
        
        if not data:
            ax.text(0.5, 0.5, '데이터가 없습니다', 
                   ha='center', va='center', fontsize=14, fontfamily='Malgun Gothic')
            self.category_canvas.draw()
            return
        
        categories = [item['category'] for item in data]
        counts = [item['count'] for item in data]
        important_counts = [item.get('important_count', 0) for item in data]
        
        x = range(len(categories))
        width = 0.6
        
        bars = ax.bar(x, counts, width, label='전체', color='#2563eb', alpha=0.8)
        bars_important = ax.bar(x, important_counts, width, label='중요', color='#ef4444', alpha=0.8)
        
        ax.set_xlabel('구분', fontsize=12, fontfamily='Malgun Gothic')
        ax.set_ylabel('건수', fontsize=12, fontfamily='Malgun Gothic')
        ax.set_title('구분별 상담 통계', fontsize=14, fontweight='bold', fontfamily='Malgun Gothic')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=0, fontfamily='Malgun Gothic')
        legend = ax.legend(fontsize=10)
        for text in legend.get_texts():
            text.set_fontfamily('Malgun Gothic')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, (bar, count) in enumerate(zip(bars, counts)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{count}',
                   ha='center', va='bottom', fontsize=10)
        
        self.category_canvas.figure.tight_layout()
        self.category_canvas.draw()
    
    def draw_student_chart(self, data):
        self.student_canvas.figure.clear()
        ax = self.student_canvas.figure.add_subplot(111)
        
        # 한글 폰트 설정
        try:
            plt.rcParams['font.family'] = 'Malgun Gothic'
        except:
            try:
                plt.rcParams['font.family'] = 'NanumGothic'
            except:
                plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.unicode_minus'] = False
        
        if not data:
            ax.text(0.5, 0.5, '데이터가 없습니다', 
                   ha='center', va='center', fontsize=14, fontfamily='Malgun Gothic')
            self.student_canvas.draw()
            return
        
        # Limit to top 10
        data = data[:10]
        student_names = [f"{item.get('number', '')}번 {item['name']}" for item in data]
        counts = [item['log_count'] for item in data]
        
        x = range(len(student_names))
        width = 0.6
        
        bars = ax.barh(x, counts, width, color='#10b981', alpha=0.8)
        
        ax.set_xlabel('상담 건수', fontsize=12, fontfamily='Malgun Gothic')
        ax.set_ylabel('학생', fontsize=12, fontfamily='Malgun Gothic')
        ax.set_title('학생별 상담 통계 (상위 10명)', fontsize=14, fontweight='bold', fontfamily='Malgun Gothic')
        ax.set_yticks(x)
        ax.set_yticklabels(student_names, fontfamily='Malgun Gothic')
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels on bars
        for i, (bar, count) in enumerate(zip(bars, counts)):
            width_bar = bar.get_width()
            ax.text(width_bar, bar.get_y() + bar.get_height()/2.,
                   f' {count}',
                   ha='left', va='center', fontsize=10)
        
        self.student_canvas.figure.tight_layout()
        self.student_canvas.draw()

class StudentListPanel(QWidget):
    from PyQt6.QtCore import pyqtSignal
    student_selected = pyqtSignal(int, str) # student_id, student_name

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("학생 목록")
        title.setFont(QFont("Malgun Gothic", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 이름 검색...")
        self.search_input.textChanged.connect(self.filter_students)
        layout.addWidget(self.search_input)
        
        # List
        self.student_list = QListWidget()
        self.student_list.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.student_list)
        
        # Buttons Layout
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("학생 추가")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.clicked.connect(self.open_add_student_dialog)
        btn_layout.addWidget(self.add_btn)
        
        self.import_btn = QPushButton("엑셀 등록")
        self.import_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.import_btn.setStyleSheet("background-color: #10b981;") # Green
        self.import_btn.clicked.connect(self.import_excel)
        btn_layout.addWidget(self.import_btn)
        
        layout.addLayout(btn_layout)
        
        # Search Logs Button
        self.search_logs_btn = QPushButton("🔍 상담 기록 검색")
        self.search_logs_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_logs_btn.setStyleSheet("background-color: #8b5cf6;") # Violet
        self.search_logs_btn.clicked.connect(self.open_search_dialog)
        layout.addWidget(self.search_logs_btn)
        
        # Statistics Button
        self.statistics_btn = QPushButton("📊 상담 통계")
        self.statistics_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.statistics_btn.setStyleSheet("background-color: #f59e0b;") # Amber
        self.statistics_btn.clicked.connect(self.open_statistics_dialog)
        layout.addWidget(self.statistics_btn)
        
        self.export_btn = QPushButton("전체 데이터 엑셀 저장")
        self.export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_btn.setStyleSheet("background-color: #64748b;") # Slate
        self.export_btn.clicked.connect(self.export_excel)
        layout.addWidget(self.export_btn)
        
        self.setLayout(layout)
        self.load_students()

    def load_students(self):
        self.student_list.clear()
        students = database.get_all_students()
        for s in students:
            item_text = f"{s['number']}번 {s['name']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, s['id'])
            item.setData(Qt.ItemDataRole.UserRole + 1, s['name'])
            self.student_list.addItem(item)

    def filter_students(self, text):
        self.student_list.clear()
        if text:
            students = database.search_students(text)
        else:
            students = database.get_all_students()
            
        for s in students:
            item_text = f"{s['number']}번 {s['name']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, s['id'])
            item.setData(Qt.ItemDataRole.UserRole + 1, s['name'])
            self.student_list.addItem(item)

    def on_item_clicked(self, item):
        student_id = item.data(Qt.ItemDataRole.UserRole)
        student_name = item.data(Qt.ItemDataRole.UserRole + 1)
        self.student_selected.emit(student_id, student_name)

    def open_add_student_dialog(self):
        dialog = AddStudentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_students()

    def open_search_dialog(self):
        dialog = LogSearchDialog(self)
        dialog.exec()
    
    def open_statistics_dialog(self):
        dialog = StatisticsDialog(self)
        dialog.exec()

    def import_excel(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "학생 명단 엑셀 불러오기", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            try:
                df = pd.read_excel(file_name)
                required = ['번호', '이름']
                if not all(col in df.columns for col in required):
                    QMessageBox.warning(self, "오류", "엑셀 파일에 '번호', '이름' 컬럼이 있어야 합니다.")
                    return
                
                count = 0
                for _, row in df.iterrows():
                    number = row['번호']
                    name = row['이름']
                    gender = row.get('성별', '')
                    memo = row.get('특이사항', '')
                    database.add_student(number, name, gender, memo)
                    count += 1
                
                QMessageBox.information(self, "완료", f"{count}명의 학생이 등록되었습니다.")
                self.load_students()
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일을 읽는 중 오류가 발생했습니다:\n{str(e)}")

    def export_excel(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "데이터 내보내기", "class_log_export.xlsx", "Excel Files (*.xlsx)")
        if file_name:
            try:
                conn = database.get_connection()
                df_logs = pd.read_sql_query("SELECT * FROM counsel_logs", conn)
                df_students_raw = pd.read_sql_query("SELECT * FROM students", conn)
                conn.close()
                
                with pd.ExcelWriter(file_name) as writer:
                    df_students_raw.to_excel(writer, sheet_name='Students', index=False)
                    df_logs.to_excel(writer, sheet_name='Counsel_Logs', index=False)
                    
                QMessageBox.information(self, "완료", "데이터가 성공적으로 내보내졌습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"내보내기 중 오류가 발생했습니다:\n{str(e)}")

class LogPanel(QWidget):
    from PyQt6.QtCore import pyqtSignal
    log_added = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_student_id = None
        self.current_student_name = None
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 0, 0, 0)
        layout.setSpacing(15)
        
        # Header
        self.header_label = QLabel("학생을 선택해주세요")
        self.header_label.setFont(QFont("Malgun Gothic", 18, QFont.Weight.Bold))
        self.header_label.setStyleSheet("color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(self.header_label)
        
        # Input Form
        self.form_group = QFrame()
        self.form_group.setObjectName("white_bg")
        self.form_group.setFrameShape(QFrame.Shape.StyledPanel)
        self.form_group.setStyleSheet("#white_bg { border: 1px solid #e2e8f0; }")
        
        form_layout = QFormLayout()
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)
        
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumWidth(150)
        
        self.category_combo = QComboBox()
        self.category_combo.addItems(["생활", "학습", "학부모", "교우", "기타"])
        self.category_combo.setMinimumWidth(150)
        
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("상담 내용을 입력하세요...")
        self.content_edit.setMaximumHeight(100)
        
        self.important_check = QCheckBox("중요 (★)")
        self.important_check.setStyleSheet("font-weight: bold; color: #ef4444;")
        
        self.save_btn = QPushButton("기록 저장")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setMinimumHeight(40)
        self.save_btn.clicked.connect(self.save_log)
        
        form_layout.addRow("날짜", self.date_edit)
        form_layout.addRow("구분", self.category_combo)
        form_layout.addRow("내용", self.content_edit)
        form_layout.addRow("", self.important_check)
        form_layout.addRow("", self.save_btn)
        
        self.form_group.setLayout(form_layout)
        
        # Shadow for form
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 15))
        shadow.setOffset(0, 4)
        self.form_group.setGraphicsEffect(shadow)
        
        layout.addWidget(self.form_group)
        
        # History Area with Filter
        history_header = QHBoxLayout()
        history_label = QLabel("상담 이력")
        history_label.setFont(QFont("Malgun Gothic", 12, QFont.Weight.Bold))
        history_header.addWidget(history_label)
        
        # Date Filter
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("날짜 필터:"))
        
        self.filter_start_date = QDateEdit()
        self.filter_start_date.setCalendarPopup(True)
        self.filter_start_date.setDate(QDate.currentDate().addMonths(-1))
        self.filter_start_date.setMaximumWidth(120)
        
        self.filter_end_date = QDateEdit()
        self.filter_end_date.setCalendarPopup(True)
        self.filter_end_date.setDate(QDate.currentDate())
        self.filter_end_date.setMaximumWidth(120)
        
        self.filter_btn = QPushButton("적용")
        self.filter_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.filter_btn.setMaximumWidth(60)
        self.filter_btn.clicked.connect(self.refresh_history)
        
        self.clear_filter_btn = QPushButton("초기화")
        self.clear_filter_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_filter_btn.setMaximumWidth(60)
        self.clear_filter_btn.clicked.connect(self.clear_filter)
        
        filter_layout.addWidget(self.filter_start_date)
        filter_layout.addWidget(QLabel("~"))
        filter_layout.addWidget(self.filter_end_date)
        filter_layout.addWidget(self.filter_btn)
        filter_layout.addWidget(self.clear_filter_btn)
        filter_layout.addStretch()
        
        history_header.addLayout(filter_layout)
        
        history_header_widget = QWidget()
        history_header_widget.setLayout(history_header)
        layout.addWidget(history_header_widget)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.history_container = QWidget()
        self.history_layout = QVBoxLayout(self.history_container)
        self.history_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.history_layout.setSpacing(10)
        self.history_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area.setWidget(self.history_container)
        
        layout.addWidget(self.scroll_area)
        
        self.setLayout(layout)
        
        # Disable input until student selected
        self.form_group.setEnabled(False)

    def load_student(self, student_id, student_name):
        self.current_student_id = student_id
        self.current_student_name = student_name
        self.header_label.setText(f"{student_name} 학생 상담 기록")
        self.form_group.setEnabled(True)
        self.refresh_history()

    def save_log(self):
        if not self.current_student_id:
            return
        
        content = self.content_edit.toPlainText()
        if not content.strip():
            QMessageBox.warning(self, "경고", "내용을 입력해주세요.")
            return
            
        date = self.date_edit.date().toString("yyyy-MM-dd")
        category = self.category_combo.currentText()
        is_important = self.important_check.isChecked()
        
        database.add_log(self.current_student_id, date, category, content, is_important)
        
        self.content_edit.clear()
        self.important_check.setChecked(False)
        self.log_added.emit()
        QMessageBox.information(self, "성공", "저장되었습니다.")

    def clear_filter(self):
        self.filter_start_date.setDate(QDate.currentDate().addMonths(-1))
        self.filter_end_date.setDate(QDate.currentDate())
        self.refresh_history()

    def refresh_history(self):
        # Clear existing items
        while self.history_layout.count():
            child = self.history_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not self.current_student_id:
            return
        
        # Get date range from filters
        start_date = self.filter_start_date.date().toString("yyyy-MM-dd")
        end_date = self.filter_end_date.date().toString("yyyy-MM-dd")
            
        logs = database.get_logs_by_student(self.current_student_id, start_date, end_date)
        for log in logs:
            card = LogCard(log, self)
            self.history_layout.addWidget(card)

class LogCard(QFrame):
    def __init__(self, log_data, parent_panel=None):
        super().__init__()
        self.setObjectName("log_card")
        self.log_id = log_data['id']
        self.parent_panel = parent_panel
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Header: Date | Category | Important | Delete Button
        header_layout = QHBoxLayout()
        
        date_lbl = QLabel(log_data['date'])
        date_lbl.setObjectName("date_label")
        
        cat_lbl = QLabel(log_data['category'])
        cat_lbl.setObjectName("category_label")
        
        header_layout.addWidget(date_lbl)
        header_layout.addWidget(cat_lbl)
        
        if log_data['is_important']:
            imp_lbl = QLabel("★ 중요")
            imp_lbl.setObjectName("important_label")
            header_layout.addWidget(imp_lbl)
            
        header_layout.addStretch()
        
        # Delete Button
        delete_btn = QPushButton("삭제")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setMaximumWidth(50)
        delete_btn.setMaximumHeight(25)
        delete_btn.setStyleSheet("background-color: #ef4444; color: white; font-size: 11px; padding: 2px 8px;")
        delete_btn.clicked.connect(self.delete_log)
        header_layout.addWidget(delete_btn)
        
        layout.addLayout(header_layout)
        
        # Content
        content_lbl = QLabel(log_data['content'])
        content_lbl.setWordWrap(True)
        content_lbl.setStyleSheet("font-size: 14px; line-height: 1.4;")
        layout.addWidget(content_lbl)
        
        self.setLayout(layout)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
    
    def delete_log(self):
        reply = QMessageBox.question(
            self, 
            '삭제 확인', 
            '이 상담 기록을 삭제하시겠습니까?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            database.delete_log(self.log_id)
            if self.parent_panel:
                self.parent_panel.refresh_history()
            QMessageBox.information(self, "완료", "상담 기록이 삭제되었습니다.")
