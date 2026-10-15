# Lehrplan – woher jedes Kapitel kommt

Stand: 11.10.2026. Dieser Plan ist für Autoren verbindlich. Jedes Kapitel setzt `quelle=` auf die
Fundstelle aus der Spalte „Quelle“.

## Quellen

| Kürzel | Dokument | Ort |
|---|---|---|
| **MHB** | Modulhandbuch B.Sc. Informatik, PO 2023 (Stand 30.09.2022): „Mathematik I für Informatik“ (04-10-0118, 9 CP, WiSe) und „Mathematik II für Informatik“ (04-10-0119, 9 CP, SoSe). Prüfung: Klausur 90 Minuten; Zulassung über Hausübungen | `Unterlagen/TU_Recherche/Modulhandbuch_BSc_Informatik_PO2023.pdf` (S. 12 und 20) |
| **DIS** | **Verbindlich für Mathe 1:** Skript „Mathematik I für Informatik“, Prof. Dr. Yann Disser, WS 2026/27 (Stand 11.10.2026, Kap. 1–7) und Vorlesungsfolien (VL 1 vom 12.10.2026) | `Unterlagen/Mathe1_Disser_2026/` |
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
das Skript Mathe I (DIS) setzt $\mathbb{N} = \{0, 1, 2, \ldots\}$ und schreibt $\mathbb{N} \setminus \{0\}$ für die positiven.

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
| *(zurückgestellt seit 13.10.2026: v12–v26, Mathe 1 nach DIS hat Vorrang)* | | | | |
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

## Mathe 1 (`teil="mathe1"`, Quelle „Skript Disser WS 26/27, Abschn. x“)

**Grundlage ist ausschließlich das aktuelle Skript DIS** (es ersetzt die frühere Planung nach SKR).
Reihenfolge, Definitionen, Satznummern, Beispiele und Notation folgen DIS. Kapitel zitieren die
Nummern („nach Satz 1.17“), damit Jason Skript und Lernsystem nebeneinander nutzen kann.
Vorlesung: Mo 13:30 und Do 9:50; Gruppenübungen ab 19.10.; **Zwischenprüfung 30.11.–4.12.2026
(Klausurzulassung)**, 12 Übungsquizze (≥ 9 bestanden ⇒ Notenbonus). Diese Termine bestimmen die
Reihenfolge der Bearbeitung: zuerst Kap. 1, dann 2, 3 usw.

**Notation DIS (verbindlich in allen m1-Kapiteln):** $\mathbb{N} = \{0, 1, 2, \ldots\}$, positive
natürliche Zahlen $\mathbb{N} \setminus \{0\}$; $Z_{\geq 0}$; Wahrheitswerte „wahr/falsch“; $:=$
definierend; Beweisende □, Beispielende △; Mengenschreibweise $\{x \in G \mid E(x)\}$; Intervalle
$(a, b]$; Vektoren fett als Spalten $(x_1, \ldots, x_n)^\top$, Einheitsvektoren $e^{(j)}$;
Standardskalarprodukt $(x \mid y)$, Norm $\lVert x \rVert$; lineare Hülle $\langle M \rangle$;
Koordinatenvektor $[v]_{\mathfrak{B}}$; Darstellungsmatrix $[f]_{\mathfrak{C} \leftarrow \mathfrak{B}}$,
Basiswechsel $S_{\mathfrak{C} \leftarrow \mathfrak{B}}$; Spalte $A_{\cdot j}$, Eintrag $A_{ij}$;
Einheitsmatrix $\mathbb{I}_n$; Restklassen $[a]_n$, $\mathbb{Z}/n\mathbb{Z}$, $\mathbb{F}_2$;
$a \operatorname{div} b$, $a \bmod b$; charakteristisches Polynom $\chi_A(t) = \det(A - t\mathbb{I}_n)$;
Landau-Symbole $\mathcal{O}, \Omega, \Theta, o, \omega$.

