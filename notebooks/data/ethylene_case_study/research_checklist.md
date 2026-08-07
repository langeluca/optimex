# Recherche-Checkliste fuer die Ethylen-Fallstudie

Stand: 1. August 2026

Diese Checkliste folgt der Reihenfolge der Foreground Activities in der
Ethylen-System-Map. Sie basiert auf dem aktuellen Stand von
`ethylene_case_study.ipynb`, `cost_inputs.csv`, `case_study_assumptions.md` und
`cost_lifetime_research_report.md`.

## Statuslegende

- `[x] REPO`: im Repo umgesetzt oder als dokumentierter Proxy vorhanden
- `[ ] RESEARCH`: externe Preis- oder Lebensdauerrecherche offen
- `[ ] DECISION`: methodische Entscheidung oder Modellabbildung offen
- `[ ] SCREEN`: Kostenrelevanz grob pruefen
- `[ ] CUTOFF`: nach Screening mit Preis null und Begruendung ausschliessen

Ein gesetzter Haken bedeutet nicht automatisch, dass der Wert fuer eine finale
BA-Interpretation belastbar ist. Viele vorhandene Werte sind weiterhin
`PROXY`.

## 0. Inventory-Uebernahme und gemeinsame Preisgrundlagen

### Installationsinventare

- [x] REPO Installationskoeffizienten unveraendert aus ecoinvent,
  disco2very oder `methanol_and_iron` uebernehmen.
- [x] REPO Alle Installations-Exchanges mit `operation=False` modellieren.
- [x] REPO Keine Multiplikation der Koeffizienten mit 20 oder 50 Jahren.
- [x] REPO Keine Recherche der Amortisationsdauer des Quellinventars mehr.
- [ ] DECISION Bei unklaren Komponenten weiterhin Bedeutung, Einheit und
  Systemgrenze des Inventory-Flows klaeren, nicht dessen Amortisationsdauer.

### Strom

- [x] REPO Vorlaeufiger deutscher Strompreis von
  `0.08932 EUR_2025/kWh` fuer beide Mittelspannungs-Flows vorhanden.
- [ ] RESEARCH Entscheiden, ob ein Day-Ahead-Boersenpreis oder ein industrieller
  Bezugspreis inklusive Netzentgelten, Steuern und Umlagen zur Perspektive der
  Fallstudie passt.
- [ ] RESEARCH Konsistente reale Preisentwicklung fuer 2020, 2030, 2040 und
  2050 recherchieren oder begruendet festlegen.
- [ ] DECISION Dieselbe Trajektorie fuer `market for electricity, medium
  voltage` und `market group for electricity, medium voltage` dokumentieren.

### Erdgaswaerme

- [x] REPO Brennstoffbasierter Proxy von `0.011231884 EUR_2025/MJ Waerme`
  aus THE-Gaspreis und einem Wirkungsgrad von 0.920 vorhanden.
- [ ] RESEARCH Reale Gaspreisentwicklung fuer 2020, 2030, 2040 und 2050
  recherchieren oder begruendet festlegen.
- [ ] DECISION Dokumentieren, dass Kessel-CAPEX und fixe O&M nicht enthalten
  sind.

### Wasser und Abwasser

- [x] REPO Europa-Proxy fuer deionisiertes Wasser von `0.002 EUR/kg`
  vorhanden.
- [ ] RESEARCH Proxy belegen oder durch eine zitierfaehige Quelle ersetzen.
- [ ] DECISION Den Schweizer Steam-Cracking-Flow mit dem Europa-Proxy
  harmonisieren oder separat bepreisen.
- [x] REPO Proxy fuer unbelastetes Abwasser vorhanden.
- [ ] SCREEN Durchschnittliches und unbelastetes Abwasser gemeinsam bewerten.

## 1. Steam Cracking

### CAPEX

- [x] REPO `steam cracker installation` kapselt `1 unit chemical factory
  construction, organics`; der äußere Koeffizient bleibt unverändert
  `1.1516356618335166e-10 unit/kg Ethylen`.
- [x] REPO Tiggeloven liefert eine route-spezifische CAPEX-Funktion fuer einen
  konventionellen Naphtha-Cracker.
