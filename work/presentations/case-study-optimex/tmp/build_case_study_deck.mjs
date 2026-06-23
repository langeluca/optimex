import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT = "C:\\Users\\lucal\\Brightway\\optimex\\outputs\\case-study-optimex.pptx";
const PREVIEW_DIR = "C:\\Users\\lucal\\Brightway\\optimex\\work\\presentations\\case-study-optimex\\tmp\\preview";
const LAYOUT_DIR = "C:\\Users\\lucal\\Brightway\\optimex\\work\\presentations\\case-study-optimex\\tmp\\layout";
const QA_DIR = "C:\\Users\\lucal\\Brightway\\optimex\\work\\presentations\\case-study-optimex\\tmp\\qa";
const RWTH_BLUE = "#00549F";
const RWTH_BLUE_LIGHT = "#E8F1FA";

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

function addText(slide, text, position, style = {}) {
  const box = slide.shapes.add({
    geometry: "textbox",
    position,
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  box.text = text;
  box.text.style = {
    fontSize: style.fontSize ?? 20,
    color: style.color ?? "slate-800",
    bold: style.bold ?? false,
    alignment: style.alignment ?? "left",
  };
  return box;
}

function addRule(slide, left, top, width, fill = "slate-300") {
  slide.shapes.add({
    geometry: "rect",
    position: { left, top, width, height: 2 },
    fill,
    line: { style: "solid", fill, width: 0 },
  });
}

function addFooter(slide, number) {
  addText(slide, `Case Study optimex | ${number}`, { left: 72, top: 672, width: 260, height: 24 }, {
    fontSize: 14,
    color: "slate-500",
  });
}

function addSlideTitle(slide, title, number, kicker = "Case Study") {
  slide.background.fill = "slate-50";
  addText(slide, kicker, { left: 72, top: 44, width: 260, height: 26 }, {
    fontSize: 16,
    bold: true,
    color: "slate-500",
  });
  addText(slide, title, { left: 72, top: 82, width: 1080, height: 64 }, {
    fontSize: 36,
    bold: true,
    color: "slate-950",
  });
  addRule(slide, 72, 154, 220, RWTH_BLUE);
  addFooter(slide, number);
}

function addBullets(slide, bullets, x, y, w, fontSize = 21, gap = 50) {
  bullets.forEach((bullet, index) => {
    addText(slide, "•", { left: x, top: y + index * gap, width: 24, height: 30 }, {
      fontSize,
      color: RWTH_BLUE,
      bold: true,
    });
    addText(slide, bullet, { left: x + 34, top: y + index * gap, width: w - 34, height: gap - 4 }, {
      fontSize,
      color: "slate-800",
    });
  });
}

function addQuestion(slide, question, y = 500) {
  slide.shapes.add({
    geometry: "roundRect",
    position: { left: 72, top: y, width: 1136, height: 92 },
    fill: "white",
    line: { style: "solid", fill: "slate-200", width: 1 },
    borderRadius: "rounded-lg",
  });
  addText(slide, "Forschungsfrage", { left: 100, top: y + 16, width: 260, height: 26 }, {
    fontSize: 16,
    bold: true,
    color: RWTH_BLUE,
  });
  addText(slide, question, { left: 100, top: y + 42, width: 1050, height: 38 }, {
    fontSize: 18,
    color: "slate-800",
  });
}

function addTwoColumnSlide(presentation, number, title, leftItems, rightTitle, rightItems, question) {
  const slide = presentation.slides.add();
  addSlideTitle(slide, title, number);
  addText(slide, "Ausgangspunkt", { left: 72, top: 198, width: 470, height: 30 }, {
    fontSize: 24,
    bold: true,
    color: "slate-900",
  });
  addBullets(slide, leftItems, 72, 242, 500, 20, 48);
  addText(slide, rightTitle, { left: 680, top: 198, width: 460, height: 30 }, {
    fontSize: 24,
    bold: true,
    color: "slate-900",
  });
  addBullets(slide, rightItems, 680, 242, 500, 20, 48);
  addQuestion(slide, question, 510);
}

function addStep(slide, label, text, left, top, fill = "white") {
  slide.shapes.add({
    geometry: "roundRect",
    position: { left, top, width: 205, height: 102 },
    fill,
    line: { style: "solid", fill: "slate-300", width: 1 },
    borderRadius: "rounded-lg",
  });
  addText(slide, label, { left: left + 16, top: top + 14, width: 170, height: 24 }, {
    fontSize: 16,
    bold: true,
    color: RWTH_BLUE,
  });
  addText(slide, text, { left: left + 16, top: top + 42, width: 170, height: 42 }, {
    fontSize: 17,
    color: "slate-800",
  });
}

const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });

{
  const slide = presentation.slides.add();
  slide.background.fill = "slate-50";
  addText(slide, "Case Study", { left: 72, top: 72, width: 300, height: 36 }, {
    fontSize: 24,
    bold: true,
    color: RWTH_BLUE,
  });
  addText(slide, "Ökonomische Erweiterung von optimex", { left: 72, top: 160, width: 1040, height: 72 }, {
    fontSize: 54,
    bold: true,
    color: "slate-950",
  });
  addText(slide, "Gedanken zur Struktur der Case Study und zu den Analyseperspektiven", { left: 72, top: 250, width: 950, height: 36 }, {
    fontSize: 24,
    color: "slate-700",
  });
  addRule(slide, 72, 330, 340, RWTH_BLUE);
  addText(slide, "Übergeordnete Forschungsfrage", { left: 72, top: 380, width: 520, height: 30 }, {
    fontSize: 24,
    bold: true,
    color: "slate-900",
  });
  addText(slide, "Wie ermöglicht die ökonomische Erweiterung von optimex die Bestimmung kostenoptimaler Transformationspfade unter Berücksichtigung zeitexpliziter Lebenszyklus-Umweltwirkungen?", { left: 72, top: 426, width: 1020, height: 80 }, {
    fontSize: 24,
    color: "slate-800",
  });
  addFooter(slide, 1);
}

{
  const slide = presentation.slides.add();
  addSlideTitle(slide, "Ausgangspunkt und Fokus", 2);
  addBullets(slide, [
    "Zusätzliche Analyse- und Entscheidungsmöglichkeiten durch die ökonomische Erweiterung von optimex",
    "Bestimmung kostenoptimaler Transformationspfade",
    "Basis: zeitexplizite Lebenszyklusbetrachtung",
  ], 92, 210, 1080, 23, 62);
  addText(slide, "Trade-offs, die betrachtet werden sollen", { left: 92, top: 430, width: 700, height: 32 }, {
    fontSize: 24,
    bold: true,
    color: "slate-900",
  });
  addBullets(slide, [
    "Kosten",
    "Umweltwirkungen",
    "Technologieeinsatz",
    "Transformationszeitpunkt",
  ], 92, 482, 920, 21, 42);
}

{
  const slide = presentation.slides.add();
  addSlideTitle(slide, "Logik der Case Study", 3);
  addText(slide, "Die Analyse entwickelt sich von einfachen Referenzfällen hin zu einer entscheidungsrelevanten Transformationsanalyse.", { left: 72, top: 190, width: 1040, height: 56 }, {
    fontSize: 24,
    color: "slate-800",
  });
  addStep(slide, "1", "Cost-only: ökonomischer Referenzfall", 72, 300);
  addStep(slide, "2", "Environmental-only: ökologischer Extremfall", 302, 300);
  addStep(slide, "3", "Emission budget: kostenoptimale Zielerfüllung", 532, 300, RWTH_BLUE_LIGHT);
  addStep(slide, "4", "Budget sweep / Pareto curve", 762, 300);
  addStep(slide, "5", "CO₂ price: ökonomische Anreizwirkung", 992, 300);
  addText(slide, "Kern der Case Study", { left: 532, top: 426, width: 210, height: 26 }, {
    fontSize: 18,
    bold: true,
    color: RWTH_BLUE,
    alignment: "center",
  });
}

