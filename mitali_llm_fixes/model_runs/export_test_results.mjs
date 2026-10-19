import fs from 'node:fs/promises';
import { SpreadsheetFile, Workbook } from '@oai/artifact-tool';

const [input, output] = process.argv.slice(2);
if (!input || !output) throw Error('Usage: node export_test_results.mjs results.json output.xlsx');
const { plan, records } = JSON.parse(await fs.readFile(input, 'utf8'));
const index = new Map();
for (const r of records) {
  const key = `${r.case}|${r.version}|${r.target}`;
  if (index.has(key)) throw Error(`Duplicate test result: ${key}`);
  index.set(key, r);
}
const wb = Workbook.create();
const exits = wb.worksheets.add('Exit results');
const details = wb.worksheets.add('Detailed reasons');
const summary = wb.worksheets.add('Summary');
const raw = [['Case Number', 'Qiskit Version', 'Buggy Result', 'Human Fix Result', 'Luna Fix Result',
  'Human Exit Code', 'Luna Exit Code', 'Buggy Exit Code', 'Test File', 'Buggy Log', 'Human Log', 'Luna Log']];
const reviewed = [['Case Number', 'Qiskit Version', 'Buggy Result', 'Human Fix Result', 'Reason',
  'Luna Fix Result', 'Luna Reason', 'Review Required', 'Test File', 'Buggy Log', 'Human Log', 'Luna Log']];
const get = (entry, version, target) => index.get(`${entry.case}|${version}|${target}`);
for (const entry of plan.cases) {
  for (const version of entry.versions) {
    const b = get(entry, version, 'BUGGY');
    const h = get(entry, version, 'HUMAN_FIXED');
    const l = get(entry, version, 'LUNA_FIXED');
    raw.push([entry.case, version, b?.raw_result ?? 'NOT RUN', h?.raw_result ?? 'NOT RUN', l?.raw_result ?? 'NOT RUN',
      h?.exit_code ?? null, l?.exit_code ?? null, b?.exit_code ?? null,
      entry.test, b?.log ?? '', h?.log ?? '', l?.log ?? '']);
    reviewed.push([entry.case, version, b?.raw_result ?? 'NOT RUN', h?.classification ?? 'NOT RUN',
      h?.reason ?? 'Not yet tested.', l?.classification ?? 'NOT RUN', l?.reason ?? 'Not yet tested.',
      h?.review_required || l?.review_required ? 'YES' : (h && l ? 'NO' : 'PENDING'),
      entry.test, b?.log ?? '', h?.log ?? '', l?.log ?? '']);
  }
}
const last = raw.length;
const literal = v => typeof v === 'string' && /^[=+@]/.test(v) ? `'${v}` : v;
exits.getRange(`A1:L${last}`).values = raw.map(row => row.map(literal));
details.getRange(`A1:L${last}`).values = reviewed.map(row => row.map(literal));
for (const sheet of [exits, details]) {
  sheet.showGridLines = true;
  sheet.getRange(`A1:L${last}`).format.font = { name: 'Arial', size: 10 };
  sheet.getRange(`A1:L${last}`).format.verticalAlignment = 'top';
  sheet.getRange(`A1:L${last}`).format.rowHeight = 25;
  sheet.getRange('A1:L1').format.font.bold = true;
  sheet.getRange('A1:L1').format.rowHeight = 32;
  sheet.getRange('A1:L1').format.wrapText = true;
  sheet.getRange('A1:L1').format.borders = { bottom: { style: 'thin', color: '#888888' } };
  sheet.freezePanes.freezeRows(1);
  for (const [col, width] of [['A',18],['B',17],['C',17],['D',20],['E',20],['F',20],['G',20],['H',18],['I',55],['J',55],['K',55],['L',55]]) {
    sheet.getRange(`${col}1:${col}${last}`).format.columnWidth = width;
  }
  sheet.getRange(`I2:L${last}`).format.wrapText = true;
}
exits.getRange(`F2:H${last}`).setNumberFormat('0');
details.getRange(`E1:E${last}`).format.columnWidth = 75;
details.getRange(`G1:G${last}`).format.columnWidth = 85;
details.getRange(`E2:E${last}`).format.wrapText = true;
details.getRange(`G2:G${last}`).format.wrapText = true;
const lineCount = (value, size) => String(value || '').split('\n').reduce((n, line) => n + Math.max(1, Math.ceil(line.length / size)), 0);
for (let r = 2; r <= last; r++) {
  const lines = Math.max(lineCount(reviewed[r-1][4], 72), lineCount(reviewed[r-1][6], 82),
    ...reviewed[r-1].slice(8).map(v => lineCount(v, 52)));
  details.getRange(`A${r}:L${r}`).format.rowHeight = Math.max(28, lines * 14 + 8);
  exits.getRange(`A${r}:L${r}`).format.rowHeight = Math.max(28, ...raw[r-1].slice(8).map(v => lineCount(v, 52) * 14 + 8));
}
details.getRange('N1:O1').values = [['Metric', 'Count']];
const metrics = [['Human PASS','D','PASS'],['Human ERROR','D','ERROR'],['Human FAIL','D','FAIL'],
  ['Luna PASS','F','PASS'],['Luna ERROR','F','ERROR'],['Luna FAIL','F','FAIL'],['Luna NOT RUN','F','NOT RUN']];
