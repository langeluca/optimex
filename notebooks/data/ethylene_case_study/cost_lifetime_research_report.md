# Kosten- und Lebensdauerrecherche fuer die Ethylen-Fallstudie

## Status und Abgrenzung

Stand: 31. Juli 2026

Dieser Bericht wertet die fuenf bereitgestellten Quellen aus und dokumentiert
die daraus verbleibenden Modellannahmen. Er trennt:

- Rohwerte aus den Quellen,
- deren Eignung fuer das konkrete Optimex-Modell,
- nachvollziehbare Umrechnungen,
- Modelllebensdauern,
- weiterhin offene Datenluecken.

Brightway, der `LCADataProcessor` und der Solver wurden bei dieser Bereinigung
nicht ausgefuehrt. `ethylene_case_study.ipynb` und
`case_study_assumptions.md` wurden an die unveraenderte Uebernahme der
Inventory-Mengen angepasst. `cost_inputs.csv` bleibt unveraendert.

Die Quellenwerte werden grundsaetzlich zunaechst in Originalwaehrung und
Originalpreisjahr dokumentiert. Eine Umrechnung auf `EUR_2025` erfolgt nur mit
einem expliziten Faktor und einer separaten Indexquelle. Fuer Naphtha wurde
dies inzwischen mit den HICP-Jahresraten des Euroraums fuer 2023-2025
umgesetzt; die uebrigen neu extrahierten Werte bleiben vorerst in ihrer
Originalbasis. Es wird keine stillschweigende Umrechnung vorgenommen.

## Kurzfazit

1. Tiggeloven liefert die wertvollsten route-spezifischen Kostenfunktionen:
   Steam Cracking, direkte Methanolsynthese aus CO2, MTO und
   CO2-Elektrolyse. Die Werte sind `EUR_2022` und enthalten einen
   kapazitaetsabhaengigen sowie teilweise einen fixen Kostenanteil.
2. Diese route-spezifischen Anlagenkosten werden nicht als Preis der generischen
   Brightway-Infrastruktur eingetragen. Steam Cracking, MTO und das aggregierte
   eCO2R-System verwenden stattdessen eindeutig benannte Installations-Wrapper;
   ihre Preise bleiben bis zur Umrechnung der recherchierten TPC-Werte technische
   `PLACEHOLDER`.
3. Fuer Naphtha liegt ein direkt brauchbarer Rohpreis vor. Er wird fuer diese
   Fallstudie als `PROXY` fuer den gesamten allokierten Steam-Cracker-Feedstock-
   Slate verwendet. Sieben Feedstock-Inputs sind dazu in der Case-Study-Activity
   `steam cracking feedstock mix` gebuendelt. Strom,
   Erdgaswaerme und Ethane koennen nur als Szenario- oder Regionsproxys
   verwendet werden. Der Grossteil der Hilfsstoffe, Kuehlmedien, Wasser- und
   Abfallbehandlungen bleibt durch die bereitgestellten Quellen ungedeckt.
4. Deutz und Bardow stuetzen die gewaehlte DAC-Modelllebensdauer von 20 Jahren.
   Diepers nennt als alternative Fallstudienannahmen 15 Jahre fuer DAC und
   CO2-Hydrierung sowie 8 Jahre fuer PEM. Fuer die aktuelle Case Study werden
   stattdessen Tiggelovens 25 Jahre fuer
   Steam Cracking, die Elektrolyseanlage, direkte Methanolsynthese aus CO2, MTO,
   CO2-Elektrolyse und die ASU-basierte Aufbereitung uebernommen.
5. Die Literaturwerte werden nur als Optimex-Modelllebensdauern verwendet.
   Installationsexchanges werden mit ihren normalen Inventory-Mengen
   unveraendert uebernommen; eine Recherche der Quellenlebensdauern und eine
   Multiplikation der Koeffizienten mit einer Lebensdauer entfallen.

## Bewertungslogik

| Eignung | Bedeutung |
|---|---|
| `DIRECT` | Technologie, Kostenbasis und Bezugsmenge passen direkt oder mit rein mechanischer Einheitenumrechnung. |
| `PROXY` | Fachlich nutzbare Naeherung, aber Technologie, Region, Systemgrenze oder Kapazitaetsbasis weichen ab. |
| `NOT_SUITABLE` | Der Wert sollte fuer den betreffenden Modellparameter nicht verwendet werden. |
| `UNCLEAR` | Kontext, Kostenumfang oder Bezugsbasis reichen fuer eine belastbare Zuordnung nicht aus. |

`DIRECT` bedeutet nicht automatisch, dass ein Wert bereits in die CSV
eingetragen werden kann. Die Modellabbildung und die Umrechnung auf `EUR_2025`
muessen ebenfalls geklaert sein.

## Aktueller Modellstand

### Modelllebensdauern

| Prozess | Aktueller Wert | Status im Notebook |
|---|---:|---|
| Steam Cracking | 25 a | Recherchierter Wert aus Tiggeloven, Tabelle C.1 |
| DAC | 20 a | Recherchierter Wert aus Deutz und Bardow (2021) |
| PEM-Elektrolyse | 25 a | Tiggeloven-AEC-Anlagenproxy; separater 9-jaehriger Stacktausch nicht modelliert |
| CO2-Hydrierung | 25 a | Recherchierter Wert fuer direkte Methanolsynthese aus CO2 aus Tiggeloven |
| MTO | 25 a | Recherchierter Wert aus Tiggeloven |
| eCO2R-Reaktor | 25 a | Tiggeloven-Proxy fuer CO2-Elektrolyse |
| eCO2R-Aufbereitung | 25 a | Tiggeloven-ASU-Proxy |