addTwoColumnSlide(
  presentation,
  4,
  "1. Cost-only: Ökonomischer Referenzfall",
  [
    "Transformationspfad bei reiner Kostenminimierung",
    "Keine Berücksichtigung ökologischer Restriktionen",
    "Wirtschaftlicher Referenzfall",
    "Sichtbar wird, welche Technologieentscheidungen ohne Umweltconstraints getroffen werden",
  ],
  "Zentrales Argument",
  [
    "Kosten können als Zielfunktion formuliert werden",
    "Framework leitet daraus einen kostenoptimalen Technologie- und Betriebspfad ab",
    "Referenzfall zeigt, ob ökologische Zielgrößen verfehlt werden",
  ],
  "Welcher Transformationspfad ergibt sich, wenn ausschließlich Kosten minimiert werden und keine Umweltconstraints berücksichtigt werden?"
);

addTwoColumnSlide(
  presentation,
  5,
  "2. Environmental-only: Ökologischer Extremfall",
  [
    "Bestimmung des rein umweltoptimalen Transformationspfads",
    "Knüpft an die bisherige Logik von optimex an",
    "Umweltwirkungen werden als Zielfunktion minimiert",
  ],
  "Zentrales Argument",
  [
    "Vergleich mit Cost-only zeigt den grundsätzlichen Zielkonflikt",
    "Cost-only liefert die wirtschaftlich günstigste Lösung",
    "Environmental-only liefert die ökologische Bestlösung",
    "Die Differenz verdeutlicht die Notwendigkeit einer integrierten Betrachtung",
  ],
  "Welcher Transformationspfad ergibt sich, wenn ausschließlich die Umweltwirkung minimiert wird, und wie unterscheidet sich dieser Pfad vom rein kostenoptimalen Pfad?"
);

addTwoColumnSlide(
  presentation,
  6,
  "3. Kostenminimierung mit Emissionsbudget",
  [
    "Kern der Case Study",
    "Nicht mehr entweder Kosten oder Umwelt minimieren",
    "Ökologisches Ziel als Nebenbedingung",
    "Gesucht wird der kostengünstigste Pfad, der ein vorgegebenes Emissionsbudget einhält",
  ],
  "Zentrales Argument",
  [
    "Adressiert die zentrale Forschungslücke der Arbeit",
    "Umweltwirkungen werden als Constraints berücksichtigt",
    "Kosten werden als Zielfunktion minimiert",
    "optimex wird zu einem entscheidungsunterstützenden Framework für Transformationen unter ökologischen Zielvorgaben",
  ],
  "Welcher kostenminimale Transformationspfad erfüllt ein vorgegebenes Emissionsbudget auf Basis zeitexpliziter Lebenszyklus-Umweltwirkungen?"
);

addTwoColumnSlide(
  presentation,
  7,
  "4. Budget Sweep / Pareto Curve",
  [
    "Wiederholung der Kostenminimierung für unterschiedlich strenge Emissionsbudgets",
    "Dadurch entsteht eine Kosten-Emissions-Front",
    "Der Trade-off zwischen ökonomischer und ökologischer Zielerfüllung wird sichtbar",
  ],
  "Zentrales Argument",
  [
    "Zeigt zusätzliche Kosten ambitionierterer Umweltziele",
    "Zeigt Budgetgrenzen, ab denen bestimmte Technologien oder frühere Investitionen notwendig werden",
    "Charakterisiert den Lösungsraum zwischen kostengünstiger und emissionsarmer Transformation",
  ],
  "Wie verändern sich die minimalen Transformationskosten, wenn das zulässige Emissionsbudget schrittweise verschärft wird?"
);

