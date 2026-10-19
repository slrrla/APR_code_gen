import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { Workbook } from '@oai/artifact-tool';

const base = path.dirname(fileURLToPath(import.meta.url));
const caseDir = path.join(path.dirname(base), 'issue_061');
const records = JSON.parse(await fs.readFile(path.join(base, 'results.json'), 'utf8'));
assert.equal(records.length, 90);
const variants = ['buggy', 'fixed', 'fixed_luna'];
const headers = ['qiskit_version', ...['old', 'new'].flatMap(suite => variants.map(v => `${suite}_${v}`)),
  'old_fixed_luna_reason'];
const versions = [...new Set(records.map(row => row.version))].sort((a,b) => {
  const x=a.split('.').map(Number), y=b.split('.').map(Number);
  return x[0]-y[0] || x[1]-y[1] || x[2]-y[2];
});
assert.equal(versions.length,15);
const matrix = [headers, ...versions.map(version => {
  const get = (suite,variant) => {
    const matching = records.filter(row => row.version===version && row.suite===suite && row.variant===variant);
    assert.equal(matching.length,1);
    assert.equal(matching[0].packages.qiskit,version);
    return matching[0];
  };
  const lunaOld = get('old','fixed_luna');
  return [version, ...['old','new'].flatMap(suite => variants.map(variant => get(suite,variant).status)),
    lunaOld.status==='FAIL' ? 'Print format/order differs from the old test\'s exact call list.' : lunaOld.detail];
})];
const workbook = Workbook.create();
const sheet = workbook.worksheets.add('Results');
sheet.getRange('A1').write(matrix);
workbook.recalculate();
assert.deepEqual(sheet.getRange('A1:H16').values,matrix);
console.log((await workbook.inspect({kind:'table',range:'Results!A1:H3',include:'values',
  tableMaxRows:3,tableMaxCols:8,maxChars:2500})).ndjson);
function field(value) {
  const text=String(value??'');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"','""')}"` : text;
}
const values=sheet.getRange('A1:H16').values;
const csv='\ufeff'+values.map(row=>row.map(field).join(',')).join('\r\n')+'\r\n';
let output=path.join(caseDir,'test_results.csv');
try { await fs.writeFile(output,csv,'utf8'); }
catch(error) {
  if(!['EACCES','EPERM','EBUSY'].includes(error.code)) throw error;
  output=path.join(caseDir,'test_results_hardened.csv');
  await fs.writeFile(output,csv,'utf8');
}
const imported=await Workbook.fromCSV((await fs.readFile(output,'utf8')).replace(/^\ufeff/,''),{sheetName:'Results'});
assert.deepEqual(imported.worksheets.getItem('Results').getRange('A1:H16').values,values);
await fs.writeFile(path.join(base,'csv_output.json'),JSON.stringify({output,versions:15},null,2),'utf8');
console.log('CSV VERIFIED',output);
