from pathlib import Path


project_root = Path(__file__).resolve().parent


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


pyz = PYZ(
    a.pure
)


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
