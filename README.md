# Утилита извлечения данных из Telegram Desktop

[Burger language](README.en.md)

[Основной репозиторий](https://gitflic.ru/project/consensus/tdata-decrypt)

Практически польностью переписанная версия [tdesktop-decrypter](https://github.com/ntqbit/tdesktop-decrypter)

# Установка:
```bash
git clone https://github.com/si6Och4j/tdata-decrypt
pip install ./tdata-decrypt
```

# Использование
```bash
tdata-decrypt /path/to/tdata
```

Стандартные папки для хранения tdata:
 - Linux - `/home/*user*/.local/share/TelegramDesktop/tdata`
 - Windows (Для текущего пользователя) - `%AppData%\Roaming\TelegramDesktop\tdata`
 - MacOS - iToddlers имеют право поплакать

Поскольку это *"Практически польностью переписанная версия"* все переписанные части распространяются под лицензией AGPL-3.0-only

# TODO:
> `¯\_(ツ)_/¯` Мы все знаем как работают планы
 - Расшифровывание кеша
 - Возможность замена данных кеша

# Основано на:
https://github.com/ntqbit/tdesktop-decrypter

https://github.com/atilaromero/telegram-desktop-decrypt

https://github.com/MihaZupan/TelegramStorageParser
