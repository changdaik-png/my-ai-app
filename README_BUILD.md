# My Class Log - EXE 빌드 가이드

## 빌드 방법

### 방법 1: 배치 파일 사용 (권장)

1. `build_exe.bat` 파일을 더블클릭하여 실행
2. 빌드가 완료되면 `dist` 폴더에 `MyClassLog.exe` 파일이 생성됩니다

### 방법 2: 수동 빌드

명령 프롬프트에서 다음 명령어를 실행:

```bash
cd my_class_log
pip install -r requirements.txt
pyinstaller --name="MyClassLog" --onefile --windowed --noconsole main.py
```

## 필요한 패키지

- PyQt6
- pandas
- openpyxl
- matplotlib
- pyinstaller

## 주의사항

1. 빌드 전에 `requirements.txt`에 명시된 모든 패키지가 설치되어 있어야 합니다
2. EXE 파일은 `dist` 폴더에 생성됩니다
3. EXE 파일을 다른 컴퓨터에서 실행하려면 해당 컴퓨터에 Python이 설치되어 있지 않아도 됩니다
4. 데이터베이스 파일(`class_log.db`)은 프로그램 실행 시 자동으로 생성됩니다

## 문제 해결

### 한글 폰트가 깨지는 경우
- Windows 시스템에 'Malgun Gothic' 폰트가 설치되어 있는지 확인하세요
- 그래프의 한글 폰트는 자동으로 설정됩니다

### EXE 파일이 실행되지 않는 경우
- Windows Defender나 백신 프로그램이 차단하는지 확인하세요
- 관리자 권한으로 실행해보세요


