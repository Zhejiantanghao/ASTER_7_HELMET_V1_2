@echo off
chcp 65001 >nul
cd /d "%~dp0.."
py -m pip install -r scripts\requirements.txt
if errorlevel 1 goto err
py scripts\acquire_sources.py fetch-all
py scripts\acquire_sources.py report
py scripts\sync_reference_md.py
echo.
echo 候选图位于 references\_incoming，需要逐张打开核对后 approve。
echo 未审核的图片不会作为正式参考图。
pause
exit /b 0
:err
echo 请检查 Python 及网络连接。
pause
exit /b 1