- [x] REPO Route-spezifischen Steam-Cracker-CAPEX auf den eigenen
  Installations-Flow abgebildet; bis zur TPC-Umrechnung bleibt dessen Preis ein
  technischer `PLACEHOLDER`.
- [ ] DECISION Kapazitaetsbasis, Auslastung, Kostenumfang und fixe
  Instandhaltung von 4 Prozent TPC/a dokumentieren.

### Prioritaere OPEX-Preise

- [x] REPO Naphtha-Rohwert von `0.732 EUR_2022/kg` aus Tiggeloven gefunden.
- [x] RESEARCH Naphtha mit den HICP-Jahresraten 2023-2025 auf
  `0.806635610112 EUR_2025/kg` umgerechnet.
- [x] DECISION Den Naphtha-Wert vorlaeufig real konstant als
  Naphtha-aequivalenten Preisproxy fuer den gesamten allokierten
  Steam-Cracker-Feedstock-Slate verwenden.
- [x] REPO Die sieben anhand der ecoinvent-Dokumentation bestaetigten
  Feedstock-Inputs in `steam cracking feedstock mix` gebuendelt: Butan, Ethan,
  Naphtha, NGL, Propan, Refinery Gas und Diesel als Proxy fuer Atmospheric Gas
  Oil. Energie-, Hilfsstoff- und Behandlungsinputs bleiben außerhalb.
- [x] REPO Die sieben einzelnen Feedstock-Zeilen in `cost_inputs.csv` durch die
  echte Mix-Identitaet mit `0.806635610112 EUR_2025/kg` ersetzt.
- [ ] VERIFY LCIA-Gleichheit zum bisherigen direkten Inventar pruefen und
  sicherstellen, dass `cost_relevant_op_flows` nur den Mix statt seiner
  Feedstock-Bestandteile als direkte Kostenposition ausweist.
- [x] REPO Ethane-Rohwert von `0.330 USD_2023/kg` aus Cattry gefunden.
- [ ] OPTIONAL Separate europaeische Preise fuer die sieben Mixbestandteile nur
  recherchieren, falls der gebuendelte Naphtha-Proxy spaeter durch
  bestandteilspezifische Kosten ersetzt werden soll.
- [x] REPO Strompreis wird aus der gemeinsamen Stromtrajektorie uebernommen.
- [x] REPO Deionisiertes Wasser wird aus der gemeinsamen Wasserannahme
  uebernommen, sobald CH und Europa harmonisiert sind.

Naphtha, Butan, Diesel, Ethane und Propan decken rund 96 Prozent der Masse der
aufgefuehrten Kohlenwasserstoffe und Brennstoffe ab. Das ist ein
Screening-Scope, kein nachgewiesener Kostenanteil.

### Abgeleitete Utility-Kosten

- [x] REPO Druckluftpreis aus dem ecoinvent-Strombedarf abgeleitet:
  `0.01403896 EUR_2025/m3`.
- [ ] DECISION Nach Einfuehrung der Stromtrajektorie den Druckluftpreis fuer
  jedes Stuetzjahr neu berechnen.

### Screening und Cut-off

- [ ] SCREEN Natural Gas Liquids.
- [ ] SCREEN Raffineriegas.
- [ ] CUTOFF Fluessigen Stickstoff nach dokumentiertem Screening auf null
  setzen.
- [ ] CUTOFF Natriumhydroxid nach dokumentiertem Screening auf null setzen.
- [ ] CUTOFF Kleine Methanolmenge nach dokumentiertem Screening auf null
  setzen.
- [ ] SCREEN Behandlung gefaehrlicher Abfaelle, Inertabfall und Abwasser mit
  groben Entsorgungsgebuehren bewerten.

## 2. Direct Air Capture

### CAPEX

- [x] REPO DAC-Installationskoeffizient `1.25e-8 unit/kg CO2` unveraendert
  uebernommen.
- [x] REPO DAC-Installationsflow auf die reproduzierte disco2very-Konstruktion
  eines Solid-Sorbent-Systems mit `4 kt CO2/a` umgestellt; die interne
  Anlagen-EoL-Kante bleibt entsprechend der Baseline ausgeschlossen.
- [x] REPO Die Nennkapazitaet des Deutz-und-Bardow-Inventars stimmt mit der
  Kapazitaetsbasis der Kostendaten aus Sievert et al. ueberein.
