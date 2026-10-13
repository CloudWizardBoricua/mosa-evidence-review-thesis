"use strict";
(() => {
  const script = document.currentScript;
  const assetBase = new URL("../", script.src);
  const modes = {baseline: "Fixed workflow", fixed: "Fixed workflow", adaptive: "Rule based adaptive workflow", openrouter: "Model agent", model: "Model agent"};
  const outcomes = {ready: ["Ready", "ready"], needs_review: ["Further review", "review"], not_ready: ["Blocking problem", "blocked"]};
  const splits = {heldout: "Additional-case evaluation", development: "Development", pilot: "Capstone pilot"};
  const node = (tag, text, className) => {
    const element = document.createElement(tag);
    if (text !== undefined) element.textContent = String(text);
    if (className) element.className = className;
    return element;
  };
  const format = (value, digits = 0) => value === null || value === undefined ? "Not reported" : Number(value).toLocaleString(undefined, {maximumFractionDigits: digits});
  const badge = value => {
    const label = outcomes[value] || [value === null ? "No recommendation returned" : "Unknown result", "review"];
    return node("span", label[0], `legend ${label[1]}`);
  };
  const safeLink = (text, href) => {
    const element = node("a", text);
    try {
      const url = new URL(href, location.href);
      if (url.protocol !== "https:" && url.protocol !== "http:") throw new Error("Unsupported source link");
      if (url.origin !== location.origin && url.hostname !== "github.com" && url.hostname !== "raw.githubusercontent.com") throw new Error("Unexpected source host");
      element.href = url.href;
    } catch (_) {
      return node("span", `${text} (reference unavailable)`);
    }
    return element;
  };
  async function load(name) {
    const response = await fetch(new URL(name, assetBase), {credentials: "same-origin"});
    if (!response.ok) throw new Error(`Saved data could not be read (${response.status})`);
    const data = await response.json();
    if (data.schema_version !== 1) throw new Error("Unsupported saved data version");
    return data;
  }
  function record(run) {
    const article = node("article", undefined, "review-record");
    article.append(node("h3", `${run.case_id}: ${modes[run.mode] || run.mode}, repeat ${run.repeat}`));
    article.append(node("p", `Dataset: ${run.dataset || "new benchmark"}. Split: ${splits[run.split] || run.split}. Run: ${run.run_id}.`, "source-ref"));
    if (run.status) article.append(node("p", `Recorded execution status: ${run.status}.`));
    const decisions = node("div", undefined, "review-outcomes");
    decisions.append(node("strong", "Raw recommendation:"), badge(run.raw_disposition), node("strong", "After the guard:"), badge(run.guarded_disposition));
    article.append(decisions);
    const metrics = run.metrics || {};
    const metricRow = node("p", undefined, "metric-grid");
    const tokenValue = run.status === "failed" && run.mode === "openrouter" ? null : metrics.tokens;
    metricRow.append(node("span", `Tool invocations: ${format(metrics.tool_invocations)}`), node("span", `Elapsed: ${format(metrics.elapsed_ms, 3)} ms`), node("span", `Tokens: ${format(tokenValue)}`), node("span", `Cost: ${metrics.cost_usd === undefined || metrics.cost_usd === null ? "Not reported" : "$" + format(metrics.cost_usd, 6)}`));
    article.append(metricRow, node("h4", "What was checked"));
    const eventList = node("ol");
    for (const event of run.events || []) {
      const item = node("li", `${event.tool || event.type}: ${event.status || "recorded"}. ${event.reason || ""}`);
      eventList.append(item);
    }
    if (!eventList.children.length) eventList.append(node("li", "The saved record does not include individual tool events."));
    article.append(eventList, node("h4", "What was found and what to correct"));
    for (const finding of run.findings || []) {
      const item = node("div", undefined, `finding ${finding.severity === "unknown" ? "unknown" : ""}`);
      item.append(node("strong", finding.id), node("p", finding.message || "Consult the recorded finding."));
      const reference = node("p", undefined, "source-ref");
      reference.append(node("strong", "Source: "));
      const source = (run.sources || []).find(s => s.artifact === finding.artifact);
      const referenceText = `${finding.artifact || "Source artifact not recorded"} / ${finding.field || "Field not recorded"}`;
      reference.append(source && source.url ? safeLink(referenceText, source.url) : node("span", `${referenceText}. Direct source link unavailable.`));
      item.append(reference, node("p", `Correction: ${finding.remediation || "Consult the private review record for the correction."}`));
      if (finding.citation_valid !== undefined) item.append(node("p", `Reference checked: ${finding.citation_valid ? "Yes" : "No or unavailable"}.`));
      article.append(item);
    }
    if (!(run.findings || []).length) article.append(node("p", "No findings are recorded for this run. Required validation coverage still determines the recommendation."));
    article.append(node("h4", "What remains unknown"));
    const unknowns = node("ul");
    for (const note of run.guard_notes || []) unknowns.append(node("li", note));
    for (const note of run.limitations || []) unknowns.append(node("li", note));
    if (run.failure_kind) unknowns.append(node("li", `Recorded failure: ${run.failure_kind}. This run remains in the evaluation record.`));
    if (!unknowns.children.length) unknowns.append(node("li", "No additional guard notes were recorded. The result remains limited to this synthetic research profile."));
    article.append(unknowns);
    return article;
  }
  async function reviews(panel) {
    const data = await load("reviews.json");
    if (!Array.isArray(data.runs)) throw new Error("Saved run list is missing");
    panel.replaceChildren();
    const controls = node("div", undefined, "review-controls");
    const caseLabel = node("label", "Choose a saved case");
    const caseSelect = node("select"); caseSelect.id = "review-case";
    const cases = [...new Set(data.runs.map(r => r.case_id))].sort();
    for (const id of cases) { const option = node("option", id); option.value = id; caseSelect.append(option); }
    caseLabel.append(caseSelect);
    const modeLabel = node("label", "Choose a review method");
    const modeSelect = node("select"); modeSelect.id = "review-mode";
    const all = node("option", "All recorded methods"); all.value = "all"; modeSelect.append(all);
    for (const mode of [...new Set(data.runs.map(r => r.mode))]) { const option = node("option", modes[mode] || mode); option.value = mode; modeSelect.append(option); }
    modeLabel.append(modeSelect); controls.append(caseLabel, modeLabel);
    const count = node("p"); count.setAttribute("role", "status"); count.setAttribute("aria-live", "polite");
    const output = node("div");
    const render = () => {
      const runs = data.runs.filter(r => r.case_id === caseSelect.value && (modeSelect.value === "all" || r.mode === modeSelect.value));
      count.textContent = `${runs.length} saved run${runs.length === 1 ? "" : "s"} shown. All dates and outcomes come from the saved records.`;
      output.replaceChildren(...runs.map(record));
    };
    caseSelect.addEventListener("change", render); modeSelect.addEventListener("change", render);
    panel.append(controls, count, output); render();
  }
  async function results(panel) {
    const data = await load("study_summary.json");
    panel.replaceChildren(node("h2", "Recorded dataset status"));
    for (const dataset of data.datasets || []) {
      const label = dataset.id === "study40-heldout" ? "New benchmark: additional-case evaluation" : dataset.label || dataset.id;
      panel.append(node("h3", label), node("p", `Status: ${dataset.status || "recorded"}. Unique cases: ${format(dataset.cases)}. Runs: ${format(dataset.runs)}.`));
      const list = node("ul");
      for (const note of dataset.notes || []) list.append(node("li", note));
      if (list.children.length) panel.append(list);
    }
    if (data.budget) panel.append(node("p", `New study spending ceiling: $${format(data.budget.limit_usd, 2)}. Recorded spending: ${data.budget.spent_usd === null || data.budget.spent_usd === undefined ? "Not reported" : "$" + format(data.budget.spent_usd, 6)}.`));
  }
  const start = () => {
    const review = document.querySelector("[data-review-explorer]");
    const summary = document.querySelector("[data-study-results]");
    if (review) reviews(review).catch(error => review.replaceChildren(node("p", `${error.message}. Download the saved data or use the walkthrough below.`)));
    if (summary) results(summary).catch(error => summary.replaceChildren(node("p", `${error.message}. Use the verified tables above.`)));
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
