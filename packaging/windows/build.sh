#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

test "${MSYSTEM:-}" = "UCRT64"
mkdir -p build/windows

glib-compile-resources \
  --sourcedir=data \
  --target=build/windows/diffuse.gresource \
  data/diffuse.gresource.xml

export PYTHONPATH="$repo_root/src"
python -m unittest discover -s tests -p 'test_*.py' -v
python -m PyInstaller --clean --noconfirm packaging/windows/diffuse.spec

pacman -Q \
  mingw-w64-ucrt-x86_64-python \
  mingw-w64-ucrt-x86_64-python-gobject \
  mingw-w64-ucrt-x86_64-gtk3 \
  mingw-w64-ucrt-x86_64-pyinstaller \
  > dist/Diffuse/MSYS2-PACKAGES.txt

sha256sum dist/Diffuse/Diffuse.exe > dist/Diffuse/SHA256SUMS
