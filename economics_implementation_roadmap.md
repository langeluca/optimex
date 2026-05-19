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

- [ ] `intermediate_costs_cap` bleibt unveraendert.
- [ ] `intermediate_costs_op` bleibt unveraendert.
- [ ] `discount_rate` bleibt unveraendert.
- [ ] `discount_reference_year` bleibt unveraendert.

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

- [ ] `save_inputs()` erweitert.
- [ ] `load_inputs()` erweitert.
- [ ] JSON-Roundtrip-Test ergaenzen.

## Schritt 5: Parser-Defaults setzen

Datei:

```text
src/optimex/converter.py
```

In `ModelInputManager.parse_from_lca_processor()` beim Erzeugen der
`OptimizationModelInputs` ergaenzen:

```python
"intermediate_costs_cap": None,
"intermediate_costs_op": None,
"discount_rate": None,
"discount_reference_year": None,
```

Checkliste:

- [ ] Defaults ergaenzt.
- [ ] Bestehende Parser-Tests laufen weiterhin.

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

- [ ] Neues Argument `objective` mit Default `"environmental"`.
- [ ] Validierung fuer erlaubte Werte.
- [ ] Rueckwaertskompatibilitaet erhalten.

## Schritt 7: Kosten-Parameter in Pyomo anlegen

Datei:

```text
src/optimex/optimizer.py
```

In `create_model()` bei den Parametern ergaenzen:

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

- [ ] `intermediate_costs_cap` Param.
- [ ] `intermediate_costs_op` Param.
- [ ] `discount_rate` Param.
- [ ] `discount_reference_year` Param.
- [ ] Defaults auf 0 bzw. `min(SYSTEM_TIME)`.

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

- [ ] `background_purchase_cap[i,t]` in realen Einheiten.
- [ ] `background_purchase_op[i,t]` in realen Einheiten.
- [ ] `fg_scale` korrekt angewendet.

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

- [ ] `discount_factor[t]`.
- [ ] `cost_cap[t]`.
- [ ] `cost_op[t]`.
- [ ] `total_cost`.
- [ ] Test mit `discount_rate = 0`.
- [ ] Test mit `discount_rate > 0`.

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

- [ ] `objective="environmental"` verhaelt sich wie vorher.
- [ ] `objective="cost"` minimiert `model.total_cost`.
- [ ] Unbekanntes Objective wirft `ValueError`.

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

- [ ] Cost Objective wird nicht mit Foreground- oder Charakterisierungsskalen multipliziert.
- [ ] Environmental Objective bleibt unveraendert.

## Schritt 12: Tests schreiben

Empfohlene neue Datei:

```text
tests/test_economics.py
```

### Test 1: Serialization

Ziel:

- `intermediate_costs_cap` setzen.
- `intermediate_costs_op` setzen.
- JSON speichern und laden.
- Tuple-Keys muessen erhalten bleiben.

Check:

```python
assert loaded.intermediate_costs_cap == original.intermediate_costs_cap
assert loaded.intermediate_costs_op == original.intermediate_costs_op
```

### Test 2: Purchase Split

Ziel:

- Ein Modell mit construction Edge und operation Edge.
- Pruefen, dass Mengen korrekt getrennt werden:

```python
background_purchase_cap[i,t]
background_purchase_op[i,t]
```

### Test 3: Cost Calculation

Ziel:

- Einfache Preise setzen.
- Erwartete Kosten manuell berechnen.

Check:

```python
cost_cap[t] == price_cap * purchase_cap
cost_op[t] == price_op * purchase_op
total_cost == sum(discounted costs)
```

### Test 4: Cost Objective Chooses Cheaper Route

Ziel:

- Zwei Prozesse koennen dieselbe Nachfrage erfuellen.
- Prozess A ist teurer.
- Prozess B ist guenstiger.

Check:

```python
objective="cost"
```

waehlt den guenstigeren Prozess.

### Test 5: Cost Objective mit Umweltbudget

Ziel:

- Kosten minimieren.
- `cumulative_category_impact_limits` setzen.
- Guenstige, aber zu schmutzige Option muss ausgeschlossen werden.

### Test 6: Backward Compatibility

Ziel:

- Bestehender Aufruf ohne `objective` funktioniert.
- `objective="environmental"` liefert bisheriges Verhalten.

## Schritt 13: Dokumentation ergaenzen

Moegliche Dateien:

```text
docs/api/optimizer.md
docs/content/optimization_setup.md
docs/content/constraints.md
docs/content/economic_optimization.md
```

Dokumentieren:

- [ ] `objective="environmental"`.
- [ ] `objective="cost"`.
- [ ] `intermediate_costs_cap`.
- [ ] `intermediate_costs_op`.
- [ ] `discount_rate`.
- [ ] `discount_reference_year`.
- [ ] First-level Background Pricing.
- [ ] Keine rekursive Background-Kostenrechnung.
- [ ] CAPEX/OPEX-artige Accounting-Trennung.

Methodischer Textvorschlag:

```text
Costs are applied only to first-level background purchases directly required by
the foreground system. They are not recursively applied to upstream products
inside the background inventory. The upstream background system remains relevant
for environmental impacts, while economic costs are represented by time-specific
market prices for direct background products.
```

## Schritt 14: ReadTheDocs-Seite fuer Economic Optimization erstellen

Neue Datei:

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

- [ ] Neue Seite `docs/content/economic_optimization.md` anlegen.
- [ ] Konzept first-level pricing erklaeren.
- [ ] Mathematische Formulierung aufnehmen.
- [ ] CAPEX/OPEX Accounting sauber einordnen.
- [ ] Input-Felder dokumentieren.
- [ ] Codebeispiel fuer `objective="cost"` ergaenzen.
- [ ] Codebeispiel fuer Kostenoptimierung mit Umweltbudget ergaenzen.
- [ ] Ergebnisinterpretation dokumentieren.
- [ ] Scaling-Hinweis aufnehmen.

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

## Schritt 19: Beispielseite fuer Economic Optimization ergaenzen

Optionale, aber fuer die Bachelorarbeit sehr wertvolle Seite:

```text
docs/content/examples/economic_optimization.md
```

Ziel:

Ein kleines durchgaengiges Beispiel, das zeigt:

- zwei Technologien koennen dieselbe Nachfrage bedienen,
- Kostenpreise werden fuer first-level Background-Produkte gesetzt,
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

- [ ] Kleine Story fuer Beispiel festlegen.
- [ ] Codebeispiel schreiben.
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
