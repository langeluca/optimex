# Optimex Economics Implementation Roadmap

Diese Roadmap beschreibt die geplante Erweiterung von `optimex` um eine
ökonomische Kostenoptimierung mit getrennten CAPEX/OPEX-artigen Kostenkonten.

## Ziel

Die Kosten sollen auf direkte first-level Background-Einkaeufe angewendet werden:

```text
total_cost =
  sum_t discount_factor[t] * (cost_cap[t] + cost_op[t])
```

mit:

```text
cost_cap[t] =
  sum_i intermediate_costs_cap[i,t] * background_purchase_cap[i,t]

cost_op[t] =
  sum_i intermediate_costs_op[i,t] * background_purchase_op[i,t]
```

Wichtig:

- Preise werden nur auf direkte Background-Produkte angewendet.
- Interne Foreground-Produkte werden nicht bepreist.
- Upstream-Prozesse innerhalb des Background-Systems werden nicht nochmal
  oekonomisch bewertet.
- Das Background-System bleibt fuer Umweltwirkungen weiterhin voll relevant.
- Die cap/op-Trennung ist primaer eine Accounting-Struktur zur Auswertung von
  installationsbezogenen und betriebsbezogenen Kosten.

## Ziel-API

Am Ende soll ein Aufruf wie dieser moeglich sein:

```python
model_inputs.intermediate_costs_cap = {
    ("steel", 2030): 900,
    ("dac_system", 2030): 2_000_000,
}

model_inputs.intermediate_costs_op = {
    ("electricity_mv", 2030): 80,
}

model_inputs.discount_rate = 0.05
model_inputs.discount_reference_year = 2030

model = optimizer.create_model(
    model_inputs,
    name="cost_model",
    objective_category="climate_change",
    objective="cost",
)
```

Im Pyomo-Modell sollen danach verfuegbar sein:

```python
model.background_purchase_cap[i, t]
model.background_purchase_op[i, t]
model.cost_cap[t]
model.cost_op[t]
model.discount_factor[t]
model.total_cost
```

## Mathematische Einordnung

Die Implementierung entspricht:

```text
min sum_t [
    (c_cap_t)^T p_cap_t
  + (c_op_t)^T p_op_t
]
```

mit:

```text
p_cap_t = direkte Background-Einkaeufe aus installationsbezogenen Edges
p_op_t  = direkte Background-Einkaeufe aus operationalen Edges
```

Die bestehenden Entscheidungsvariablen bleiben unveraendert:

```text
var_installation[p,t] = installierte Kapazitaet
var_operation[p,v,t] = Betrieb einer Vintage
```

## Uebersicht nach Pyomo-Bausteinen

### Sets

Keine neuen Sets noetig.

Bestehende relevante Sets:

| Set | Rolle |
|---|---|
| `PROCESS` | Foreground-Prozesse |
| `INTERMEDIATE_FLOW` | First-level Background-Produkte, die bepreist werden |
| `SYSTEM_TIME` | Kalenderjahre fuer Preise und Diskontierung |
| `ACTIVE_VINTAGE_TIME` | Gueltige Kombinationen aus Prozess, Vintage und Jahr |

### Params

Neu:

| Parameter | Bedeutung |
|---|---|
| `intermediate_costs_cap[i,t]` | Preis fuer installationsbezogene first-level Background-Einkaeufe |
| `intermediate_costs_op[i,t]` | Preis fuer betriebsbezogene first-level Background-Einkaeufe |
| `discount_rate` | Diskontierungsrate, z. B. `0.05` |
| `discount_reference_year` | Referenzjahr fuer Diskontierung |

### Vars

Keine neuen Variablen.

Bestehend:

| Variable | Bedeutung |
|---|---|
| `var_installation[p,t]` | Neubau von Prozess `p` in Jahr `t` |
| `var_operation[p,v,t]` | Betrieb von Prozess `p`, gebaut in `v`, im Jahr `t` |

### Expressions

Neu:

| Expression | Bedeutung |
|---|---|
| `background_purchase_cap[i,t]` | Reale Menge von Background-Flow `i`, aus installationsbezogenen Edges |
| `background_purchase_op[i,t]` | Reale Menge von Background-Flow `i`, aus operationalen Edges |
| `discount_factor[t]` | Diskontierungsfaktor fuer Jahr `t` |
| `cost_cap[t]` | Installationsbezogene Kosten in Jahr `t` |
| `cost_op[t]` | Betriebskosten in Jahr `t` |
| `total_cost` | Diskontierte Gesamtkosten |

### Constraints

Keine neuen Constraints fuer die Minimalversion.

Bestehende Constraints bleiben gueltig:

| Constraint | Rolle bei Kostenoptimierung |
|---|---|
| `ProductDemandFulfillment` | Nachfrage muss erfuellt werden |
| `OperationCapacity` | Betrieb darf Kapazitaet nicht ueberschreiten |
| `ProcessDeploymentLimitMax/Min` | Ausbaugrenzen |
| `ProcessOperationLimitMax/Min` | Betriebsgrenzen |
| `CategoryImpactLimits` | Zeitliche Umweltbudgets |
| `CumulativeCategoryImpactLimits` | Kumulative Umweltbudgets |
| `FlowLimitMax/Min` | Flow-Grenzen |
| `ProcessCouplingConstraint` | Technische Kopplungen |

### Objective

Neu:

```python
objective="environmental"
```

bleibt Standard und minimiert:

```python
model.total_impact[model._objective_category]
```

Neu:

```python
objective="cost"
```

minimiert:

```python
model.total_cost
```

## Schritt 1: Datenmodell erweitern

Datei:

```text
src/optimex/converter.py
```

In `OptimizationModelInputs` ergaenzen:

```python
intermediate_costs_cap: Optional[Dict[Tuple[str, int], float]] = Field(
    None,
    description=(
        "Time-specific prices for installation-related first-level background "
        "purchases. Maps (intermediate_flow, system_time) to price per real unit."
    ),
)

intermediate_costs_op: Optional[Dict[Tuple[str, int], float]] = Field(
    None,
    description=(
        "Time-specific prices for operation-related first-level background "
        "purchases. Maps (intermediate_flow, system_time) to price per real unit."
    ),
)

discount_rate: Optional[float] = Field(
    None,
    description="Discount rate for cost objective, e.g. 0.05 for 5%.",
)

discount_reference_year: Optional[int] = Field(
    None,
    description="Reference year for discounting. Defaults to min(SYSTEM_TIME).",
)
```

Checkliste:

- [X] Felder in `OptimizationModelInputs` ergaenzen.
- [X] Keine Skalierung der Preise einfuehren.
- [X] Bestehende Pflichtfelder nicht veraendern.

## Schritt 2: Validierung ergaenzen

Datei:

```text
src/optimex/converter.py
```

Validierung fuer folgende Felder ergaenzen:

```python
intermediate_costs_cap
intermediate_costs_op
```

Regeln:

```text
key = (flow, year)
flow muss in INTERMEDIATE_FLOW sein
year muss in SYSTEM_TIME sein
price sollte numerisch sein
```

Ausserdem:

```text
discount_rate >= 0
```

Hinweis:

`discount_reference_year` muss nicht zwingend in `SYSTEM_TIME` liegen. Ein
Referenzjahr vor Modellstart kann sinnvoll sein. Wenn `None`, wird spaeter
`min(SYSTEM_TIME)` verwendet.

Checkliste:

- [X] Key-Validierung fuer `intermediate_costs_cap`.
- [X] Key-Validierung fuer `intermediate_costs_op`.
- [X] Negative `discount_rate` verhindern.