### Installationskoeffizienten aus den Inventories

| Installation | Verwendeter Koeffizient | Inventory-Basis |
|---|---:|---|
| Steam-Cracker-Installation | `1.1516356618335166e-10` | `unit steam cracker installation/kg ethylene`; Wrapper enthält `1 unit chemical factory construction, organics` |
| DAC-System | `1.25e-8` | `unit/kg CO2` |
| PEM-Stack | `1.34989e-6` | `unit/kg H2` |
| PEM Balance of Plant | `3.37373e-7` | `unit/kg H2` |
| CO2-Hydrierungsinstallation | `3.5842e-12` | `unit CO2 hydrogenation installation/kg methanol`; Wrapper enthält `1 unit chemical factory construction, organics` |
| MTO-Installation | `3.584e-12` | `unit methanol-to-olefins installation/kg ethylene`; Wrapper enthält `1 unit chemical factory construction, organics` |
| eCO2R-Systeminstallation | `4e-10` | `unit installation/kg ethylene`; intern `1 unit chemical factory construction, organics`, `0.185 kg copper` und `7544.1975 kg steel` je Wrapper-Einheit. Korrektur nach Rücksprache mit dem disco2very-Ersteller; die absoluten Kupfer- und Stahlmengen bleiben unverändert. |

Die Betrags- und Referenzproduktbasis bleibt mit Ausnahme der bestätigten
eCO2R-Korrektur identisch zum Quellinventory. `operation=False` kennzeichnet die
zeitliche Skalierung als Installation, fuehrt aber nicht zu einer Umrechnung
auf Jahreskapazitaet.

## Rohwerte aus den Quellen

### 1. Tiggeloven (2026)

Quelle: Julia Tiggeloven, *Breaking and re-forming the chemical industry:
Optimizing the transition from fossil-based clusters to net zero*.

#### Anlagenkosten

Tabelle C.1, gedruckte Seite 168, PDF-Seite 183. Alle Kosten sind
`EUR_2022`. Die Kostenfunktion lautet:

```text
Total plant cost = lambda * size + zeta
```

| Technologie | Groessenbasis | lambda | zeta | Instandhaltung | Lebensdauer | Eignung |
|---|---|---:|---:|---:|---:|---|
| Conventional cracker, current layout | t Naphtha/h | 2.083 MEUR/(t/h) | 543 MEUR | 4.0 % TPC/a | 25 a | `PROXY` fuer Steam Cracking |
| Conventional cracker with carbon capture | t Naphtha/h | 2.730 MEUR/(t/h) | 558 MEUR | 4.0 % TPC/a | 25 a | `NOT_SUITABLE` fuer aktuelle Route ohne CCS |
| Electric cracker | t Naphtha/h | 2.083 MEUR/(t/h) | 543 MEUR | 4.0 % TPC/a | 25 a | `NOT_SUITABLE` fuer fossile Referenz |
| Alkaline electrolysis (AEC) | MW_el | 0.753 MEUR/MW | 0 | 2.0 % TPC/a | 25 a | `NOT_SUITABLE` fuer PEM-CAPEX |
| Direct methanol synthesis from CO2 | t CO2/h | 1.613 MEUR/(t/h) | 104 MEUR | 2.5 % TPC/a | 25 a | `PROXY`, technisch sehr nah |
| Methanol-to-olefins | t Methanol/h | 1.051 MEUR/(t/h) | 66 MEUR | 2.5 % TPC/a | 25 a | `PROXY` |
| CO2 electrolysis | t CO2/h | 9.461 MEUR/(t/h) | 0 | 2.0 % TPC/a | 25 a | `PROXY`, Prozessbasis weicht stark ab |
| Air separation unit | MW_el | 4.224 MEUR/MW | 25 MEUR | 4.2 % TPC/a | 25 a | `PROXY` fuer kryogene Apparate, nicht fuer gesamte eCO2R-Aufbereitung |
| Gas boiler | MW_gas | 0.106 MEUR/MW | 0 | 4.0 % TPC/a | 25 a | nur zur Waermeableitung |

Die Quelle annualisiert die Investition mit Instandhaltung und Annuitaetsfaktor:

```text
annual cost = (maintenance fraction + annuity factor)
              * (lambda * size + zeta)
```

Der Investitionswert selbst ist damit nicht annualisiert. Der
Instandhaltungssatz ist nicht im TPC enthalten, sondern wird jaehrlich als
Anteil des TPC angesetzt (Gleichung 4.4, gedruckte Seite 90, PDF-Seite 105).

#### Technische Bezugsdaten

Tabelle C.2, gedruckte Seite 169, PDF-Seite 184:

| Technologie | Relevante Verhaeltnisse |
|---|---|
| Conventional cracker | Input Naphtha 1; Output Ethylen 0.303, jeweils auf Massenbasis |
| Direkte Methanolsynthese | Input CO2 1; Output Methanol 0.685 |
| MTO | Input Methanol 1; Output Ethylen 0.592 |
| CO2-Elektrolyse | Input CO2 1; Output Ethylen 0.602 |
| Gas boiler | 0.920 MJ Dampf je MJ Erdgas |

#### Energie- und Feedstockpreise

Tabelle 4.2, gedruckte Seite 88, PDF-Seite 103:

| Kostenposition | Kurzfristig | Mittelfristig | Langfristig | Einheit | Eignung |
|---|---:|---:|---:|---|---|
| DAC-CO2 | 618 | 475 | 355 | EUR_2022/t CO2 | Validierung, nicht als Marktpreis des foreground-DAC |
| DAC-CO2, optimistisch | 355 | 275 | 200 | EUR_2022/t CO2 | Validierung |
| Methan | 56 | 56 | 59 | EUR_2022/MWh | `PROXY` fuer Erdgaswaerme |
| Naphtha | 732 | 732 | 732 | EUR_2022/t | `DIRECT` als Rohwert fuer `market for naphtha` |

Der Text ordnet die drei Zukunftszustaende den Jahren 2030, 2040 und 2050 zu.

Strompreise:

- Niederlaendischer Day-ahead-Mittelwert 2019: `0.0412 EUR/kWh`.
- Synthetisches Zukunftsprofil: Mittelwert `0.068 EUR/kWh`.
- Chemelot: 2030 `108.2`, 2040 `272.9`, 2050 `20.5 EUR/MWh`.
- Zeeland: 2030 `79.7`, 2040 `253.7`, 2050 `13.0 EUR/MWh`.

Die standortspezifischen Werte stammen aus einem Stromsystem-Szenario mit
Knappheitsspitzen und sind nicht mit `REMIND-EU_SSP2-NDC` identisch. Sie sind
daher nur `PROXY`, nicht eine allgemeine europaeische Industriestromprognose
(Abbildung C.1, gedruckte Seite 172, PDF-Seite 187).

#### Elektrolyseur-Komponenten

Gedruckte Seite 159, PDF-Seite 174:

- Elektrolyseur-Stacks: 9 Jahre.
- Uebrige Anlagenteile: 25 Jahre.
- Stack-Anteil an den Anlagenkosten: 23.8 %.

Die betrachtete Technologie ist AEC, nicht PEM. Die Lebensdauertrennung ist
deshalb ein guter konzeptioneller Proxy fuer Stack und Balance of Plant, aber
kein direkter PEM-Kostenwert.

### 2. Cattry et al. (2025)

Quelle: Alexandre Cattry, Chaitanya Vuppanapalli und Dharik S. Mallapragada,
*Comparative reactor, process, techno-economic, and life cycle emissions
assessment of ethylene production via electrified and thermal steam cracking*,
Green Chemistry 27 (2025), 13357.

Basis der techno-oekonomischen Analyse (PDF-Seite 7):

- 1,000 kt Ethylen/a.
- Ethane-basierter Steam Cracker in Texas/ERCOT.
- Anlagenlebensdauer 30 Jahre.
- Capacity Factor 95 %.
- Diskontsatz 8 %.
- Kostenbasis `USD_2023`.
- Total overnight cost umfasst Prozessausruestung, Nebenanlagen, direkte und
  indirekte Arbeit, Contractor Services und Contingency.

| Kostenposition | Wert | Einheit | Eignung |
|---|---:|---|---|
| Ethane, 2024 | 330 | USD_2023/t Ethane | `PROXY`, USA und Ethane-Feed |
| Erdgas | 14.4 | USD_2023/MWh HHV | `PROXY`, USA |
| ERCOT-Strom 2022 | 60 | USD_2023/MWh | `PROXY`, USA |
| ERCOT-Strom 2035 | 29.84 bis 63.53 | USD_2023/MWh | Szenarioband, `PROXY` |

Levelized cost of ethylene (PDF-Seiten 11-12):

| Route | Wert | Einheit | Verwendung |
|---|---:|---|---|
| Thermal steam cracking | 747 | USD_2023/t Ethylen | Plausibilitaetskontrolle |
| Thermal steam cracking mit CCS | 788 | USD_2023/t Ethylen | nicht aktuelle Route |
| Elektrifizierte Varianten | ca. 578 bis 733 | USD_2023/t Ethylen | nicht aktuelle Route |

Diese Werte sind aggregierte Produktionskosten und duerfen nicht zusaetzlich zu
einzelnen Feedstock-, Energie- und Anlagenpreisen eingetragen werden. Sonst
entsteht Doppelzaehlung.

Die in der Sensitivitaetsanalyse genannte Reaktorlebensdauer von rund 5 Jahren
bezieht sich nur auf den neuartigen elektrischen i-ERH-Reaktor. Sie ist kein
geeigneter Wert fuer den konventionellen Steam Cracker im Modell.

### 3. Diepers

Quelle: `Dissertation_Diepers_Einreichung.pdf`, Abbildung 5.2, gedruckte
Seite 68, PDF-Seite 88.

| Prozess | Modelllebensdauer | Eignung |
|---|---:|---|
| DAC | 15 a | `PROXY`, alternative Annahme aus dem Optimex-Fallstudienvorbild; nicht fuer die aktuelle Case Study gewaehlt |
| PEM-Elektrolyse | 8 a | `PROXY`, direkt aus dem Optimex-Fallstudienvorbild |
| CO2-Hydrierung | 15 a | `PROXY`, direkt aus dem Optimex-Fallstudienvorbild |
| Erdgasreformierung | 25 a | keine direkte Uebertragung auf Steam Cracking |

Die Werte bleiben als Vergleich mit dem Optimex-Fallstudienvorbild dokumentiert,
werden fuer die aktuelle Ethylen-Case-Study aber nicht verwendet. Fuer die
unveraenderte Uebernahme der disco2very-Inventory-Mengen werden keine weiteren
Lebensdauerangaben benoetigt.

### 4. Zibunas et al. (2022)