details.getRange('N2:N8').values = metrics.map(r=>[r[0]]);
details.getRange('O2:O8').formulas = metrics.map(r=>[`=COUNTIF(${r[1]}2:${r[1]}${last},"${r[2]}")`]);
details.getRange('N10:O12').values = [['Model',plan.model],['Reasoning effort','medium'],
  ['Reason source','Recorded tests; non-PASS rows require attribution review.']];
details.getRange('N1:N12').format.columnWidth = 23;
details.getRange('O1:O12').format.columnWidth = 70;
details.getRange('O12').format.wrapText = true;

const countCases = plan.cases.length;
const summaryEnd = countCases + 1;
summary.getRange('A1:G1').values = [['Case Number','Versions Tested','Luna PASS','Luna ERROR','Luna FAIL','Assigned Versions','Pending']];
summary.getRange(`A2:A${summaryEnd}`).values = plan.cases.map(c=>[c.case]);
summary.getRange(`F2:F${summaryEnd}`).values = plan.cases.map(c=>[c.versions.length]);
summary.getRange(`B2:E${summaryEnd}`).formulas = plan.cases.map((c,i)=>{
  const r=i+2;
  return [`=SUM(C${r}:E${r})`, ...['PASS','ERROR','FAIL'].map(s=>`=COUNTIFS('Detailed reasons'!$A$2:$A$${last},A${r},'Detailed reasons'!$F$2:$F$${last},"${s}")`)];
});
summary.getRange(`G2:G${summaryEnd}`).formulas = plan.cases.map((c,i)=>[`=F${i+2}-B${i+2}`]);
const totals = summaryEnd + 1;
summary.getRange(`A${totals}`).values = [['TOTAL']];
summary.getRange(`B${totals}:G${totals}`).formulas = [['B','C','D','E','F','G'].map(col=>`=SUM(${col}2:${col}${summaryEnd})`)];
summary.getRange(`A1:G${totals}`).format.font = { name:'Arial',size:10 };
summary.getRange(`A1:G${totals}`).format.columnWidth = 20;
summary.getRange(`A1:G${totals}`).format.rowHeight = 25;
summary.getRange('A1:G1').format.font.bold = true;
summary.getRange(`A${totals}:G${totals}`).format.font.bold = true;
summary.getRange(`B2:G${totals}`).setNumberFormat('0');
summary.freezePanes.freezeRows(1);
summary.getRange('I1:J1').values = [['Classification','Definition']];
summary.getRange('I2:J9').values = [
  ['PASS','All recorded tests completed successfully. This is a test result, not independent proof of correctness.'],
  ['ERROR','Target/test setup cannot complete, including runtime exceptions, native crashes and timeouts. Reason identifies the observed stop.'],
  ['FAIL','Output, behavior or required interface does not satisfy a test. Test-side output inspection errors are included here.'],
  ['NOT RUN','No completed run yet. Never counted as PASS, ERROR or FAIL.'],
  ['Review required','Non-PASS results need review to distinguish model mistakes from test/environment issues. No manual review is claimed.'],
  ['Versions tested','Completed Luna attempts, including ERROR. Assigned and pending versions remain separate.'],
  ['Source', 'Per-target console.log, unittest.json and result.json files in this batch; versions from valid_104 column D.'],
  ['Model',plan.model]
];
summary.getRange('I1:I9').format.columnWidth = 23;
summary.getRange('J1:J9').format.columnWidth = 90;
summary.getRange('I1:J9').format.font = {name:'Arial',size:10};
summary.getRange('J1:J9').format.wrapText = true;
for(let r=2;r<=9;r++) summary.getRange(`A${r}:J${r}`).format.rowHeight = 50;
wb.recalculate();
for(let i=0;i<countCases;i++) {
  const entry=plan.cases[i];
  const results=records.filter(r=>r.case===entry.case&&r.target==='LUNA_FIXED');
  const counts=['PASS','ERROR','FAIL'].map(s=>results.filter(r=>r.classification===s).length);
  const expected=[results.length,...counts,entry.versions.length,entry.versions.length-results.length];
  const actual=summary.getRange(`B${i+2}:G${i+2}`).values[0];
  if(JSON.stringify(expected)!==JSON.stringify(actual)) throw Error(`Summary mismatch: ${entry.case}`);
}
const completed=records.filter(r=>r.target==='LUNA_FIXED').length;
if(summary.getRange(`B${totals}`).values[0][0]!==completed) throw Error('Total count mismatch');
const xlsx=await SpreadsheetFile.exportXlsx(wb);
const temp=output+'.tmp.xlsx';
await xlsx.save(temp);
await fs.rename(temp,output);
console.log(`Workbook saved: ${output}. Completed Luna versions: ${completed}/${last-1}.`);
if(process.env.APR_RENDER_PREVIEW==='1') {
  const preview=await wb.render({sheetName:'Summary',range:'A1:G8',scale:1,format:'png'});
  await fs.writeFile(output+'.preview.png',new Uint8Array(await preview.arrayBuffer()));
}
