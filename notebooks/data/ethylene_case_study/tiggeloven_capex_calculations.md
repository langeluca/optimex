# Tiggeloven-CAPEX fuer die Ethylen-Case-Study

## Zweck und Status

Diese Notiz leitet die vier Tiggeloven-basierten Anlagen-CAPEX fuer eine
gemeinsame Referenzgroesse von `1 Mt Ethylen/a` her. Berechnet werden
vollstaendige, nicht annualisierte Total Plant Costs (TPC) vor einer
oekonomischen Allokation. Die kapazitaetsbasierten Wrapper und die hier
hergeleiteten Preise sind im Case-Study-Notebook und in `cost_inputs.csv`
statisch umgesetzt. Die Laufzeitpruefung steht noch aus.

## Quellen und Konventionen

Quelle ist Julia Tiggeloven (2026), *Breaking and re-forming the chemical
industry: Optimizing the transition from fossil-based clusters to net zero*:

- Gleichung 4.4, gedruckte Seite 90 / PDF-Seite 105;
- Tabelle C.1, gedruckte Seite 168 / PDF-Seite 183;
- Tabelle C.2, gedruckte Seite 169 / PDF-Seite 184.

Tiggelovens einmalige Investitionskosten lauten:

```text
TPC_MEUR_2022(S) = lambda_kEUR_2022_per_unit * S / 1000 + zeta_MEUR_2022
```

Der Instandhaltungsfaktor `psi` und der Annuitaetenfaktor `omega` stehen in
Gleichung 4.4 ausserhalb von `(lambda * S + zeta)`. Sie gehoeren deshalb nicht
in den einmaligen Optimex-Wrapperpreis.

Gemeinsame Annahmen:

```text
E = 1,000,000 t Ethylen/a
h = 8,760 h/a
alpha_LCA = 1 fuer die hier ausgewiesenen vollstaendigen Roh-TPC
```

Die Umrechnung von `EUR_2022` auf `EUR_2025` folgt der fuer die Case Study
festgelegten HVPI-Methode:

```text
f_2022_to_2025 = HVPI_2025 / HVPI_2022
               = 100 / 90.73
               = 1.1021712774165105
```

## 1. Steam Cracking

Tabelle C.2 gibt `0.303 t Ethylen/t Naphtha` an. Die fuer `1 Mt Ethylen/a`
erforderliche Naphtha-Kapazitaet ist daher:

```text
S_steam = E / 0.303 / h
        = 1,000,000 / 0.303 / 8,760
        = 376.7500038 t Naphtha/h
```

Tabelle C.1: `lambda = 2.083 MEUR_2022/(t Naphtha/h)`,
`zeta = 543 MEUR_2022`.

```text
TPC_2022 = 2.083 * 376.7500038 + 543
         = 1,327.7702578 MEUR_2022

TPC_2025 = 1,327.7702578 * 1.1021712774
         = 1,463.4302412 MEUR_2025
```

## 2. Methanol-to-Olefins

Tabelle C.2 gibt fuer MTO `0.163 t Ethylen/t Methanol` und zusaetzlich
`0.165 t Propylen/t Methanol` an. Der Wert `0.592` in derselben Tabelle gehoert
zur Ethanol-Dehydratisierung und darf nicht fuer MTO verwendet werden.

```text
S_MTO = E / 0.163 / h
      = 1,000,000 / 0.163 / 8,760
      = 700.3389641 t Methanol/h
```

Dies entspricht einem Methanolbedarf von:

```text
Q_methanol = 700.3389641 * 8,760
           = 6,134,969.3252 t Methanol/a
```

Tabelle C.1: `lambda = 1.051 MEUR_2022/(t Methanol/h)`,
`zeta = 66 MEUR_2022`.

```text
TPC_2022 = 1.051 * 700.3389641 + 66
         = 802.0562512 MEUR_2022

TPC_2025 = 802.0562512 * 1.1021712774
         = 884.0033630 MEUR_2025
```

## 3. Direkte Methanolsynthese aus CO2