Quelle: Zibunas et al., *Cost-optimal pathways towards net-zero chemicals and
plastics based on a circular carbon economy*.

- Neue und bestehende Chemieanlagen: 30 Jahre.
- Jaehrliche Stilllegung bestehender Kapazitaet: 1/30.
- Erneuerung nach 30 Jahren wird mit den Kosten einer Neuanlage angenaehert.
- WACC: 8 %.
- Off-grid-Strom bis 2030: 36 USD/MWh.
- Unsicherheitsband Strom: 26 bis 79 USD/MWh.
- Unsicherheitsband Erdgas: 4.9 bis 8.2 USD/GJ.

Der allgemeine Chemieanlagenwert von 30 Jahren ist ein guter
Plausibilitaetsbereich, aber weniger technologiespezifisch als Tiggelovens
25 Jahre fuer Steam Cracking und MTO. Die bereitgestellte Hauptpublikation
enthaelt keine ausreichend detaillierte Kostenmatrix fuer die konkreten
Foreground-Anlagen.

### 5. Kaetelhoen et al. (2016)

Quelle: Kaetelhoen et al., *Stochastic Technology Choice Model for
Consequential Life Cycle Assessment*.

Die Publikation begruendet, warum Kostenunsicherheit die Technologiewahl
beeinflussen kann. Sie enthaelt keine direkt verwendbaren Preise oder
Lebensdauern fuer die modellierten Ethylenrouten.

## Nachvollziehbare CAPEX-Normalisierung

### Gemeinsame Annahmen

Die folgenden Rechnungen dienen der Modellzuordnung, nicht einer automatischen
CSV-Aenderung:

```text
Ethylennachfrage = 1e9 kg/a
Betriebsstunden = 8760 h/a
```

Ein zusaetzlicher Capacity Factor wird nicht eingerechnet. Die so berechnete
Groesse ist eine kontinuierliche Jahreskapazitaet. Fuer andere
Auslastungsannahmen muss die Nennkapazitaet entsprechend angepasst werden.

Der fixe Kostenanteil `zeta` wird bei der Normierung auf genau
`1e9 kg Ethylen/a` verteilt. Das ist eine Fallstudienannahme. Eine lineare
Optimierung kann den fixen Kostenblock nicht fuer beliebige Anlagengroessen
exakt abbilden.

### Steam Cracking

Tiggeloven-Basis:

```text
Naphtha-Durchsatz
  = 1e9 kg Ethylen/a / 0.303 / 8760 h/a / 1000 kg/t
  = 376.750 t Naphtha/h

TPC
  = 2.083 MEUR/(t/h) * 376.750 t/h + 543 MEUR
  = 1,327.770 MEUR_2022

Normierter TPC
  = 1,327.770 MEUR / 1e9 kg Ethylen/a
  = 1.327770 EUR_2022/(kg Ethylen/a)

Jaehrliche Instandhaltung
  = 4.0 % * 1,327.770 MEUR
  = 53.111 MEUR_2022/a
```

Bewertung: `PROXY`. Die Kostenfunktion bezieht sich auf einen
Naphtha-Cracker. Das ecoinvent-Inventar verwendet einen europaeischen
Feedstock-Mix aus Naphtha, Ethane, Propan, Butan und weiteren Komponenten.

### MTO

Mit dem aktuellen Modellkoeffizienten
`2.3920583664 kg Methanol/kg Ethylen`:

```text
Methanol-Durchsatz
  = 1e9 * 2.3920583664 / 8760 / 1000
  = 273.066 t Methanol/h

TPC
  = 1.051 MEUR/(t/h) * 273.066 t/h + 66 MEUR
  = 352.992 MEUR_2022

Normierter TPC
  = 0.352992 EUR_2022/(kg Ethylen/a)

Jaehrliche Instandhaltung
  = 2.5 % * 352.992 MEUR
  = 8.825 MEUR_2022/a
```

Tiggelovens eigener Ethylenertrag von `0.592 kg/kg Methanol` ergaebe dagegen
`192.830 t Methanol/h` und `268.664 MEUR_2022`. Fuer die interne Konsistenz
waere der aktuelle Foreground-Koeffizient zu verwenden; die Abweichung muss
als Unsicherheit dokumentiert werden.

### Direkte Methanolsynthese aus CO2

Mit dem aktuellen Foreground-Koeffizienten
`1.435820454 kg CO2/kg Methanol` und der Methanolmenge fuer die MTO-Route:

```text
CO2-Durchsatz
  = 1e9 * 2.3920583664 * 1.435820454 / 8760 / 1000
  = 392.074 t CO2/h

TPC
  = 1.613 MEUR/(t/h) * 392.074 t/h + 104 MEUR
  = 736.415 MEUR_2022

Normiert auf Methanolkapazitaet
  = 736.415 MEUR / 2.3920583664e9 kg Methanol/a
  = 0.307858 EUR_2022/(kg Methanol/a)

Jaehrliche Instandhaltung
  = 2.5 % * 736.415 MEUR
  = 18.410 MEUR_2022/a
```

Tiggelovens Verhaeltnis entspricht `1 / 0.685 = 1.460 kg CO2/kg Methanol` und
liegt damit nahe am aktuellen Foreground-Wert. Dies ist die technisch staerkste
CAPEX-Uebereinstimmung der bereitgestellten Quellen.

### eCO2R

Mit dem aktuellen Foreground-Koeffizienten
`9.229 kg CO2/kg Roh-Ethylen`:

```text
CO2-Durchsatz
  = 1e9 * 9.229 / 8760 / 1000
  = 1,053.539 t CO2/h

TPC
  = 9.461 MEUR/(t/h) * 1,053.539 t/h
  = 9,967.531 MEUR_2022

Normierter TPC
  = 9.967531 EUR_2022/(kg Ethylen/a)
```

Mit Tiggelovens eigenem Ethylenertrag von `0.602 kg/kg CO2` ergaeben sich:

```text
CO2-Durchsatz = 189.627 t/h
TPC = 1,794.058 MEUR_2022
Normierter TPC = 1.794058 EUR_2022/(kg Ethylen/a)
```

Die Differenz ist zu gross fuer eine unkommentierte Uebertragung. Der Wert ist
`UNCLEAR/PROXY`, bis geklaert ist, ob die Prozesse dieselbe Systemgrenze,
Konversion, Produktreinheit und Rueckfuehrung abbilden.

### Industrielle Waerme aus Erdgas

Mit Tiggelovens Methanpreis und dem Kesselwirkungsgrad von 0.920:

```text
2030 und 2040:
56 EUR_2022/MWh_gas / 0.920 / 3600 MJ/MWh
= 0.016908 EUR_2022/MJ_waerme

2050:
59 EUR_2022/MWh_gas / 0.920 / 3600 MJ/MWh
= 0.017814 EUR_2022/MJ_waerme
```

Diese Ableitung enthaelt nur den Brennstoff. Kessel-CAPEX und Instandhaltung
sind nicht enthalten. Der Wert ist daher `PROXY`.

### Direkte Betriebspreise

| Flow | Rohwert | Mechanische Umrechnung | Eignung |
|---|---:|---:|---|
| Naphtha | 732 EUR_2022/t | 0.732 EUR_2022/kg; 0.806635610112 EUR_2025/kg nach HICP-Umrechnung | `DIRECT` als Rohwert, `PROXY` fuer den gebuendelten Feedstock-Slate |
| Ethane | 330 USD_2023/t | 0.330 USD_2023/kg | `PROXY`, USA |
| Strom NL 2019 | 41.2 EUR/MWh | 0.0412 EUR/kWh | `PROXY` |
| Strom Chemelot 2030/2040/2050 | 108.2 / 272.9 / 20.5 EUR/MWh | 0.1082 / 0.2729 / 0.0205 EUR/kWh | `PROXY`, stark szenarioabhaengig |
| Strom Zeeland 2030/2040/2050 | 79.7 / 253.7 / 13.0 EUR/MWh | 0.0797 / 0.2537 / 0.0130 EUR/kWh | `PROXY`, stark szenarioabhaengig |

#### Entscheidung zum Steam-Cracker-Feedstock

Tiggeloven nennt `732 EUR_2022/t` als durchschnittlichen Naphtha-Preis fuer
2022 und verweist auf die INSEE-Spotpreisreihe fuer nordwesteuropaeisches
Naphtha. Der Quellenwert stammt damit nicht aus einer eigenen Preisschaetzung
von Tiggeloven. Die unveraenderte Fortschreibung in Tabelle 4.2 ist dagegen
eine Modellannahme.

Fuer `EUR_2025` wird der Quellenwert mit den HICP-Jahresraten des Euroraums fuer
2023 bis 2025 umgerechnet:

```text
0.732 * 1.054 * 1.024 * 1.021
= 0.806635610112 EUR_2025/kg
```

Der Wert wird real konstant fuer alle Stutzjahre auf `steam cracking feedstock
mix` eingetragen. Die Activity buendelt Butan, Ethan, Naphtha, Natural Gas
Liquids, Propan, Refinery Gas und Atmospheric Gas Oil, das im ecoinvent-Inventar
durch Diesel approximiert wird. Ihre internen Massenanteile betragen
`16.2/4.5/64.0/2.2/7.6/1.5/4.0 %`; der Steam Cracker bezieht insgesamt
`1.21675954200327 kg Mix/kg Ethylen`.

Nur der direkte Mix-Flow wird bepreist. Die sieben internen premise-Inputs
erscheinen deshalb nicht mehr als eigene direkte Kostenpositionen. Die statische
Modell- und CSV-Umstellung ist umgesetzt; die Laufzeitprüfung des
`LCADataProcessor` und der LCIA-Gleichheit steht aus.

## Empfohlene Modelllebensdauern

Diese Tabelle betrifft ausschliesslich die zeitliche Verfuegbarkeit und
Ersetzung von Optimex-Kapazitaeten. Die Werte veraendern keine
Inventory-Koeffizienten.

| Prozess | Aktuell | Literatur | Vorlaeufige Empfehlung | Begruendung |
|---|---:|---|---:|---|
| Steam Cracking | 25 a | 25 a Tiggeloven; 30 a Cattry/Zibunas | 25 a, `RESEARCHED` | technologiespezifischer Wert aus Tiggelovens Tabelle C.1 |
| DAC | 20 a | 20 a Deutz und Bardow; 15 a Diepers | 20 a, `RESEARCHED` | Deutz und Bardow liefern das verwendete DAC-LCI und nehmen fuer dasselbe System 20 Jahre an |
| PEM-Elektrolyse | 25 a | 8 a Diepers; Stack 9 a und restliche Anlage 25 a bei Tiggeloven-AEC | 25 a, `PROXY` | AEC-Anlagenlebensdauer wird auf PEM uebertragen; separater Stacktausch bleibt außerhalb des Ein-Prozess-Modells |
| CO2-Hydrierung | 25 a | 15 a Diepers; 25 a Tiggeloven | 25 a, `RESEARCHED` | direkter Wert fuer Methanolsynthese aus CO2 in Tiggelovens Tabelle C.1 |
| MTO | 25 a | 25 a Tiggeloven; 30 a generische Chemieanlage Zibunas | 25 a, `RESEARCHED` | technologiespezifischer Wert aus Tiggelovens Tabelle C.1 |
| Aggregierter eCO2R-Prozess | 25 a | 25 a Tiggeloven CO2-Elektrolyse und ASU-/Chemieanlagenproxy | 25 a, `PROXY` | gemeinsame Modelllebensdauer fuer Reaktion und Aufbereitung |