## Schritt 3: Scaling pruefen

Datei:

```text
src/optimex/converter.py
```

In `get_scaled_copy()` pruefen:

- [X] `intermediate_costs_cap` bleibt unveraendert.
- [X] `intermediate_costs_op` bleibt unveraendert.
- [X] `discount_rate` bleibt unveraendert.
- [X] `discount_reference_year` bleibt unveraendert.

Wichtig:

Die Kostenpreise sind reale Preise pro realer Mengeneinheit. Die Mengen aus
`scaled_technosphere...` werden spaeter im Optimizer mit
`model.scales["foreground"]` zurueckgerechnet.

## Schritt 4: JSON-Serialization erweitern

Datei:

```text
src/optimex/converter.py
```

In `ModelInputManager.save_inputs()` die Liste `tuple_key_fields` ergaenzen:

```python
"intermediate_costs_cap",
"intermediate_costs_op",
```

Dasselbe in `ModelInputManager.load_inputs()`.

Checkliste:

- [X] `save_inputs()` erweitert.
- [X] `load_inputs()` erweitert.
- [X] JSON-Tests ergaenzen und durchfuehren

## Schritt 5: Kosten aus Background-Node-Attributen in die Pipeline integrieren

Dateien:

```text
src/optimex/economics.py
src/optimex/lca_processor.py
src/optimex/converter.py
```

Ziel:

Kosten sollen nicht nur manuell nachtraeglich auf `model_inputs` gesetzt werden
koennen, sondern optional direkt aus Brightway-Background-Nodes kommen.

Die Kosten werden dabei analog zur bestehenden Background-Inventory-Logik
behandelt:

```text
Foreground Edge verweist auf einen Background-Node, z. B. aus der 2020 DB
    -> optimex speichert dessen code als INTERMEDIATE_FLOW
    -> fuer Kosten wird zuerst wie bisher der Node mit diesem code gesucht
    -> falls das fehlschlaegt, wird fuer Kosten ueber name/location/product/unit gesucht
    -> dort wird ein market_price gelesen
    -> Preise werden ueber die bestehende mapping[bkg,t]-Matrix auf SYSTEM_TIME interpoliert
```

Beispiel fuer User Input:

```python
from optimex.economics import set_market_prices

price_data = [
    {
        "name": "market group for electricity, medium voltage",
        "location": "RER",
        "year": 2020,
        "price": 90.0,
    },
    {
        "name": "market group for electricity, medium voltage",
        "location": "RER",
        "year": 2030,
        "price": 70.0,
    },
]

set_market_prices(
    price_data=price_data,
    background_databases={
        2020: "ei312_REMIND-EU_SSP2_NDC_2020",
        2030: "ei312_REMIND-EU_SSP2_NDC_2030",
        2040: "ei312_REMIND-EU_SSP2_NDC_2040",
        2050: "ei312_REMIND-EU_SSP2_NDC_2050",
    },
)
```

Der Preis haengt am Background-Node in der jeweiligen zeitspezifischen
Background-Datenbank, nicht an der Foreground-Edge.

Die CAPEX/OPEX-artige Trennung entsteht weiterhin ueber die konkrete Foreground
Edge:

```text
operation=False Edge -> flow wird fuer intermediate_costs_cap relevant
operation=True Edge  -> flow wird fuer intermediate_costs_op relevant
```

Wenn derselbe Background-Node in unterschiedlichen Edges sowohl operational als
auch nicht-operational verwendet wird, wird derselbe interpolierte Marktpreis in
beiden Kostenvektoren verwendet. Das passiert dann nicht blind, sondern weil
beide Verwendungen im Foreground-System tatsaechlich vorkommen.

### Schritt 5.1: Node-Attribut festlegen

Fuer die erste Implementierung wird auf Background-Nodes nur ein Attribut
unterstuetzt:

```text
market_price
```

Format:

```python
node["market_price"] = price
```

Beispiel:

```python
node["market_price"] = 80.0
node.save()
```

Nicht Teil der ersten Version:

- `market_prices = {year: price}` auf einem einzelnen Node,
- separate cap/op Preise auf Nodes,
- cost improvement factors,
- waehrungsspezifische Metadaten,
- automatische Discount-Konfiguration.

Die Zeitabhaengigkeit kommt stattdessen aus den verschiedenen premise Background-
Datenbanken und der bestehenden `mapping`-Interpolation.

Checkliste:

- [x] Attributname `market_price` festlegen.
- [x] Format `node["market_price"] = float` dokumentieren.
- [x] Preisattribute auf zeitspezifischen Background-Nodes dokumentieren.
- [x] Keine weiteren Preisformate in der Minimalversion unterstuetzen.

### Schritt 5.2: Helper fuer User Input bereitstellen

Datei:

```text
src/optimex/economics.py
```

Ziel:

Der User soll Preise komfortabel als Tabelle bzw. Liste von Records eingeben
koennen:

```text
process/name, location, year, price
```

Optional bei mehrdeutigen Brightway-Lookups:

```text
product/reference product
unit
```

Wichtig:

```text
Brightway `code` wird bewusst nicht als zeitreihenuebergreifender Identifier
verwendet. In premise-generierten zeitspezifischen Datenbanken koennen
inhaltlich gleiche Activities in unterschiedlichen Jahren unterschiedliche
`code`- und `id`-Werte haben. Fuer Preiszeitreihen ueber mehrere premise-
Datenbanken ist `code` daher nicht robust genug.
```

Die Helper-Funktion schreibt daraus automatisch:

```python
node["market_price"] = price
node.save()
```

auf den passenden Background-Node in der passenden zeitspezifischen Background-
Datenbank.

Vorgeschlagene Funktion:

```python
def set_market_prices(
    price_data,
    background_databases: dict[int, str],
    name_col: str = "name",
    year_col: str = "year",
    price_col: str = "price",
    location_col: str | None = "location",
    product_col: str | None = None,
    unit_col: str | None = None,
    price_attribute: str = "market_price",
    overwrite: bool = True,
    strict: bool = True,
) -> None:
    ...
```

`price_data` sollte mindestens unterstuetzen:

- `list[dict]`
- `pandas.DataFrame`

Beispiel mit `list[dict]`:

```python
price_data = [
    {
        "name": "market for electricity, medium voltage",
        "location": "RER",
        "product": "electricity, medium voltage",
        "unit": "kilowatt hour",
        "year": 2020,
        "price": 90.0,
    },
    {
        "name": "market for electricity, medium voltage",
        "location": "RER",
        "product": "electricity, medium voltage",
        "unit": "kilowatt hour",
        "year": 2030,
        "price": 70.0,
    },
]
```

Beispiel mit DataFrame:

```python
prices = pd.DataFrame(price_data)
set_market_prices(prices, background_databases=background_databases)
```

Interne Logik:

```text
for row in price_data:
    year = row[year_col]
    db_name = background_databases[year]
    node = bd.get_node(
        database=db_name,
        name=row[name_col],
        location=row[location_col],
        product=row[product_col],  # only if product_col is provided
        unit=row[unit_col],  # only if unit_col is provided
    )
    node[price_attribute] = row[price_col]
    node.save()
```

Verhalten:

- `strict=True`: Fehler werfen, wenn Jahr, Datenbank oder Node nicht gefunden wird.
- `strict=False`: Warnung loggen und mit der naechsten Zeile fortfahren.
- `overwrite=False`: vorhandene `market_price` Attribute nicht ueberschreiben.
- `product_col`: optionaler Disambiguator fuer Activities mit gleichem Namen
  und gleicher Location, aber unterschiedlichem Produkt bzw. unterschiedlicher Einheit.
