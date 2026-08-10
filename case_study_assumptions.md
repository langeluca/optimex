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
| Prozessdaten | DECIDED | Foreground-Activities und Exchanges werden im Case-Study-Notebook manuell nach dem Muster von `methanol_and_iron.ipynb` angelegt; die Zahlenbasis stammt aus den ausgewählten disco2very-Inventaren und dokumentierten Proxys. Fallstudienspezifische Activities werden reproduzierbar in vier eigenen Stützjahresdatenbanken angelegt und verweisen intern auf premise. |
| Workflow-Blueprints | DECIDED | `notebooks/basic_example_econ.ipynb` und `notebooks/methanol_and_iron.ipynb` |
| Routen | DECIDED | Steam Cracking; DAC + PEM + CO2-Hydrierung + MTO; DAC + aggregierte eCO2R-Reaktion und Aufbereitung |
| MTO-Koppelproduktbehandlung | DECIDED | Massenallokation: `allocation="weight"`, kein Avoided Burden |
| Anlagenmodellierung | DECIDED | DAC, PEM, CO2-Hydrierung, MTO und der aggregierte eCO2R-Prozess als eigenständige Foreground-Anlagen; Steam, PEM, CO2-Hydrierung, MTO und eCO2R verwenden eindeutig benannte Installations-Wrapper. |
| Gemeinsame DAC-Versorgung | DECIDED | CO2-Hydrierung und eCO2R greifen auf denselben manuell angelegten DAC-Produktknoten und damit auf einen gemeinsamen Pool installierter DAC-Kapazität zu |
| eCO2R-Aufbereitung | DECIDED | Reaktion und die Betriebsinputs der fünf Trennschritte werden in einem gemeinsamen Foreground-Prozess sichtbar aggregiert, weil der verfügbare CAPEX-Proxy das Gesamtsystem abbildet. |
| Kapazitätsbasis | DECIDED | Effektiv verfügbare Jahresproduktion in `kg Referenzprodukt/a` je Anlage |
| Zeithorizont | DECIDED | 2025 bis 2050 einschließlich, jährliche Auflösung |
| Geografische Systemgrenze | DECIDED | Europa; RER/REMIND-EU als Zielregion, deutsche Datensätze nur als dokumentierte Proxys |
| Hintergrundszenario | DECIDED | Ausschließlich `REMIND-EU_SSP2-NDC`; vier Case-Study-Interface-Datenbanken für 2020, 2030, 2040 und 2050 verweisen intern auf die jeweiligen premise-Stützjahre und bilden die einzige an optimex übergebene zeitliche Datenbankfamilie. |
| Zweck der Case Study | DECIDED | Demonstration der ökonomischen optimex-Erweiterung, keine Prognose oder Suche nach besonders interessanten Ethylen-Ergebnissen |
| Modellierungstiefe | DECIDED | Fit-for-purpose-Demonstration des Frameworks; belastbar dokumentierte Proxys und vereinfachte Annahmen sind zulässig, eine vollständige Markt- oder Technologieprognose ist nicht erforderlich |
| Umweltziel | DECIDED | Ausschließlich Minimierung der Wirkungskategorie Climate Change; keine Mehrkriteriengewichtung |
| LCIA-Methode | DECIDED | Brightway-Methode `("IPCC 2021", "climate change", "GWP 100a, incl. H and bio CO2")`, entsprechend `methanol_and_iron.ipynb` |
| Zeitliche Aggregation des Umweltziels | DECIDED | Minimierung der kumulierten Klimawirkung über alle Jahre 2025 bis 2050; keine jährliche Klimagrenze und kein isoliertes Zieljahr |
| Weitere Wirkungskategorien | OUT_OF_SCOPE | Feinstaub, Landnutzung, Wassernutzung und weitere Kategorien werden nicht systematisch optimiert oder ausgewertet |
| Use Phase | OUT_OF_SCOPE | Die Nutzungsphase der aus Ethylen hergestellten Produkte bleibt in jedem Fall ausgeschlossen |
| Produkt-End-of-Life | DEFERRED | In der Baseline ausgeschlossen; die eCO2R-Route entspricht `create_eCO2R_cryo_sep(eol="no")`. Bei einer späteren EoL-Erweiterung gemeinsam mit Anlagenstilllegung und Anlagen-EoL aufnehmen. |
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
| DAC-Modelllebensdauer | DECIDED | `20 Jahre` nach Deutz und Bardow (2021), DOI `10.1038/s41560-020-00771-9`; `operation_time_limits=(0, 19)` bildet damit genau 20 Betriebsjahre ab |
| Übrige Modelllebensdauern | DECIDED | Jeweils `25 Jahre` nach Tiggeloven (2026), Tabelle C.1: Steam Cracking, PEM-Anlage als AEC-Proxy, CO2-Hydrierung, MTO, eCO2R-Reaktor als CO2-Elektrolyse-Proxy und eCO2R-Aufbereitung als ASU-Proxy; jeweils `operation_time_limits=(0, 24)` |
| PEM-Stackersatz | OUT_OF_SCOPE | Tiggeloven nennt `9 Jahre` für AEC-Stacks und `25 Jahre` für die übrige Anlage. Das aktuelle Ein-Prozess-Modell verwendet einen vollständigen PEM-Systemwrapper mit `25 Jahren`; Stacktausch und separate Ersatzkosten werden nicht modelliert. |
| Aktuelle Kostenstufe | DECIDED | Zunächst Kostenoptimierung ohne CO2-Preis |
| Ökonomische Perspektive | DECIDED | Zentraler Systemplaner mit einem einheitlichen realen Diskontsatz; keine technologiespezifischen Investoren-WACC |
| Diskontierung | PLACEHOLDER | Einheitlicher realer Diskontsatz von `3 %`, Referenzjahr 2025, entsprechend `basic_example_econ.ipynb`; Wert und Quelle vor finalen Kostenläufen prüfen |
| Kostenbasis | DECIDED | Sämtliche Kostendaten werden auf reale Euro des Jahres 2025 (`EUR_2025`) vereinheitlicht; ursprüngliche Währung, Preisjahr und Umrechnung bleiben dokumentiert |
| Zeitpunkt der Investitionskosten | DECIDED | Installationsbezogene Kosten fallen vollständig im Installationsjahr an; keine Verteilung als Annuität über die Anlagenlebensdauer |
| Restwert am Zeithorizont | OUT_OF_SCOPE | Kein Salvage Value für nach 2050 verbleibende Anlagenlebensdauer; Investitionen tragen ihre vollständigen Kosten im Installationsjahr |
| Ökonomische Systemgrenze | DECIDED | Bepreisung ausschließlich der direkten Käufe aus den Case-Study-Hintergrunddatenbanken, wie sie in `LCADataProcessor.cost_relevant_op_flows` und `cost_relevant_cap_flows` erscheinen; interne premise-Inputs werden nicht zusätzlich bepreist. |
| Kostenallokation | DECIDED | Kosten folgen den im verwendeten LCI enthaltenen oekologischen Allokationsregeln. OPEX erben die allokierten Exchange-Mengen; route-spezifische CAPEX-Wrapper verwenden denselben Allokationsfaktor auf den vollstaendigen TPC. Ohne Allokation gilt `alpha_LCA = 1`. |
| Wärme aus Erdgas | PROXY | `0.011231884058 EUR_2025/MJ Wärme`: THE-Day-Ahead-Gaspreis 2025 von `37.2 EUR/MWh` nach FfE/EEX, geteilt durch `3600 MJ/MWh` und den Gasboiler-Wirkungsgrad `0.920` aus Tiggeloven (2026), Tabelle C.2, gedruckte Seite 169/PDF 184; nur Brennstoffkosten, ohne Kessel-CAPEX und O&M; bis zur Preisprojektion real konstant |
| Absorptionskühlung | PROXY | `0.020543646377 EUR_2025/MJ Kühlenergie`: `1.67 MJ` Wärme aus Erdgas zu `0.011231884058 EUR/MJ` plus `0.0200 kWh` Strom zu `0.08932 EUR/kWh`; Wasser bleibt unbepreist; bis zu den Gas- und Strompreisprojektionen real konstant |
| DAC-Sorbens | PROXY | `9.232482229249 EUR_2025/kg`: `8.821 USD_2022/kg` für Lewatit VP OC 1065 aus Sievert, Schmidt und Steffen (2024), SI Tabelle S21, mit dem dokumentierten EZB-/HVPI-Faktor `1.04664802508205` umgerechnet; Übertragung auf PEI auf Aluminiumoxid und reale konstante Fortschreibung; laufender Flow als Sorbensersatz, initiale Befüllung weiterhin im DAC-TPC |
| DAC-Anlage | PROXY | `23928990.4734383 EUR_2025` je Solid-Sorbent-TVSA-Anlage mit `4 kt CO2/a`: TPC-Mittelwert `22.8625 Mio. USD_2022` aus Sievert, Schmidt und Steffen (2024), SI Tabellen S12 und S15-S16, mit EZB-Jahresmittelkurs und Eurostat-HVPI umgerechnet; nicht annualisiert und bis zu einer gesonderten Projektion real konstant |
| PEM-System | PROXY | `920000 EUR_2025` je `1 MWe`-Wrapper, fuer alle Stuetzjahre real konstant. IRENA (2020), Tabelle ES1 und Tabelle 6, nennt `700-1400 USD_2020/kW` fuer vollstaendige PEM-Systeme mit mindestens `10 MW`; der spezifische Preis wird linear auf `1 MWe` uebertragen. Skaleneffekte werden nicht modelliert, die exakte EUR_2025-Umrechnung bleibt abzusichern. |
| Nicht inventarisierte Kosten | OUT_OF_SCOPE | Personal, Versicherung, Verwaltung, fixe Wartung und weitere Kosten werden nur berücksichtigt, wenn sie als explizite bepreisbare Flows im Inventar vorkommen; kein separates Zusatzkostenmodell |
| Prüfung der Preisvollständigkeit | DECIDED | Keine zusätzliche Strict-Implementierung; fehlende `market_price`-Werte erzeugen die bestehende Warnung des `LCADataProcessor`, und die Prüfung vor finalen Läufen bleibt User Responsibility |
| Zeitliche Preisentwicklung | DECIDED | Für jeden kostenrelevanten Flow wird eine zeitliche Entwicklung recherchiert oder mindestens eine quellenbasierte Entwicklungshypothese begründet; real konstante Preise sind kein automatischer Default |
| Preisinterpolation | DECIDED | Literaturwerte werden nach der Umrechnung auf `EUR_2025` auf die vier Case-Study-Stützjahre übertragen; `LCADataProcessor` interpoliert diese Preise mit der Hintergrund-Mapping-Matrix jährlich auf 2025 bis 2050. |
| Preisextrapolation und Proxys | DECIDED | Keine unbemerkte automatische Extrapolation; fehlende Randjahre dürfen mit einer expliziten einfachen Fortschreibung oder einem dokumentierten Proxy abgedeckt werden |
| Anzahl der Preispfade | DECIDED | Je kostenrelevantem Flow zunächst genau ein zentraler Baseline-Preispfad; alternative Preisannahmen können bei Bedarf nachträglich als separates Szenario gerechnet werden |
| Kosten-CSV | DECIDED | Eine gemeinsame CSV für installierungs- und betriebsbezogene Preise; `cost_class` unterscheidet `cap`, `op` und `cap_and_op` |
| Erzeugung der Recherchevorlage | DECIDED | Die versionierte Kosten-CSV ist ein vorbereiteter Modellinput; das öffentliche Notebook liest sie ein und prüft ihre Abdeckung, erzeugt oder überschreibt sie aber nicht |
| Öffentliche Notebook-Fassung | DECIDED | Das Notebook bleibt leserorientiert und enthält nur einen kompakten Abschnitt für Kostenflussliste, CSV und Preisstatus; Research Mode, Blocker-Gates und Entwicklerworkflow werden nicht gezeigt |
| Veröffentlichung der Kosten-CSV | DECIDED | Die fertig recherchierte CSV wird als reproduzierbarer Modellinput im öffentlichen Repository versioniert; Weitergaberechte der Preisquellen und enthaltenen Daten vor Veröffentlichung prüfen |
| Aktivitätsidentität in der CSV | DECIDED | Öffentliche Preiszeilen verwenden `name`, `product`, `location`, `unit` und `year`; keine datenbankspezifischen Brightway-Activity-Codes |
| Voraussetzungen des öffentlichen Notebooks | DECIDED | `optimex_remind`, die benötigten premise-Datenbanken und die Biosphere-Datenbank werden vorausgesetzt. Die vier Case-Study-Hintergrunddatenbanken werden vom Notebook erstellt; `disco2very` bleibt keine Laufzeitabhängigkeit. premise wird dabei nicht verändert. |