addTwoColumnSlide(
  presentation,
  8,
  "5. CO₂-Preis als optionale Policy-Interpretation",
  [
    "CO₂-Preis kann als zusätzlicher Kostenbestandteil berücksichtigt werden",
    "Emissionsbudget: harte ökologische Zielvorgabe",
    "CO₂-Preis: ökonomischer Anreiz zur Emissionsreduktion",
  ],
  "Zentrales Argument",
  [
    "Übersetzt die Kosten-Emissions-Front in eine politisch-ökonomische Interpretation",
    "Analyse kann zeigen, ob ein CO₂-Preis einen emissionsarmen Pfad auslöst",
    "Verbindung zu CO₂-Bepreisung und Emissionshandel",
  ],
  "Welcher CO₂-Preis wäre erforderlich, um emissionsarme Transformationspfade wirtschaftlich attraktiv zu machen, und reicht ein gegebener CO₂-Preis aus, um ein bestimmtes Emissionsbudget einzuhalten?"
);

{
  const slide = presentation.slides.add();
  addSlideTitle(slide, "Roter Faden", 9);
  const rows = [
    ["Cost-only", "zeigt, was aus rein wirtschaftlicher Sicht optimal wäre"],
    ["Environmental-only", "zeigt, was aus rein ökologischer Sicht optimal wäre"],
    ["Emission budget", "verbindet beide Perspektiven: ökologische Ziele zu minimalen Kosten erreichen"],
    ["Budget sweep / Pareto curve", "quantifiziert die Mehrkosten strengerer Umweltanforderungen"],
    ["CO₂ price", "interpretiert die Ergebnisse als ökonomische Anreiz- und Politikinstrumente"],
  ];
  rows.forEach(([label, text], index) => {
    const top = 204 + index * 82;
    addText(slide, label, { left: 92, top, width: 330, height: 34 }, {
      fontSize: 23,
      bold: true,
      color: index === 2 ? RWTH_BLUE : "slate-900",
    });
    addText(slide, text, { left: 450, top: top + 2, width: 690, height: 44 }, {
      fontSize: 21,
      color: "slate-800",
    });
    if (index < rows.length - 1) {
      addRule(slide, 92, top + 58, 1040, "slate-200");
    }
  });
}

{
  const slide = presentation.slides.add();
  addSlideTitle(slide, "Zentrale Capability der Erweiterung", 10);
  addText(slide, "optimex kann nicht nur Umweltwirkungen zeitexplizit bewerten oder minimieren.", { left: 72, top: 194, width: 1020, height: 42 }, {
    fontSize: 24,
    color: "slate-800",
  });
  addText(slide, "Zusätzlich kann das Framework:", { left: 72, top: 274, width: 620, height: 32 }, {
    fontSize: 24,
    bold: true,
    color: "slate-900",
  });
  addBullets(slide, [
    "kostenoptimale Transformationspfade unter ökologischen Zielvorgaben bestimmen",
    "ökonomische und ökologische Trade-offs analysieren",
    "Kosten der Zielerfüllung quantifizieren",
    "Technologieentscheidungen und Transformationszeitpunkte unter Kosten- und Umweltrestriktionen untersuchen",
    "CO₂-Preise als mögliche Anreizmechanismen interpretieren",
  ], 92, 330, 1040, 21, 49);
}

await fs.mkdir(path.dirname(OUT), { recursive: true });
await fs.mkdir(PREVIEW_DIR, { recursive: true });
await fs.mkdir(LAYOUT_DIR, { recursive: true });
await fs.mkdir(QA_DIR, { recursive: true });

for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  await writeBlob(path.join(PREVIEW_DIR, `${stem}.png`), await presentation.export({ slide, format: "png", scale: 1 }));
  await fs.writeFile(path.join(LAYOUT_DIR, `${stem}.layout.json`), await (await slide.export({ format: "layout" })).text(), "utf8");
}
await writeBlob(path.join(QA_DIR, "deck-montage.webp"), await presentation.export({ format: "webp", montage: true, scale: 1 }));

const snapshot = await presentation.inspect({ kind: "slide,textbox,shape", maxChars: 12000 });
await fs.writeFile(path.join(QA_DIR, "inspect.ndjson"), snapshot.ndjson, "utf8");

const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(OUT);
console.log(OUT);