- `unit_col`: optionaler Disambiguator fuer Activities mit gleichem Namen,
  gleicher Location und gleichem Produkt, aber unterschiedlicher Einheit.

Warum dieser Helper wichtig ist:

```text
Methodisch liegen Preise sauber auf den zeitspezifischen Background-Nodes.
Praktisch muss der User aber nur eine einfache Tabelle mit process, year, price liefern.
```

Checkliste:

- [x] Neue Datei `src/optimex/economics.py` anlegen.
- [x] `set_market_prices()` implementieren.
- [x] `list[dict]` Input unterstuetzen.
- [x] `pandas.DataFrame` Input unterstuetzen.
- [x] Lookup ueber Name und Location verwenden.
- [x] Optionalen Product-Lookup zur Disambiguierung unterstuetzen.
- [x] Optionalen Unit-Lookup zur Disambiguierung unterstuetzen.
- [x] Dokumentieren, dass Brightway `code` ueber premise-Datenbanken hinweg nicht stabil genug ist.
- [x] `background_databases={year: db_name}` verwenden.
- [x] `market_price` auf korrekten Background-Node schreiben.
- [x] `strict` und `overwrite` Verhalten definieren.
- [x] Tests fuer Helper schreiben.
- [x] In ReadTheDocs dokumentieren.

### Schritt 5.3: `LCADataProcessor` um interne Kosten-Dicts erweitern

Datei:

```text
src/optimex/lca_processor.py
```

In `LCADataProcessor.__init__` ergaenzen:

```python
self._background_costs = {}
self._intermediate_costs_cap = {}
self._intermediate_costs_op = {}
```

Properties ergaenzen:

```python
@property
def background_costs(self) -> dict:
    return self._background_costs

@property
def intermediate_costs_cap(self) -> dict:
    return self._intermediate_costs_cap

@property
def intermediate_costs_op(self) -> dict:
    return self._intermediate_costs_op
```

Checkliste:

- [x] Interne Dicts in `__init__` anlegen:
  - `_background_costs`
  - `_intermediate_costs_cap`
  - `_intermediate_costs_op`
- [x] Read-only Properties ergaenzen.

### Schritt 5.4: Merken, welche Intermediate Flows cap/op-relevant sind

Datei:

```text
src/optimex/lca_processor.py
```

Geeignete Stelle:

In `_construct_foreground_tensors()` im Block fuer externe Intermediate-Flows:

```python
elif edge_type == bd.labels.consumption_edge_default:
    if input_db == self.foreground_db.name:
        ...
    else:
        # External intermediate: background consumption
        ...
        self._intermediate_flows.setdefault(input_code, input_name)
```

Beim Durchlaufen der Foreground-Edges sollte gemerkt werden, ob ein
Intermediate Flow ueber mindestens eine operation Edge oder mindestens eine
non-operation Edge vorkommt.

```python
if exc.get("operation"):
    self._cost_relevant_op_flows.add(input_code)
else:
    self._cost_relevant_cap_flows.add(input_code)
```

Diese Sets koennen intern in `__init__` angelegt werden:

```python
self._cost_relevant_cap_flows = set()
self._cost_relevant_op_flows = set()
```

Checkliste:

- [x] Interne Sets fuer cap/op-relevante Intermediate Flows anlegen.
- [x] Nur externe Background-Inputs beruecksichtigen.
- [x] `operation=True` Edge markiert Flow als op-relevant.
- [x] Edge ohne `operation=True` markiert Flow als cap-relevant.
- [x] Interne Foreground-Produkte und Biosphere-Flows nicht bepreisen.

### Schritt 5.5: `market_price` aus allen zeitspezifischen Background-Datenbanken lesen

Datei:

```text
src/optimex/lca_processor.py
```

Neue Hilfslogik, nachdem `self._intermediate_flows` bekannt ist und bevor die
finalen `intermediate_costs_*` an den Converter gehen.

Prinzip:

```python
for db_name in self.background_dbs:
    db = bd.Database(db_name)
    for flow_code in self._intermediate_flows:
        try:
            activity = db.get(code=flow_code)
        except Exception:
            logger.warning(...)
            continue

        price = activity.get("market_price")
        if price is not None:
            self._background_costs[(db_name, flow_code)] = price
```

Bedeutung:

```text
background_costs[(bkg, i)] = Preis des Background-Produkts i in Background-DB bkg
```

Wichtig:

- Es wird nicht nur der 2020-Node gelesen.
- `flow_code` bleibt der stabile interne `INTERMEDIATE_FLOW` Key aus dem
  Foreground-Edge.
- Um die bestehende optimex-Logik nicht zu veraendern, wird der Preis zunaechst
  ueber denselben Code gelesen, den auch die Background-Inventory-Logik nutzt.
- Wenn premise aequivalenten Activities in verschiedenen Jahren unterschiedliche
  Codes gibt, nutzt nur die Kostenlogik einen Fallback ueber gespeicherte
  Metadaten: `name`, `location`, `product/reference product` und `unit`.
- Die Background-Inventory-Logik bleibt davon unberuehrt.
- Fehlende `market_price` Attribute fuer kostenrelevante Intermediate Flows
  muessen mindestens eine Warnung erzeugen.
- Fehlende Preise bedeuten spaeter effektiv Preis 0 und koennen Ergebnisse
  verfaelschen, wenn der User sie versehentlich vergessen hat.
- Eine spaetere strengere Coverage-Validierung kann fehlende Preise optional als
  Fehler behandeln.

Checkliste:

- [x] Neue Hilfsfunktion oder Logik fuer `_background_costs` ergaenzen.
- [x] Fuer jede Background-DB nach `flow_code` suchen.
- [x] `market_price` lesen.
- [x] Fehlende Nodes oder Preise mit Warnung behandeln.
- [x] In Warnungen klar nennen:
  - Background-DB
  - Flow-Code
  - Flow-Name, falls verfuegbar
  - ob der Flow cap- und/oder op-relevant ist
- [x] Keine rekursive Background-Kostenrechnung durchfuehren.

### Schritt 5.6: Background-Kosten ueber `mapping` auf Systemzeit interpolieren

Datei:

```text
src/optimex/lca_processor.py
```

Nachdem `self._mapping` erstellt wurde, koennen die finalen
`intermediate_costs_cap` und `intermediate_costs_op` berechnet werden.

Formel:

```text
intermediate_price[i,t] =
    sum_bkg background_costs[bkg,i] * mapping[bkg,t]
```

Vorgeschlagene Logik:

```python
for flow_code in self._intermediate_flows:
    for year in self._system_time:
        interpolated_price = sum(
            self._background_costs.get((db_name, flow_code), 0)
            * self._mapping.get((db_name, year), 0)
            for db_name in self.background_dbs
        )

        if flow_code in self._cost_relevant_cap_flows:
            self._intermediate_costs_cap[(flow_code, year)] = interpolated_price

        if flow_code in self._cost_relevant_op_flows:
            self._intermediate_costs_op[(flow_code, year)] = interpolated_price
```

Wichtig:

- Die cap/op-Zuordnung kommt aus der Foreground-Edge.
- Der Preis kommt aus dem zeitspezifischen Background-Node.
- Die Zeitinterpolation kommt aus der bestehenden `mapping`-Matrix.

Checkliste:

- [x] Interpolierte Preise pro `(flow_code, year)` berechnen.
- [x] Cap-relevante Flows in `intermediate_costs_cap` schreiben.
- [x] Op-relevante Flows in `intermediate_costs_op` schreiben.
- [x] Bestehende `mapping`-Matrix wiederverwenden.
- [ ] Verhalten bei fehlenden Preisen dokumentieren: Fehlende `market_price`
  Attribute erzeugen beim Preislesen eine Warnung; fehlende
  `background_costs[(db, flow)]` gehen in der Interpolation mit 0 ein.