Die Kapazitätsbasis bezieht sich jeweils auf das Referenzprodukt der Anlage:

- DAC: `kg CO2/a`
- PEM: `kg H2/a`
- CO2-Hydrierung: `kg Methanol/a`
- MTO: `kg Ethylen/a`
- aggregierter eCO2R-Prozess: `kg Ethylen/a`

Die Kapazität ist als effektive Jahresproduktion definiert. Eine zusätzliche
Multiplikation mit einem Auslastungsgrad erfolgt nicht, sofern die recherchierten
Kapazitätsdaten bereits auf diese effektive Basis umgerechnet wurden.

## Infrastruktur und Installationsskalierung

### Kapazitaetsbasierter Installations-Wrapper

**Status:** Im Case-Study-Notebook und in `cost_inputs.csv` statisch umgesetzt;
Brightway-, LCA- und Solver-Laufzeitpruefung stehen noch aus.

Umweltinventar, physische Anlagenkapazitaet und Anlagenkosten werden als drei
getrennte Groessen behandelt:

- `s_env`: urspruenglicher LCI-Infrastrukturkoeffizient in
  `Umwelt-Infrastruktureinheiten/kg Produkt`;
- `Q`: gewaehlte effektive Nennkapazitaet eines routenspezifischen Wrappers in
  `kg Produkt/a`;
