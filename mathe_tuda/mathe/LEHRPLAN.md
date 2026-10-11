# Lehrplan – woher jedes Kapitel kommt

Stand: 11.10.2026. Dieser Plan ist für Autoren verbindlich. Jedes Kapitel setzt `quelle=` auf die
Fundstelle aus der Spalte „Quelle“.

## Quellen

| Kürzel | Dokument | Ort |
|---|---|---|
| **MHB** | Modulhandbuch B.Sc. Informatik, PO 2023 (Stand 30.09.2022): „Mathematik I für Informatik“ (04-10-0118, 9 CP, WiSe) und „Mathematik II für Informatik“ (04-10-0119, 9 CP, SoSe). Prüfung: Klausur 90 Minuten; Zulassung über Hausübungen | `Unterlagen/TU_Recherche/Modulhandbuch_BSc_Informatik_PO2023.pdf` (S. 12 und 20) |
| **MVK** | Mathematik-Vorkurs TU Darmstadt 2026/27 (A. Ihrig), Vorlesungen 1–15 als Handout/Prehandout, Übung „Folgen“, Induktionsaufgabe | `Unterlagen/Vorkurs/` |
| **SKR** | Skript „Mathematik I/II für Inf, WInf“, R. Haller-Dintelmann, TU Darmstadt (Fassungen WS 15/16 und 2015/16). Gliederung entspricht genau den Lerninhalten des MHB | `Unterlagen/TU_Recherche/Skript_*.pdf` |
| **UEB** | Offizielle Übungsblätter mit Lösungen, Mathe I für Inf (WS 09/10) und Mathe II für Inf (SoSe 10) | `Unterlagen/TU_Recherche/Uebungen_*` |
| **KL** | Klausur „Mathematik II für Inf-BSc“, 11.03.2010: 6 Aufgaben, 60 Punkte, 90 Minuten | `Unterlagen/TU_Recherche/Klausur_MatheII_Inf_2010-03-11.pdf` |

**Nicht** in Mathe I/II (eigene Module laut MHB): Aussagen- und Prädikatenlogik (2. Semester),
Wahrscheinlichkeit und Statistik („Probabilistische Methoden“, 3. Semester), Graphentheorie und
Kombinatorik als eigenes Thema. Logik und Binomialkoeffizient kommen nur so weit vor, wie Vorkurs
und Skript sie brauchen.

**Klausurstil (KL, UEB):** „Bei der Bearbeitung der Aufgaben müssen alle verwendeten Sätze und
Verfahren, die erforderlichen Voraussetzungen, die Rechengänge und sämtliche Zwischenergebnisse
angegeben werden.“ Aufgaben sind meist Rechenaufgaben mit Begründung (Inverse, Eigenwerte und
Eigenräume, Extrema in zwei Variablen, Lagrange, Anfangswertproblem, DGL-System, Hesse-Normalform)
plus kurze Beweise. Hilfsmittel damals: vier handbeschriebene A4-Seiten, einfacher Taschenrechner.
Praxisaufgaben mit `uebungsblatt=True` folgen diesem Stil: Aufgabenstellung im Sie-Stil der Blätter
zitieren ist erlaubt, Erklärungen bleiben in der Du-Form.

**Notation:** siehe ARCHITEKTUR.md Abschnitt 6. Wichtig: Der Vorkurs setzt $\mathbb{N} = \{1, 2, \ldots\}$,
das Skript Mathe I/II setzt $\mathbb{N} = \{0, 1, 2, \ldots\}$ und $\mathbb{N}^* = \{1, 2, \ldots\}$.

## Fundament (Schulstoff, `teil="fundament"`, Quelle „Schulstoff (Voraussetzung für den TU-Vorkurs)“)

Der Vorkurs setzt diesen Stoff voraus. Fertig: f01 Zahlen, f02 Rechnen, f03 Brüche.

