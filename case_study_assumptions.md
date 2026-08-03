# Ethylene Case Study: Annahmen, Entscheidungen und offene Punkte

Stand: 2026-07-18

Dieses Dokument ist das zentrale Register für methodische Entscheidungen,
vorläufige Platzhalter und noch zu recherchierende Eingabedaten der
Ethylen-Case-Study. Dokumentierte `PROXY`- und `PLACEHOLDER`-Werte dürfen eine
durchgehend ausführbare Demonstration ermöglichen. Solche Läufe bleiben
vorläufig und dürfen nicht als finale Umwelt- oder Kostenergebnisse der
Bachelorarbeit interpretiert werden.

## Statusdefinitionen

- `DECIDED`: methodisch festgelegt
- `OPEN`: Entscheidung oder Datengrundlage fehlt
- `PROXY`: plausible und dokumentierte Ersatzannahme; vor finaler Interpretation prüfen
- `PLACEHOLDER`: vorläufiger technischer Wert; nicht für Ergebnisinterpretation
- `DEFERRED`: bewusst für eine spätere Ausbaustufe zurückgestellt
- `OUT_OF_SCOPE`: für diese Bachelorarbeit bewusst ausgeschlossen
- `BLOCKER`: muss vor finalen Szenarioläufen geklärt werden

## Festgelegter Modellrahmen