- `L`: Modelllebensdauer des Foreground-Prozesses in Jahren;
- `TPC(Q)`: nicht annualisierte Gesamtinvestition einer Anlage der Groesse `Q`.

Der aeussere Installations-Exchange vom Foreground-Prozess zum Wrapper lautet:

```text
a_wrapper = 1 / (Q * L)   [Wrapper/kg Produkt]
```

Der interne Exchange vom Wrapper zum urspruenglichen Umweltinventar lautet:

```text
a_internal = s_env / a_wrapper = s_env * Q * L
```

Damit bleibt das Umweltinventar exakt erhalten:

```text
a_wrapper * a_internal = s_env
```

Gleichzeitig ist die physische Kapazitaet konsistent. Da eine Optimex-
Prozesseinheit ueber `L` Jahre insgesamt eine Produkteinheit liefert, werden
bei einem konstanten Jahresbedarf `D` insgesamt `D * L` Prozesseinheiten
installiert. Daraus folgen `D / Q` Wrapper und damit genau `D` Einheiten
Jahreskapazitaet.

Der Ausgangswert des Wrappers ist `TPC(Q)` in `EUR_2025/Wrapper`. Fuer die
Baseline folgt die wirtschaftliche Zuordnung der im verwendeten LCI
enthaltenen oekologischen Allokation:

```text
CAPEX_wrapper = alpha_LCA * TPC(Q)
```

