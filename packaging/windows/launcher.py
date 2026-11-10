"""PyInstaller entry point for the supported Windows 10/11 build."""

import gettext
import locale
import os
import signal
import sys

from pathlib import Path

import gi  # type: ignore

gi.require_version('Gio', '2.0')
from gi.repository import Gio  # type: ignore # noqa: E402


VERSION = '0.12.1'


def bundle_directory() -> Path:
    return Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))


def windows_language() -> str:
    language = locale.getlocale()[0] or 'en_US'
    if language.lower().startswith('russian'):
        return 'ru_RU'
    return language.replace('-', '_')


def run() -> int:
    bundle = bundle_directory()
    os.environ.setdefault('PYTHONUTF8', '1')
    os.environ.setdefault('LANGUAGE', windows_language())
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gettext.bindtextdomain('diffuse', localedir=str(bundle / 'locale'))
    gettext.textdomain('diffuse')

    resource = Gio.resource_load(str(bundle / 'diffuse.gresource'))
    Gio.Resource._register(resource)

    from diffuse import main

    return main.main(VERSION, '.')


if __name__ == '__main__':
    sys.exit(run())