| Punkt | Status | Festlegung |
|---|---|---|
| Brightway-Projekt | DECIDED | `optimex_remind` |
| Prozessdaten | DECIDED | Foreground-Activities und Exchanges werden im Case-Study-Notebook manuell nach dem Muster von `methanol_and_iron.ipynb` angelegt; die Zahlenbasis stammt aus den ausgewählten disco2very-Inventaren und dokumentierten Proxys |
| Workflow-Blueprints | DECIDED | `notebooks/basic_example_econ.ipynb` und `notebooks/methanol_and_iron.ipynb` |
| Routen | DECIDED | Steam Cracking; DAC + PEM + CO2-Hydrierung + MTO; DAC + eCO2R + Aufbereitung |
| MTO-Koppelproduktbehandlung | DECIDED | Massenallokation: `allocation="weight"`, kein Avoided Burden |
| Anlagenmodellierung | DECIDED | DAC, PEM, CO2-Hydrierung, MTO und eCO2R-Reaktor als eigenständige Foreground-Anlagen |
| Gemeinsame DAC-Versorgung | DECIDED | CO2-Hydrierung und eCO2R greifen auf denselben manuell angelegten DAC-Produktknoten und damit auf einen gemeinsamen Pool installierter DAC-Kapazität zu |
| eCO2R-Aufbereitung | DECIDED | Die Betriebsinputs der fünf Trennschritte werden im Notebook sichtbar zu einer Aufbereitungsanlage aggregiert |
| Kapazitätsbasis | DECIDED | Effektiv verfügbare Jahresproduktion in `kg Referenzprodukt/a` je Anlage |
| Zeithorizont | DECIDED | 2025 bis 2050 einschließlich, jährliche Auflösung |
| Geografische Systemgrenze | DECIDED | Europa; RER/REMIND-EU als Zielregion, deutsche Datensätze nur als dokumentierte Proxys |
| Hintergrundszenario | DECIDED | Ausschließlich `REMIND-EU_SSP2-NDC`; vorhandene premise-Stützjahre mit jährlicher Interpolation |
| Zweck der Case Study | DECIDED | Demonstration der ökonomischen optimex-Erweiterung, keine Prognose oder Suche nach besonders interessanten Ethylen-Ergebnissen |
| Modellierungstiefe | DECIDED | Fit-for-purpose-Demonstration des Frameworks; belastbar dokumentierte Proxys und vereinfachte Annahmen sind zulässig, eine vollständige Markt- oder Technologieprognose ist nicht erforderlich |
| Umweltziel | DECIDED | Ausschließlich Minimierung der Wirkungskategorie Climate Change; keine Mehrkriteriengewichtung |
| LCIA-Methode | DECIDED | Brightway-Methode `("IPCC 2021", "climate change", "GWP 100a, incl. H and bio CO2")`, entsprechend `methanol_and_iron.ipynb` |
| Zeitliche Aggregation des Umweltziels | DECIDED | Minimierung der kumulierten Klimawirkung über alle Jahre 2025 bis 2050; keine jährliche Klimagrenze und kein isoliertes Zieljahr |
| Weitere Wirkungskategorien | OUT_OF_SCOPE | Feinstaub, Landnutzung, Wassernutzung und weitere Kategorien werden nicht systematisch optimiert oder ausgewertet |
| Use Phase | OUT_OF_SCOPE | Die Nutzungsphase der aus Ethylen hergestellten Produkte bleibt in jedem Fall ausgeschlossen |
| Produkt-End-of-Life | DEFERRED | In der Baseline ausgeschlossen; bei einer späteren EoL-Erweiterung gemeinsam mit Anlagenstilllegung und Anlagen-EoL aufnehmen |
| Anlagenstilllegung und Anlagen-EoL | DEFERRED | In der Baseline ausgeschlossen; bei einer späteren EoL-Erweiterung gemeinsam mit dem Produkt-EoL aufnehmen |
| Optimierungstyp | DECIDED | Brownfield-Optimierung: Zu Beginn des Modellzeitraums ist fossile Steam-Cracking-Kapazität vorhanden; zusätzliche Kapazitäten können endogen gebaut werden |
| Ethylennachfrage | DECIDED | Konstant `1 Mt/a = 1e9 kg/a` von 2025 bis 2050; keine recherchierte sektorale Nachfrageprojektion erforderlich |
| Bestehende fossile Kapazität | DECIDED | Steam Cracking deckt 2025 den vollständigen Demand von `1e9 kg Ethylen/a`; 2005 und 2015 dienen bis zur Recherche als sichtbare Proxy-Installationsjahre |
| Struktur der Steam-Cracker-Vintages | DECIDED | Zwei gleich große Bestandskohorten mit jeweils `0.5e9 kg Ethylen/a`; die Proxy-Jahre 2005 und 2015 werden später zusammen mit der recherchierten Anlagenlebensdauer geprüft |
| Steam-Cracker-Betriebsinventar | DECIDED | Beide Bestandsvintages und neu gebaute Steam-Cracker verwenden dieselben direkten Technosphere- und Biosphere-Koeffizienten des ecoinvent-3.12-Datensatzes; das gebündelte Hintergrundinventar wird nicht als einzelner Betriebsinput verwendet |
| Neubau fossiler Kapazität | DECIDED | Der Optimierer darf ab 2025 neue Steam-Cracking-Kapazität installieren; es wird kein exogener Ausstieg aus der fossilen Route erzwungen |
| Bilanzierung der Bestandsanlagen | DECIDED | CAPEX und Herstellungsumweltwirkungen der vor 2025 installierten Steam-Cracker gelten als versunkene Aufwände außerhalb des Modellhorizonts; ab 2025 werden ihre laufenden Kosten und Betriebswirkungen bilanziert |
| Betrieb der Bestandsanlagen | DECIDED | Bestehende Steam-Cracker sind verfügbare Kapazität, aber nicht must-run; Unterauslastung oder operative Stilllegung vor dem technischen Lebensende ist ohne gesonderte Rückbaukosten zulässig |
| Bestehende grüne Kapazitäten | DECIDED | Baseline startet ohne bestehende DAC-, PEM-, grüne Methanol- oder eCO2R-Kapazität; diese Anlagen werden endogen gebaut. Brownfield bezieht sich damit zunächst auf die bestehende fossile Infrastruktur |
| Ausbaugrenzen | OUT_OF_SCOPE | Keine jährlichen technologiespezifischen Ramp-up- oder Deployment-Limits in der Baseline; der Optimierer darf benötigte Kapazität grundsätzlich in einem Modelljahr installieren |
| Bauzeit und Betriebsbeginn | DECIDED | Keine Inbetriebnahmeverzögerung: Konstruktion und erster möglicher Betrieb liegen im Installationsjahr; `operation_time_limits` beginnen bei `0` |
| Aktuelle Kostenstufe | DECIDED | Zunächst Kostenoptimierung ohne CO2-Preis |
| Ökonomische Perspektive | DECIDED | Zentraler Systemplaner mit einem einheitlichen realen Diskontsatz; keine technologiespezifischen Investoren-WACC |
| Diskontierung | PLACEHOLDER | Einheitlicher realer Diskontsatz von `3 %`, Referenzjahr 2025, entsprechend `basic_example_econ.ipynb`; Wert und Quelle vor finalen Kostenläufen prüfen |
| Kostenbasis | DECIDED | Sämtliche Kostendaten werden auf reale Euro des Jahres 2025 (`EUR_2025`) vereinheitlicht; ursprüngliche Währung, Preisjahr und Umrechnung bleiben dokumentiert |
| Zeitpunkt der Investitionskosten | DECIDED | Installationsbezogene Kosten fallen vollständig im Installationsjahr an; keine Verteilung als Annuität über die Anlagenlebensdauer |
| Restwert am Zeithorizont | OUT_OF_SCOPE | Kein Salvage Value für nach 2050 verbleibende Anlagenlebensdauer; Investitionen tragen ihre vollständigen Kosten im Installationsjahr |
| Ökonomische Systemgrenze | DECIDED | Bepreisung ausschließlich der direkten Hintergrundkäufe aus `LCADataProcessor.cost_relevant_op_flows` und `cost_relevant_cap_flows` |
| Wärme aus Erdgas | PROXY | `0.011231884 EUR_2025/MJ Wärme`: THE-Day-Ahead-Gaspreis 2025 von `37.2 EUR/MWh` nach FfE/EEX, geteilt durch `3600 MJ/MWh` und den Gasboiler-Wirkungsgrad `0.920` aus Tiggeloven (2026), Tabelle C.2, gedruckte Seite 169/PDF 184; nur Brennstoffkosten, ohne Kessel-CAPEX und O&M; bis zur Preisprojektion real konstant |
| Absorptionskühlung | PROXY | `0.020543646 EUR_2025/MJ Kühlenergie`: `1.67 MJ` Wärme aus Erdgas zu `0.011231884 EUR/MJ` plus `0.0200 kWh` Strom zu `0.08932 EUR/kWh`; Wasser bleibt unbepreist; bis zu den Gas- und Strompreisprojektionen real konstant |
| Nicht inventarisierte Kosten | OUT_OF_SCOPE | Personal, Versicherung, Verwaltung, fixe Wartung und weitere Kosten werden nur berücksichtigt, wenn sie als explizite bepreisbare Flows im Inventar vorkommen; kein separates Zusatzkostenmodell |
| Prüfung der Preisvollständigkeit | DECIDED | Keine zusätzliche Strict-Implementierung; fehlende `market_price`-Werte erzeugen die bestehende Warnung des `LCADataProcessor`, und die Prüfung vor finalen Läufen bleibt User Responsibility |
| Zeitliche Preisentwicklung | DECIDED | Für jeden kostenrelevanten Flow wird eine zeitliche Entwicklung recherchiert oder mindestens eine quellenbasierte Entwicklungshypothese begründet; real konstante Preise sind kein automatischer Default |
| Preisinterpolation | DECIDED | Literaturwerte werden nach der Umrechnung auf `EUR_2025` zunächst auf die tatsächlich verwendeten premise-Stützjahre übertragen; `LCADataProcessor` interpoliert diese Preise mit der Hintergrund-Mapping-Matrix jährlich auf 2025 bis 2050 |
| Preisextrapolation und Proxys | DECIDED | Keine unbemerkte automatische Extrapolation; fehlende Randjahre dürfen mit einer expliziten einfachen Fortschreibung oder einem dokumentierten Proxy abgedeckt werden |
| Anzahl der Preispfade | DECIDED | Je kostenrelevantem Flow zunächst genau ein zentraler Baseline-Preispfad; alternative Preisannahmen können bei Bedarf nachträglich als separates Szenario gerechnet werden |
| Kosten-CSV | DECIDED | Eine gemeinsame CSV für installierungs- und betriebsbezogene Preise; `cost_class` unterscheidet `cap`, `op` und `cap_and_op` |
| Erzeugung der Recherchevorlage | DECIDED | Die versionierte Kosten-CSV ist ein vorbereiteter Modellinput; das öffentliche Notebook liest sie ein und prüft ihre Abdeckung, erzeugt oder überschreibt sie aber nicht |
| Öffentliche Notebook-Fassung | DECIDED | Das Notebook bleibt leserorientiert und enthält nur einen kompakten Abschnitt für Kostenflussliste, CSV und Preisstatus; Research Mode, Blocker-Gates und Entwicklerworkflow werden nicht gezeigt |
| Veröffentlichung der Kosten-CSV | DECIDED | Die fertig recherchierte CSV wird als reproduzierbarer Modellinput im öffentlichen Repository versioniert; Weitergaberechte der Preisquellen und enthaltenen Daten vor Veröffentlichung prüfen |
| Aktivitätsidentität in der CSV | DECIDED | Öffentliche Preiszeilen verwenden `name`, `product`, `location`, `unit` und `year`; keine datenbankspezifischen Brightway-Activity-Codes |
| Voraussetzungen des öffentlichen Notebooks | DECIDED | `optimex_remind`, die benötigten premise-Datenbanken und die Biosphere-Datenbank werden vorausgesetzt; die `disco2very`-Datenbank ist keine Laufzeitabhängigkeit der Case Study |

