import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';

const base = path.dirname(fileURLToPath(import.meta.url));
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(path.join(base, 'validity_before.xlsx')));
const sheet = workbook.worksheets.getItem('Sheet1');
const ids = new Set([772, 790, 927, 858, 901, 921]);
const rows = sheet.getRange('A1:F104').values;
const selected = rows.map((row, i) => ({ row: i + 1, id: Number(row[0]), previous: row[1] }))
  .filter(item => ids.has(item.id));
if (selected.length !== ids.size || new Set(selected.map(item => item.id)).size !== ids.size) {
  throw new Error('Expected exactly one row per requested case');
}
console.log(JSON.stringify(selected));
console.log((await workbook.inspect({ kind: 'table', range: 'Sheet1!A75:D98', include: 'values,formulas', tableMaxRows: 24, tableMaxCols: 4, maxChars: 4500 })).ndjson);
const before = await workbook.render({ sheetName: 'Sheet1', range: 'A75:D98', scale: 1.5, format: 'png' });
await fs.writeFile(path.join(base, 'validity_before.png'), new Uint8Array(await before.arrayBuffer()));
if (process.argv.includes('--edit')) {
  for (const item of selected) sheet.getRange(`B${item.row}`).values = [['p']];
  workbook.recalculate();
  for (const item of selected) {
    if (sheet.getRange(`B${item.row}`).values[0][0] !== 'p') throw new Error('P update failed');
  }
  const after = await workbook.render({ sheetName: 'Sheet1', range: 'A75:D98', scale: 1.5, format: 'png' });
  await fs.writeFile(path.join(base, 'validity_after.png'), new Uint8Array(await after.arrayBuffer()));
  const blob = await SpreadsheetFile.exportXlsx(workbook);
  await blob.save(path.join(base, 'validity_updated.xlsx'));
  await fs.writeFile(path.join(base, 'validity_changes.json'), JSON.stringify(selected.map(item => ({ ...item, updated: 'p' })), null, 2));
  console.log('Updated exactly six validity cells.');
}
