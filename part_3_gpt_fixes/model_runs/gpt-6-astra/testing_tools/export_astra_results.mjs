import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const require = createRequire(process.env.APR_NODE_MODULES
  ? path.join(process.env.APR_NODE_MODULES, '_apr_loader.cjs')
  : import.meta.url);
const { Workbook, SpreadsheetFile } = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const input = path.resolve(process.argv[2]);
const { plan, records } = JSON.parse(await fs.readFile(input, 'utf8'));
if (plan.model !== 'gpt-6-astra') throw new Error('Wrong model');
const index = new Map(records.map(r => [`${r.case}|${r.version}`, r]));
if (index.size !== records.length || records.some(r => r.target !== 'ASTRA_FIXED')) throw new Error('Duplicate or wrong-model records');
const pairs = plan.cases.reduce((n, c) => n + c.versions.length, 0);
const wb = Workbook.create();
const exits = wb.worksheets.add('Exit results');
const details = wb.worksheets.add('Detailed reasons');
const summary = wb.worksheets.add('Summary');
const rawRows = [['Case Number', 'Qiskit Version', 'Buggy Result', 'Human Fix Result', 'Astra Fix Result', 'Human Exit Code', 'Astra Exit Code']];
const detailRows = [['Case Number', 'Qiskit Version', 'Buggy Result', 'Human Fix Result', 'Reason', 'Astra Fix Result', 'Astra Reason', 'Test Sensitivity', 'Test File', 'Review Required', 'Human Log', 'Astra Log']];
const absent = {raw_result:'NOT TESTED', classification:'NOT TESTED', reason:'Not yet tested.', review_required:false};
const counts = new Map();
const spacers = [];
let matched = 0;
for (const entry of plan.cases) {
  const tally = {PASS:0, ERROR:0, FAIL:0, 'NOT TESTED':0};
  for (const version of entry.versions) {
    const old = entry.inherited[version];
    const record = index.get(`${entry.case}|${version}`);
    if (record) matched++;
    const sol = record ?? absent;
    if (!(sol.classification in tally)) throw new Error(`Unexpected status: ${sol.classification}`);
    tally[sol.classification]++;
    rawRows.push([entry.case, version, old.buggy_result, old.human_raw_result, sol.raw_result, old.human_exit_code, sol.exit_code ?? null]);
    detailRows.push([entry.case, version, old.buggy_result, old.human_classification, old.human_reason,
      sol.classification, sol.reason, '', path.basename(entry.test),
      record ? (sol.review_required ? 'YES' : '') : 'PENDING', old.human_log, sol.log ?? '']);
  }
  counts.set(entry.case, tally);
  rawRows.push(Array(7).fill(null));
  detailRows.push(Array(12).fill(null));
  spacers.push(rawRows.length);
}
if (matched !== records.length || pairs !== 1015 || plan.cases.length !== 73) throw new Error('Unexpected case/version coverage');
const lastDataRow = rawRows.length;
exits.getRange(`A1:G${lastDataRow}`).values = rawRows;
details.getRange(`A1:L${lastDataRow}`).values = detailRows;
summary.getRange('A1:E1').values = [['Case Number', 'Versions Tested', 'Astra PASS', 'Astra ERROR', 'Astra FAIL']];
const lastCaseRow = plan.cases.length + 1;
const totalRow = lastCaseRow + 1;
for (let i = 0; i < plan.cases.length; i++) {
  const row = i + 2;
  summary.getRange(`A${row}`).values = [[plan.cases[i].case]];
  summary.getRange(`C${row}:E${row}`).formulas = [['PASS','ERROR','FAIL'].map(s =>
    `=COUNTIFS('Detailed reasons'!$A$2:$A$${lastDataRow},A${row},'Detailed reasons'!$F$2:$F$${lastDataRow},"${s}")`)];
  summary.getRange(`B${row}`).formulas = [[`=SUM(C${row}:E${row})`]];
}
summary.getRange(`A${totalRow}`).values = [['TOTAL']];
summary.getRange(`B${totalRow}:E${totalRow}`).formulas = [['B','C','D','E'].map(c => `=SUM(${c}2:${c}${lastCaseRow})`)];
summary.getRange('G1:H8').values = [
  ['Classification', 'Definition / Provenance'],
  ['PASS', 'Selected test completed successfully: exit 0, at least one test, and OK without skips. Not independent proof of full question correctness.'],
  ['ERROR', 'Target exception, import/parser error, crash, timeout or test setup failure. Review the log before attributing blame to the model.'],
  ['FAIL', 'Completed assertion/output/interface checks failed without an established target execution exception. May need question/code/test review.'],
  ['NOT TESTED', 'No completed classified test result. Excluded from Versions Tested; shown separately in counts.'],
  ['Inherited results', 'Buggy and human results/reasons are copied from the supplied 6-Luna baseline, including revised human case 790. Neither is rerun.'],
  ['Astra review', 'Astra reasons use saved logs and the existing classification method, not an LLM semantic review. Column H starts blank, meaning not yet reviewed for test sensitivity.'],
  ['Re-export warning', 'Automatic export rebuilds the workbook from records. Keep later manually reviewed workbooks separately to preserve annotations.']
];
summary.getRange('G10:H14').values = [
  ['Model', plan.model], ['Assigned case/version pairs', pairs], ['Planned new Astra executions', pairs],
  ['Saved Astra execution records', records.length], ['Source baseline', plan.source_baseline]
];
summary.getRange('G16:H16').values = [['Metric', 'Count']];
const metrics = [['Human PASS','D','PASS'], ['Human ERROR','D','ERROR'], ['Human FAIL','D','FAIL'], ['Human NOT TESTED','D','NOT TESTED'],
  ['Astra PASS','F','PASS'], ['Astra ERROR','F','ERROR'], ['Astra FAIL','F','FAIL'], ['Astra NOT TESTED','F','NOT TESTED']];