Die Kapazitätsbasis bezieht sich jeweils auf das Referenzprodukt der Anlage:

- DAC: `kg CO2/a`
- PEM: `kg H2/a`
- CO2-Hydrierung: `kg Methanol/a`
- MTO: `kg Ethylen/a`
- eCO2R-Reaktor und Aufbereitung: `kg des jeweiligen Zwischen- oder Endprodukts/a`

Die Kapazität ist als effektive Jahresproduktion definiert. Eine zusätzliche
Multiplikation mit einem Auslastungsgrad erfolgt nicht, sofern die recherchierten
Kapazitätsdaten bereits auf diese effektive Basis umgerechnet wurden.

## Infrastruktur und Installationsskalierung

### Inventory-Uebernahmeregel

Normale Brightway-LCI-Inventory-Mengen werden fuer die Case Study unveraendert
uebernommen. Das gilt auch fuer Infrastrukturkoeffizienten wie:

```text
unit factory / kg product
```

`operation=False` klassifiziert den Exchange als Installation und steuert seine
zeitliche Skalierung. Es aendert weder den Betrag noch die Bezugsbasis des
Quellinventars. Daher gibt es keine Umrechnung von `unit/kg` auf
`unit/(kg/a)` und keine Multiplikation mit einer Quellen- oder
Modelllebensdauer.