Bei MTO gilt `alpha_LCA = 0.4`; Prozesse ohne Produktallokation verwenden
`alpha_LCA = 1`. Beim Steam Cracking existiert dagegen kein einzelnes
flussuebergreifendes `alpha_LCA`: Nach PlasticsEurope (2017), Abschnitte 3.2
und 3.3, werden Feedstocks auf alle allokierbaren Produkte, Energie und
Emissionen aber nur auf die definierten Hauptprodukte verteilt. ecoinvent 3.12
uebernimmt diese flussspezifische Regel. Fuer die Baseline wird die
Steam-Cracker-CAPEX analog
zu Energie, Utilities und Emissionen nach dem Ethylen-Massenanteil an allen
definierten Hauptprodukten alloziert:

```text
alpha_Steam_CAPEX = m_Ethylen / sum(m_Hauptprodukte)
```

Dies ist eine explizite Modellannahme, keine von PlasticsEurope vorgeschriebene
CAPEX-Regel. Mangels offengelegter Hauptproduktmassen des ecoinvent-
Industriemixes werden die Produktausbeuten aus Tiggeloven (2026), Tabelle A.6,
gedruckte Seite 155/PDF-Seite 170, verwendet. Tiggeloven uebernimmt sie aus
Zimmermann und Walzl [52] fuer High-Severity-Naphthacracking. Als eindeutig
zuordenbare Hauptproduktgruppen werden Ethylen (`0.303 t/t Naphtha`), Propylen
(`0.1481`), BTX (`0.0766`) und C4-Produkte (`0.0525`) beruecksichtigt:

```text
alpha_Steam_CAPEX = 0.303 / (0.303 + 0.1481 + 0.0766 + 0.0525)
                  = 0.5222337125
```

Der separate Wasserstoff-Yield ist in Tabelle A.6 nicht ausgewiesen; der Faktor
ist deshalb ein dokumentierter `PROXY` und tendenziell leicht zu hoch. Er wird
nicht aus dem ecoinvent-Infrastrukturkoeffizienten zurueckgerechnet. Die von
Tiggeloven in Gleichung A.3 verwendete preisbasierte Koppelproduktallokation wird
nicht uebernommen.

Die Kapazitaet `Q` wird weiterhin aus einer physischen Anlagen- oder
Kostenquelle gewaehlt und nicht durch Invertieren von `s_env` abgeleitet. Eine
Quellenlebensdauer erklaert nur die Herkunft von `s_env`; fuer die physische
Wrapper-Skalierung ist die Optimex-Modelllebensdauer `L` massgeblich.

Da Optimex Bruchteile eines Wrappers installieren kann, wird `TPC(Q)/Q` nach
der Wahl von `Q` effektiv linear fortgeschrieben. Diskrete Anlagengroessen und
endogene Skaleneffekte sind damit nicht abgebildet.

### Kapazitaetsangaben in Tiggeloven

Tiggeloven stellt fuer die in Tabelle C.1 betrachteten Technologien keine
einheitlichen fertigen Anlagen-TPC bei jeweils einer ausgewiesenen
Referenzkapazitaet bereit. Stattdessen wird die affine Kostenfunktion
`TPC(S) = lambda * S + zeta` in der jeweils nativen Kapazitaetseinheit
parametrisiert. Wartung `psi` und Annuitaetenfaktor `omega` liegen in den
Zielfunktionen ausserhalb von `TPC` und duerfen daher nicht in den einmaligen
Wrapperpreis eingehen.

- Fuer Steam Cracking beschreibt Kapitel 2 ausdruecklich eine typische
  Weltanlage mit `1000 kt Ethylen/a`, entsprechend rund `115 t Ethylen/h`.
  Tabelle 2.3 gibt dafuer die Kostenparameter in `EUR_2019`; Gleichung 2.3 und
  Abbildung 2.7 implizieren bei dieser Kapazitaet einen TPC von rund
  `0.994 Mrd. EUR_2019`. Dies ist eine geeignete, quellennahe Wrappergroesse.
- Tabelle C.1 gibt fuer Conventional Cracking, Direct Methanol Synthesis from
  CO2, MTO, CO2 Electrolysis, AEC und ASU nur `lambda`, `zeta`, Einheit und
  Lebensdauer in `EUR_2022` an. Die jeweilige Wrapperkapazitaet muss deshalb
  transparent gewaehlt und `TPC(Q)` mit der Kostenfunktion berechnet werden.
- Tabelle 4.1 nennt `1314 kt/a` Ethylen fuer Chemelot und `1822 kt/a` fuer
  Zeeland. Dies sind Nameplate-Kapazitaeten ganzer bestehender Cluster und
  keine Referenzgroessen der einzelnen alternativen Anlagen.
- In Tabellen mit `Smax` aufgefuehrte Werte sind modellierte Ausbaugrenzen der
  Cluster. Sie sind ebenfalls keine dokumentierten Nennkapazitaeten einer
  Kostenreferenzanlage.

Die fuer die Case Study relevanten Zeilen aus Tabelle C.1 lauten:

| Technologie | Native Groesse `S` | `lambda` [`kEUR_2022/Einheit`] | `zeta` [`MEUR_2022`] |
|---|---|---:|---:|
| Conventional cracker | `t Naphtha/h` | 2083 | 543 |
| AEC (Proxy fuer PEM) | `MW Stromaufnahme` | 753 | 0 |
| Direct methanol synthesis from CO2 | `t CO2/h` | 1613 | 104 |
| MTO | `t Methanol/h` | 1051 | 66 |
| CO2 electrolysis (Proxy fuer eCO2R) | `t CO2/h` | 9461 | 0 |
| ASU (Proxy fuer eCO2R-Aufbereitung) | `MW Stromaufnahme` | 4224 | 25 |

