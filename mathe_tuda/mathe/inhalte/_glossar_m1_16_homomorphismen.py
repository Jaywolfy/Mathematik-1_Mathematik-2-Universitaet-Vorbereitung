# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 16: Untergruppen und Gruppenhomomorphismen (Skript Disser, Abschn. 3.2)."""
from .glossar import eintrag

eintrag("Untergruppe", "Eine Teilmenge $U \\subseteq G$, die mit der eingeschränkten Verknüpfung selbst eine Gruppe ist (Def. 3.19). "
        "Kriterium: $U \\ne \\emptyset$ und $a \\ast b^{-1} \\in U$ für alle $a, b \\in U$ (Satz 3.24).",
        r"$2\mathbb{Z}$ ist Untergruppe von $(\mathbb{Z}, +)$, $\mathbb{N}$ nicht.",
        "gruppenhomomorphismen", ["Untergruppen", "Untergruppenkriterium"])
eintrag("erzeugte Untergruppe", "Zu $M \\subseteq G$ die kleinste Untergruppe $\\langle M \\rangle$, die $M$ enthält: der Schnitt aller Untergruppen, die $M$ umfassen (Def. 3.26, Satz 3.27).",
        r"$\langle \{[2]_6\} \rangle = \{[0]_6, [2]_6, [4]_6\}$ in $(\mathbb{Z}/6\mathbb{Z}, +)$.",
        "gruppenhomomorphismen", ["Erzeugnis", "Gruppenerzeugnis"])
eintrag("Gruppenhomomorphismus", "Eine Abbildung $f\\colon G \\to H$ zwischen Gruppen mit $f(a \\ast b) = f(a) \\star f(b)$ für alle $a, b$ (Def. 3.32). "
        "Sie bildet $e_G$ auf $e_H$ ab und Inverse auf Inverse (Satz 3.38).",
        r"$\pi_n\colon (\mathbb{Z}, +) \to (\mathbb{Z}/n\mathbb{Z}, +),\ a \mapsto [a]_n$.",
        "gruppenhomomorphismen", ["Homomorphismus", "Gruppenhomomorphismen", "Homomorphismen"])
eintrag("Isomorphismus", "Ein bijektiver Homomorphismus. Zwei Strukturen mit einem Isomorphismus zwischen ihnen heißen isomorph: Sie haben dieselbe Struktur, "
        "nur andere Namen für die Elemente (Def. 3.32, 3.55, 3.71). Ein Isomorphismus von $G$ nach $G$ heißt Automorphismus.",
        r"$\langle \{\sigma_1, \sigma_2\} \rangle \cong B_2$ (Spiegelungen und Bitgruppe).",
        "gruppenhomomorphismen", ["isomorph", "Isomorphismen", "Automorphismus"])
eintrag("Kern (Gruppenhomomorphismus)", "Zu $f\\colon G \\to H$ die Menge $\\ker(f) = \\{g \\in G \\mid f(g) = e_H\\}$ aller Elemente, die auf das Neutrale abgebildet werden (Def. 3.40). "
        "Er ist eine Untergruppe von $G$ und $f$ ist genau dann injektiv, wenn $\\ker(f) = \\{e_G\\}$.",
        r"$\ker(\pi_n) = n\mathbb{Z}$.",
        "gruppenhomomorphismen", ["Kern eines Gruppenhomomorphismus", "ker"])
