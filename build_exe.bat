@echo off
chcp 65001 >nul
echo ========================================
echo   My Class Log - EXE 빌드 스크립트
echo ========================================
echo.

REM 현재 디렉토리로 이동
cd /d "%~dp0"

REM 가상환경 활성화 (있는 경우)
if exist venv\Scripts\activate.bat (
    echo 가상환경 활성화 중...
    call venv\Scripts\activate.bat
)

REM 필요한 패키지 설치 확인
echo.
echo 필요한 패키지 설치 확인 중...
pip install -r requirements.txt --quiet

echo.
echo PyInstaller로 EXE 파일 생성 중...
echo (이 작업은 몇 분 정도 소요될 수 있습니다...)
echo.

REM 기존 빌드 파일 정리
if exist build (
    rmdir /s /q build
)
if exist dist (
    rmdir /s /q dist
)

REM PyInstaller로 exe 파일 생성
pyinstaller --name="MyClassLog" ^
    --onefile ^
    --windowed ^
    --noconsole ^
    --hidden-import=PyQt6 ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=matplotlib ^
    --hidden-import=matplotlib.backends.backend_qt5agg ^
    --hidden-import=pandas ^
    --hidden-import=openpyxl ^
    --hidden-import=sqlite3 ^
    --collect-all=matplotlib ^
    --collect-all=PyQt6 ^
    --collect-submodules=matplotlib ^
    main.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   빌드 완료!
    echo ========================================
    echo.
    echo EXE 파일 위치: dist\MyClassLog.exe
    echo.
    echo 빌드 폴더 정리 중...
    if exist build (
        rmdir /s /q build
    )
    if exist MyClassLog.spec (
        del /q MyClassLog.spec
    )
    echo.
    echo 완료! dist 폴더에서 MyClassLog.exe를 확인하세요.
) else (
    echo.
    echo ========================================
    echo   빌드 실패!
    echo ========================================
    echo 오류가 발생했습니다. 위의 오류 메시지를 확인하세요.
)

echo.
pause