| Datei | Slug | Titel | Inhalt |
|---|---|---|---|
| f04_dezimal_prozent | dezimal_prozent | Dezimalzahlen und Prozent | Stellenwerte, Umwandeln Bruch ↔ Dezimal, periodisch, Runden, Prozent |
| f05_potenzen | potenzen | Potenzen | Potenzgesetze, negative Exponenten, Zweierpotenzen, Zehnerpotenzen |
| f06_wurzeln | wurzeln | Wurzeln | Quadratwurzel, n-te Wurzel, rationale Exponenten, teilweise Wurzelziehen, Nenner rational machen |
| f07_terme | terme | Terme und binomische Formeln | Zusammenfassen, Ausmultiplizieren, Ausklammern, binomische Formeln, Bruchterme kürzen |
| f08_gleichungen | gleichungen | Gleichungen und Formeln umstellen | Äquivalenzumformungen, lineare Gleichungen, Bruchgleichungen mit Definitionsmenge, Formeln umstellen |
| f09_ungleichungen | ungleichungen | Ungleichungen | Umformen, Zeichen kippt bei negativer Multiplikation, Lösungsmenge als Intervall |
| f10_quadratisch | quadratisch | Quadratische Gleichungen | pq-Formel, Mitternachtsformel, quadratische Ergänzung, Diskriminante, Satz von Vieta |
| f11_polynome | polynome | Polynome und Polynomdivision | Grad, Nullstellen raten, Polynomdivision, Linearfaktoren, Horner-Schema |
| f12_betrag | betrag | Betrag | Abstand zur Null, Fallunterscheidung, Betragsgleichungen und -ungleichungen, Dreiecksungleichung |
| f13_funktionen | funktionen | Funktionen und Graphen | Funktionsbegriff, lineare Funktionen, Parabeln, Verschieben und Strecken |
| f14_exp_log | exp_log | Exponentialfunktion und Logarithmus | Wachstum, $e$, Logarithmusgesetze, $\log_2$, Exponentialgleichungen |
| f15_trigonometrie | trigonometrie | Trigonometrie und Bogenmaß | sin, cos, tan am Einheitskreis, Bogenmaß, wichtige Werte, $\sin^2 + \cos^2 = 1$ |
| f16_mathe_lesen | mathe_lesen | Mathematik lesen | Symbole ($\forall\ \exists\ \Rightarrow\ :=$), griechische Buchstaben, Definition, Satz, Beweis, ℕ-Konventionen |

## Vorkurs (`teil="vorkurs"`, Quelle „MVK 2026, VL n“)

Folgt den 15 Vorlesungen des Vorkurses, aufgeteilt in Kapitel mit je einem Hauptgedanken.
Die Lernziele der Folien sind die Lernziele der Kapitel.