Alle Empfehlungen bleiben Annahmen fuer eine Framework-Demonstration.

## Inventory-Uebernahmeregel

- Normale ecoinvent-, disco2very- und andere Brightway-Inventory-Mengen werden
  unveraendert uebernommen, auch fuer PEM Stack und Balance of Plant.
- Fuer die Installationsskalierung muss keine Quellenlebensdauer recherchiert
  werden.
- Weiterhin fachlich zu entscheiden ist, ob ein Exchange Betrieb
  (`operation=True`) oder Installation (`operation=False`) darstellt.
- Nur die Lebensdauern der Optimex-Foreground-Prozesse steuern Verfuegbarkeit
  und Ersatz von Kapazitaetsvintages.

## Abdeckung der aktuellen Kosten-CSV

Die CSV enthaelt 38 eindeutige Flow-Identitaeten mit je vier Stuetzwerten
(2020, 2030, 2040, 2050). Alle 38 bleiben formal abgedeckt. Die folgende
Bewertung sagt, ob die neu bereitgestellten Quellen einen vorhandenen Wert
inhaltlich verbessern.

### Investitionsflows

| CSV-Flow | Neue Evidenz | Bewertung und naechster Schritt |
|---|---|---|
| `eCO2R system installation` | eCO2R-CAPEX aus Tiggeloven | Eindeutiger unit-Wrapper ist umgesetzt; vorläufig `1 EUR_2025/unit` als `PLACEHOLDER`, bis der aggregierte TPC auf die Fabrikeinheitenbasis umgerechnet ist. |
| `steam cracker installation` | Steam-Cracker-CAPEX aus Tiggeloven | Eindeutiger unit-Wrapper ist umgesetzt; vorläufig `1 EUR_2025/unit` als `PLACEHOLDER`, bis der TPC auf die Wrapper-Einheit umgerechnet ist. |
| `methanol-to-olefins installation` | MTO-CAPEX aus Tiggeloven | Eindeutiger unit-Wrapper ist umgesetzt; vorläufig `1 EUR_2025/unit` als `PLACEHOLDER`, bis der TPC auf die Wrapper-Einheit umgerechnet ist. |
| `direct air capture system construction, solid sorbent, 4 ktCO2/a` | Deutz-und-Bardow-Inventar und kapazitaetsgleiche Kostendaten aus Sievert et al. | Der fruehere solvent-basierte 1-Mt-Proxy wurde entfernt. Den TPC aus Sievert et al. auf `EUR_2025` umrechnen und direkt je 4-kt-Einheit eintragen; bis dahin bleibt `1 EUR/Einheit` ein technischer `PLACEHOLDER`. |
| `electrolyzer production, 1MWe, PEM, Balance of Plant` | AEC-Lebensdauertrennung, kein PEM-CAPEX | Vorhandene IRENA-Proxys behalten; AEC-CAPEX nicht uebertragen. |
| `electrolyzer production, 1MWe, PEM, Stack` | AEC-Stack 9 a, Kostenanteil 23.8 %, kein PEM-CAPEX | Lebensdauerhinweis dokumentieren; vorhandene IRENA-Proxys behalten. |
| `CO2 hydrogenation installation` | direkte CO2-Methanolsynthese-CAPEX-Funktion | Eindeutiger unit-Wrapper ist umgesetzt; den recherchierten TPC auf die Wrapper-Einheit umrechnen. Der frühere premise-Flow `methanol production facility, construction` wurde entfernt, weil sein abstrahierter Einheitenmaßstab nicht zum disco2very-Koeffizienten passt. |

### Betriebsflows

