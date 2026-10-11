#!/bin/sh
# ==========================================================================
#  Python-Vorkurs-Lernquiz - Start fuer Linux
#  Ausfuehrbar machen (einmalig):  chmod +x start.sh    Starten:  ./start.sh
#  Alle Parameter werden weitergereicht, z. B.:  ./start.sh --terminal
#  Hinweis: Diese Datei braucht Unix-Zeilenenden (LF).
# ==========================================================================
cd "$(dirname "$0")" || exit 1

PY=""
ALT=""
for kandidat in python3 python3.14 python3.13 python3.12 python3.11 python3.10 python; do
    if command -v "$kandidat" >/dev/null 2>&1; then
        if "$kandidat" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then
            PY="$kandidat"
            break
        fi
        version=$("$kandidat" --version 2>&1 | head -n 1)
        case "$version" in
            Python*) ALT="$version" ;;
        esac
    fi
done

if [ -z "$PY" ]; then
    echo ""
    if [ -n "$ALT" ]; then
        echo "  Gefunden wurde nur $ALT - das ist zu alt."
    fi
    echo "  Python 3.10 oder neuer wurde nicht gefunden."
    echo ""
    echo "  So installierst du Python:"
    echo "    Ubuntu/Debian:  sudo apt install python3"
    echo "    Fedora:         sudo dnf install python3"
    echo "    Arch:           sudo pacman -S python"
    echo "    oder:           https://www.python.org/downloads/"
    echo ""
    exit 1
fi

exec "$PY" vorkurs_quiz.py "$@"
