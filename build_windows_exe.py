#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')

"""
Windows EXE Build Script
Run this file on Windows to generate the parcel-scanner.exe file.

Usage:
1. pip install -r requirements.txt  (includes PyInstaller)
2. python build_windows_exe.py
3. Find parcel-scanner.exe in the dist folder
"""

import PyInstaller.__main__
import shutil

def build_exe():
    """Build Windows EXE"""

    print("=" * 60)
    print("Parcel Address Scanner System - Windows EXE Build")
    print("=" * 60)
    print()

    # Clean up existing build folders
    print("[1/4] Cleaning up existing build folders...")
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  ✓ {folder}/ removed")

    spec_file = "parcel_scanner.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"  ✓ {spec_file} removed")
    print()

    # Create barcodes folder if it doesn't exist
    if not os.path.exists('barcodes'):
        os.makedirs('barcodes')
        print("  ✓ Created barcodes/ folder")
    print()

    # Run PyInstaller
    print("[2/4] Running PyInstaller... (estimated 3-5 minutes)")
    print()

    try:
        args = [
            '--onefile',
            '--windowed',
            '--name=parcel_scanner',
            '--icon=NONE',
            '--hidden-import=cv2',
            '--hidden-import=easyocr',
            '--hidden-import=qrcode',
            '--hidden-import=barcode',
            '--hidden-import=pyusb',
            '--hidden-import=openpyxl',
            '--hidden-import=PIL',
            'main.py'
        ]

        # Add barcodes folder only if it exists and has content
        if os.path.exists('barcodes') and os.listdir('barcodes'):
            args.insert(4, '--add-data=barcodes:barcodes')

        PyInstaller.__main__.run(args)
        print()
        print("[3/4] EXE file generated successfully!")
        print()

    except Exception as e:
        print(f"[ERROR] Build failed: {e}")
        sys.exit(1)

    # Verify generated file
    print("[4/4] Verifying generated files...")
    exe_path = os.path.join('dist', 'parcel_scanner.exe')

    if os.path.exists(exe_path):
        exe_size = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"  ✓ {exe_path}")
        print(f"  ✓ File size: {exe_size:.1f} MB")
        print()
        print("=" * 60)
        print("[SUCCESS] Build completed!")
        print("=" * 60)
        print()
        print(f"Location: {os.path.abspath(exe_path)}")
        print()
        print("Next steps:")
        print("1. Run dist\\parcel_scanner.exe file")
        print("2. Upload or distribute on GitHub")
        print()

    else:
        print(f"[ERROR] EXE file not found: {exe_path}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
