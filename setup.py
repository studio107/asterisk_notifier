from setuptools import setup

APP = ['main.py']
DATA_FILES = [('images', ["logo.png"]), ]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'plist': {
        'LSUIElement': True,
        # 'CFBundleShortVersionString': '0.1.0',
    },
    'packages': ['requests'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app', 'requests'],
)