| Datei | Slug | Titel | Quelle | Inhalt |
|---|---|---|---|---|
| v01_mengen | mengen | Mengen | MVK VL 1 | Notation, Element, Teilmenge, Gleichheit, ∪ ∩ \ Komplement, kartesisches Produkt, Zahlenmengen, Intervalle |
| v02_aussagen | aussagen | Aussagen und Wahrheitstafeln | MVK VL 1–2 | Aussage, Negation, ∧, ∨, Wahrheitstafeln |
| v03_implikation | implikation | Implikation, Äquivalenz, Tautologie | MVK VL 1–2 | ⇒, ⇔, notwendig/hinreichend, Tautologie, Widerspruch, De Morgan |
| v04_quantoren | quantoren | Quantoren | MVK VL 1 | ∀, ∃, Negation von Quantoren, Beispiel und Gegenbeispiel |
| v05_summen | summen | Summen- und Produktzeichen | MVK VL 2 | Σ, Π, Indexverschiebung, leere Summe/leeres Produkt, Rechenregeln |
| v06_binomial | binomial | Fakultät und Binomialkoeffizient | MVK VL 2–3 | n!, $\binom{n}{k}$, Pascalsches Dreieck, Symmetrie |
| v07_beweise | beweise | Direkter Beweis | MVK VL 3 | Aufbau (Voraussetzung, Behauptung, Beweis, □), direkter Beweis, gerade/ungerade |
| v08_kontraposition | kontraposition | Kontraposition und Widerspruch | MVK VL 3 | Kontraposition, Widerspruchsbeweis ($\sqrt 2$ irrational), Annahmen formulieren |
| v09_induktion | induktion | Vollständige Induktion | MVK VL 3 + Induktionsaufgabe | IA, IV, IS, Summenformeln, Teilbarkeit, Beweisschritte ordnen |
| v10_abbildungen | abbildungen | Funktionen, Bild und Urbild | MVK VL 4 | $f\colon D \to W$, Definitions-/Zielmenge, Graph, Bild $f(A)$, Urbild $f^{-1}(B)$ |
| v11_injektiv | injektiv | Injektiv, surjektiv, bijektiv | MVK VL 4–5 | Definitionen, Nachweis, Gegenbeispiel, Umkehrfunktion |
| v12_verkettung | verkettung | Verkettung und Umkehrfunktion | MVK VL 5 | $g \circ f$, Rechenoperationen, Umkehrfunktion der Verkettung |
| v13_reelle_funktionen | reelle_funktionen | Eigenschaften reeller Funktionen | MVK VL 5–6 | gerade/ungerade, Monotonie, Beschränktheit, Zusammenhänge |
| v14_folgen | folgen | Folgen | MVK VL 6 | explizit, rekursiv, Monotonie, Beschränktheit |
| v15_grenzwerte_folgen | grenzwerte_folgen | Konvergenz und Grenzwerte von Folgen | MVK VL 7 + Übung Folgen | ε-Definition, Nullfolgen, wichtige Grenzwerte, Grenzwertsätze, Sandwich, bestimmte Divergenz |
| v16_grenzwerte_funktionen | grenzwerte_funktionen | Grenzwerte von Funktionen | MVK VL 8 | links-/rechtsseitig, im Unendlichen, Polstellen, Asymptoten, rationale Funktionen |
| v17_stetigkeit | stetigkeit | Stetigkeit | MVK VL 8–9 | Definition, anschaulich, Regeln, elementare Funktionen, Zwischenwertsatz |
| v18_ableitung | ableitung | Ableitung | MVK VL 9–10 | Differenzenquotient, Differenzierbarkeit, Tangente, Ableitungsregeln |
| v19_kettenregel | kettenregel | Kettenregel, höhere Ableitungen, Mittelwertsatz | MVK VL 10 | Kettenregel, Umkehrfunktion, höhere Ableitungen, Mittelwertsatz, Tangentennäherung |
| v20_extrema | extrema | Extrema und Wendepunkte | MVK VL 11 | lokal/global, notwendige und hinreichende Bedingung, Vorzeichenwechsel, Wende- und Sattelpunkt |
| v21_stammfunktionen | stammfunktionen | Stammfunktionen | MVK VL 11 | Stammfunktion, unbestimmtes Integral, wichtige Stammfunktionen, Linearität |
| v22_integrale | integrale | Bestimmte Integrale und Integrationstechniken | MVK VL 12 | Fläche, Hauptsatz, Intervall-Additivität, partielle Integration, Substitution, Partialbruchzerlegung, uneigentliche Integrale |
| v23_vektoren | vektoren | Vektoren und Norm | MVK VL 13 | $\mathbb{R}^n$, Addition, Skalarmultiplikation, geometrisch, euklidische Norm, normieren, parallel |
| v24_matrizen | matrizen | Matrizen | MVK VL 14 | Notation, Matrix-Vektor-Produkt, Matrizenprodukt, Transponieren, Einheits-, Diagonal-, symmetrische Matrix |
| v25_inverse_det | inverse_det | Inverse und Determinante | MVK VL 14 | Invertierbarkeit, Determinante 2×2 und 3×3 (Sarrus), Inverse 2×2 |
| v26_komplexe_zahlen | komplexe_zahlen | Komplexe Zahlen | MVK VL 15 | $i$, Real-/Imaginärteil, Rechnen, Konjugation, Division, Zahlenebene, Polarkoordinaten |

## Mathe 1 (`teil="mathe1"`, Quelle „Mathe I (PO 2023); Skript Kap. x“)

MHB-Lerninhalt: Mengen, Relationen, Funktionen, algebraische Grundstrukturen; modulare Arithmetik,
RSA; endlichdimensionale Vektorräume, lineare Abbildungen und Matrizen, Gauß-Algorithmus,
Determinanten, Eigenwerte; reelle und komplexe Zahlen; Folgen und Konvergenz.