| Datei | Slug | Titel | DIS | Inhalt |
|---|---|---|---|---|
| m1_01_aussagen | uni_aussagen | Aussagen und logische Verknüpfungen | 1.1–1.2 | Aussage, Aussageform, ¬ ∧ ∨ ⊕ ⇒ ⇔, Wahrheitstabellen, hinreichend/notwendig, ex falso quodlibet, Kontrapositionsgesetz, De Morgan, Bem. 1.9 |
| m1_02_beweisformen | beweisformen | Logisches Schließen und Beweisformen | 1.3 | Satz/Theorem/Lemma/Korollar, Schlussregeln (Modus ponens/tollens, Elimination), direkt, Äquivalenzumformung, Kontraposition, Widerspruch ($\sqrt 2$), Fallunterscheidung (Satz 1.19, 1.20) |
| m1_03_mengen | uni_mengen | Mengen | 1.4 | Aufzählung, Aussonderung, ℕ und ℤ, ∪ ∩ \, disjunkt, Distributivgesetz beweisen (Satz 1.23), Tupel, kartesisches Produkt, $A^0$, Potenzmenge |
| m1_04_quantoren | uni_quantoren | All- und Existenzquantor | 1.5 | ∀, ∃, Negation von Quantoren, Vereinigung und Schnitt über Mengensysteme, leerer Schnitt |
| m1_05_relationen | relationen | Relationen und ihre Eigenschaften | 1.6 | Relation als Teilmenge, gerichteter Graph, reflexiv, symmetrisch, antisymmetrisch, transitiv (Beispiele 1.39–1.41) |
| m1_06_ordnungen | ordnungen | Ordnungen, Supremum und Infimum | 1.6 | Ordnungsrelation, Totalordnung, Maximum/Minimum, Schranken, sup/inf, Satz 1.58 |
| m1_07_aequivalenzrelationen | aequivalenzrelationen | Äquivalenzrelationen | 1.6 | Äquivalenzklasse, Satz 1.63, Faktormenge, ℚ als Faktormenge (Bsp. 1.65) |
| m1_08_abbildungen | uni_abbildungen | Abbildungen | 1.7 | Abbildung als Relation, Bild/Urbild, injektiv/surjektiv/bijektiv, Verkettung, Umkehrabbildung, Einschränkung, Satz 1.82 |
| m1_09_induktion | peano_induktion | Natürliche Zahlen und vollständige Induktion | 2.1–2.2 | Peano-Axiome, ℕ als Mengen, Nachfolger, Induktionsanfang/-schritt, Abwandlungen (Bem. 2.9) |
| m1_10_zaehlen | zaehlen | Endliche Mengen, Addition und Subtraktion | 2.3–2.4 | Kardinalität über Bijektionen, $\lvert A \cup B\rvert$, Summenzeichen, Subtraktion, Satz 2.27 |
| m1_11_division | division_rest | Multiplikation, Division und Division mit Rest | 2.5 | $\lvert A \times B \rvert$, Produktzeichen, Summenformel per Induktion, Teilbarkeit, div und mod, Rechnen mit Resten (Satz 2.44) |
| m1_12_kombinatorik | kombinatorik | Potenz, Fakultät und Binomialkoeffizient | 2.6–2.8 | Abbildungen zählen, $\lvert\mathcal{P}(M)\rvert = 2^{\lvert M\rvert}$, Permutationen, $n!$, $\binom{n}{k}$, Pascal, binomischer Lehrsatz |
| m1_13_rsa | rsa | Kryptographie: RSA | 2.9 | Primzahl, Primzahllemma, kleiner Satz von Fermat, RSA-Schlüssel, Ver-/Entschlüsseln, Korrektheit, Beispiel $n = 55$ |
| m1_14_ganze_zahlen | ganze_zahlen | Die ganzen Zahlen | 3.1 | ℤ als $\mathbb{N}^2/\sim$, Addition, Subtraktion, Multiplikation, Vorzeichenregeln |
| m1_15_gruppen | gruppen | Gruppen | 3.2 | Gruppenaxiome, abelsch, Eindeutigkeit (Satz 3.9), Lösbarkeit, Kürzungsregeln, Beispiele: ℤ, Bitgruppe, Permutationen, $\mathbb{Z}/n\mathbb{Z}$ |
| m1_16_homomorphismen | gruppenhomomorphismen | Untergruppen und Homomorphismen | 3.2 | Untergruppenkriterium, erzeugte Untergruppe, Homomorphismus, Iso-/Automorphismus, Kern, Injektivität ⇔ Kern trivial |
| m1_17_ringe_koerper | ringe_koerper | Ringe, Körper und die rationalen Zahlen | 3.3–3.5 | Ring, Vorzeichenregeln, Restklassenring, Nullteiler, ℚ, Körper, $\mathbb{Z}/p\mathbb{Z}$, Körperhomomorphismus, angeordnete Körper |
| m1_18_reelle_zahlen | reelle_zahlen | Die reellen Zahlen | 3.6 | Vollständigkeitsaxiom, Intervalle, ℚ dicht, n-te Wurzel, rationale Potenz, Betrag, Dreiecksungleichung |
| m1_19_komplexe_zahlen | komplexe_zahlen_uni | Die komplexen Zahlen | 3.7–3.8 | ℂ = ℝ², i, kartesische Darstellung, Konjugation, Betrag, Inverse, nicht anordenbar, Fundamentalsatz, Zahlbereiche |
| m1_20_geometrie_rn | geometrie_rn | Geometrie des ℝⁿ | 4.1 | Vektoren, Geraden, Ebenen, Schnittpunkte, Skalarprodukt, Länge, Orthogonalität, Hyperebene, Abstand (Satz 4.15), Kreuzprodukt, Fläche und Spatvolumen |
| m1_21_vektorraeume | vektorraeume | Vektorräume und Untervektorräume | 4.2–4.3 | Axiome, $K^n$, $K[X]$, Funktionenräume, Unterraumkriterium, lineare Hülle, Linearkombination |
| m1_22_basis_dimension | basis_dimension | Basen und Dimension | 4.4–4.5 | lineare Unabhängigkeit, Basis, Koordinatenvektor, Austauschsatz, Basisergänzung, Dimensionsformel für Untervektorräume |
| m1_23_skalarprodukt | skalarprodukt | Skalarprodukte, Normen und Orthonormalbasen | 4.6–4.7 | Skalarprodukt-Axiome, Cauchy–Schwarz, Normen ($\lVert\cdot\rVert_1$, $\lVert\cdot\rVert_\infty$), Abstand, Orthonormalbasis, Gram–Schmidt |
| m1_24_projektionen | projektionen | Projektionen und affine Räume | 4.8–4.9 | orthogonales Komplement, Orthogonalprojektion, affiner Raum, Dimension einer Hyperebene |
| m1_25_lineare_abbildungen | lineare_abbildungen | Lineare Abbildungen, Kern, Bild und Rang | 5.1–5.2 | Linearität, Basisbilder (Satz 5.9), $\mathrm{Hom}_K(V,W)$, Kern, Bild, Rang, Urbilder, Dimensionsformel, Isomorphie |
| m1_26_matrizen | matrizen_uni | Matrizen und Rechnen mit Matrizen | 5.3–5.4 | Matrix-Vektor-Produkt, Darstellungsmatrix, Matrixprodukt = Verkettung, Rechenregeln, Nullteiler, Transponierte |
| m1_27_invertierbarkeit | invertierbarkeit | Invertierbarkeit | 5.5 | Inverse, Äquivalenzen (Satz 5.65), $AB = \mathbb{I}_n \Rightarrow BA = \mathbb{I}_n$, $\mathrm{GL}_n(K)$ |
| m1_28_basiswechsel | basiswechsel | Basiswechsel und Ähnlichkeit | 5.6–5.7 | Basiswechselmatrix, $S^{-1}AS$, Ähnlichkeit, Haar-Bildcodierung |
| m1_29_lgs_gauss | lgs_gauss | Lineare Gleichungssysteme und Gauß-Verfahren | 6.1–6.2 | Lösungsstruktur, Rangkriterium, Zeilenumformungen, (reduzierte) Zeilenstufenform, Kernbasis, Bildbasis, Inverse per Gauß, über $\mathbb{F}_2$, $\mathbb{F}_5$ |
| m1_30_determinanten | determinanten | Determinanten | 6.3 | Axiome (multilinear, alternierend, normiert), Spaltenumformungen, Berechnung per Gauß, Produktregel, $\det(A^\top)$, Fläche/Volumen |
| m1_31_eigenwerte | eigenwerte | Eigenwerte und Diagonalisierung | 6.4 | Eigenvektor, Eigenraum, $\chi_A$, Ähnlichkeit, Diagonalisierbarkeit, Matrixpotenzen, Fibonacci |
| m1_32_symmetrische_matrizen | symmetrische_matrizen | Symmetrische Matrizen und quadratische Formen | 6.5 | orthogonale Matrizen, Spektralsatz, orthogonale Diagonalisierung, Definitheit |
| m1_33_folgen | folgen_uni | Folgen und Konvergenz | 7.1 | Folge, beschränkt, monoton, ε-Definition, Grenzwertregeln, Einschließung, bestimmt divergent, geometrische Folge, Monotoniekriterium |
| m1_34_teilfolgen | teilfolgen | Teilfolgen und Cauchy-Folgen | 7.1 | Teilfolge, Häufungswert, Bolzano–Weierstraß, Cauchy-Kriterium |
| m1_35_reihen | reihen | Reihen und Konvergenzkriterien | 7.2 | Partialsummen, geometrische/harmonische/Teleskopreihe, absolute Konvergenz, Majorante/Minorante, Leibniz, Quotient, Wurzel, Produktsatz |
| m1_36_asymptotik | asymptotik | Asymptotik und Landau-Symbole | 7.3 | $\mathcal{O}, \Omega, \Theta, o, \omega$, Rechenregeln, Wachstumshierarchie, Laufzeiten |

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
| k_00_zwischenpruefung | klausur | Übungs-Zwischenprüfung Mathe I (Woche 30.11.–4.12.2026, Klausurzulassung), Stoff DIS Kap. 1 bis zum dann erreichten Stand, Stil der Übungsquizze |
| k_01_klausur_mathe1 | klausur | Aufgabenpool im Stil von Mathe I: Beweis (Induktion), Relation/Abbildung, Modulo/RSA, Gruppe/Körper, LGS mit Parameter, Determinante, Eigenwerte, Grenzwert, Reihenkonvergenz |
| k_02_klausur_mathe2 | klausur | Aufgabenpool im Stil von KL: Stetigkeit, Potenzreihe, Taylor, Extrema in 2 Variablen, Lagrange, Integral, Fourier, AWP, DGL-System |

Die Probeklausur zieht 6 Aufgaben (90 Minuten, 60 Punkte) aus dem jeweiligen Teil und dem Pool.
