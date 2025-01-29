from setuptools import setup

APP = ['main.py']
DATA_FILES = ['.env']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'requests', 'dotenv'],
    'iconfile': 'app_icon.icns',  # You'll need to create an icon file
    'plist': {
        'CFBundleName': "Text to Speech Converter",
        'CFBundleDisplayName': "Text to Speech Converter",
        'CFBundleGetInfoString': "Convert text to speech using OpenAI",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 