Der einmalige TPC in Millionen Euro des Jahres 2022 wird daraus berechnet als:

```text
TPC_MEUR_2022(S) = lambda * S / 1000 + zeta
```

Diese Tabelle definiert also die Kostenbasis, aber noch nicht die jeweilige
Wrappergroesse `Q`. Die zuvor fuer einen gemeinsamen Output von `1 Mt
Ethylen/a` berechneten Stoffstroeme sind eigene Systemskalierungen der Case
Study und keine von Tiggeloven ausgewiesenen Nennkapazitaeten der einzelnen
Anlagen.

Die vier Referenzrechnungen sind vollstaendig in
[`notebooks/data/ethylene_case_study/tiggeloven_capex_calculations.md`](notebooks/data/ethylene_case_study/tiggeloven_capex_calculations.md)
dokumentiert. Aus Tabelle C.1 und C.2 ergeben sich fuer die auf `1 Mt
Ethylen/a` dimensionierten Anlagen folgende vollstaendige, nicht annualisierte
TPC:

| Anlage | `MEUR_2022` | `MEUR_2025` |
|---|---:|---:|
| Steam Cracking | `1327.770258` | `1463.430241` |
| CO2-Hydrierung | `1753.119342` | `1932.237784` |
| MTO | `802.056251` | `884.003363` |
| eCO2R, CO2-Elektrolyse-Proxy | `1794.057859` | `1977.359042` |

Die Tabelle zeigt zunaechst die vollstaendigen Roh-TPC bei `alpha_LCA = 1`.
Fuer den aktiven MTO-Wrapper gilt in der Baseline
`0.4 * 884.003363 = 353.601345 MEUR_2025`. Fuer den Steam-Wrapper gilt
`0.5222337125 * 1463.430241 = 764.252608 MEUR_2025`. Der verwendete
Allokationsfaktor folgt der PlasticsEurope-Hauptproduktregel mit den
Zimmermann-und-Walzl-Ausbeuten aus Tiggeloven Tabelle A.6.
CO2-Hydrierung und eCO2R verwenden nach dem aktuell eingesetzten LCI
`alpha_LCA = 1`.

Die physische MTO-Relation von `6.134969 kg Methanol/kg Ethylen` weicht vom
allokierten Notebook-Exchange von `2.3920583664 kg Methanol/kg Ethylen` ab.
Diese Weitergabe der Allokation an CO2-Hydrierung, PEM und DAC ist fuer die
Baseline beabsichtigt: Auch die vorgelagerten OPEX und CAPEX folgen dadurch
den allokierten LCI-Mengen.

### Einheiten der ecoinvent-Infrastruktur

- `chemical factory construction, organics`: internes Umweltinventar bezogen auf
  `unit`; direkte Preise liegen auf den getrennten Steam-, MTO- und
  eCO2R-Wrappern.

Der disco2very-Ersteller hat bestätigt, dass der bisher für eCO2R verwendete
Input `chemical factory construction` mit der Einheit `kg factory` fehlerhaft
war. Korrekt sind `4e-10 unit chemical factory construction, organics` pro kg
Ethylen.

Fuer die in `my_activities.py` dokumentierten Mengen bleibt lediglich zu
pruefen, welcher konkrete Datensatz und welche Einheit verwendet wurden. Eine
Quellenlebensdauer ist fuer ihre Uebernahme nicht erforderlich.

### `operation=False`-Exchanges und Wrapper-Stand

Die folgende Tabelle beschreibt den aktuellen technischen Zwischenstand. Bei
den routenspezifischen Wrappern sind die bisherigen aeusseren LCI-Koeffizienten
durch `1 / (Q * L)` ersetzt. Das interne Umweltinventar ist gleichzeitig so
skaliert, dass der jeweilige urspruengliche Nettokoeffizient erhalten bleibt.