Die Optimex-Modelllebensdauer bleibt davon getrennt. Sie steuert
Verfuegbarkeit und Ersatz der Foreground-Kapazitaetsvintages, nicht die
Inventory-Menge. Die Regel setzt den korrigierten `var_installation`-Pfad
voraus; vor finalen Szenariolaeufen muss dessen mehrjaehrige Aequivalenz zu
einer statischen LCA getestet werden. Dabei sind auch die Brownfield-Kapazitaeten
erneut gegen die korrigierte Variablensemantik zu pruefen.

### Einheiten der ecoinvent-Infrastruktur

- `chemical factory construction, organics`: Preis und Exchange bezogen auf `unit`
- `chemical factory construction`: Preis und Exchange bezogen auf `kg factory`

Fuer die in `my_activities.py` dokumentierten Mengen bleibt lediglich zu
pruefen, welcher konkrete Datensatz und welche Einheit verwendet wurden. Eine
Quellenlebensdauer ist fuer ihre Uebernahme nicht erforderlich.

### Wahrscheinliche `operation=False`-Exchanges

| Anlage | Installations- oder EoL-Kandidaten | Status |
|---|---|---|
| MTO | `chemical factory construction, organics` | Inventory-Menge unveraendert uebernommen; Activity-Identitaet pruefen |
| CO2-Hydrierung | `chemical factory construction, organics` | Inventory-Menge unveraendert uebernommen; Activity-Identitaet pruefen |
| PEM | Stahl, Aluminium, Kupfer, Kunststoff, Elektronik, Beton, Titan, Edelstahl, Nafion, Aktivkohle, Iridium, Platin | Inventory-Mengen unveraendert uebernommen; separate Komponentenwechsel sind eine optionale Modellerweiterung |
| PEM EoL | zugehörige Recycling- und Entsorgungsprozesse | OPEN: Zeitpunkt und Skalierung prüfen |
| DAC | `construction of direct air capture, 2016` | Inventory-Menge unveraendert uebernommen; Activity-Identitaet pruefen |
| DAC EoL | `treatment of direct air capture, 2016` | OPEN: Zeitpunkt und Skalierung prüfen |
| eCO2R-Reaktor | `chemical factory construction` | Inventory-Menge unveraendert uebernommen; Einheit `kg factory` pruefen |
| eCO2R-Reaktor | Kupferelektrode | Inventory-Menge unveraendert uebernommen; Infrastruktur oder Verbrauchsmaterial klaeren |
| eCO2R-Aufbereitung | Stahl des Vapor-Liquid-Separators | Inventory-Menge unveraendert uebernommen; Activity-Identitaet pruefen |
| eCO2R-Aufbereitung | Anlagen für DeOx, Amine Wash, TSA und Kryotrennung | OPEN: explizite Infrastruktur fehlt weitgehend |
| Steam Cracking | `chemical factory construction, organics` | Dokumentierter ecoinvent-Koeffizient `1.1516356618335166e-10 unit/kg Ethylen` unveraendert als Installation modelliert |

