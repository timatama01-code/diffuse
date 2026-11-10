#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

test "${MSYSTEM:-}" = "UCRT64"
dist_root="${DIFFUSE_WINDOWS_DIST_ROOT:-dist}"
work_root="${DIFFUSE_WINDOWS_WORK_ROOT:-build/windows-pyinstaller}"
mkdir -p build/windows/locale/ru/LC_MESSAGES
mkdir -p "$dist_root" "$work_root"

glib-compile-resources \
  --sourcedir=data \
  --target=build/windows/diffuse.gresource \
  data/diffuse.gresource.xml

msgfmt --check \
  --output-file=build/windows/locale/ru/LC_MESSAGES/diffuse.mo \
  po/ru.po

export PYTHONPATH="$repo_root/src"
python -m unittest discover -s tests -p 'test_*.py' -v
python -m PyInstaller \
  --noconfirm \
  --distpath "$dist_root" \
  --workpath "$work_root" \
  packaging/windows/diffuse.spec

pacman -Q \
  mingw-w64-ucrt-x86_64-python \
  mingw-w64-ucrt-x86_64-python-gobject \
  mingw-w64-ucrt-x86_64-gtk3 \
  mingw-w64-ucrt-x86_64-pyinstaller \
  > "$dist_root/Diffuse/MSYS2-PACKAGES.txt"

sha256sum "$dist_root/Diffuse/Diffuse.exe" > "$dist_root/Diffuse/SHA256SUMS"
