#!/bin/bash
# ==========================================================================
#  Mathe-Lernsystem - Start fuer macOS (Doppelklick im Finder)
#  Beim ersten Mal ggf. ausfuehrbar machen:  chmod +x Start.command
#  Alle Parameter werden weitergereicht, z. B.:  ./Start.command --kein-browser
#  Hinweis: Diese Datei braucht Unix-Zeilenenden (LF).
# ==========================================================================
cd "$(dirname "$0")" || exit 1

# Erst die echten Installationen (python.org, Homebrew), dann python3 aus dem PATH.
# /usr/bin/python3 kommt zuletzt: Ohne Xcode-Werkzeuge oeffnet es nur einen
# Installationsdialog und ist meist Python 3.9 (zu alt).
PY=""
ALT=""
for kandidat in \
        /Library/Frameworks/Python.framework/Versions/Current/bin/python3 \
        /opt/homebrew/bin/python3 /usr/local/bin/python3 \
        python3.14 python3.13 python3.12 python3.11 python3.10 python3 /usr/bin/python3; do
    if command -v "$kandidat" >/dev/null 2>&1; then
        if "$kandidat" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then
            PY="$kandidat"
            break
        fi
        version=$("$kandidat" --version 2>/dev/null)
        [ -n "$version" ] && ALT="$version"
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
    echo "    1. Empfohlen: https://www.python.org/downloads/ (Installer fuer macOS)"
    echo "    2. Oder mit Homebrew:  brew install python@3.12"
    echo ""
    echo "  Danach Start.command noch einmal doppelklicken."
    echo ""
    read -r -p "  [Enter] zum Schliessen " _
    exit 1
fi

"$PY" mathe_quiz.py "$@"
code=$?
if [ $code -ne 0 ]; then
    echo ""
    read -r -p "  Das Programm wurde mit Fehlercode $code beendet. [Enter] zum Schliessen " _
fi
exit $code