### Schritt 5.7: Kostenfelder im Converter aus dem LCA Processor uebernehmen

Datei:

```text
src/optimex/converter.py
```

In `ModelInputManager.parse_from_lca_processor()` beim Erzeugen der
`OptimizationModelInputs` ergaenzen:

```python
"intermediate_costs_cap": (
    lca_processor.intermediate_costs_cap
    if lca_processor.intermediate_costs_cap
    else None
),
"intermediate_costs_op": (
    lca_processor.intermediate_costs_op
    if lca_processor.intermediate_costs_op
    else None
),
"discount_rate": None,
"discount_reference_year": None,
```

Hinweis:

`discount_rate` und `discount_reference_year` bleiben erstmal manuelle
Szenarioannahmen auf `model_inputs`. Sie werden nicht aus Brightway-Nodes
ausgelesen.

Checkliste:

- [x] `intermediate_costs_cap` aus `lca_processor` uebernehmen.
- [x] `intermediate_costs_op` aus `lca_processor` uebernehmen.
- [x] Leere Kosten-Dicts als `None` uebergeben.
- [x] `discount_rate` und `discount_reference_year` mit `None` initialisieren.

### Schritt 5.8: Tests fuer Pipeline-Integration

Testdatei:

```text
tests/test_economics.py
```

Umgesetzte Teststruktur:

```text
1. Helper-Tests fuer set_market_prices()
2. Pipeline-Tests fuer set_market_prices -> LCADataProcessor -> ModelInputManager
```

Getestete Helper-Faelle:

- `list[dict]` Input schreibt `market_price`.
- `pandas.DataFrame` Input schreibt `market_price`.
- Custom Column Names funktionieren.
- `overwrite=False` schuetzt vorhandene Preise.
- Fehlendes Jahr wirft bei `strict=True`.
- Fehlender Node wirft bei `strict=True`.

Getestete Pipeline-Faelle:

- Background-Nodes mit gleichem Code in mehreren zeitspezifischen Background-
  Datenbanken anlegen.
- Background-Nodes mit unterschiedlichem Code, aber gleicher Activity-Identitaet
  anlegen und pruefen, dass der Kosten-Lookup ueber Metadaten funktioniert.
- `set_market_prices()` schreibt `market_price` auf diese Nodes.
- Foreground-Prozess konsumiert den 2020-Referenznode ueber eine construction Edge.
- Foreground-Prozess konsumiert einen 2020-Referenznode ueber eine operation Edge.
- `LCADataProcessor` ausfuehren.
- Pruefen:

```python
lca_data.background_costs[(db_2020, flow_code)] == price_2020
lca_data.background_costs[(db_2030, flow_code)] == price_2030
lca_data.intermediate_costs_cap[(construction_flow_code, year)] == interpolated_price
lca_data.intermediate_costs_op[(operation_flow_code, year)] == interpolated_price
```

Dann:

```python
manager = converter.ModelInputManager()
model_inputs = manager.parse_from_lca_processor(lca_data)
```

Pruefen:

```python
model_inputs.intermediate_costs_cap[(flow_code, year)] == interpolated_price
model_inputs.intermediate_costs_op[(flow_code, year)] == interpolated_price
```

Checkliste:

- [x] Test fuer Extraktion aus zeitspezifischen Background-Nodes.
- [x] Test fuer Interpolation ueber `mapping`.
- [x] Test fuer Zuordnung anhand von `operation=True`.
- [x] Test fuer Uebergabe in `OptimizationModelInputs`.
- [x] Test fuer fehlende `market_price`: Warnung wird ausgegeben.

## Schritt 6: `create_model` API erweitern

Datei:

```text
src/optimex/optimizer.py
```

Signatur erweitern:

```python
def create_model(
    inputs: OptimizationModelInputs,
    name: str,
    objective_category: str,
    debug_path: str = None,
    objective: str = "environmental",
) -> pyo.ConcreteModel:
```

Direkt nach Modell-Erzeugung:

```python
if objective not in {"environmental", "cost"}:
    raise ValueError(
        f"Unknown objective '{objective}'. Expected 'environmental' or 'cost'."
    )

model._objective = objective
model._objective_category = objective_category
```

Checkliste:

- [x] Neues Argument `objective` mit Default `"environmental"`.
- [x] Validierung fuer erlaubte Werte.
- [x] Rueckwaertskompatibilitaet erhalten.

## Schritt 7: Kosten-Parameter in Pyomo anlegen

Datei:

```text
src/optimex/optimizer.py
```

In `create_model()` bei den Parametern ergaenzen:

Wichtig:

```text
intermediate_costs_cap/op sind bereits im LCADataProcessor auf SYSTEM_TIME
interpoliert. Im Optimizer duerfen sie nicht erneut ueber BACKGROUND_ID und
mapping gewichtet werden.
```

```python
model.intermediate_costs_cap = pyo.Param(
    model.INTERMEDIATE_FLOW,
    model.SYSTEM_TIME,
    within=pyo.Reals,
    default=0,
    initialize=(
        scaled_inputs.intermediate_costs_cap
        if scaled_inputs.intermediate_costs_cap is not None
        else {}
    ),
)

model.intermediate_costs_op = pyo.Param(
    model.INTERMEDIATE_FLOW,
    model.SYSTEM_TIME,
    within=pyo.Reals,
    default=0,
    initialize=(
        scaled_inputs.intermediate_costs_op
        if scaled_inputs.intermediate_costs_op is not None
        else {}
    ),
)
```

Diskontierung:

```python
discount_reference_year = (
    scaled_inputs.discount_reference_year
    if scaled_inputs.discount_reference_year is not None
    else min(scaled_inputs.SYSTEM_TIME)
)

model.discount_rate = pyo.Param(
    within=pyo.NonNegativeReals,
    default=0,
    initialize=scaled_inputs.discount_rate or 0,
)

model.discount_reference_year = pyo.Param(
    within=pyo.Reals,
    initialize=discount_reference_year,
)
```

Checkliste:

- [x] `intermediate_costs_cap` Param.
- [x] `intermediate_costs_op` Param.
- [x] `discount_rate` Param.
- [x] `discount_reference_year` Param.
- [x] Defaults auf 0 bzw. `min(SYSTEM_TIME)`.

## Schritt 8: Background-Purchase Expressions bauen

Datei:

```text
src/optimex/optimizer.py
```

Guter Ort: nach `model.total_intermediate_flow`.

```python
def background_purchase_cap_rule(model, i, t):
    fg_scale = model.scales["foreground"]
    return fg_scale * sum(
        model.scaled_technosphere_dependent_on_installation[p, i, t]
        for p in model.PROCESS
    )

model.background_purchase_cap = pyo.Expression(
    model.INTERMEDIATE_FLOW,
    model.SYSTEM_TIME,
    rule=background_purchase_cap_rule,
)
```

```python
def background_purchase_op_rule(model, i, t):
    fg_scale = model.scales["foreground"]
    return fg_scale * sum(
        model.scaled_technosphere_dependent_on_operation[p, i, t]
        for p in model.PROCESS
    )

model.background_purchase_op = pyo.Expression(
    model.INTERMEDIATE_FLOW,
    model.SYSTEM_TIME,
    rule=background_purchase_op_rule,
)
```

Checkliste:

- [x] `background_purchase_cap[i,t]` in realen Einheiten.
- [x] `background_purchase_op[i,t]` in realen Einheiten.
- [x] `fg_scale` korrekt angewendet.

## Schritt 9: Kosten-Expressions bauen

Datei:

```text
src/optimex/optimizer.py
```

```python
def discount_factor_rule(model, t):
    return 1 / ((1 + model.discount_rate) ** (t - model.discount_reference_year))

model.discount_factor = pyo.Expression(
    model.SYSTEM_TIME,
    rule=discount_factor_rule,
)
```

```python
def cost_cap_rule(model, t):
    return sum(
        model.intermediate_costs_cap[i, t]
        * model.background_purchase_cap[i, t]
        for i in model.INTERMEDIATE_FLOW
    )

model.cost_cap = pyo.Expression(
    model.SYSTEM_TIME,
    rule=cost_cap_rule,
)
```

```python
def cost_op_rule(model, t):
    return sum(
        model.intermediate_costs_op[i, t]
        * model.background_purchase_op[i, t]
        for i in model.INTERMEDIATE_FLOW
    )

model.cost_op = pyo.Expression(
    model.SYSTEM_TIME,
    rule=cost_op_rule,
)
```

```python
def total_cost_rule(model):
    return sum(
        model.discount_factor[t] * (model.cost_cap[t] + model.cost_op[t])
        for t in model.SYSTEM_TIME
    )

model.total_cost = pyo.Expression(rule=total_cost_rule)
```

Checkliste:

- [x] `discount_factor[t]`.
- [x] `cost_cap[t]`.
- [x] `cost_op[t]`.
- [x] `total_cost`.
- [x] Test mit `discount_rate = 0`.
- [x] Test mit `discount_rate > 0`.

## Schritt 10: Objective-Switch einfuehren

Datei:

```text
src/optimex/optimizer.py
```

Aktuelle Objective-Funktion ersetzen:

```python
def objective_function(model):
    if model._objective == "environmental":
        return model.total_impact[model._objective_category]
    if model._objective == "cost":
        return model.total_cost
    raise ValueError(f"Unknown objective: {model._objective}")
```

`model.OBJ` bleibt:

```python
model.OBJ = pyo.Objective(sense=pyo.minimize, rule=objective_function)
```

Checkliste:

- [x] `objective="environmental"` verhaelt sich wie vorher.
- [x] `objective="cost"` minimiert `model.total_cost`.
- [x] Unbekanntes Objective wirft `ValueError`.

## Schritt 11: `solve_model` Denormalisierung anpassen

Datei:

```text
src/optimex/optimizer.py
```

In `solve_model()` wird der Objective-Wert fuer Environmental Objective
zurueckskaliert. Fuer Cost Objective darf das nicht passieren.

Neue Logik:

```python
if getattr(model, "_objective", "environmental") == "cost":
    true_obj = pyo.value(model.OBJ)
else:
    # bisherige environmental denormalization
```

Checkliste:

- [x] Cost Objective wird nicht mit Foreground- oder Charakterisierungsskalen multipliziert.
- [x] Environmental Objective bleibt unveraendert.

## Schritt 12: Tests fuer Optimizer-Integration

Bisher bereits abgedeckt:

```text
- Serialization der neuen Kostenfelder
- `set_market_prices()` Helper
- Preisextraktion aus Background-Nodes
- Interpolation ueber `mapping`
- Uebergabe in `OptimizationModelInputs`
- Cost Expressions:
  - `background_purchase_cap`
  - `background_purchase_op`
  - `cost_cap`
  - `cost_op`
  - `discount_factor`
  - `total_cost`
```

Weitere Tests sollten in:

```text
tests/test_economics.py
```

ergaenzt werden.

Solverbasierte Tests sollen bevorzugt mit HiGHS laufen:

```python
solver_name = "highs"
```

Falls HiGHS in einer Umgebung nicht verfuegbar ist, sollen die betreffenden Tests
sauber geskippt werden, statt die Testsuite wegen fehlendem Solver scheitern zu
lassen.

Moeglicher Helper:

```python
def require_highs():
    try:
        available = pyo.SolverFactory("highs").available(exception_flag=False)
    except Exception as exc:
        pytest.skip(f"HiGHS solver not available: {exc}")
    if not available:
        pytest.skip("HiGHS solver not available")
    return "highs"
```

### Schritt 12.1: Objective-Switch ohne Solver testen

Ziel:

- Pruefen, dass `objective="environmental"` weiterhin
  `total_impact[objective_category]` nutzt.
- Pruefen, dass `objective="cost"` `total_cost` nutzt.
- Pruefen, dass ein unbekanntes Objective einen `ValueError` wirft.

Diese Tests brauchen keinen Solver.

Checkliste:

- [x] `objective="environmental"` ist Default und bleibt rueckwaertskompatibel.
- [x] `objective="cost"` setzt `model.OBJ` auf `model.total_cost`.
- [x] Ungueltiges Objective wirft `ValueError`.

### Schritt 12.2: Cost Objective waehlt guenstigere Route

Ziel:

- Zwei Prozesse koennen dieselbe Nachfrage erfuellen.
- Prozess A ist teurer.
- Prozess B ist guenstiger.
- Bei `objective="cost"` wird Prozess B gewaehlt.

Dieser Test braucht einen Solver. HiGHS soll verwendet werden.

Checkliste:

- [x] Einfaches Zwei-Routen-System bauen.
- [x] Kosten so setzen, dass eine Route eindeutig guenstiger ist.
- [x] Modell mit `objective="cost"` und `solver_name="highs"` loesen.
- [x] Pruefen, dass die guenstige Route genutzt wird.

### Schritt 12.3: Cost Objective mit Umweltbudget testen

Ziel:

- Guenstige Route ist umweltschaedlicher.
- Teurere Route ist sauberer.
- Ohne Umweltbudget waehlt das Modell die guenstige Route.
- Mit `cumulative_category_impact_limits` muss das Modell die sauberere Route
  waehlen.

Dieser Test braucht einen Solver. HiGHS soll verwendet werden.

Checkliste:

- [x] Zwei-Routen-System mit unterschiedlichem Impact bauen.
- [x] Kostenobjective ohne Budget testen.
- [x] Kostenobjective mit Impact-Budget testen.
- [x] Pruefen, dass Environmental Constraints weiterhin bei Cost Objective wirken.

### Schritt 12.4: `solve_model()` Denormalisierung testen

Ziel:

- Bei `objective="environmental"` wird der Objective-Wert wie bisher
  denormalisiert.
- Bei `objective="cost"` wird der Objective-Wert nicht mit `fg_scale` oder
  Charakterisierungsskalen multipliziert.

Dieser Test braucht einen Solver. HiGHS soll verwendet werden.

Checkliste:

- [x] Environmental Objective liefert realen Impact.
- [x] Cost Objective liefert reale Kosten.
- [x] Cost Objective wird nicht doppelt skaliert.

### Schritt 12.5: Backward Compatibility testen

Ziel:

- Bestehende Aufrufe ohne `objective` funktionieren weiterhin.
- Bestehende Environmental-Optimierung bleibt unveraendert.

Checkliste:

- [x] `create_model(inputs, name, objective_category)` funktioniert.
- [x] Default ist `objective="environmental"`.
- [ ] Bestehende Tests bleiben gruen.

## Schritt 13: API- und Feature-Dokumentation vervollstaendigen

Status:

```text
abgeschlossen
```

Die grundlegende ReadTheDocs-Seite existiert bereits:

```text
docs/content/economic_optimization.md
```

Sie dokumentiert bisher vor allem:

- node-basierte Preisdefinition ueber `market_price`,
- `set_market_prices()`,
- Lookup ueber `name`, `location` und optional `product`, `unit`,
- premise/code-Problematik fuer Preiszeitreihen,
- CAPEX/OPEX-artige Accounting-Trennung ueber das `operation` Edge-Attribut.

Ziel dieses Schritts:

Die bereits vorhandene Seite und ggf. API-nahe Dokumentation so erweitern, dass
das implementierte Feature als Optimex-Funktion vollstaendig verstaendlich ist.

Dokumentierte Punkte:

- [x] `objective="environmental"` als rueckwaertskompatibler Default.
- [x] `objective="cost"` als neue Objective-Auswahl.
- [x] `intermediate_costs_cap`.
- [x] `intermediate_costs_op`.
- [x] `discount_rate`.
- [x] `discount_reference_year`.
- [x] First-level Background Pricing.
- [x] Keine rekursive Background-Kostenrechnung.
- [x] CAPEX/OPEX-artige Accounting-Trennung.
- [x] Ergebnisgroessen:
  - `model.cost_cap[t]`,
  - `model.cost_op[t]`,
  - `model.discount_factor[t]`,
  - `model.total_cost`.
- [x] Scaling-Hinweis:
  Preise sind reale Preise; die gekauften Background-Mengen werden fuer die
  Kostenberechnung wieder in reale Einheiten gebracht.
- [x] Zusammenspiel mit Umweltconstraints:
  `objective="cost"` kann mit `category_impact_limits` und
  `cumulative_category_impact_limits` kombiniert werden.

Moegliche Dateien:

```text
docs/content/economic_optimization.md
docs/api/optimizer.md
docs/content/optimization_setup.md
docs/content/constraints.md
```

Methodischer Textvorschlag:

```text
Costs are applied only to first-level background purchases directly required by
the foreground system. They are not recursively applied to upstream products
inside the background inventory. The upstream background system remains relevant
for environmental impacts, while economic costs are represented by time-specific
market prices for direct background products.
```

## Schritt 14: ReadTheDocs-Seite fuer Economic Optimization finalisieren

Status:

```text
begonnen
```

Datei:

```text
docs/content/economic_optimization.md
```

Ziel:

Die oekonomische Erweiterung soll nicht nur im Code existieren, sondern als
vollwertiger Teil von `optimex` erklaert werden. Die Seite sollte so geschrieben
sein, dass neue Nutzerinnen und Nutzer verstehen:

- welches Kostenkonzept verwendet wird,
- welche Daten sie angeben muessen,
- wie sie eine Kostenoptimierung starten,
- wie sie CAPEX/OPEX-artige Ergebnisse interpretieren,
- wie Kostenoptimierung mit Umweltconstraints kombiniert wird.

Empfohlene Struktur:

```markdown
# Economic Optimization

## Overview

Short explanation of cost optimization in optimex.

## Concept

Explain first-level background purchases:

- Costs are applied only to direct background products bought by the foreground system.
- Internal foreground products are not priced.
- Upstream background processes are not priced recursively.
- Background inventories remain relevant for environmental impacts.

## Mathematical Formulation

Introduce:

- p_cap
- p_op
- c_cap
- c_op
- discount_factor
- total_cost

## CAPEX/OPEX Accounting

Explain that cap/op is an accounting distinction:

- non-operational edges contribute to installation-related purchases,
- operation=True edges contribute to operation-related purchases,
- c_cap and c_op may contain identical market prices,
- separation enables reporting and interpretation.

## Input Fields

Document:

- intermediate_costs_cap
- intermediate_costs_op
- discount_rate
- discount_reference_year

## Creating a Cost Optimization Model

Show code with objective="cost".

## Combining Cost Optimization with Environmental Constraints

Show code with cumulative_category_impact_limits.

## Interpreting Results

Explain:

- model.cost_cap[t]
- model.cost_op[t]
- model.discount_factor[t]
- model.total_cost

## Notes on Scaling

Explain that prices are real prices and background purchases are converted back
to real units before costs are calculated.
```

Checkliste:

- [x] Neue Seite `docs/content/economic_optimization.md` anlegen.
- [x] Konzept first-level pricing erklaeren.
- [x] Mathematische Formulierung aufnehmen:
  - `background_purchase_cap`,
  - `background_purchase_op`,
  - `cost_cap`,
  - `cost_op`,
  - `discount_factor`,
  - `total_cost`.
- [x] CAPEX/OPEX Accounting sauber einordnen.
- [x] Input-Felder dokumentieren:
  - `intermediate_costs_cap`,
  - `intermediate_costs_op`,
  - `discount_rate`,
  - `discount_reference_year`.
- [x] User-Input ueber `set_market_prices()` dokumentieren.
- [x] Node-Lookup ueber `name`, `location`, optional `product`, `unit`
  dokumentieren.
- [x] Codebeispiel fuer `objective="cost"` ergaenzen.
- [x] Codebeispiel fuer Kostenoptimierung mit Umweltbudget ergaenzen.
- [x] Ergebnisinterpretation dokumentieren.
- [x] Scaling-Hinweis aufnehmen.
- [ ] Hinweis aufnehmen, dass die Seite den aktuellen Stand der
  Implementierung beschreibt und spaeter ggf. um ein ausfuehrliches Beispiel
  erweitert wird.

## Schritt 15: Navigation der Dokumentation erweitern

Pruefen, wo die ReadTheDocs-Navigation konfiguriert ist.

Wahrscheinliche Datei:

```text
mkdocs.yml
```

Falls es keine explizite Navigation gibt, pruefen, ob `docs/index.md` oder eine
andere Strukturdatei angepasst werden muss.

Ziel:

Die neue Seite soll in der Dokumentation sichtbar sein, z. B. unter:

```text
User Guide
  - Optimization Setup
  - Constraints
  - Economic Optimization
```

Checkliste:

- [ ] Navigationsdatei finden.
- [ ] `economic_optimization.md` in die Navigation aufnehmen.
- [ ] Link von `optimization_setup.md` zur neuen Seite setzen.
- [ ] Link von `constraints.md` zur neuen Seite setzen, falls passend.

## Schritt 16: `optimization_setup.md` erweitern

Datei:

```text
docs/content/optimization_setup.md
```

Neue oder erweiterte Abschnitte:

```text
Choosing the objective
Environmental objective
Cost objective
```

Erklaeren:

```python
model = optimizer.create_model(
    model_inputs,
    name="my_model",
    objective_category="climate_change",
    objective="environmental",
)
```

und:

```python
model = optimizer.create_model(
    model_inputs,
    name="cost_model",
    objective_category="climate_change",
    objective="cost",
)
```

Wichtig:

`objective_category` bleibt auch bei `objective="cost"` relevant, weil
Impact-Kategorien weiterhin fuer Umweltconstraints und Reporting verwendet
werden.

Checkliste:

- [ ] Objective-Auswahl dokumentieren.
- [ ] Default `"environmental"` erklaeren.
- [ ] `"cost"` Objective erklaeren.
- [ ] Hinweis zu `objective_category` bei Kostenoptimierung aufnehmen.

## Schritt 17: `constraints.md` erweitern

Datei:

```text
docs/content/constraints.md
```

Ergaenzen:

```text
Environmental constraints can also be used with cost optimization.
```

Beispiel:

```python
model_inputs.cumulative_category_impact_limits = {
    "climate_change": 5000000,
}

model = optimizer.create_model(
    model_inputs,
    name="least_cost_with_carbon_budget",
    objective_category="climate_change",
    objective="cost",
)
```

Erklaerung:

```text
This minimizes total discounted cost while requiring the system to remain within
the specified cumulative climate budget.
```

Checkliste:

- [ ] Abschnitt zu Cost Objective mit Environmental Constraints ergaenzen.
- [ ] Beispiel fuer kumulatives Umweltbudget aufnehmen.
- [ ] Klarstellen, dass bestehende Constraints unveraendert funktionieren.

## Schritt 18: API-Dokumentation aktualisieren

Datei:

```text
docs/api/optimizer.md
```

Ergaenzen:

- `create_model()` unterstuetzt `objective="environmental"` und
  `objective="cost"`.
- `solve_model()` gibt bei Cost Objective einen nicht-denormalisierten
  Kostenwert in realen Geldeinheiten zurueck.
- Kosten-Expressions:
  - `background_purchase_cap`
  - `background_purchase_op`
  - `cost_cap`
  - `cost_op`
  - `total_cost`

Checkliste:

- [ ] API-Seite auf neue Objective-Auswahl pruefen.
- [ ] Kurzen erklaerenden Abschnitt zu Kostenobjective einfuegen.
- [ ] Rueckwaertskompatibilitaet des Defaults erwaehnen.

## Schritt 19: Vollstaendiges Economic-Optimization-Beispiel ergaenzen

Dieser Schritt wurde vorgezogen, um vor der weiteren Dokumentation zuerst einen
End-to-End-Test an einem realistischeren Beispiel zu haben.

Erste Umsetzung als Notebook:

```text
notebooks/methanol_and_iron_cost.ipynb
```

Ziel:

Ein durchgaengiges Beispiel auf Basis von `notebooks/methanol_and_iron.ipynb`,
das zeigt:

- Kostenpreise werden auf zeitspezifische Background-Nodes geschrieben,
- `LCADataProcessor` liest und interpoliert diese Preise,
- `OptimizationModelInputs` enthaelt `intermediate_costs_cap/op`,
- `create_model(..., objective="cost")` baut das Cost Objective,
- `solve_model(..., solver_name="highs")` loest das Modell,
- CAPEX/OPEX-artige Kosten koennen nach Jahr ausgewertet werden.

Nicht im ersten Notebook-Ziel:

- finale wissenschaftliche Preisdatengrundlage,
- ReadTheDocs-Beispieltext,
- Umweltbudget-Vergleich.

Spaeter kann daraus zusaetzlich eine kurze ReadTheDocs-Beispielseite entstehen:

```text
docs/content/examples/economic_optimization.md
```

Moegliche Doku-Story:

- zwei Technologien koennen dieselbe Nachfrage bedienen,
- `objective="cost"` waehlt die guenstigere Option,
- ein Umweltbudget kann die Entscheidung veraendern,
- CAPEX/OPEX-artige Kosten koennen ausgewertet werden.

Empfohlene Struktur:

```markdown
# Economic Optimization Example

## Scenario

Short description of the system.

## Define Cost Data

Show intermediate_costs_cap and intermediate_costs_op.

## Create and Solve Cost Model

Show create_model(..., objective="cost").

## Inspect Cost Results

Show cost_cap, cost_op, total_cost.

## Add Environmental Budget

Show cumulative_category_impact_limits.

## Compare Results

Explain how the chosen pathway changes.
```

Checkliste:

- [x] Methanol/Iron-Beispiel als eigenes Cost-Notebook kopieren/adaptieren.
- [x] Illustrative Preisannahmen auf Background-Nodes schreiben.
- [x] LCAProcessor nach dem Schreiben der Preise ausfuehren.
- [x] Cost Objective mit `objective="cost"` anlegen.
- [x] HiGHS als Solver im Notebook verwenden.
- [x] Ergebniszellen fuer `total_cost`, `cost_cap` und `cost_op` ergaenzen.
- [ ] Notebook lokal vollstaendig ausfuehren und Ergebnis pruefen.
- [ ] Ergebnisinterpretation aufnehmen.
- [ ] In Beispiele-Navigation verlinken.

## Schritt 20: Dokumentation lokal bauen und pruefen

Ziel:

Vor dem Abschluss sollte die Dokumentation lokal gebaut und visuell geprueft
werden.

Moegliche Checks:

```text
mkdocs build
mkdocs serve
```

Pruefen:

- [ ] Navigation enthaelt neue Seite.
- [ ] Codebloecke rendern korrekt.
- [ ] Mathematische Formeln rendern korrekt.
- [ ] Links funktionieren.
- [ ] Begriffe sind konsistent:
  - first-level background purchases
  - installation-related costs
  - operation-related costs
  - cost objective
  - environmental objective
- [ ] Keine ueberholten Hinweise auf nur eine Objective-Art.

## Optional fuer spaeter

Diese Punkte gehoeren nicht zur Minimalimplementierung, sollten aber als
moegliche Weiterentwicklung festgehalten werden.

### Optionales Cost Objective Scaling

Motivation:

Die Preise sollen in der ersten Implementierung nicht skaliert werden. Stattdessen
werden die skalierten Background-Mengen im Optimizer wieder in reale Mengen
zurueckgerechnet:

```text
real_background_purchase = fg_scale * scaled_background_purchase
```

Damit gilt:

```text
cost = real_price * real_background_purchase
```

Das ist fuer Interpretation, Tests und Dokumentation am klarsten, weil:

- Kostenpreise echte Marktpreise bleiben,
- Background-Kaeufe echte physische Mengen sind,
- `cost_cap`, `cost_op` und `total_cost` echte Geldeinheiten haben.

Falls sich spaeter zeigt, dass sehr grosse Kostenwerte numerische Probleme im
Solver verursachen, kann ein separates Objective Scaling eingefuehrt werden.

Moegliche spaetere Erweiterung:

```python
cost_scale = 1_000_000
model.total_cost_scaled = model.total_cost / cost_scale
```

Dann koennte der Solver minimieren:

```python
model.total_cost_scaled
```

waehrend Reporting und Postprocessing weiterhin echte Kosten verwenden:

```python
model.total_cost
```

Wichtig:

```text
Nicht die Input-Preise selbst skalieren, sondern optional nur die Objective-
Expression fuer den Solver.
```

Checkliste fuer spaeter:

- [ ] Bedarf fuer Cost Objective Scaling anhand numerischer Probleme pruefen.
- [ ] Optionales Feld `cost_scale` oder automatische Skalierung diskutieren.
- [ ] `total_cost` weiterhin in realen Geldeinheiten halten.
- [ ] Nur die zu minimierende Objective-Expression skalieren.
- [ ] `solve_model()` entsprechend dokumentieren.

### CO2-Preis / Carbon Pricing

Motivation:

Neben Marktpreisen fuer first-level Background-Produkte koennte spaeter ein
CO2-Preis integriert werden. Damit koennen Szenarien modelliert werden, in denen
Treibhausgasemissionen zusaetzliche Kosten verursachen.

Moegliche Modellierungsvarianten:

1. CO2-Preis als zusaetzlicher Kostenanteil auf charakterisierte
   Klimawirkungen:

```text
carbon_cost[t] = carbon_price[t] * time_specific_impact["climate_change", t]
```

2. CO2-Preis direkt auf bestimmte Elementary Flows, z. B. fossiles CO2:

```text
carbon_cost[t] = sum_e carbon_price[e,t] * total_elementary_flow[e,t]
```

3. CO2-Preis als separater Reporting-Posten, ohne ihn direkt in der Objective zu
   minimieren.

Offene Designfragen:

- Soll der CO2-Preis auf charakterisierte CO2-equivalent Impacts angewendet
  werden oder direkt auf einzelne Emissionsfluesse?
