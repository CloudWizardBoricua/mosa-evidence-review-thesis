"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const source = fs.readFileSync(path.join(__dirname, "../docs/assets/javascripts/readers.js"), "utf8");

class Element {
  constructor(tag) { this.tagName = tag; this.children = []; this.attributes = {}; this.handlers = {}; this._text = ""; this.value = ""; }
  set textContent(value) { this._text = value; this.children = []; }
  get textContent() { return this._text + this.children.map(child => child.textContent).join(" "); }
  append(...children) {
    this.children.push(...children);
    if (this.tagName === "select" && !this.value && this.children.length) this.value = this.children[0].value;
  }
  replaceChildren(...children) { this._text = ""; this.children = []; this.append(...children); }
  setAttribute(key, value) { this.attributes[key] = value; }
  addEventListener(name, handler) { this.handlers[name] = handler; }
}

function descendants(element) { return [element, ...element.children.flatMap(descendants)]; }
function fixture(caseId, mode, raw, guarded) {
  return {run_id: `${caseId}-${mode}`, case_id: caseId, split: "heldout", mode, repeat: 1, status: "completed", raw_disposition: raw, guarded_disposition: guarded, findings: [], events: [{type: "tool", tool: "inspect_evidence_package", status: "ok", reason: "Inspect records."}], guard_notes: [], metrics: {tool_invocations: 1, elapsed_ms: 12, tokens: 0, cost_usd: 0}, sources: []};
}

async function boot(saved, fail = false) {
  const panel = new Element("div");
  const requests = [];
  const context = {
    document: {currentScript: {src: "https://reader.example/mosa-evidence-review-thesis/assets/javascripts/readers.js"}, readyState: "complete", createElement: tag => new Element(tag), querySelector: selector => selector === "[data-review-explorer]" ? panel : null},
    location: {href: "https://reader.example/mosa-evidence-review-thesis/review/", origin: "https://reader.example"}, URL,
    fetch: async (url, options) => {
      requests.push({url: url.href, options});
      return {ok: !fail, status: fail ? 404 : 200, json: async () => saved};
    }
  };
  vm.runInNewContext(source, context);
  await new Promise(resolve => setImmediate(resolve));
  return {panel, requests};
}

test("saved reader fetches the project-relative record and filters cases and methods", async () => {
  const runs = [fixture("c0001", "baseline", "ready", "ready"), fixture("c0001", "openrouter", "not_ready", "needs_review"), fixture("c0002", "adaptive", "not_ready", "not_ready")];
  const {panel, requests} = await boot({schema_version: 1, runs});
  assert.equal(requests[0].url, "https://reader.example/mosa-evidence-review-thesis/assets/reviews.json");
  assert.equal(requests[0].options.credentials, "same-origin");
  let articles = descendants(panel).filter(element => element.tagName === "article");
  assert.equal(articles.length, 2);
  assert.match(panel.textContent, /Additional-case evaluation/);
  const mode = descendants(panel).find(element => element.id === "review-mode");
  mode.value = "openrouter"; mode.handlers.change();
  articles = descendants(panel).filter(element => element.tagName === "article");
  assert.equal(articles.length, 1);
  assert.match(articles[0].textContent, /Raw recommendation:.*Blocking problem.*After the guard:.*Further review/);
  const selection = descendants(panel).find(element => element.id === "review-case");
  selection.value = "c0002"; mode.value = "all"; selection.handlers.change();
  articles = descendants(panel).filter(element => element.tagName === "article");
  assert.equal(articles.length, 1);
  assert.match(articles[0].textContent, /Rule based adaptive workflow/);
});

test("reader preserves failed execution context and renders data as plain text", async () => {
  const run = fixture("c0001", "openrouter", "needs_review", "needs_review");
  run.status = "failed"; run.failure_kind = "api_failure";
  run.findings = [{id: "UNKNOWN", artifact: "manifest.json", field: "/", severity: "unknown", message: '<img src=x onerror="unexpected()">', remediation: "Supply the record."}];
  run.sources = [{artifact: "manifest.json", url: "javascript:unexpected()"}];
  const {panel} = await boot({schema_version: 1, runs: [run]});
  assert.match(panel.textContent, /Recorded execution status: failed/);
  assert.match(panel.textContent, /Recorded failure: api_failure/);
  assert.match(panel.textContent, /<img src=x/);
  assert.match(panel.textContent, /reference unavailable/);
  assert.equal(descendants(panel).filter(element => element.tagName === "img").length, 0);
  assert.equal(descendants(panel).filter(element => element.tagName === "button").length, 0, "Public saved reviews have no approval action");
});

test("unavailable saved data reports its reading limit and keeps a download route", async () => {
  const {panel} = await boot({}, true);
  assert.match(panel.textContent, /could not be read \(404\)/);
  assert.match(panel.textContent, /Download the saved data/);
});