- [ ] RESEARCH Den TPC aus Sievert et al. auf `EUR_2025` umrechnen und direkt
  als Preis einer 4-kt-Einheit eintragen; der technische CSV-Fallback von
  `1 EUR/Einheit` darf nicht interpretiert werden.
- [ ] RESEARCH Zukunftstrajektorie des DAC-TPC festlegen oder eine reale
  konstante Fortschreibung transparent begruenden.

### OPEX

- [x] REPO Strom wird aus der gemeinsamen Stromtrajektorie uebernommen.
- [x] REPO Waermepumpenwaerme aus dem ecoinvent-Strombedarf abgeleitet:
  `0.005511044 EUR_2025/MJ`.
- [ ] DECISION Waermepumpenpreis nach Einfuehrung der Stromtrajektorie je
  Stuetzjahr neu berechnen.
- [x] REPO Der unpassende Aktivkohleproxy wurde durch die originale
  disco2very-Activity `adsorbent, amine on alumina` ersetzt; ihr Inventar
  besteht aus PEI und Aluminiumoxid.
- [ ] RESEARCH Sorbenspreis aus Sievert et al. auf die Einheit
  `EUR_2025/kg adsorbent` uebertragen und den technischen CSV-Fallback ersetzen.
- [ ] SCREEN Sorbens und Behandlung wegen `0.0075 kg/kg CO2` auf
  Kostenrelevanz pruefen und Quellenqualitaet bewerten.

## 3. CO2 Hydrogenation

### CAPEX

- [x] REPO Installationskoeffizient `3.5842e-12 unit/kg Methanol`
  unveraendert uebernommen.
- [x] REPO Tiggeloven liefert eine technisch passende CAPEX-Funktion fuer
  direkte Methanolsynthese aus CO2.
- [ ] DECISION Route-spezifischen Anlagen-CAPEX in einen passenden
  Installations-Flow ueberfuehren.
- [ ] DECISION Fixe Instandhaltung von 2.5 Prozent TPC/a behandeln, ohne CAPEX
  oder OPEX doppelt zu zaehlen.

### OPEX

- [x] REPO Strom wird aus der gemeinsamen Stromtrajektorie uebernommen.
- [ ] SCREEN Abwasserbehandlung.
- [x] REPO Fuer Foreground-Wasserstoff und Foreground-CO2 werden keine
  zusaetzlichen Marktpreise gesetzt.

## 4. Methanol-to-Olefins

### CAPEX

- [x] REPO Installationskoeffizient `3.584e-12 unit/kg Ethylen` unveraendert
  uebernommen.
- [x] REPO Tiggeloven liefert eine route-spezifische MTO-CAPEX-Funktion.
- [x] REPO `methanol-to-olefins installation` als eigenen Installations-Flow
  umgesetzt; der äußere Koeffizient bleibt `3.584e-12 unit/kg Ethylen`.
- [ ] DECISION Kapazitaetsbasis auf Methanoldurchsatz und fixe
  Instandhaltung von 2.5 Prozent TPC/a dokumentieren.

### OPEX

- [x] REPO Strom wird aus der gemeinsamen Stromtrajektorie uebernommen.
- [x] REPO Allgemeine Kuehlung als Absorptionskuehlung aus Erdgaswaerme und
  Strom abgeleitet: `0.020543646 EUR_2025/MJ`.
- [x] REPO Kuehlung bei -25 Grad C und -100 Grad C aus dem jeweiligen
  ecoinvent-Strombedarf abgeleitet.
- [ ] DECISION Alle Kuehlpreise mit den neuen Strom- und Gastrajektorien je
  Stuetzjahr aktualisieren.
- [ ] SCREEN Abwasserbehandlung.
- [x] REPO Foreground-Methanol erhaelt keinen zusaetzlichen Marktpreis.

## 5. PEM Electrolysis

### CAPEX

- [x] REPO PEM-Stack und Balance of Plant sind als getrennte
  Installations-Flows modelliert.
- [x] REPO Vorlaeufige IRENA-basierte Preisproxies und Trajektorien sind in der
  CSV vorhanden.