for (let i = 0; i < metrics.length; i++) {
  const [label, column, status] = metrics[i];
  const row = i + 17;
  summary.getRange(`G${row}`).values = [[label]];
  summary.getRange(`H${row}`).formulas = [[`=COUNTIF('Detailed reasons'!$${column}$2:$${column}$${lastDataRow},"${status}")`]];
}
for (const [sheet, last, col] of [[exits,lastDataRow,'G'],[details,lastDataRow,'L'],[summary,totalRow,'H']]) {
  const range = sheet.getRange(`A1:${col}${last}`);
  range.format.font = {name:'Arial', size:10};
  range.format.verticalAlignment = 'top';
  range.format.rowHeight = 22;
  sheet.freezePanes.freezeRows(1);
  sheet.getRange(`A1:${col}1`).format.rowHeight = 32;
  sheet.getRange(`A1:${col}1`).format.wrapText = true;
  sheet.getRange('A:A').format.columnWidth = 20;
  sheet.getRange('B:D').format.columnWidth = 19;
}
for (const [sheet, range] of [[exits,'A1:G1'],[details,'A1:L1'],[summary,'A1:E1'],[summary,'G1:H1'],[summary,'G16:H16']]) {
  sheet.getRange(range).format.fill = '#D9E5F2';
  sheet.getRange(range).format.font.bold = true;
}
exits.getRange('E:G').format.columnWidth = 19;
details.getRange('E:E').format.columnWidth = 82;
details.getRange('F:F').format.columnWidth = 19;
details.getRange('G:G').format.columnWidth = 100;
details.getRange('H:H').format.columnWidth = 85;
details.getRange('I:J').format.columnWidth = 22;
details.getRange('K:L').format.columnWidth = 55;
details.getRange(`E2:L${lastDataRow}`).format.wrapText = true;
details.getRange(`A2:L${lastDataRow}`).format.rowHeight = 95;
for (const row of spacers) {
  exits.getRange(`A${row}:G${row}`).format.rowHeight = 10;
  details.getRange(`A${row}:L${row}`).format.rowHeight = 10;
}
summary.getRange('E:E').format.columnWidth = 19;
summary.getRange('F:F').format.columnWidth = 3;
summary.getRange('G:G').format.columnWidth = 30;
summary.getRange('H:H').format.columnWidth = 100;
summary.getRange('G2:H8').format.wrapText = true;
summary.getRange('G2:H8').format.rowHeight = 60;
summary.getRange('G14:H14').format.wrapText = true;
summary.getRange('G14:H14').format.rowHeight = 55;
summary.getRange(`A${totalRow}:E${totalRow}`).format.font.bold = true;
summary.getRange(`B2:E${totalRow}`).setNumberFormat('0');
wb.recalculate();
for (const [name, tested, pass, error, fail] of summary.getRange(`A2:E${lastCaseRow}`).values) {
  const t = counts.get(name);
  if (pass !== t.PASS || error !== t.ERROR || fail !== t.FAIL || tested !== pass + error + fail) throw new Error(`Summary mismatch: ${name}`);
}
for (const range of ['H17:H20', 'H21:H24']) {
  const total = summary.getRange(range).values.flat().reduce((a,b) => a+b,0);
  if (total !== pairs) throw new Error(`Metric totals mismatch: ${range}`);
}
const output = path.join(path.dirname(input), '73_cases_6_astra_fixes.xlsx');
if (process.env.APR_REPORT_QA_PREVIEW === '1') {
  for (const [sheetName, range, name] of [['Exit results','A1:G6','exit'], ['Detailed reasons','A1:H4','reasons'], ['Summary','A1:E10','summary']]) {
    const blob = await wb.render({sheetName, range, scale:1});
    await fs.writeFile(path.join(path.dirname(input), `qa_${name}.png`), new Uint8Array(await blob.arrayBuffer()));
  }
}
const file = await SpreadsheetFile.exportXlsx(wb);
await file.save(output);
console.log(`Workbook saved: ${output}`);
