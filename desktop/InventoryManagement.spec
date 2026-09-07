from pathlib import Path

from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import PYZ, EXE


project_root = Path(__file__).resolve().parent


# =========================================================
# ANALYSIS
# =========================================================

a = Analysis(
    [
        str(project_root / "main.py"),
    ],

    pathex=[
        str(project_root),
    ],

    binaries=[],

    datas=[
        (
            str(
                project_root
                / "app"
                / "core"
                / "ui"
                / "styles"
            ),
            "app/core/ui/styles",
        ),
    ],

    hiddenimports=[],

    hookspath=[],

    hooksconfig={},

    runtime_hooks=[],

    excludes=[
        "pytest",
        "tests",
    ],

    noarchive=False,
)


# =========================================================
# PYTHON ZIP
# =========================================================

pyz = PYZ(
    a.pure,
)


# =========================================================
# EXECUTABLE
# =========================================================

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],

    name="InventoryManagement",

    debug=False,

    bootloader_ignore_signals=False,

    strip=False,

    upx=True,

    console=False,
)
