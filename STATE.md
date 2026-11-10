# STATE - Diffuse secure cross-platform 0.12.1

## Обновление 2026-11-10 (+03:00)

- Исправлена русская локализация Windows: `po/ru.po` компилируется в
  `locale/ru/LC_MESSAGES/diffuse.mo`, каталог включается в PyInstaller, а
  launcher задаёт `LANGUAGE` по системной локали Windows.
- Версия синхронно поднята до `0.12.1`; опубликованный `v0.12.0` не изменяется.
- Локальный установщик: `I:\Diffuse-0.12.1-Windows-x64-Setup.exe`.
- SHA-256 локальной сборки:
  `42785B0C91DFAE926E079E6EA5F1C6E59E275696C1C84598CBCB33BEF8C087A9`.
- Установка завершилась с кодом 0; запущенное окно отвечает и имеет русский
  заголовок `Слияние Файлов 1 - Diffuse`.
- Проверки: 13 unittest (1 штатно пропущен), Flake8 изменённых Python-файлов,
  Bandit (0 находок), Gitleaks (0 утечек).
- Известный остаток: установщик пока без Authenticode-подписи.

Обновлено: 2026-11-09 (+03:00)

- Fork: `https://github.com/timatama01-code/diffuse`.
- Рабочая ветка: `secure-cross-platform-0.12`.
- База upstream: `2f52fad93acc8369229ba4443109133c7d904a17`.
- Все HIGH/MEDIUM первичного аудита исправлены; отчёты находятся в `audit/`.
- Windows 10/11 x64 EXE и installer локально собраны и smoke-tested.
- Linux WSL Meson/Ninja/AppStream и unittest прошли.
- Статус: завершено. Проверенный commit `3be64e2` опубликован в `main`.
- GitHub Actions: CI `42682176358` и Windows `42682176456` — success.
- Release `v0.12.0` опубликован с Windows installer и SHA-256.
- Остаточные риски: нет Authenticode; нет полного hash-lock транзитивных пакетов.
