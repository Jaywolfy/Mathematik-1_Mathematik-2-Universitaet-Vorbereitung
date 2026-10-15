# -*- coding: utf-8 -*-
"""Glossar-Einträge von Mathe 1, Kapitel 25: Lineare Abbildungen, Kern, Bild und Rang (Skript Disser, Abschn. 5.1 und 5.2)."""
from .glossar import eintrag

eintrag("lineare Abbildung", "Eine Abbildung $f\\colon V \\to W$ zwischen Vektorräumen über demselben Körper $K$ mit "
        "$f(v + w) = f(v) + f(w)$ und $f(\\lambda v) = \\lambda f(v)$ für alle $v, w \\in V$, $\\lambda \\in K$ (Def. 5.1). "
        "Sie erhält Linearkombinationen. Auch Vektorraumhomomorphismus genannt.",
        r"$f\colon \mathbb{R}^2 \to \mathbb{R}^2,\ (x, y)^\top \mapsto (2x + y,\ x - y)^\top$ ist linear, $x \mapsto x + 1$ nicht.",
        "lineare_abbildungen", ["Vektorraumhomomorphismus", "linear", "lineare Abbildungen", "linearer Abbildung"])
eintrag("Kern einer linearen Abbildung", "Zu $f\\colon V \\to W$ linear die Menge $\\ker(f) = \\{v \\in V \\mid f(v) = 0_W\\}$ aller Vektoren, die auf null "
        "abgebildet werden. Sie ist ein Untervektorraum von $V$ (Satz 5.14). $f$ ist genau dann injektiv, wenn $\\ker(f) = \\{0_V\\}$ (Beob. 5.17).",
        r"Für die Projektion $\pi_G$ auf $G = \langle (1, 1)^\top \rangle$ gilt $\ker(\pi_G) = \langle (1, -1)^\top \rangle$.",
        "lineare_abbildungen", ["Kern", "Kern einer Matrix", "Kern der Matrix"])
eintrag("Rang", "Der Rang einer linearen Abbildung $f$ ist $\\mathrm{rang}(f) := \\dim f(V)$, die Dimension des Bildes (Def. 5.15). "
        "Der Rang einer Matrix ist der Rang ihrer Abbildung $f_A$, also die Dimension des von den Spalten erzeugten Raums (Def. 5.32, Beob. 5.33).",
        r"Die Projektion $\pi_G$ hat Rang $1$, die Identität auf $\mathbb{R}^2$ hat Rang $2$.",
        "lineare_abbildungen", ["Rang einer Abbildung", "Rang einer Matrix", "Rang einer linearen Abbildung"])
eintrag("Dimensionsformel für lineare Abbildungen", "Für $f\\colon V \\to W$ linear und $\\dim V < \\infty$ gilt $\\dim V = \\dim\\ker(f) + \\mathrm{rang}(f)$ (Satz 5.20). "
        "Was der Kern verschluckt, fehlt im Bild.",
        r"$f\colon \mathbb{R}^3 \to \mathbb{R}^2,\ (x, y, z)^\top \mapsto (x + y, z)^\top$: $3 = 1 + 2$.",
        "lineare_abbildungen", ["Rangsatz", "Dimensionssatz", "Rang-Kern-Satz"])
eintrag("Spiegelung", "Die Spiegelung $s_G$ an einer Geraden $G$ durch $0$ behält den Anteil in $G$ und kehrt den Anteil senkrecht zu $G$ um: "
        "$s_G = 2\\pi_G - \\mathrm{id}$ (Bsp. 5.12). Sie ist linear und ihre eigene Umkehrung.",
        r"Die Spiegelung an $\langle (1, 1)^\top \rangle$ vertauscht die beiden Koordinaten.",
        "lineare_abbildungen", ["Spiegelung an einer Geraden"])
