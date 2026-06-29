@echo off
chcp 65001 >nul
REM =====================================================
REM   Icon 裁剪工具 - 一键打包脚本
REM   生成 dist\Icon裁剪工具.exe （单文件、内嵌HTML、带图标）
REM =====================================================

echo [1/4] 检查 PyInstaller ...
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo     未安装，正在使用国内镜像安装 PyInstaller ...
    python -m pip install pyinstaller -i https://mirrors.tencent.com/pypi/simple/
    if errorlevel 1 (
        echo [ERROR] PyInstaller 安装失败
        pause
        exit /b 1
    )
)

echo [2/4] 清理旧的构建产物 ...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [3/4] 开始打包（会花十几秒到一分钟）...
REM 直接使用版本受控的 .spec 文件打包，保证配置唯一、可复现
python -m PyInstaller --noconfirm --clean "Icon裁剪工具.spec"

if errorlevel 1 (
    echo [ERROR] 打包失败
    pause
    exit /b 1
)

echo [4/4] 打包完成！
echo.
echo    产物位置： dist\Icon裁剪工具.exe
echo.
if exist "dist\Icon裁剪工具.exe" (
    for %%F in ("dist\Icon裁剪工具.exe") do echo    文件大小： %%~zF 字节
)
echo.
pause