| Anlage | Installations- oder EoL-Kandidaten | Status |
|---|---|---|
| MTO | `methanol-to-olefins installation` | `Q = 1e9 kg Ethylen/a`, aeusserer Koeffizient `4e-11 Wrapper/kg Ethylen`, intern `0.0896 unit chemical factory construction, organics`; Nettokoeffizient `3.584e-12` bleibt erhalten. |
| CO2-Hydrierung | `CO2 hydrogenation installation` | `Q = 6.134969325e9 kg Methanol/a`, aeusserer Koeffizient `6.52e-12 Wrapper/kg Methanol`, intern `0.5497239264 unit chemical factory construction, organics`; Nettokoeffizient `3.5842e-12` bleibt erhalten. |
| PEM | `PEM electrolyzer system installation, 1 MWe` | `Q = 156414.347247488 kg H2/a` aus `1 MWe * 8760 h/a / 56.00509259 kWh/kg H2`, `L = 25 Jahre`, aeusserer Koeffizient `2.55731016392694e-7 Wrapper/kg H2`; intern `5.2785540801` Stack- und `1.3192494393` Balance-of-Plant-Einheiten. Die Nettokoeffizienten `1.34989e-6` beziehungsweise `3.37373e-7 unit/kg H2` bleiben erhalten. |
| PEM EoL | zugehörige Recycling- und Entsorgungsprozesse | OPEN: Zeitpunkt und Skalierung prüfen |
| DAC | `direct air capture system construction, solid sorbent, 4 ktCO2/a` | Bereits kapazitaetsbezogen: `Q = 4 kt CO2/a`, `L = 20 Jahre` und `1/(Q*L) = 1.25e-8 unit/kg CO2`; die Activity enthaelt das Umweltinventar einer ganzen Anlage. |
| DAC EoL | `treatment of direct air capture, 2016` | In der disco2very-Konstruktionsactivity enthalten, für die Baseline aber bewusst nicht übernommen, da Anlagen-EoL außerhalb der Systemgrenze liegt. |
| eCO2R-Gesamtsystem | `eCO2R system installation` | `Q = 1e9 kg Ethylen/a`, aeusserer Koeffizient `4e-11 Wrapper/kg Ethylen`; intern `10 unit` Fabrik, `1.85 kg` Kupfer und `75441.975 kg` Stahl. Die drei urspruenglichen Nettokoeffizienten bleiben erhalten. |
| eCO2R-Aufbereitung | Anlagen für DeOx, Amine Wash, TSA und Kryotrennung | OPEN: explizite Infrastruktur fehlt weitgehend |
| Steam Cracking | `steam cracker installation` | `Q = 1000 kt Ethylen/a`, aeusserer Koeffizient `4e-11 Wrapper/kg Ethylen`, intern `2.8790891546 unit chemical factory construction, organics`; der ecoinvent-Nettokoeffizient bleibt erhalten. |

### Abgleich der disco2very-Background-Inputs

Der Abgleich mit dem vollständigen disco2very-Repository ergab folgende
bewusste Abweichungen im Case-Study-Modell:

| Prozess | Ergebnis |
|---|---|
| Steam Cracking | Das ecoinvent-Inventar wird eine Ebene tiefer aufgeschlüsselt. Die sieben Feedstocks werden ökologisch unverändert in `steam cracking feedstock mix` gebündelt; Diesel bleibt der dokumentierte Proxy für atmospheric gas oil. |
| DAC | Korrigiert: Amine-on-Alumina ersetzt den früheren Aktivkohleproxy; die 4-kt-Solid-Sorbent-Konstruktion ersetzt die frühere premise-Activity für ein solvent-basiertes System. |
| PEM | Die disco2very-Material- und Entsorgungsinputs sind bewusst durch die Stack- und Balance-of-Plant-Inventare aus `methanol_and_iron` ersetzt; beide liegen intern in einem gemeinsam bepreisten 1-MWe-Systemwrapper. Betriebsstrom, Wasser und Abwasser entsprechen disco2very. |
| CO2-Hydrierung | Betriebsinputs entsprechen disco2very; die Installation wird ueber den routenspezifischen Wrapper `CO2 hydrogenation installation` eindeutig bepreist. |
| MTO | Mengen entsprechen `allocation="weight"`; die disco2very-Kühlaktivitäten bei -30 °C und -75 °C werden durch verfügbare premise-Proxys bei -25 °C beziehungsweise -100 °C ersetzt. |
| eCO2R-Reaktion und Aufbereitung | Beide bisherigen Foreground-Prozesse sind zu `eCO2R ethylene production` aggregiert. Alle Betriebs- und Biosphere-Mengen bleiben erhalten; die disco2very-Kühlaktivität bei -75 °C wird weiterhin durch den premise-Proxy bei -100 °C ersetzt. Der fehlerhafte Fabrikmasseninput wurde nach Rücksprache mit dem disco2very-Ersteller durch `4e-10 unit chemical factory construction, organics/kg Ethylen` ersetzt. |

Die DAC-Konstruktionsactivity beschreibt ein System mit `4 kt CO2/a`
Nennkapazität. Diese Kapazitätsbasis stimmt mit den betrachteten Kostendaten aus
Sievert et al. überein und ermöglicht eine direkte Zuordnung des dort
abgeleiteten TPC. Die im Deutz-und-Bardow-Quellinventar genannten `20 Jahre`
werden auch als Optimex-Modelllebensdauer der DAC-Anlage verwendet. Mit beiden
Groessen wird der aeussere Wrapperkoeffizient berechnet; der urspruengliche
LCI-Koeffizient bleibt ueber den internen Exchange erhalten.

Strom, Wärme, Kühlenergie, Wasser, Abwasser, CO2, H2, Methanol und andere
produktionsabhängige Zwischenprodukte werden grundsätzlich als
`operation=True` behandelt. Für Adsorbens, Schmiermittel, Elektroden und
Katalysatormaterialien muss anhand der Stand- und Ersatzzeiten entschieden
werden, ob sie Betriebs- oder Installationsflüsse sind.

## Pflichtrecherche vor finalen Szenarioläufen

