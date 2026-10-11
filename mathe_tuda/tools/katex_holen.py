#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entwickler-Werkzeug: KaTeX EINMALIG herunterladen und lokal ablegen.

Lädt das npm-Paket "katex" (Tarball von registry.npmjs.org), prüft die
sha512-Integrität aus der Registry und entpackt nur die benötigten Dateien nach
mathe/web/static/vendor/katex/. Zur Laufzeit braucht das Lernsystem KEIN Internet.

Aufruf:  python3 tools/katex_holen.py [VERSION]     (Standard: 0.19.0)
"""
import base64
import hashlib
import io
import json
import shutil
import sys
import tarfile
import urllib.request
from pathlib import Path

VERSION = sys.argv[1] if len(sys.argv) > 1 else "0.19.0"
ZIEL = Path(__file__).resolve().parent.parent / "mathe" / "web" / "static" / "vendor" / "katex"


def laden(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def main():
    meta = json.loads(laden(f"https://registry.npmjs.org/katex/{VERSION}"))
    tarball, integritaet = meta["dist"]["tarball"], meta["dist"]["integrity"]
    daten = laden(tarball)
    algo, soll = integritaet.split("-", 1)
    ist = base64.b64encode(hashlib.new(algo, daten).digest()).decode()
    if ist != soll:
        sys.exit(f"Integritätsprüfung fehlgeschlagen: {ist} != {soll}")
    if ZIEL.exists():
        shutil.rmtree(ZIEL)
    (ZIEL / "fonts").mkdir(parents=True)
    (ZIEL / "contrib").mkdir()
    wanted = {"package/dist/katex.min.css": "katex.min.css",
              "package/dist/katex.min.js": "katex.min.js",
              "package/dist/contrib/auto-render.min.js": "contrib/auto-render.min.js",
              "package/LICENSE": "LICENSE"}
    with tarfile.open(fileobj=io.BytesIO(daten), mode="r:gz") as tar:
        for m in tar.getmembers():
            if not m.isfile():
                continue
            if m.name in wanted:
                ziel = ZIEL / wanted[m.name]
            elif m.name.startswith("package/dist/fonts/") and m.name.endswith(".woff2"):
                ziel = ZIEL / "fonts" / Path(m.name).name
            else:
                continue
            ziel.write_bytes(tar.extractfile(m).read())
    (ZIEL / "VERSION.txt").write_text(f"KaTeX {VERSION}\n{tarball}\n{integritaet}\n", encoding="utf-8")
    print(f"KaTeX {VERSION} nach {ZIEL} entpackt (Integrität geprüft).")


if __name__ == "__main__":
    main()
