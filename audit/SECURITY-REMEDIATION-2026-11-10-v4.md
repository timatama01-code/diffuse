# Diffuse 0.12.1 — итоговая приёмка релиза

Дата: 2026-11-10 (+03:00)

## Принятый результат

Коммит `6db16af78be1f5be914468a63c8cca0463f21150` прошёл Linux CI и Windows
сборку. Релизный установщик скачан из артефакта GitHub Actions, записан на диск
I, установлен повторно и проверен по живому окну.

## Релизный артефакт

- `I:\Diffuse-0.12.1-Windows-x64-Setup.exe`
- Размер: 25 858 705 байт.
- SHA-256: `0FE6A7D9F7B213142F64A68E7A4EA898DFC861F67BB8517C73D0BA4A802DA116`.
- Release: `https://github.com/timatama01-code/diffuse/releases/tag/v0.12.1`.

## Гейты

- CI `42899479897`: success (Flake8, MyPy, Meson tests, Flatpak build).
- Windows `42899479941`: success (standalone build, smoke test, installer).
- Локально: 13 unittest успешно, 1 Windows-проверка симлинка пропущена.
- Bandit: 0 находок; Gitleaks: 0 утечек.
- Установка: код 0; `diffuse.mo` присутствует, 17 858 байт.
- Программа отвечает; заголовок `Слияние Файлов 1 - Diffuse` содержит
  кириллицу.

## Остаточный риск

Установщик не подписан Authenticode. Это не меняет контрольную сумму и
результаты аудита, но SmartScreen может показать предупреждение издателя.