| Datei | Slug | Titel | Skript | Inhalt |
|---|---|---|---|---|
| m1_01_aussagen_mengen | uni_mengen | Aussagen und Mengen an der Uni | 1.1–1.2 | Aussageformen, Quantoren präzise, Mengenalgebra, Potenzmenge, ℕ-Konvention des Skripts |
| m1_02_ordnungsrelationen | ordnungsrelationen | Relationen und Ordnungen | 1.3.1 | Relation als Teilmenge, reflexiv, antisymmetrisch, transitiv, total, Halbordnung |
| m1_03_aequivalenzrelationen | aequivalenzrelationen | Äquivalenzrelationen | 1.3.2 | symmetrisch, Klassen, Partition, Repräsentanten, Restklassen als Beispiel |
| m1_04_abbildungen | uni_abbildungen | Abbildungen präzise | 1.4 | Abbildung als Relation, Komposition, Umkehrabbildung, Bild/Urbild-Regeln, Mächtigkeit |
| m1_05_beweisprinzipien | beweisprinzipien | Beweisprinzipien | 1.5 | direkt, Kontraposition, Widerspruch, Induktion (Ungleichungen, Teilbarkeit, starke Induktion) |
| m1_06_teilbarkeit | teilbarkeit | Teilbarkeit und Primzahlen | 2.1 | Teiler, Division mit Rest, Primzahlen, Primfaktorzerlegung, ggT/kgV |
| m1_07_modulo | modulo | Modulare Arithmetik | 2.1.1 | Kongruenz, Rechnen mod n, $\mathbb{Z}_n$, Rechenregeln, schnelles Potenzieren |
| m1_08_euklid | euklid | Euklidischer Algorithmus | 2.1.2 | ggT per Euklid, erweiterter Euklid, Bézout, modulare Inverse |
| m1_09_fermat | fermat | Kleiner Satz von Fermat | 2.1.3 | Fermat, Euler-φ, Satz von Euler |
| m1_10_rsa | rsa | RSA | 2.2 | Schlüsselerzeugung, Verschlüsseln, Entschlüsseln, warum es funktioniert |
| m1_11_gruppen | gruppen | Gruppen | 2.3 | Verknüpfung, Axiome, Beispiele, Eindeutigkeit von neutralem/inversem Element, Ordnung |
| m1_12_untergruppen | untergruppen | Untergruppen und Homomorphismen | 2.3.1–2.3.2 | Untergruppenkriterium, Homomorphismus, Kern, Bild, Isomorphismus |
| m1_13_ringe_koerper | ringe_koerper | Ringe und Körper | 2.4 | Ring, Körper, Nullteiler, $\mathbb{Z}_n$ Körper genau für n prim |
| m1_14_komplex_koerper | komplex_koerper | Der Körper ℂ | 2.5 | ℂ als Paare, Rechnen, Betrag, Polardarstellung, Euler-Formel, Wurzeln, Einheitswurzeln |
| m1_15_vektorraeume | vektorraeume | Vektorräume | 3.1 | Axiome, $K^n$, Polynome, Funktionen, Summenschreibweise |
| m1_16_unterraeume | unterraeume | Untervektorräume und Spann | 3.2.1 | Unterraumkriterium, Linearkombination, Erzeugnis |
| m1_17_basis | basis | Lineare Unabhängigkeit, Basis, Dimension | 3.2.2 | linear unabhängig, Basis, Dimension, Basisergänzung |
| m1_18_skalarprodukt | skalarprodukt | Normen und Skalarprodukte | 3.4 | Norm, Skalarprodukt, Cauchy-Schwarz, Winkel, Orthogonalität, Orthonormalbasis, Gram-Schmidt |
| m1_19_geometrie | geometrie | Geometrie im ℝⁿ | 3.5 | Geraden, Ebenen, Kreuzprodukt, Hesse-Normalform, Abstände, Schnittpunkte |
| m1_20_lineare_abbildungen | lineare_abbildungen | Lineare Abbildungen | 3.6 | Linearität, Kern, Bild, Dimensionsformel, injektiv ⇔ Kern = {0} |
| m1_21_abbildungsmatrix | abbildungsmatrix | Matrizen und Abbildungsmatrix | 3.7 | Matrixrechnung, Abbildungsmatrix bzgl. Basen, Komposition = Produkt |
| m1_22_lgs | lgs | Lineare Gleichungssysteme | 3.8 | Lösbarkeit, Rang, Lösungsstruktur (partikulär + Kern), Gauß-Algorithmus, Inverse per Gauß |
| m1_23_basiswechsel | basiswechsel | Basiswechsel | 3.9 | Koordinaten, Transformationsmatrix, $T^{-1} A T$ |
| m1_24_determinanten | determinanten | Determinanten | 3.10 | Eigenschaften, Laplace-Entwicklung, Zeilenumformungen, $\det(AB)$, Invertierbarkeit |
| m1_25_eigenwerte | eigenwerte | Eigenwerte und Eigenvektoren | 3.11 | Definition, charakteristisches Polynom, Eigenräume, Vielfachheiten |
| m1_26_diagonalisierung | diagonalisierung | Diagonalisierung | 3.11 | diagonalisierbar, $S^{-1} A S = D$, symmetrische Matrizen, Potenzen |
| m1_27_reelle_zahlen | reelle_zahlen | Die reellen Zahlen | 5.1–5.2 | Körper- und Anordnungsaxiome, Betrag, Supremum/Infimum, Vollständigkeit, Bernoulli |
| m1_28_konvergenz | konvergenz | Konvergenz von Folgen | 5.3.1 | ε-Definition sauber, Beweise von Grenzwerten, wichtige Beispiele ($q^n$, $\sqrt[n]{n}$) |
| m1_29_konvergenzkriterien | konvergenzkriterien | Konvergenzkriterien für Folgen | 5.3.2–5.3.3 | monoton + beschränkt, Cauchy-Folgen, Teilfolgen, Häufungswerte, Bolzano-Weierstraß, $e$ |
| m1_30_asymptotik | asymptotik | Asymptotik und Landau-Symbole | 5.4 | $O$, $o$, $\Theta$, Wachstumsvergleich, Laufzeiten |
| m1_31_reihen | reihen | Reihen | 5.5 | Partialsummen, geometrische, harmonische, Teleskop-Reihe, notwendiges Kriterium |
| m1_32_reihenkriterien | reihenkriterien | Konvergenzkriterien für Reihen | 5.5.1–5.5.2 | Majorante/Minorante, Quotienten-, Wurzel-, Leibniz-Kriterium, absolute Konvergenz, Cauchy-Produkt |
| m1_33_normierte_raeume | normierte_raeume | Konvergenz in normierten Räumen | 5.6 | Normen im $\mathbb{R}^n$, Konvergenz komponentenweise, offen, abgeschlossen, kompakt |