Strom, Wärme, Kühlenergie, Wasser, Abwasser, CO2, H2, Methanol und andere
produktionsabhängige Zwischenprodukte werden grundsätzlich als
`operation=True` behandelt. Für Adsorbens, Schmiermittel, Elektroden und
Katalysatormaterialien muss anhand der Stand- und Ersatzzeiten entschieden
werden, ob sie Betriebs- oder Installationsflüsse sind.

## Pflichtrecherche vor finalen Szenarioläufen

| Parameter | Betroffene Prozesse | Status | Benötigte Dokumentation |
|---|---|---|---|
| Betriebslebensdauer | alle Foreground-Anlagen | BLOCKER | Wert, Einheit, Quelle, Unsicherheit |
| Bauzeit / Betriebsbeginn | alle Foreground-Anlagen | DECIDED | Keine Bauzeit im Modell; Same-year-Konvention entsprechend `methanol_and_iron.ipynb` |
| Installationenskalierung | alle Anlagen mit `operation=False` | SOFTWARE PREREQUISITE | Korrigierten `var_installation`-Pfad mit einem mehrjaehrigen Static-LCA-Aequivalenztest validieren |
| Komponentenstandzeiten und Ersatz | PEM, DAC, eCO2R | OPTIONAL | Nur fuer eine explizite Komponentenwechsel-Modellierung erforderlich; nicht fuer die Uebernahme normaler Inventory-Mengen |
| Altersstruktur bestehender Kapazität | Steam Cracking | BLOCKER | Installationsjahre der zwei Kohorten und resultierende Restlebensdauern in Abstimmung mit der recherchierten Anlagenlebensdauer festlegen |
| Früheste Verfügbarkeit | neue Routen | OPEN | Jahr und Quelle |
| Infrastruktur der eCO2R-Aufbereitung | Aufbereitungsanlage | OPEN | Umfang und Kapazitätsnormalisierung |
| Modellierung Steam Cracking | fossile Route | BLOCKER | Direkte Betriebs- und Biosphere-Exchanges sowie der unveraenderte ecoinvent-Infrastrukturkoeffizient sind umgesetzt; Neubau-CAPEX und die Eignung von 50 Jahren als Optimex-Modelllebensdauer bleiben zu pruefen |
| Realer Diskontsatz | Gesamtsystem | PLACEHOLDER | Vorläufig `3 %` mit Referenzjahr 2025; endgültigen Wert und zitierfähige methodische Begründung recherchieren |
| Preisbasis | alle Kostendaten | DECIDED | `EUR_2025`; ursprünglichen Wert, ursprüngliche Währung und ursprüngliches Preisjahr sowie Inflations- und Währungsumrechnung dokumentieren |
| Preisentwicklung 2025-2050 | alle kostenrelevanten `op`- und `cap`-Flows | BLOCKER | Für jeden Flow Zeitreihe, dokumentierten Proxy oder begründete Entwicklungshypothese sowie Quellen, Stützjahre und Umgang mit Datenlücken festhalten |

Bei `operation_time_limits=(start, end)` sind beide Grenzen inklusive. Die
Anzahl der modellierten Betriebsjahre ist daher:

```text
lifetime = end - start + 1
```

`infer_construction_td_from_limits` legt den Konstruktionsfluss technisch auf
`start`. Bei `start=0` fallen Konstruktion und erster möglicher Betrieb daher in
dasselbe Installationsjahr. Der Docstring spricht abweichend von einem Jahr vor
Betriebsbeginn; für die Case Study ist das tatsächliche Codeverhalten maßgeblich.

Das Blueprint-Notebook `methanol_and_iron.ipynb` enthält Beschreibungen wie
"8-year stack lifetime" zusammen mit `(0, 8)`, was technisch neun
Betriebsjahre ergibt. Diese Werte werden nicht ungeprüft übernommen.

Die Brownfield-Struktur des Blueprints wird methodisch übernommen: bestehende
fossile Kapazität deckt zu Beginn die Nachfrage, während neue Prozess- und
Lieferkettenoptionen ab 2025 zur Verfügung stehen. Die dort gewählte Aufteilung
auf 2005 und 2015 wird im ausführbaren Demonstrationsmodell als sichtbarer Proxy
übernommen. Für die finale Ethylen-Case-Study müssen Altersstruktur und
Restlebensdauer der bestehenden Steam-Cracker separat begründet werden.

