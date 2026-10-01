import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { Workbook } from '@oai/artifact-tool';

const base = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(base);
const records = JSON.parse(await fs.readFile(path.join(base, 'results.json'), 'utf8'));
assert.equal(records.length, 144);
const variants = ['buggy', 'fixed', 'fixed_luna'];
const headers = ['qiskit_version',
  ...['old', 'new'].flatMap(suite => variants.map(variant => `${suite}_${variant}`)),
  'old_fixed_luna_reason'];

function csvField(value) {
  const text = String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

for (const caseName of ['issue_021_se', 'issue_058_se']) {
  const rows = records.filter(row => row.case === caseName);
  assert.equal(rows.length, 72);
  const versions = [...new Set(rows.map(row => row.version))].sort((a, b) => {
    const x = a.split('.').map(Number), y = b.split('.').map(Number);
    return x[0]-y[0] || x[1]-y[1] || x[2]-y[2];
  });
  assert.equal(versions.length, 12);
  const matrix = [headers, ...versions.map(version => {
    const byVersion = rows.filter(row => row.version === version);
    const get = (suite, variant) => {
      const matches = byVersion.filter(row => row.suite === suite && row.variant === variant);
      assert.equal(matches.length, 1);
      return matches[0];
    };
    const packages = byVersion[0].packages;
    assert.equal(packages.qiskit, version);
    return [version,
      ...['old', 'new'].flatMap(suite => variants.map(variant => get(suite, variant).status)),
      get('old', 'fixed_luna').detail];
  })];
  const workbook = Workbook.create();
  const sheet = workbook.worksheets.add('Results');
  sheet.getRange('A1').write(matrix);
  workbook.recalculate();
  assert.deepEqual(sheet.getRange('A1:H13').values, matrix);
  console.log(caseName, (await workbook.inspect({kind: 'table', range: 'Results!A1:H3',
    include: 'values', tableMaxRows: 3, tableMaxCols: 8, maxChars: 3000})).ndjson);
  // CSV has no formatting or formulas. Export the verified cell values as RFC 4180 text.
  const values = sheet.getRange('A1:H13').values;
  const csv = '\ufeff' + values.map(row => row.map(csvField).join(',')).join('\r\n') + '\r\n';
  const output = path.join(root, caseName, 'test_results.csv');
  await fs.writeFile(output, csv, 'utf8');
  const imported = await Workbook.fromCSV((await fs.readFile(output, 'utf8')).replace(/^\ufeff/, ''), {sheetName: 'Results'});
  assert.deepEqual(imported.worksheets.getItem('Results').getRange('A1:H13').values, values);
  console.log('CSV VERIFIED', output, versions.length, 'versions');
}
