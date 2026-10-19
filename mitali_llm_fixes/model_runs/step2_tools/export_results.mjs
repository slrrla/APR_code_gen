import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

// Resolve the public entry point from the bundled runtime, not repository packages.
const modules = path.join(os.homedir(), '.cache', 'codex-runtimes', 'codex-primary-runtime', 'dependencies', 'node', 'node_modules');
const require = createRequire(path.join(modules, '_apr_loader.cjs'));
const { Workbook, SpreadsheetFile } = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const input = path.resolve(process.argv[2]);
const payload = JSON.parse(await fs.readFile(input, 'utf8'));
const { plan, records } = payload;
const pairs = plan.cases.reduce((n, entry) => n + entry.versions.length, 0);
const lastDataRow = pairs + 1;
const lastCaseRow = plan.cases.length + 1;
const totalRow = lastCaseRow + 1;
const index = new Map(records.map(r => [`${r.case}|${r.version}|${r.target}`, r]));
if (index.size !== records.length) throw new Error('Duplicate result keys');
const wb = Workbook.create();
const exits = wb.worksheets.add('Exit results');
const details = wb.worksheets.add('Detailed reasons');
const summary = wb.worksheets.add('Summary');
const rawRows = [['Case Number', 'Qiskit Version', 'Buggy Result', 'Human Fix Result', 'Luna Fix Result', 'Human Exit Code', 'Luna Exit Code']];
const detailRows = [['Case Number', 'Qiskit Version', 'Buggy Result', 'Human Fix Result', 'Reason', 'Luna Fix Result', 'Luna Reason']];
const auditRows = [['Test File', 'Review Required', 'Human Log', 'Luna Log']];
const absent = {raw_result:'NOT TESTED', classification:'NOT TESTED', reason:'Not yet tested in this batch.', review_required:false};
const safe = s => typeof s === 'string' && /^[=+@-]/.test(s) ? `'${s}` : s;
const counts = new Map();
for (const entry of plan.cases) {
  const tally = {PASS:0,ERROR:0,FAIL:0,'NOT TESTED':0};
  for (const v of entry.versions) {
    const human = index.get(`${entry.case}|${v}|HUMAN_FIXED`) ?? absent;
    const luna = index.get(`${entry.case}|${v}|LUNA_FIXED`) ?? absent;
    const buggy = entry.buggy_recorded[v];
    rawRows.push([entry.case,v,buggy,human.raw_result,luna.raw_result,human.exit_code ?? null,luna.exit_code ?? null]);
    detailRows.push([entry.case,v,buggy,human.classification,human.reason,luna.classification,luna.reason].map(safe));
    auditRows.push([path.basename(entry.test), human.review_required || luna.review_required ? 'YES' : '', human.log ?? '', luna.log ?? '']);
    if (!(luna.classification in tally)) throw new Error(`Unexpected classification: ${luna.classification}`);
    tally[luna.classification]++;
  }
  counts.set(entry.case,tally);
}
if (rawRows.length !== lastDataRow) throw new Error(`Expected ${pairs} case/version rows, found ${rawRows.length-1}`);
exits.getRange(`A1:G${rawRows.length}`).values = rawRows;
details.getRange(`A1:G${detailRows.length}`).values = detailRows;
details.getRange(`I1:L${auditRows.length}`).values = auditRows;
summary.getRange('A1:E1').values = [['Case Number','Versions Tested','Luna PASS','Luna ERROR','Luna FAIL']];
for (let i=0;i<plan.cases.length;i++) {
  const row=i+2;
  summary.getRange(`A${row}`).values=[[plan.cases[i].case]];
  summary.getRange(`C${row}:E${row}`).formulas=[['PASS','ERROR','FAIL'].map(s=>
    `=COUNTIFS('Detailed reasons'!$A$2:$A$${lastDataRow},A${row},'Detailed reasons'!$F$2:$F$${lastDataRow},"${s}")`)];
  summary.getRange(`B${row}`).formulas=[[`=SUM(C${row}:E${row})`]];
}
summary.getRange(`A${totalRow}`).values=[['TOTAL']];
summary.getRange(`B${totalRow}:E${totalRow}`).formulas=[['B','C','D','E'].map(c=>`=SUM(${c}2:${c}${lastCaseRow})`)];
summary.getRange('G1:H7').values=[
  ['Classification','Definition'],
  ['PASS','The selected test ran at least one test, completed with OK, and exited 0.'],
  ['ERROR','Target execution exception, parser/import error, simulator crash, timeout or test setup failure. Reason identifies the observed issue; not automatically model blame.'],
  ['FAIL','Test assertions/output checks fail without a target execution exception established by the traceback. Review may still identify a test-interface issue.'],
  ['NOT TESTED','Pending, could not launch, or no complete unskipped unittest success. Excluded from Versions Tested.'],
  ['Buggy','Copied from the supplied 5.6 workbook, not rerun. Human and 6-Luna are rerun.'],
  ['Review','Reasons are generated from logs, not a fresh semantic review of each question. Check flagged cases before final submission.']
];
summary.getRange('G9:H12').values=[['Batch',`gpt-6-luna / ${plan.cases.length} cases`],['Assigned case/version pairs',pairs],['Planned human + Luna executions',pairs * 2],['Completed processes recorded',records.length]];
summary.getRange('G14:H14').values=[['Metric','Count']];
const metrics=[['Human PASS','D','PASS'],['Human ERROR','D','ERROR'],['Human FAIL','D','FAIL'],['Human NOT TESTED','D','NOT TESTED'],['Luna PASS','F','PASS'],['Luna ERROR','F','ERROR'],['Luna FAIL','F','FAIL'],['Luna NOT TESTED','F','NOT TESTED']];
for (let i=0;i<metrics.length;i++) {
  const [label,col,status]=metrics[i], row=15+i;
  summary.getRange(`G${row}`).values=[[label]];
  summary.getRange(`H${row}`).formulas=[[`=COUNTIFS('Detailed reasons'!$${col}$2:$${col}$${lastDataRow},"${status}")`]];
}
for (const [sheet,last,col] of [[exits,lastDataRow,'G'],[details,lastDataRow,'L'],[summary,Math.max(totalRow,22),'H']]) {
  const range=sheet.getRange(`A1:${col}${last}`);
  range.format.font={name:'Arial',size:10};
  range.format.verticalAlignment='top';
  range.format.rowHeight=22;
  sheet.freezePanes.freezeRows(1);
  sheet.getRange(`A1:${col}1`).format.rowHeight=32;
  sheet.getRange(`A1:${col}1`).format.wrapText=true;
  sheet.getRange('A:A').format.columnWidth=20;
  sheet.getRange('B:D').format.columnWidth=19;
}
for (const [sheet,range] of [[exits,'A1:G1'],[details,'A1:G1'],[details,'I1:L1'],[summary,'A1:E1'],[summary,'G1:H1'],[summary,'G14:H14']]) {
  sheet.getRange(range).format.fill='#D9E5F2';
  sheet.getRange(range).format.font.bold=true;
}
exits.getRange('E:G').format.columnWidth=19;
details.getRange('E:E').format.columnWidth=82;
details.getRange('F:F').format.columnWidth=19;
details.getRange('G:G').format.columnWidth=100;
details.getRange(`E2:G${lastDataRow}`).format.wrapText=true;
details.getRange(`A2:L${lastDataRow}`).format.rowHeight=90;
details.getRange('H:H').format.columnWidth=3;
details.getRange('I:J').format.columnWidth=22;
details.getRange('K:L').format.columnWidth=55;
details.getRange(`K2:L${lastDataRow}`).format.wrapText=true;
summary.getRange('E:E').format.columnWidth=19;
summary.getRange('F:F').format.columnWidth=3;
summary.getRange('G:G').format.columnWidth=30;
summary.getRange('H:H').format.columnWidth=100;
summary.getRange('G2:H7').format.wrapText=true;
summary.getRange('G2:H7').format.rowHeight=55;
summary.getRange(`A${totalRow}:E${totalRow}`).format.font.bold=true;
summary.getRange(`B2:E${totalRow}`).setNumberFormat('0');
wb.recalculate();
const actual=summary.getRange(`A2:E${lastCaseRow}`).values;
for (const [name,tested,pass,error,fail] of actual) {
  const t=counts.get(name);
  if (pass!==t.PASS || error!==t.ERROR || fail!==t.FAIL || tested!==pass+error+fail) throw new Error(`Summary mismatch: ${name}`);
}
const output=path.join(path.dirname(input),'gpt_6_luna_first35_results.xlsx');
const file=await SpreadsheetFile.exportXlsx(wb);
await file.save(output);
console.log(`Workbook saved: ${output}`);