Bei der Mengenskalierung wird der Blueprint ebenfalls nicht numerisch kopiert:
Die Produktknoten in `methanol_and_iron.ipynb` haben die Einheit `kg`, während
Demand und Bestandskapazitäten mit `1e6` beziehungsweise `0.5e6` als "Mt scale"
eingetragen sind. In Kilogramm entsprechen `1 Mt` jedoch `1e9 kg`. Für die
Ethylen-Case-Study müssen Demand und alle Vintage-Kapazitäten daher konsistent
in `kg/a` angegeben werden und zusammen initial `1e9 kg/a` ergeben.

## Kostenrecherche und CSV-Übergabe

Nach Aufbau des Foregrounds werden die tatsächlich benötigten direkten
Hintergrundpreise aus folgenden Mengen bestimmt:

```python
lca_data_processor.cost_relevant_op_flows
lca_data_processor.cost_relevant_cap_flows
```

Für die schnelle Recherchevorlage werden dieselben Mengen zunächst direkt aus
den Foreground-Consumption-Exchanges und deren `operation`-Attribut abgeleitet.
Dadurch müssen nicht schon für den CSV-Export alle premise-Hintergrundinventare
berechnet werden. Sobald ein vollständiger `LCADataProcessor`-Lauf vorliegt,
prüft das Notebook die Gleichheit der direkt ermittelten Flow-Codes mit den
beiden Properties automatisch.

Die geplante Kosten-CSV soll mindestens enthalten:

| Spalte | Bedeutung |
|---|---|
| `name` | Brightway-Name des Hintergrundprozesses |
| `product` | Produkt beziehungsweise Referenzprodukt zur eindeutigen Zuordnung |
| `location` | Brightway-Standort |
| `unit` | Einheit des Market Price |
| `cost_class` | `op`, `cap` oder `cap_and_op` |
| `year` | Repräsentatives Jahr der premise-Hintergrunddatenbank, an deren Knoten der Preis geschrieben wird |
| `scenario` | Zunächst `REMIND-EU_SSP2-NDC`; ermöglicht bei Bedarf einen späteren alternativen Preispfad |
| `price` | Auf `EUR_2025` umgerechneter Market Price je Einheit |
| `currency` | Einheitlich `EUR_2025` |
| `price_year` | Einheitlich `2025` |
| `original_price` | Preiswert aus der Originalquelle vor Umrechnung |
| `original_currency` | Währung der Originalquelle |
| `original_price_year` | Preisjahr der Originalquelle |
| `source` | Literatur- oder Datenquelle |
| `conversion_source` | Quellen und Faktoren der Währungs- und Inflationsumrechnung |
| `trajectory_basis` | recherchierte Zeitreihe oder begründete Entwicklungshypothese |
| `interpolation` | Methode zur Erzeugung der jährlichen Werte zwischen Stützjahren |
| `status` | recherchiert, Proxy, geschätzt oder Platzhalter |
| `notes` | Umrechnung und weitere Annahmen |

Fehlende Preise dürfen in finalen Kostenläufen nicht implizit als null behandelt
werden. Es wird dafür keine zusätzliche automatische Strict-Prüfung implementiert;
die vom `LCADataProcessor` ausgegebenen Warnungen müssen vor einem finalen Lauf
vom Nutzer geprüft und aufgelöst werden.

### Steam-Cracker-Feedstock-Proxy

Entscheidung vom 2026-08-01: Der von Tiggeloven (2026) angegebene
nordwesteuropäische Naphtha-Preis von `732 EUR_2022/t` wird als Preisproxy für
den allokierten Feedstock-Slate der fossilen Steam-Cracking-Route verwendet.
Tiggeloven bezeichnet den Wert als Durchschnittspreis für 2022 und verweist auf
die INSEE-Spotpreisreihe für nordwesteuropäisches Naphtha. Die konstante
Fortschreibung ist eine Modellannahme und keine Marktpreisprognose.

Für die einheitliche CSV-Preisbasis wird der Wert mit den HICP-Jahresraten des
Euroraums für 2023, 2024 und 2025 umgerechnet:

```text
0.732 EUR_2022/kg * 1.054 * 1.024 * 1.021
= 0.806635610112 EUR_2025/kg
```