| CSV-Flow | Neue Evidenz | Bewertung und naechster Schritt |
|---|---|---|
| `cooling energy production, at -25 °C, propylene compression refrigeration system 1 MW` | keine | Vorhandenen Proxy behalten. |
| `heat production, at heat pump 30kW, allocation exergy` | keine | Vorhandenen Proxy behalten. |
| `adsorbent, amine on alumina` | disco2very-Inventar aus PEI und Aluminiumoxid; Kostendaten aus Sievert et al. | Der unpassende Aktivkohleproxy wurde entfernt. Sorbenspreis auf `EUR_2025/kg` uebertragen; bis dahin technischer `PLACEHOLDER`. |
| `steam cracking feedstock mix` | 0.732 EUR_2022/kg Naphtha; 0.806635610112 EUR_2025/kg nach HICP-Umrechnung | `PROXY` fuer den gesamten siebenkomponentigen Feedstock-Mix; interne Feedstocks werden nicht separat bepreist. |
| `market for compressed air, 700 kPa gauge` | keine | `PLACEHOLDER`; weitere Recherche. |
| `market for cooling energy` | keine | Vorhandenen Proxy behalten. |
| `market for cooling energy, at -100 °C` | keine | Vorhandenen Proxy behalten. |
| `market for cooling energy, at -15 °C` | keine | Vorhandenen Proxy behalten. |
| `market for cooling energy, at -45 °C` | keine | Vorhandenen Proxy behalten. |
| `market for cooling energy, at -55 °C` | keine | Vorhandenen Proxy behalten. |
| `market for electricity, medium voltage`, DE | NL- und Standort-Szenariowerte | Nur `PROXY`; fuer beide Stromflows eine gemeinsame, bewusst gewaehlte Trajektorie verwenden. |
| `market for hazardous waste, for incineration` | keine | Negativer Preisvorzeichenkonvention folgen; weitere Recherche. |
| `market for hazardous waste, for underground deposit` | keine | Negativer Preisvorzeichenkonvention folgen; weitere Recherche. |
| `market for heat, district or industrial, natural gas` | 0.016908 bis 0.017814 EUR_2022/MJ Brennstoffwaerme | `PROXY`; deckt keinen Kessel-CAPEX/O&M ab. |
| `market for inert waste, for final disposal` | keine | Negativer Preisvorzeichenkonvention folgen; weitere Recherche. |
| `market for methanol` | kein geeigneter Marktpreis | Steam-Cracker-Hilfsinput bleibt offen. Nicht den foreground-intern erzeugten Methanolfluss zusaetzlich bepreisen. |
| `market for nitrogen, liquid` | keine | `PLACEHOLDER`; weitere Recherche. |
| `market for sodium hydroxide, without water, in 50% solution state` | keine | `PLACEHOLDER`; weitere Recherche. |
| `market for wastewater, average` | keine | Negativer Preisvorzeichenkonvention folgen; weitere Recherche. |
| `market for wastewater, unpolluted` | keine | Vorhandenen Proxy behalten. |
| `market for water, deionised`, CH | keine | `PLACEHOLDER`; spaeter mit dem Europa-Proxy harmonisieren oder separat recherchieren. |
| `market for water, deionised`, Europe without Switzerland | keine | Vorhandenen Proxy behalten. |
| `market group for electricity, medium voltage`, DEU | dieselben Stromproxys | Dieselbe Trajektorie wie fuer den DE-Stromflow verwenden, sofern kein begruendeter Unterschied modelliert wird. |
| `treatment of spent anion exchange resin from potable water production, municipal incineration` | keine | Vorhandenen Proxy und negative Vorzeichenkonvention behalten. |

## Doppelzaehlungs- und Abbildungsrisiken

### Route-spezifischer CAPEX gegen generische Brightway-Infrastruktur

Ein `market_price` wird einem konkreten Brightway-Flow zugeordnet. Deshalb
verwenden Steam Cracking und MTO nun die getrennten Flows `steam cracker
installation` und `methanol-to-olefins installation`. Beide verweisen intern
auf `chemical factory construction, organics`, dessen Umweltinventar dadurch
erhalten bleibt, ohne ihm einen gemeinsamen route-unspezifischen Preis zu geben.

Analog fasst `eCO2R system installation` die organisch-chemische Fabrik, Kupfer
und Stahl hinter einer einzigen direkten CAPEX-Identitaet zusammen. Die drei
generischen Inputs werden nicht mehr einzeln durch optimex bepreist.

Die LCA-Infrastruktur bleibt durch die internen Wrapper-Exchanges unveraendert.
Offen ist nicht mehr die Architektur, sondern die nachvollziehbare Umrechnung
der route-spezifischen TPC-Werte auf die jeweiligen Wrapper-Einheiten.

### Fixe Anlagenkosten

Die Kostenfunktionen enthalten `zeta`, einen von der Anlagengroesse
unabhaengigen Anteil. Eine lineare Kostenrate je Einheit Kapazitaet bildet ihn
nur fuer die gewaehlte Referenzgroesse von `1 Mt/a` korrekt ab. Bei kleineren
oder mehreren Anlagen wird die Skalierung ungenau.

### Instandhaltung

Die recherchierten Instandhaltungssaetze beziehen sich auf den installierten
TPC. Sie sind kapazitaets- und nicht produktionsabhaengig. Eine Umrechnung in
variable EUR/kg und Eintragung als Betriebsflow wuerde bei Teillast und
Brownfield-Kapazitaet zu falschen Kosten fuehren.

### Aggregierte Produktionskosten

Levelized costs aus Cattry enthalten bereits CAPEX, Feedstock, Energie und
weitere Betriebskosten. Sie duerfen nur als Plausibilitaetskontrolle verwendet
werden, wenn die Einzelkomponenten im Optimex-Modell separat bepreist werden.

### Foreground-Zwischenprodukte

Im Foreground erzeugter Wasserstoff, abgeschiedenes CO2, Methanol und
Roh-Ethylen erhalten keinen zusaetzlichen Marktpreis. Ihre Kosten werden aus
den vorgelagerten Anlagen und Betriebsmitteln weitergegeben. Nur direkt aus dem
Hintergrund gekaufte Flows werden bepreist.

### CO2-Kosten

Die Fallstudie beruecksichtigt in dieser Fassung keinen CO2-Preis. Ein
Literaturpreis fuer DAC-CO2 ist keine CO2-Steuer und darf nicht als solche
eingetragen werden.

## CSV-Stand und offene Aktionen

Aktuell dokumentiert beziehungsweise noch umzusetzen:

1. Steam-Cracker-Feedstock: `steam cracking feedstock mix` ist mit
   `0.806635610112 EUR_2025/kg` fuer alle Stutzjahre umgesetzt. Nur der Mix ist
   direkte Kostenposition; die sieben internen Feedstocks wurden aus der CSV
   entfernt. Laufzeitpruefung steht aus.
2. Steam-, MTO- und eCO2R-CAPEX: Die route-spezifischen Wrapper sind umgesetzt,
   enthalten aber zunaechst `1 EUR_2025/Einheit` als `PLACEHOLDER`. Die
   recherchierten TPC-Werte auf die jeweilige Wrapper-Einheit umrechnen.
3. Beide Stromflows: gemeinsam eine Trajektorie waehlen. Tiggelovens
   standortspezifische Werte nicht automatisch uebernehmen, weil sie stark
   szenarioabhaengig und nicht REMIND-konsistent sind.
4. Erdgaswaerme: die abgeleitete Brennstoffkomponente als Proxy pruefen. Vorher
   entscheiden, ob der bestehende Marktpreis bereits Erzeugungsanlage und
   Betrieb umfasst.
5. Den bereits eindeutig benannten Methanolanlagen-CAPEX separat absichern;
   hierfuer ist kein zusaetzlicher Wrapper erforderlich.
6. `PLACEHOLDER`-Flows ohne neue Evidenz unveraendert lassen und gezielt
   nachrecherchieren.
7. Negative Abfall- und Abwasser-Exchanges weiterhin mit negativen
   `market_price`-Werten abbilden, damit die negative Exchange-Menge positive
   Behandlungskosten ergibt.

## Offene Datenluecken

### Prioritaet A: blockiert belastbarere Kostenlaeufe

- Korrigierten `var_installation`-Pfad mit einem mehrjaehrigen
  Static-LCA-Aequivalenztest validieren.
- Entscheidung ueber route-spezifische CAPEX-Abbildung.
- DAC-Anlagen-CAPEX.
- PEM-Stack- und PEM-BOP-CAPEX mit passender MW-Basis und Zukunftstrajektorie.
- EUR_2022- und USD_2023-Umrechnung auf `EUR_2025`.
- Konsistente europaeische Strompreisentwicklung 2020-2050.

### Prioritaet B: ersetzt technische Platzhalter

- Druckluft und Fluessigstickstoff.
- Natronlauge.
- Deionisiertes Wasser fuer den CH-Flow.
- Gefaehrlicher Abfall, Untertagedeponie, Inertabfall und durchschnittliches
  Abwasser.
- Fossiler Methanolpreis fuer den kleinen direkten Steam-Cracker-Input.

### Prioritaet C: verbessert vorhandene Proxys

- Temperaturabhaengige Kuehlkosten.
- Waermepumpenwaerme.
- Amine-on-Alumina-Sorbens.
- Unbelastetes Abwasser.
- Behandlung verbrauchten Anionenaustauscherharzes.
- Kupfer und niedriglegierter Stahl mit konsistenten Europa- und
  Zukunftspreisen.

## Quellenverzeichnis und Fundstellen

1. Tiggeloven, Julia (2026): *Breaking and re-forming the chemical industry:
   Optimizing the transition from fossil-based clusters to net zero*.
   Relevante Fundstellen: Naphtha-Preis und INSEE-Verweis, gedruckte Seite
   58/PDF 73; Tabelle 4.2, gedruckte Seite 88/PDF 103;
   Gleichung 4.4, gedruckte Seite 90/PDF 105; Elektrolyseurkomponenten,
   gedruckte Seite 159/PDF 174; Tabellen C.1 und C.2, gedruckte Seiten
   168-169/PDF 183-184; Abbildung C.1, gedruckte Seite 172/PDF 187.
2. Cattry, Alexandre; Vuppanapalli, Chaitanya; Mallapragada, Dharik S. (2025):
   *Comparative reactor, process, techno-economic, and life cycle emissions
   assessment of ethylene production via electrified and thermal steam
   cracking*. Green Chemistry 27, 13357. Relevante Fundstellen: PDF-Seiten
   7-8 und 11-13.
3. Diepers: `Dissertation_Diepers_Einreichung.pdf`. Relevante Fundstellen:
   Fallstudiensystem und Lebensdauern, gedruckte Seite 68/PDF 88.
4. Deutz, S.; Bardow, A. (2021): *Life-cycle assessment of an industrial
   direct air capture process based on temperature-vacuum swing adsorption*.
   Nature Energy 6, 203-213. DOI:
   https://doi.org/10.1038/s41560-020-00771-9. Verwendete Fundstelle:
   20-jaehrige Lebensdauer des zugrunde liegenden DAC-Inventars.
5. Zibunas et al. (2022): *Cost-optimal pathways towards net-zero chemicals
   and plastics based on a circular carbon economy*. Relevante Fundstellen:
   PDF-Seiten 4-5 sowie Sensitivitaetsangaben im Ergebnisteil.
6. Kaetelhoen et al. (2016): *Stochastic Technology Choice Model for
   Consequential Life Cycle Assessment*. Relevante Fundstelle: Methodik auf
   PDF-Seite 4; keine direkt verwendbaren Ethylen-Kostenwerte.
7. INSEE (2022): *International prices of imported raw materials - Naphtha
   (European Northwest)*. Spotpreisreihe:
   https://www.insee.fr/fr/statistiques/serie/001641575.
8. European Central Bank: *Past macroeconomic projections*, HICP-Jahresraten
   des Euroraums 2023-2025:
   https://www.ecb.europa.eu/mopo/devel/ecana/html/table.en.html.