- [ ] RESEARCH PEM-spezifische Stack- und BOP-CAPEX mit eindeutiger MW-Basis,
  Preisjahr, Systemgrenze und Zukunftstrajektorie absichern.
- [ ] DECISION Stack-Ersatz und laengere BOP-Lebensdauer als optionale
  Modellerweiterung behandeln oder explizit ausschliessen.

### OPEX

- [x] REPO Strom wird aus der gemeinsamen Stromtrajektorie uebernommen.
- [x] REPO Deionisiertes Wasser wird aus der gemeinsamen Wasserannahme
  uebernommen.
- [ ] CUTOFF Sehr kleine Abwassermenge nach dokumentiertem Screening auf null
  setzen.

## 6. Aggregated eCO2R Reaction and Separation

### CAPEX

- [x] REPO Reaktion und Separation zu einem Foreground-Prozess aggregiert;
  Betriebswerte und `6.091081 kg CO2/kg Ethylen` aus der Nebenproduktoxidation
  bleiben sichtbar erhalten. Dies entspricht `eol="no"`; das Ethylenprodukt-EoL
  ist ausgeschlossen.
- [x] REPO `eCO2R system installation` auf Fabrikeinheitenbasis umgesetzt. Nach
  Rücksprache mit dem disco2very-Ersteller ersetzt `4e-10 unit/kg Ethylen` den
  fehlerhaften Fabrikmasseninput. Fabrik, Kupfer und Stahl liegen intern im
  unveränderten absoluten Verhältnis.
- [x] REPO Tiggeloven liefert eine CO2-Elektrolyse-CAPEX-Funktion als Proxy.
- [ ] DECISION Systemgrenze und Kapazitaetsbasis mit dem modellierten
  eCO2R-Reaktor vergleichen.
- [x] REPO Route-spezifischen aggregierten eCO2R-CAPEX auf den eindeutigen
  Wrapper abgebildet; bis zur TPC-Umrechnung bleibt dessen Preis ein technischer
  `PLACEHOLDER`.
- [ ] DECISION Klaeren, ob Kupfer dauerhafte Infrastruktur oder regelmaessig
  ersetztes Elektrodenmaterial ist.

### OPEX

- [x] REPO Strom und deionisiertes Wasser werden aus den gemeinsamen
  Preisannahmen uebernommen.
- [x] REPO Foreground-CO2 erhaelt keinen zusaetzlichen Marktpreis.

### Separation-specific open questions

### CAPEX

- [x] REPO Stahlkoeffizient `3.017679e-6 kg/kg Ethylen` unveraendert als
  interner Bestandteil des eCO2R-Installations-Wrappers uebernommen.
- [x] REPO Air-Separation-Unit-CAPEX aus Tiggeloven als Teilproxy vorhanden.
- [ ] RESEARCH beziehungsweise DECISION Infrastruktur fuer Deoxygenierung,
  Aminwaesche, TSA und kryogene Trennung vollstaendig abgrenzen.
- [ ] DECISION Klaeren, welche Apparate der vorhandene Stahlkoeffizient bereits
  abbildet.
- [x] REPO Kein separater Aufbereitungs-CAPEX angesetzt; der verfügbare
  CO2-Elektrolyse-Proxy wird genau einmal dem aggregierten Gesamtsystem
  zugeordnet.

### OPEX

- [x] REPO Strom und Erdgaswaerme werden aus den gemeinsamen Preisannahmen
  uebernommen.
- [x] REPO Allgemeine Kuehlung sowie -15, -25, -45, -55 und -100 Grad C sind
  als dokumentierte Utility-Proxys in der CSV vorhanden.
- [ ] DECISION Alle Kuehlpreise mit den neuen Strom- und Gastrajektorien je
  Stuetzjahr aktualisieren.
- [ ] SCREEN Abwasserbehandlung.
- [x] REPO Das frühere rohe eCO2R-Zwischenprodukt wurde durch die Aggregation
  vollständig aus dem Foreground entfernt.

## 7. Route-spezifische CAPEX-Abbildung

Ein Brightway-Node traegt genau einen Marktpreis. Steam Cracking, MTO und eCO2R
verwenden deshalb eindeutige Installations-Wrapper, die intern weiterhin die
generischen Umweltinventare beziehen.