Dieser Wert steht vorläufig für alle vier Stützjahre auf der bestehenden
CSV-Identität `market for naphtha`. Der Status ist `PROXY`, weil der Preis nicht
nur Naphtha, sondern vereinfachend den gesamten allokierten Feedstock-Slate
bewertet. Die übrigen direkten Kohlenwasserstoffinputs behalten bis zur
Modelländerung ihre bisherigen CSV-Zeilen; damit sind zwischenzeitliche
Kostenläufe weiterhin nur vorläufig interpretierbar. Insbesondere bewertet der
aktuelle Modellstand numerisch nur die vorhandene Naphtha-Exchange-Menge mit
diesem Preis. Die beabsichtigte Bewertung der gesamten Feedstock-Mix-Menge wird
erst durch die neue Activity hergestellt und ist noch nicht implementiert.

Geplante, noch nicht implementierte Modelländerung:

1. Die anhand der ecoinvent-Dokumentation bestätigten Feedstock-Inputs werden in
   einer eigenen Background-Activity `steam cracking feedstock mix` gebündelt.
2. Der Steam-Cracking-Prozess konsumiert anschließend nur diesen Mix als direkten
   Betriebsinput. Energie-, Hilfsstoff- und Abfallflüsse bleiben außerhalb der
   Bündelung.
3. Die internen Exchanges der Mix-Activity erhalten die bisherige ökologische
   Zusammensetzung. Nur der direkte Mix-Flow wird in Optimex bepreist, damit die
   Bestandteile nicht zusätzlich als einzelne Kostenpositionen erscheinen.
4. Erst nach dieser Brightway-Anpassung wird die temporäre Naphtha-Identität in
   `cost_inputs.csv` durch die tatsächliche Identität der Mix-Activity ersetzt.
   Vorher wird keine vorweggenommene CSV-Zeile für diese Activity angelegt.
5. Nach der Umsetzung werden LCIA-Gleichheit zum bisherigen Inventar und die
   Ausgabe von `cost_relevant_op_flows` geprüft.

## Implementierungsstand Meilenstein 1

Stand 2026-07-18:

- `notebooks/ethylene_case_study.ipynb` ist als lineare, leserorientierte
  Fallstudie nach dem Muster von `methanol_and_iron.ipynb` aufgebaut. Es enthält
  keine Research-Mode-Schalter, Blocker-Gates oder Entwicklerworkflow-Erklärung.
- Die Product Nodes, sieben Entscheidungsprozesse und alle Foreground-Exchanges
  werden direkt im Notebook angelegt. Die Case Study benötigt zur Laufzeit keine
  vorbereiteten `disco2very`-Activities.
- Lebensdauern, Installationskoeffizienten, Brownfield-Jahre und Diskontsatz
  stehen gemeinsam in einer sichtbaren Annahmentabelle. Alle vorläufigen Werte
  sind als `PROXY` oder `PLACEHOLDER` markiert und können gezielt ersetzt werden.
- Die beiden Vintages 2005 und 2015 stellen mit jeweils `0.5e9 kg/a` die
  vollständige Steam-Cracker-Kapazität im Startjahr bereit.
- Der Steam Cracker wird eine Ebene unterhalb der gebündelten ecoinvent-Activity
  modelliert: 17 direkte Technosphere-Inputs und 44 direkte Biosphere-Exchanges
  bilden den Betrieb ab. Kumulierte Biosphere-Flows der Lieferketten werden nicht
  übernommen, sondern weiterhin durch Brightway berechnet.
- `chemical factory construction, organics` wird ausschliesslich als
  Installation verwendet. Der statische ecoinvent-Koeffizient
  `1.1516356618335166e-10 unit/kg Ethylen` wird unveraendert uebernommen. Eine
  Multiplikation mit der Modell- oder Quellenlebensdauer findet nicht statt.
- Bei 50 Jahren Modelllebensdauer bleiben die Bestandsvintages von 2005 und 2015
  bis zum Ende des Zeithorizonts 2050 verfügbar. Sie sind weiterhin nicht
  must-run und können durch andere Routen ersetzt werden.
- DAC wird von CO2-Hydrierung und eCO2R über denselben Produktknoten genutzt.
  Die eCO2R-Aufbereitung bleibt aggregiert und enthält `6.091081 kg CO2/kg
  Ethylen` aus der Oxidation der Nebenprodukte, nicht aus Produkt-EoL.
- Das Notebook liest die versionierte Kosten-CSV unter
  `notebooks/data/ethylene_case_study/cost_inputs.csv`, zeigt ihre Abdeckung für
  die direkten Kostenflüsse und gibt anschließend die tatsächlichen
  `cost_relevant_op_flows` und `cost_relevant_cap_flows` sichtbar aus.
