# Windows 10/11 build

The supported Windows package is built in a 64-bit MSYS2 UCRT64 environment.
It uses the MSYS2-signed GTK3/PyGObject packages, PyInstaller's maintained GI
hooks, and Inno Setup. The installer is per-user, does not require elevation,
does not modify `PATH`, and does not run downloaded helper executables.

## Local build

Install MSYS2, open its UCRT64 shell, and install:

```sh
pacman -S --needed \
  mingw-w64-ucrt-x86_64-python \
  mingw-w64-ucrt-x86_64-python-gobject \
  mingw-w64-ucrt-x86_64-gtk3 \
  mingw-w64-ucrt-x86_64-pyinstaller
```

Then run:

```sh
packaging/windows/build.sh
```

Compile `packaging/windows/installer.iss` with Inno Setup 6 after the
PyInstaller directory has been created. The GitHub workflow performs both
steps and smoke-tests `Diffuse.exe --version` on Windows.