Die CO2-Hydrierung wird so gross ausgelegt, dass sie den gesamten physischen
Methanolbedarf der oben definierten MTO-Referenzanlage deckt. Tabelle C.2 gibt
`0.685 t Methanol/t CO2` an.

```text
S_hydrogenation = S_MTO / 0.685
                = 700.3389641 / 0.685
                = 1,022.3926483 t CO2/h
```

Tabelle C.1: `lambda = 1.613 MEUR_2022/(t CO2/h)`,
`zeta = 104 MEUR_2022`.

```text
TPC_2022 = 1.613 * 1,022.3926483 + 104
         = 1,753.1193416 MEUR_2022

TPC_2025 = 1,753.1193416 * 1.1021712774
         = 1,932.2377842 MEUR_2025
```

## 4. eCO2R

Tiggelovens CO2-Elektrolyse dient als CAPEX-Proxy fuer eCO2R. Tabelle C.2 gibt
`0.602 t Ethylen/t CO2` sowie `0.019 t Wasserstoff/t CO2` als Koppelprodukt an.

```text
S_eCO2R = E / 0.602 / h
        = 1,000,000 / 0.602 / 8,760
        = 189.6266630 t CO2/h
```

Tabelle C.1: `lambda = 9.461 MEUR_2022/(t CO2/h)`, `zeta = 0`.

```text
TPC_2022 = 9.461 * 189.6266630
         = 1,794.0578589 MEUR_2022

TPC_2025 = 1,794.0578589 * 1.1021712774
         = 1,977.3590421 MEUR_2025
```

Der Proxy bildet die CO2-Elektrolyse ab. Ein separater CAPEX fuer die in der
Case Study aggregierte Produktaufbereitung ist damit nicht automatisch
enthalten; Tiggelovens ASU-Kosten waeren dafuer nur ein zusaetzlicher Proxy.

## Ergebnis

| Wrapper | Physische Tiggeloven-Groesse | Vollstaendiger TPC [`MEUR_2022`] | Vollstaendiger TPC [`MEUR_2025`] |
|---|---:|---:|---:|
| Steam Cracking | `376.750004 t Naphtha/h` | `1,327.770258` | `1,463.430241` |
| CO2-Hydrierung | `1,022.392648 t CO2/h` | `1,753.119342` | `1,932.237784` |
| MTO | `700.338964 t Methanol/h` | `802.056251` | `884.003363` |
| eCO2R | `189.626663 t CO2/h` | `1,794.057859` | `1,977.359042` |

Die Werte sind die vollen Anlagenkosten. In der Baseline folgt die
wirtschaftliche Zuordnung der oekologischen Allokation des verwendeten LCI:

```text
CAPEX_wrapper = alpha_LCA * TPC_2025
```

Damit ergibt sich fuer MTO mit `alpha_LCA = 0.4` ein aktiver Wrapperpreis von
`353.601345 MEUR_2025`. CO2-Hydrierung und eCO2R verwenden nach dem aktuellen
LCI `alpha_LCA = 1`.

Fuer Steam Cracking gibt es keinen einzelnen flussuebergreifenden
ecoinvent-Allokationsfaktor. Nach
PlasticsEurope (2017), Abschnitte 3.2 und 3.3, werden Feedstocks auf alle
allokierbaren Produkte verteilt; Energie und Emissionen werden nur den
definierten Hauptprodukten zugeordnet. ecoinvent 3.12 dokumentiert dieselbe
flussspezifische Vorgehensweise auf PDF-Seite 8. Weder die Empfehlung noch die
ecoinvent-Kurzdokumentation ordnet die CAPEX einer Gesamtanlage ausdruecklich
einer dieser beiden Massenbasen zu. Fuer die Baseline wird deshalb explizit
angenommen, dass die Steam-Cracker-CAPEX analog zu Energie, Utilities und
Emissionen nach dem Ethylen-Massenanteil an allen definierten Hauptprodukten
alloziert wird:

```text
alpha_Steam_CAPEX = m_Ethylen / sum(m_Hauptprodukte)
CAPEX_Steam_wrapper = alpha_Steam_CAPEX * 1,463.430241 MEUR_2025
```

Mangels offengelegter Hauptproduktmassen des ecoinvent-Industriemixes werden die
Produktausbeuten aus Tiggeloven (2026), Tabelle A.6, gedruckte Seite 155/
PDF-Seite 170, verwendet. Die Ausbeuten stammen dort aus Zimmermann und Walzl
[52] fuer High-Severity-Naphthacracking. Als eindeutig zuordenbare
Hauptproduktgruppen werden Ethylen (`0.303 t/t Naphtha`), Propylen (`0.1481`),
BTX (`0.0766`) und C4-Produkte (`0.0525`) beruecksichtigt:

```text
alpha_Steam_CAPEX = 0.303 / (0.303 + 0.1481 + 0.0766 + 0.0525)
                  = 0.5222337125

CAPEX_Steam_wrapper = 0.5222337125 * 1,463.430241 MEUR_2025
                    = 764.252608 MEUR_2025
```

Der separate Wasserstoff-Yield ist in Tabelle A.6 nicht ausgewiesen. Der Faktor
ist daher ein `PROXY` und tendenziell leicht zu hoch. Tiggelovens eigene
preisbasierte Koppelproduktallokation nach Gleichung A.3 wird nicht uebernommen.
Ebenso wird kein Faktor aus dem ecoinvent-Infrastrukturkoeffizienten
zurueckgerechnet.

## Umgesetzte Wrapper-Skalierung

Bei `L = 25 Jahren` ergeben sich fuer die drei direkt Ethylen produzierenden
Prozesse:

```text
Q_steam = Q_MTO = Q_eCO2R = 1e9 kg Ethylen/a
a_wrapper = 1 / (Q * L) = 4e-11 Wrapper/kg Ethylen
```

Fuer die CO2-Hydrierung ist das Referenzprodukt Methanol:

```text
Q_hydrogenation = 6.1349693252e9 kg Methanol/a
a_wrapper = 1 / (Q * L) = 6.52e-12 Wrapper/kg Methanol
```

Diese Koeffizienten sind gemeinsam mit der internen Reskalierung des
Umweltinventars in das Notebook uebernommen. Dadurch bleiben die urspruenglichen
Netto-LCI-Koeffizienten unveraendert.

## Auswirkung der MTO-Allokation auf die Route

Das aktuelle MTO-Foreground-Inventar konsumiert wegen der Massenallokation nur
`2.3920583664 kg Methanol/kg Ethylen`. Die physische Tiggeloven-Auslegung
verwendet dagegen:

```text
1 / 0.163 = 6.1349693252 kg Methanol/kg Ethylen
```

Dadurch ruft die aktuelle Modellkopplung bei `1 Mt Ethylen/a` nur rund
`2.392 Mt Methanol/a` von der CO2-Hydrierung ab, obwohl deren hier berechneter
voller TPC eine Anlage fuer `6.135 Mt Methanol/a` beschreibt. Optimex installiert
damit rund `2.392 / 6.135 = 38.99 %` des physischen Hydrierungswrappers und
bilanziert denselben Anteil seiner OPEX und CAPEX. Diese Weitergabe ist in der
Baseline beabsichtigt, weil die wirtschaftliche Zuordnung den allokierten
LCI-Mengen folgt. Eine davon unabhaengige oekonomische Allokation waere eine
spaetere Modellerweiterung mit getrennten Kosten- und Umweltmengen.

## Modellgrenze

Optimex darf Bruchteile dieser Referenzwrapper installieren. Damit werden die
Kosten nach Wahl der Referenzgroesse proportional skaliert. Die Berechnung
bildet keine diskreten Anlagen, Mindestgroessen oder endogenen Skaleneffekte ab
und stimmt nur am jeweiligen Referenzpunkt exakt mit Tiggelovens Kostenfunktion
ueberein.