- Der frühere Preisplatzhalter für die gebündelte Steam-Cracking-Activity ist
  entfernt. Die 17 direkten Betriebsinputs besitzen bis zur Recherche eigene
  `PLACEHOLDER`-Preispfade. Abfall- und Abwasserpreise sind bei negativen
  Exchange-Mengen ebenfalls negativ hinterlegt, damit positive Behandlungskosten
  entstehen.
- Zwei Szenarien sind enthalten: kumuliertes Klimawirkungsminimum und
  diskontiertes Kostenminimum ohne CO2-Preis. Beide sind mit Proxywerten
  konfiguriert; ihre Resultate bleiben bis zur Recherche ausdrücklich vorläufig.
- Das Notebook wurde bei dieser Überarbeitung auf ausdrücklichen Wunsch nicht
  ausgeführt. Die vollständige Brightway-, LCA- und Solver-Prüfung ist daher
  noch offen.

## Bewusst vertagte Erweiterungen

| Thema | Status | Hinweis |
|---|---|---|
| Vintage Improvements | DEFERRED | Technische Verbesserungen späterer Installationsjahrgänge erst nach stabiler Basismodellierung ergänzen |
| CO2-Preis | DEFERRED | Separate spätere Ausbaustufe; aktuelle Kostenoptimierung zunächst ohne CO2-Preis |
| Kostenoptimierung unter Emissionsbudget | DEFERRED | Nach ökologischem und rein ökonomischem Referenzlauf |
| Budget Sweep / Pareto-Kurve | DEFERRED | Nach belastbarer Kosten- und Umweltparametrisierung |
| Alternative premise-Szenarien | OUT_OF_SCOPE | Als mögliche Stellschraube dokumentiert, aber kein Szenariovergleich in der Bachelorarbeit |
| Sensitivitätsanalyse | OUT_OF_SCOPE | Keine systematische Unsicherheits- oder Parametersensitivität; der Emissionsbudget-Sweep bleibt eine eigene Capability-Demonstration |
| Alternative Preispfade | DEFERRED | Nur bei späterem Bedarf als gezieltes alternatives Szenario; keine vorab aufgebaute Low-/High-Sensitivität |
| Steam-Cracker-Feedstock-Bündelung | PENDING | Bestätigte Feedstock-Inputs in einer Background-Activity bündeln und danach die temporäre Naphtha-Identität in der Kosten-CSV ersetzen |
| Technologiespezifische Ausbaugrenzen | OUT_OF_SCOPE | Bereits bestehendes optimex-Feature und kein Beitrag der ökonomischen Erweiterung; ein theoretisch sofortiger Großausbau wird als Modellvereinfachung akzeptiert |
| Restwertmodellierung | OUT_OF_SCOPE | Keine Gutschrift für verbleibende technische Lebensdauer nach 2050; mögliche Benachteiligung später Investitionen wird als Endhorizont-Limitation ausgewiesen |
| Steigender Ethylen-Demand | DEFERRED | Optionale spätere Stellschraube; kann Kapazitätsaufbau beeinflussen, erzeugt aber ohne weitere Randbedingungen nicht automatisch Frühinvestitionen |
| Bestehende grüne Kapazitäten | DEFERRED | DAC, PEM, grünes Methanol oder eCO2R könnten als Brownfield ergänzt werden; nur mit konsistenter Kapazität der gesamten vorgelagerten Kette |
| End-of-Life-Erweiterung | DEFERRED | Nur als gemeinsame Erweiterung aus Produkt-EoL sowie Stilllegung und EoL der Anlagen; die Use Phase bleibt auch dann ausgeschlossen |

## Freigaberegel für Szenarioläufe

Ein vollständiger Umwelt- oder Kostenlauf mit dokumentierten Proxys darf zur
Demonstration des optimex-Workflows, der Foreground-Verknüpfungen und der
ökonomischen Erweiterung genutzt werden. Ergebnisse eines solchen Laufs dürfen
nicht als finale Resultate der Ethylenmodellierung interpretiert werden.

Finale Umwelt- und Kostenoptimierungen sind erst freigegeben, wenn alle als
`BLOCKER` markierten Parameter recherchiert oder als begründete, zitierfähige
Annahmen dokumentiert und alle `PLACEHOLDER`-Werte ersetzt oder entsprechend
begründet wurden.
