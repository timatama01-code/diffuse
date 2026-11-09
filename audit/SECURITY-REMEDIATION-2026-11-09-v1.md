# Отчёт об исправлении безопасности Diffuse — v1

Дата создания: 2026-11-09 (+03:00)

База: `MightyCreak/diffuse@2f52fad93acc8369229ba4443109133c7d904a17`  
Целевая версия: `0.12.0`  
Репозиторий: `timatama01-code/diffuse`

## Итог

Все HIGH/MEDIUM-находки первичного аудита устранены. Повторные Gitleaks и
Trivy не нашли секретов или известных уязвимостей; Bandit не выдал HIGH/MEDIUM.
Semgrep оставил пять проверенных ложных срабатываний на безопасные вызовы без
shell: три фиксированные системные утилиты и открытие локальной справки.

## Исправления

- F-01: `add_path.exe` полностью исключён из legacy-сборщика и installer.
- F-02/F-03: GitHub Actions и privileged Flatpak image закреплены полными SHA/digest;
  privileged job не запускается для pull request.
- F-04: Flatpak лишён `filesystem=home`, `org.freedesktop.Flatpak` и host-spawn.
- F-05: исполняемые файлы разрешаются по доверенному PATH вне рабочего репозитория.
- F-06: все применимые вызовы `xsltproc` используют `--nonet`.
- F-07: прямые Python-зависимости закреплены точными версиями.
- F-08/F-09: введён лимит 512 MiB, запрещены symlink/reparse/special inputs.
- F-10: postinstall проверяет наличие утилит и их коды возврата.
- Добавлена поддерживаемая Windows 10/11 x64 сборка: MSYS2 UCRT64, PyInstaller,
  per-user Inno Setup без администратора и изменения PATH.

## Проверки

- Windows unittest: 10 passed, 1 skipped (создание symlink запрещено политикой ОС).
- Linux/WSL unittest: 11 passed.
- flake8 и compileall: успешно.
- Meson/Ninja: успешно; Meson test: 1/1 успешно.
- `Diffuse.exe --version`: exit 0.
- Windows installer: 25 855 221 байт.
- Installer SHA-256:
  `FA7E09F0D5834937D67A376C34893D24CB443087446EF951E4E460375AF5607A`.
- Gitleaks: 0; Trivy: 0 vuln/secret/misconfig.
- Bandit: 0 HIGH, 0 MEDIUM, 21 LOW (стандартные subprocess/ложные password-метки).
- pip-audit прямых зависимостей: 0 известных уязвимостей.

Артефакты повторного сканирования: `gitleaks-postfix-v1.json`,
`bandit-postfix-v1.json`, `semgrep-postfix-v1.json`, `trivy-postfix-v1.json`.

## Остаточные риски

1. Installer пока не подписан Authenticode: Windows SmartScreen может показать
   предупреждение. Для подписи нужен доверенный code-signing сертификат.
2. Точные прямые зависимости закреплены, но полного кроссплатформенного lock-файла
   с hash для транзитивных GTK/PyGObject пакетов нет; Windows фиксирует фактические
   версии MSYS2 в `MSYS2-PACKAGES.txt`.

## Изменения ПК-1 и откат

- Установлен MSYS2 20260927 и UCRT64 Python/PyGObject/GTK3/PyInstaller.
- В Ubuntu WSL установлен `gettext` для `msgfmt`.
- Резервные копии mirrorlist сохранены как
  `C:\msys64\etc\pacman.d\mirrorlist.msys.bak-2026-11-09` и
  `mirrorlist.mingw.bak-2026-11-09`.
- Откат: восстановить эти два backup-файла; `sudo apt remove gettext`; удалить
  MSYS2 штатным деинсталлятором. Автоматический откат не выполнялся, чтобы не
  удалять файлы и сохранить воспроизводимую среду сборки.
