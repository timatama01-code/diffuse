# Отчёт об исправлении безопасности Diffuse — v2

Дата создания: 2026-11-09 (+03:00)

Это финальное дополнение к v1 после проверки в GitHub Actions и публикации.

## Проверенный результат

- Commit продукта: `3be64e2c55f438db52c3391c2773e5c2756a2d6a`.
- Linux/Flatpak CI run `42682176358`: lint, MyPy, Meson, AppStream и
  Flatpak builder — успешно.
- Windows run `42682176456`: MSYS2 build, `Diffuse.exe --version`, Inno Setup
  и upload artifact — успешно.
- Код опубликован в `main` репозитория `timatama01-code/diffuse`.
- Release: `v0.12.0`.
- CI installer: `Diffuse-0.12.0-Windows-x64-Setup.exe`, 25 855 683 байта.
- SHA-256: `645B8CE183449627206ED6FC8878782B9AC0059052F1C2CD8FBE2F9CDD6B3FC5`.

## Исправленные CI-причины

- MyPy: общий pipe типизирован как `IO[bytes]`, chunks — `List[bytes]`.
- Flatpak container: удалён несовместимый `setup-python`; используется Python SDK.
- Flatpak postinstall: необязательные cache/schema каталоги проверяются до запуска.

## Остаточные риски

- Installer не подписан Authenticode; возможен SmartScreen warning.
- Нет единого hash-lock транзитивных GTK/PyGObject зависимостей; фактические
  Windows-пакеты приложены к release в `MSYS2-PACKAGES.txt`.
