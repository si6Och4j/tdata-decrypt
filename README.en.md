# Telegram Desktop data extraction tool

Almost entirely rewritten version of [tdesktop-decrypter](https://github.com/ntqbit/tdesktop-decrypter)

# Installation:
```bash
git clone https://github.com/si6Och4j/tdata-decrypt
pip install ./tdata-decrypt
```

# Usage
```bash
tdata-decrypt /path/to/tdata
```

Default tdata folder locations:
 - Linux - `/home/*user*/.local/share/TelegramDesktop/tdata`
 - Windows (Current user) - `%AppData%\Roaming\TelegramDesktop\tdata`
 - MacOS - iToddlers has a right to cry

Beacuse of *"Almost entirely rewritten version"* all the rewritten parts are distributed under conditions of AGPL-3.0-only

# TODO:
> `¯\_(ツ)_/¯` We all know how plans work
 - Cache decryption
 - Ability to encrypt data
 - Ability to modify data

# Based on:
https://github.com/ntqbit/tdesktop-decrypter

https://github.com/atilaromero/telegram-desktop-decrypt

https://github.com/MihaZupan/TelegramStorageParser