| Parameter | Betroffene Prozesse | Status | Benötigte Dokumentation |
|---|---|---|---|
| Betriebslebensdauer | alle Foreground-Anlagen | DECIDED | DAC `20 Jahre` nach Deutz und Bardow; alle übrigen Anlagen `25 Jahre` nach Tiggeloven, mit dokumentierten Technologie-Proxys für PEM und eCO2R |
| Bauzeit / Betriebsbeginn | alle Foreground-Anlagen | DECIDED | Keine Bauzeit im Modell; Same-year-Konvention entsprechend `methanol_and_iron.ipynb` |
| Installationenskalierung | alle Anlagen mit `operation=False` | SOFTWARE PREREQUISITE | Korrigierten `var_installation`-Pfad mit einem mehrjaehrigen Static-LCA-Aequivalenztest validieren |
| Komponentenstandzeiten und Ersatz | PEM, DAC, eCO2R | OPTIONAL | Nur fuer eine explizite Komponentenwechsel-Modellierung erforderlich; nicht fuer die Uebernahme normaler Inventory-Mengen |
| Altersstruktur bestehender Kapazität | Steam Cracking | BLOCKER | Installationsjahre der zwei Kohorten und resultierende Restlebensdauern in Abstimmung mit der recherchierten Anlagenlebensdauer festlegen |
| Früheste Verfügbarkeit | neue Routen | OPEN | Jahr und Quelle |
| Infrastruktur der eCO2R-Aufbereitung | Aufbereitungsanlage | OPEN | Umfang und Kapazitätsnormalisierung |
| Modellierung Steam Cracking | fossile Route | BLOCKER | Direkte Betriebs- und Biosphere-Exchanges, kapazitaetsbezogener Wrapper, erhaltener ecoinvent-Infrastrukturkoeffizient und 25-jaehrige Modelllebensdauer sind statisch umgesetzt; Neubau-CAPEX verwendet `alpha = 0.5222337125`; Brightway-/LCA-/Solver-Laufzeitpruefung bleibt offen |
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
| `year` | Repräsentatives Jahr der Case-Study-Hintergrunddatenbank, an deren direktem Kostenknoten der Preis geschrieben wird |
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

### Einheitliche Umrechnung auf EUR_2025

Alle historischen Kosten werden als reale Euro des Jahres 2025 ausgewiesen. Als
einheitlicher Inflationsindex wird der jährliche Durchschnitt des All-items-HVPI
für den Euroraum mit 20 Ländern verwendet (`prc_hicp_ainr`, `EA20`, `TOTAL`,
`INX_A_AVG`). Eurostat weist auf der Basis `2025 = 100` folgende Indizes aus:

| Preisjahr | HVPI-Jahresdurchschnitt | Faktor auf `EUR_2025` |
|---:|---:|---:|
| 2020 | `81.59` | `100 / 81.59 = 1.22564039710749` |
| 2022 | `90.73` | `100 / 90.73 = 1.10217127741651` |
| 2025 | `100.00` | `1` |