- Soll Carbon Pricing Teil von `total_cost` sein oder separat ausgewiesen werden?
- Wie wird Doppelzaehlung vermieden, falls Background-Marktpreise bereits CO2-
  Kosten enthalten?
- Soll der CO2-Preis zeitabhaengig sein?
- Soll Carbon Pricing auch bei `objective="environmental"` berichtet werden?

Checkliste fuer spaeter:

- [ ] Geeignete mathematische Formulierung fuer Carbon Pricing auswaehlen.
- [ ] Datenmodell fuer `carbon_price` definieren.
- [ ] Klaeren, ob Preis auf Impact-Kategorie oder Elementary Flow liegt.
- [ ] Doppelzaehlung mit Marktpreisen dokumentieren.
- [ ] Tests fuer Carbon Pricing ergaenzen.
- [ ] ReadTheDocs-Doku mit eigenem Abschnitt ergaenzen.

### EconomicConfig in LCAConfig

Motivation:

In der Minimalimplementierung wird bei fehlenden Preisen fuer kostenrelevante
Background-Produkte fest eine Warnung ausgegeben. Das schuetzt Nutzerinnen und
Nutzer davor, versehentlich unbezahlte Inputs im Kostenobjective zu erzeugen.

Spaeter kann dieses Verhalten konfigurierbar gemacht werden.

Moegliche Erweiterung:

```python
class EconomicConfig(BaseModel):
    price_attribute: str = "market_price"
    missing_market_price: Literal["warn", "error", "ignore"] = "warn"
```

Dann koennte `LCAConfig` erweitert werden:

```python
class LCAConfig(BaseModel):
    ...
    economic: EconomicConfig = Field(default_factory=EconomicConfig)
```

Moegliche User-API:

```python
config = lca_processor.LCAConfig(
    demand=demand,
    temporal={...},
    characterization_methods=[...],
    economic={
        "price_attribute": "market_price",
        "missing_market_price": "error",
    },
)
```

Moegliche zukuenftige Felder:

- `price_attribute`: Name des Background-Node-Attributs fuer Marktpreise.
- `missing_market_price`: Verhalten bei fehlenden Preisen (`warn`, `error`, `ignore`).
- `currency`: optionale Waehrungsinformation, z. B. `EUR`.
- `price_unit`: optionale Einheit, z. B. `EUR/kWh`.
- `cost_scale`: optionales Objective Scaling fuer numerische Stabilitaet.
- Carbon-pricing-bezogene Felder.

Nicht sofort implementieren:

```text
Fuer die erste Version bleibt das Verhalten fest:
fehlende Preise fuer kostenrelevante Flows erzeugen mindestens eine Warnung.
```

Checkliste fuer spaeter:

- [ ] `EconomicConfig` definieren.
- [ ] `LCAConfig` um `economic` erweitern.
- [ ] `price_attribute` statt hart codiertem `"market_price"` verwenden.
- [ ] `missing_market_price` mit `warn/error/ignore` implementieren.
- [ ] Tests fuer alle Missing-Price-Modi ergaenzen.
- [ ] Doku aktualisieren.

### Postprocessing fuer Kosten

Moegliche spaetere Komfortfunktionen:

```python
extract_costs_by_year(model)
extract_cost_breakdown(model)
extract_capex_opex_summary(model)
```

Ziel:

- Kosten je Jahr auslesen,
- `cost_cap` und `cost_op` vergleichen,
- diskontierte und undiskontierte Kosten ausweisen,
- Kosten nach Background-Flow aufschluesseln.

### Automatische Kostendaten aus Brightway/LCA Processor

In der Minimalversion werden Kostenpreise manuell auf `model_inputs` gesetzt.

Spaeter koennte `lca_processor.py` oder eine eigene Economics-Schicht Preise
automatisch aus:

- Activity- oder Edge-Attributen,
- externen Preiszeitreihen,
- Szenariodateien,
- Datenbanken,

ableiten.

Moegliche spaetere Architektur:

```text
src/optimex/economics.py
src/optimex/objectives.py
```

## Definition of Done fuer ein serienreifes Feature

Das Feature kann als "serienreif" gelten, wenn:

### Code

- [ ] Rueckwaertskompatibler Default `objective="environmental"`.
- [ ] Kostenobjective `objective="cost"` funktioniert.
- [ ] Preise werden nur auf first-level Background-Kaeufe angewendet.
- [ ] Scaling ist korrekt behandelt.
- [ ] Cost Objective wird nicht falsch denormalisiert.

### Tests

- [ ] Serialization-Test fuer neue Kostenfelder.
- [ ] Test fuer cap/op Purchase Split.
- [ ] Test fuer Kostenberechnung.
- [ ] Test fuer Diskontierung.
- [ ] Test fuer Cost Objective.
- [ ] Test fuer Cost Objective mit Umweltconstraint.
- [ ] Backward-Compatibility-Test.

### Dokumentation

- [ ] Neue ReadTheDocs-Seite fuer Economic Optimization.
- [ ] Objective-Auswahl in Optimization Setup dokumentiert.
- [ ] Kombination mit Constraints dokumentiert.
- [ ] API-Dokumentation aktualisiert.
- [ ] Mindestens ein vollstaendiges Beispiel.
- [ ] Dokumentation lokal gebaut und geprueft.

## Empfohlene Arbeitsreihenfolge

1. [ ] `OptimizationModelInputs` Felder ergaenzen.
2. [ ] Parser-Defaults ergaenzen.
3. [ ] Serialization ergaenzen.
4. [ ] Serialization-Test gruen bekommen.
5. [ ] `create_model` Signatur und Objective-Switch ergaenzen.
6. [ ] Kosten-Params ergaenzen.
7. [ ] Background-Purchase Expressions ergaenzen.
8. [ ] Cost-Expressions ergaenzen.
9. [ ] `solve_model` Denormalisierung korrigieren.
10. [ ] Cost-Calculation-Test schreiben.
11. [ ] Cost-Objective-Test schreiben.
12. [ ] Cost Objective mit Environmental Constraint testen.
13. [ ] ReadTheDocs-Seite `economic_optimization.md` schreiben.
14. [ ] Dokumentationsnavigation erweitern.
15. [ ] `optimization_setup.md` erweitern.
16. [ ] `constraints.md` erweitern.
17. [ ] API-Dokumentation aktualisieren.
18. [ ] Beispielseite fuer Economic Optimization ergaenzen.
19. [ ] Dokumentation lokal bauen und pruefen.

## Wichtige Stolperstellen

### Skalierung

`scaled_technosphere_dependent_on_installation` und
`scaled_technosphere_dependent_on_operation` sind skaliert.

Deshalb:

```python
background_purchase_cap/op = fg_scale * scaled_expression
```

Preise bleiben unskaliert.

### Objective-Wert

Environmental Objective wird wie bisher denormalisiert.

Cost Objective wird nicht denormalisiert, weil `total_cost` bereits reale
Geldeinheiten verwendet.

### Interpretation von `c_cap` und `c_op`

Die Preisvektoren koennen identische Marktpreise enthalten. Sie sind getrennt,
um Kosten nach installationsbezogenen und betriebsbezogenen direkten
Background-Einkaeufen auszuweisen.

Die Trennung impliziert nicht zwingend, dass dasselbe Marktprodukt je nach
Verwendung unterschiedliche Preise hat.

### Keine neuen Constraints

Fuer die Minimalversion sind keine neuen Constraints erforderlich.

Kostenoptimierung nutzt die bestehenden physikalischen, zeitlichen und
oekologischen Nebenbedingungen.