- [x] REPO Route-spezifische Installations-Proxy-Nodes fuer Steam, MTO und das
  aggregierte eCO2R-System umgesetzt.
- [x] REPO Generische Fabrik-, Kupfer- und Stahlidentitaeten aus den direkten
  CAPEX-Zeilen der CSV entfernt.
- [ ] DECISION Fixe Kostenanteile der CAPEX-Funktionen korrekt skalieren.
- [ ] DECISION Instandhaltung aus Tiggeloven nur ergaenzen, wenn sie nicht
  bereits in anderen OPEX-Positionen enthalten ist.
- [ ] DECISION Aggregierte Produktionskosten aus Cattry nicht gemeinsam mit
  einzeln bepreisten Feedstocks, Energie und CAPEX verwenden.

## 8. Optimex-Modelllebensdauern und Brownfield

Die folgenden Lebensdauern steuern Verfuegbarkeit, Stilllegung und
Ersatzinvestitionen. Sie dienen nicht zur Skalierung der Inventory-Mengen.

- [x] REPO Steam Cracking: 25 Jahre nach Tiggeloven, Tabelle C.1.
- [x] REPO DAC: 20 Jahre nach Deutz und Bardow (2021).
- [x] REPO PEM: 25 Jahre als AEC-Anlagenproxy nach Tiggeloven; der dort genannte
  separate Stacktausch nach 9 Jahren ist im Ein-Prozess-Modell ausgeschlossen.
- [x] REPO CO2-Hydrierung: 25 Jahre nach Tiggelovens direkter Methanolsynthese
  aus CO2.
- [x] REPO MTO: 25 Jahre nach Tiggeloven.
- [x] REPO Aggregierter eCO2R-Prozess: gemeinsame Modelllebensdauer von 25
  Jahren als CO2-Elektrolyse- und Anlagenproxy nach Tiggeloven.
- [ ] DECISION Brownfield-Vintages 2005 und 2015 nach Festlegung der
  Steam-Cracker-Lebensdauer pruefen; Restlebensdauer ab 2025 dokumentieren.
- [ ] RESEARCH Realen Diskontsatz von aktuell 3 Prozent zitierfaehig
  begruenden oder ersetzen.

## 9. Transparenter Cut-off und CSV-Abschluss

- [ ] SCREEN Grobe Kostenbeitraege als `abs(amount * proxy price)` berechnen.
- [ ] DECISION Zielabdeckung festlegen, zum Beispiel mindestens 95 Prozent der
  geschaetzten OPEX.
- [ ] CUTOFF Ausgeschlossene Flows mit `price=0`, `status=CUTOFF` und
  Begruendung in `notes` in der CSV belassen.
- [ ] DECISION Positive Entsorgungsgebuehren bei negativen Waste-Exchanges als
  negative Marktpreise eintragen.
- [ ] DECISION Alle 31 kostenrelevanten CSV-Identitaeten entweder als
  recherchiert, dokumentierter Proxy oder begruendeter Cut-off klassifizieren.
- [ ] DECISION Nach jeder Preisaenderung abgeleitete Utility-Preise fuer alle
  Stuetzjahre konsistent neu berechnen.

## Naechster Recherchekern

In sinnvoller Arbeitsreihenfolge bleiben damit:

1. Strompreis-Perspektive und Trajektorie 2020 bis 2050.
2. Statische Steam-Cracker-Feedstock-Buendelung durch einen Brightway-/LCIA-Lauf
   pruefen und bestaetigen, dass nur der Mix als direkter Kostenfluss erscheint.
3. Gaspreisentwicklung und Aktualisierung aller Waerme- und Kuehlproxies.
4. Recherchierte Steam-, MTO- und aggregierte eCO2R-TPC-Werte auf die bereits
   umgesetzten Wrapper-Einheiten umrechnen; CO2-Hydrierungs-CAPEX absichern.
5. DAC- und PEM-CAPEX absichern.
6. Brownfield-Installationsjahre der Steam-Cracker final begruenden.
7. Wasser, Abwasser, Amine-on-Alumina-Sorbens und Abfallbehandlungen screenen.
8. Cut-off-Entscheidungen dokumentieren und alle PLACEHOLDER ersetzen.