## Mathe 2 (`teil="mathe2"`, Quelle „Mathe II (PO 2023); Skript Kap. x“)

MHB-Lerninhalt: Reihen und Potenzreihen; elementare Funktionen; reelle Funktionen und Stetigkeit;
Differentialrechnung, Extrema, Umkehrfunktion; Exponentialfunktion und Logarithmus;
Integralrechnung (Hauptsatz, Integrationsmethoden); Funktionen mehrerer Variablen; Taylor- und
Fourierreihen; gewöhnliche Differentialgleichungen (elementare Lösungsmethoden, lineare DGL).

| Datei | Slug | Titel | Skript | Inhalt |
|---|---|---|---|---|
| m2_01_funktionsgrenzwerte | funktionsgrenzwerte | Grenzwerte von Funktionen | 4.7.1 | Häufungspunkt, Folgenkriterium, ε-δ, einseitig, uneigentlich |
| m2_02_stetigkeit | uni_stetigkeit | Stetigkeit | 4.7.2–4.7.3 | ε-δ-Stetigkeit, Folgenstetigkeit, Zwischenwertsatz, Satz vom Maximum, stetige Fortsetzung |
| m2_03_stetigkeit_mehrdim | stetigkeit_mehrdim | Stetigkeit in mehreren Variablen | 4.8 | Funktionen $\mathbb{R}^n \to \mathbb{R}^m$, Grenzwerte entlang Wegen, Stetigkeit |
| m2_04_potenzreihen | potenzreihen | Potenzreihen | 4.9 | Konvergenzradius (Quotient, Wurzel), Konvergenzbereich, Rand |
| m2_05_exp_log | uni_exp_log | Exponentialfunktion und Logarithmus | 4.10.1 | exp als Reihe, Funktionalgleichung, ln, allgemeine Potenz |
| m2_06_trig | uni_trig | Trigonometrische und hyperbolische Funktionen | 4.10.2–4.10.4 | sin/cos als Reihe, Euler-Formel, Additionstheoreme, Polardarstellung, sinh/cosh |
| m2_07_differenzierbarkeit | differenzierbarkeit | Differenzierbarkeit und Ableitungsregeln | 5.1 | Definition, linear approximierbar, Regeln, höhere Ableitungen |
| m2_08_mittelwertsatz | mittelwertsatz | Mittelwertsatz und L'Hospital | 5.2 | Rolle, Mittelwertsatz, Monotonie, L'Hospital |
| m2_09_umkehrfunktion | umkehrfunktion | Ableitung der Umkehrfunktion | 5.1.2 | Umkehrregel, arcsin, arctan, ln |
| m2_10_taylor | taylor | Taylor-Polynom und Taylorreihe | 5.2 | Taylor-Polynom, Restglied, Taylorreihen wichtiger Funktionen, Näherung |
| m2_11_extremwerte | extremwerte | Extremwerte in einer Variablen | 5.3 | notwendig/hinreichend, höhere Ableitungen, Randextrema, Optimierungsaufgaben |
| m2_12_partielle_ableitungen | partielle_ableitungen | Partielle Ableitungen und Gradient | 5.4 | partielle Ableitung, Gradient, Richtungsableitung, Höhenlinien |
| m2_13_totale_ableitung | totale_ableitung | Totale Differenzierbarkeit | 5.5 | Jacobi-Matrix, Tangentialebene, Kettenregel |
| m2_14_extrema_mehrdim | extrema_mehrdim | Extrema in mehreren Variablen | 5.6 | kritische Punkte, Hesse-Matrix, Definitheit, Sattelpunkt |
| m2_15_lagrange | lagrange | Extrema mit Nebenbedingungen | 5.6 | Lagrange-Multiplikatoren, Kandidaten bestimmen, Vergleich |
| m2_16_riemann | riemann | Das Riemann-Integral | 5.7.1 | Zerlegung, Ober- und Untersumme, Riemann-Summe, Eigenschaften |
| m2_17_hauptsatz | hauptsatz | Hauptsatz der Differential- und Integralrechnung | 5.7.2 | Stammfunktion, Hauptsatz, Integralfunktion |
| m2_18_integrationstechniken | integrationstechniken | Integrationstechniken | 5.8 | partielle Integration, Substitution, Partialbruchzerlegung |
| m2_19_uneigentliche_integrale | uneigentliche_integrale | Uneigentliche Integrale | 5.9 | unbeschränktes Intervall, Polstellen, Integralkriterium für Reihen |
| m2_20_fourier | fourier | Fourierreihen | 5.10 | periodische Funktionen, Koeffizienten, gerade/ungerade, Beispiele |
| m2_21_dgl_grundbegriffe | dgl_grundbegriffe | Differentialgleichungen: Grundbegriffe | 6.1 | Ordnung, Lösung, Anfangswertproblem, Richtungsfeld |
| m2_22_getrennte_variablen | getrennte_variablen | Getrennte Veränderliche | 6.2.1–6.2.2 | Trennung der Variablen, homogene DGL durch Substitution |
| m2_23_lineare_dgl | lineare_dgl | Lineare DGL erster Ordnung | 6.2.3 | homogene Lösung, Variation der Konstanten, AWP |
| m2_24_dgl_systeme | dgl_systeme | Lineare DGL-Systeme | 6.3 | $y' = Ay$, Fundamentalsystem über Eigenwerte, inhomogene Systeme |
| m2_25_dgl_hoeherer_ordnung | dgl_hoeherer_ordnung | Lineare DGL höherer Ordnung | 6.4 | charakteristisches Polynom, komplexe Nullstellen, Ansatz vom Typ der rechten Seite |
| m2_26_picard_lindeloef | picard_lindeloef | Existenz und Eindeutigkeit | 6.5 | Lipschitz-Bedingung, Picard-Lindelöf, Picard-Iteration |
| m2_27_allgemeine_algebra | allgemeine_algebra | Allgemeine Algebra | 7 (bzw. Kap. 4 in WS 15/16) | Signatur, Algebren, Unteralgebren, Erzeugnis, Homomorphismen, Quotienten |

## Bonus und Klausur

| Datei | Teil | Inhalt |
|---|---|---|
| b_01_python | bonus | Mathe mit Python (niedrige Priorität) |
| k_01_klausur_mathe1 | klausur | Aufgabenpool im Stil von Mathe I: Beweis (Induktion), Relation/Abbildung, Modulo/RSA, Gruppe/Körper, LGS mit Parameter, Determinante, Eigenwerte, Grenzwert, Reihenkonvergenz |
| k_02_klausur_mathe2 | klausur | Aufgabenpool im Stil von KL: Stetigkeit, Potenzreihe, Taylor, Extrema in 2 Variablen, Lagrange, Integral, Fourier, AWP, DGL-System |

Die Probeklausur zieht 6 Aufgaben (90 Minuten, 60 Punkte) aus dem jeweiligen Teil und dem Pool.