Quelle: Eurostat, *Harmonised index of consumer prices (HICP) - ECOICOP
ver.2 - indices and rates of change, annual data*, DOI
[`10.2908/PRC_HICP_AINR`](https://doi.org/10.2908/PRC_HICP_AINR),
[API-Abfrage für EA20 und All-items](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_ainr?lang=en&geo=EA20&coicop18=TOTAL&unit=INX_A_AVG).

Für Euro-Werte gilt:

```text
Preis_EUR_2025 = Preis_EUR_y * HVPI_2025 / HVPI_y
```

USD-Werte werden zuerst mit dem jahresdurchschnittlichen ECB-Referenzkurs ihres
Preisjahres in Euro desselben Jahres umgerechnet. Die ECB-Reihe
`EXR.A.USD.EUR.SP00.A` ist in `USD je EUR` notiert; deshalb wird der USD-Wert
durch den Wechselkurs dividiert. Anschließend wird der Euro-Wert mit demselben
HVPI-Verfahren auf 2025 gebracht.

| Preisjahr | ECB-Jahresmittel `USD/EUR` | Gesamtfaktor `USD_y` auf `EUR_2025` |
|---:|---:|---:|
| 2020 | `1.1421961089494` | `(1 / 1.1421961089494) * (100 / 81.59) = 1.07305600807452` |
| 2022 | `1.0530486381323` | `(1 / 1.0530486381323) * (100 / 90.73) = 1.04664802508205` |

Quelle: Europäische Zentralbank,
[`EXR.A.USD.EUR.SP00.A`](https://data.ecb.europa.eu/data/datasets/EXR/EXR.A.USD.EUR.SP00.A),
Annual average of observations through period.

Für USD-Werte gilt damit:

```text
Preis_EUR_2025 = Preis_USD_y / ECB_USD_je_EUR_y * HVPI_2025 / HVPI_y
```

Das Preisjahr und nicht das Technologie- oder Szenariojahr bestimmt den Faktor.
Ein beispielsweise als `USD_2020` ausgewiesenes 2050-Technologieziel verwendet
daher weiterhin den Faktor für `USD_2020`. Bandbreiten werden an beiden Grenzen
mit demselben Faktor umgerechnet. Es wird nicht zwischengerundet; in der CSV
werden mindestens zwölf signifikante Stellen des Ergebnisses gespeichert.

Der All-items-HVPI ist kein spezifischer Chemieanlagen-Kostenindex. Seine
Verwendung ist eine transparente, einheitliche Modellannahme für diese
Framework-Demonstration. Währungsumrechnung und Inflation verändern nur die
Preisbasis; Technologieentwicklung und zukünftige Preiszeitreihen werden davon
getrennt modelliert.

### Steam-Cracker-Feedstock-Proxy

Entscheidung vom 2026-08-01: Der von Tiggeloven (2026) angegebene
nordwesteuropäische Naphtha-Preis von `732 EUR_2022/t` wird als Preisproxy für
den allokierten Feedstock-Slate der fossilen Steam-Cracking-Route verwendet.
Tiggeloven bezeichnet den Wert als Durchschnittspreis für 2022 und verweist auf
die INSEE-Spotpreisreihe für nordwesteuropäisches Naphtha. Die konstante
Fortschreibung ist eine Modellannahme und keine Marktpreisprognose.

Für die einheitliche CSV-Preisbasis wird der Wert nach der oben festgelegten
HVPI-Indexmethode umgerechnet:

```text
0.732 EUR_2022/kg * (100 / 90.73)
= 0.806789375069 EUR_2025/kg
```

Der Wert wird für alle vier Stützjahre auf die Case-Study-Activity
`steam cracking feedstock mix` geschrieben. Der Status bleibt `PROXY`, weil ein
Naphtha-Preis vereinfachend den gesamten Feedstock-Slate bewertet.

Die Activity produziert `1 kg` Mix aus den sieben in der ecoinvent-Dokumentation
genannten Massenanteilen: Butan `16.2 %`, Ethan `4.5 %`, Naphtha `64.0 %`, Natural
Gas Liquids `2.2 %`, Propan `7.6 %`, Refinery Gas `1.5 %` und Atmospheric Gas Oil
`4.0 %`, letzteres wie im Quellinventar durch Diesel approximiert. Steam Cracking
bezieht insgesamt `1.21675954200327 kg Mix/kg Ethylen`.

Nur der direkte Mix-Flow wird in optimex bepreist. Seine sieben internen
premise-Exchanges erhalten keinen zusätzlichen Market Price; Energie,
Hilfsstoffe und Abfallbehandlungen bleiben separate direkte Betriebsflüsse.
Die früheren sieben einzelnen Feedstock-Identitäten wurden entsprechend aus
`cost_inputs.csv` entfernt. Die vollständige Laufzeitprüfung von LCIA-Gleichheit
und `cost_relevant_op_flows` steht weiterhin aus.

## Implementierungsstand Meilenstein 1

Stand 2026-07-18:

- `notebooks/ethylene_case_study.ipynb` ist als lineare, leserorientierte
  Fallstudie nach dem Muster von `methanol_and_iron.ipynb` aufgebaut. Es enthält
  keine Research-Mode-Schalter, Blocker-Gates oder Entwicklerworkflow-Erklärung.
- Die Product Nodes, sieben Entscheidungsprozesse und alle Foreground-Exchanges
  werden direkt im Notebook angelegt. Die Case Study benötigt zur Laufzeit keine
  vorbereiteten `disco2very`-Activities.
- Lebensdauern, Installationskoeffizienten, Brownfield-Jahre und Diskontsatz
  stehen gemeinsam in einer sichtbaren Annahmentabelle. Werte sind dort als
  `RESEARCHED`, `PROXY` oder `PLACEHOLDER` gekennzeichnet und können gezielt
  ersetzt werden.
- Die beiden Vintages 2005 und 2015 stellen mit jeweils `0.5e9 kg/a` die
  vollständige Steam-Cracker-Kapazität im Startjahr bereit.
- Der Steam Cracker wird eine Ebene unterhalb der gebündelten ecoinvent-Activity
  modelliert. Sieben der 17 direkten Technosphere-Inputs bilden intern den
  Feedstock-Mix; dadurch verbleiben elf direkte Optimex-Betriebsflüsse. Die 44
  direkten Biosphere-Exchanges bleiben unverändert. Kumulierte Biosphere-Flows
  der Lieferketten werden weiterhin durch Brightway berechnet.
- `steam cracker installation` verwendet `Q = 1000 kt Ethylen/a` und
  `L = 25 Jahre` fuer den aeusseren Koeffizienten
  `1 / (Q * L)`. Der ecoinvent-Koeffizient
  `1.1516356618335166e-10 unit/kg Ethylen` wird durch entsprechende Skalierung
  des internen Exchanges als Netto-Umweltinventar erhalten.
- Bei 25 Jahren Modelllebensdauer ist das Bestandsvintage von 2005 bis
  einschließlich 2029 und das Vintage von 2015 bis einschließlich 2039
  verfügbar. Sie sind weiterhin nicht must-run und können früher durch andere
  Routen ersetzt werden.
- DAC wird von CO2-Hydrierung und eCO2R über denselben Produktknoten genutzt.
  eCO2R-Reaktion und Aufbereitung sind ein gemeinsamer Foreground-Prozess und
  enthalten `6.091081 kg CO2/kg Ethylen` aus der Oxidation der Nebenprodukte,
  nicht aus Produkt-EoL. Dies entspricht `create_eCO2R_cryo_sep(eol="no")` in
  der aktuellen disco2very-Implementierung.
- Die vier Case-Study-Hintergrunddatenbanken enthalten die Kosten-Interfaces und
  verweisen intern auf die jeweils gleichjährige premise-Datenbank. Weder eigene
  Activities noch `representative_time` werden in premise geschrieben.
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
| Steam-Cracker-Feedstock-Bündelung | IMPLEMENTED_STATIC | Sieben bestätigte Feedstocks in `steam cracking feedstock mix` gebündelt und temporäre Einzelidentitäten in der Kosten-CSV ersetzt; Brightway-/LCIA-Laufzeitprüfung steht aus. |
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
