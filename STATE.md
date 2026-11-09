# STATE — Diffuse secure cross-platform 0.12.0

Обновлено: 2026-11-09 (+03:00)

- Fork: `https://github.com/timatama01-code/diffuse`.
- Рабочая ветка: `secure-cross-platform-0.12`.
- База upstream: `2f52fad93acc8369229ba4443109133c7d904a17`.
- Все HIGH/MEDIUM первичного аудита исправлены; отчёты находятся в `audit/`.
- Windows 10/11 x64 EXE и installer локально собраны и smoke-tested.
- Linux WSL Meson/Ninja/AppStream и unittest прошли.
- До завершения: commit/push, дождаться GitHub Actions, слить в main, создать
  release `v0.12.0` с Windows installer и контрольной суммой.
- Остаточные риски: нет Authenticode; нет полного hash-lock транзитивных пакетов.
