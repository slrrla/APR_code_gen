import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';

const base = path.dirname(fileURLToPath(import.meta.url));
const selection = JSON.parse(await fs.readFile(path.join(base, 'selection.json'), 'utf8'));
const item = selection.cases[0];
if (selection.cases.length !== 1 || item.case !== 'issue_827') throw new Error('Expected only case 827');
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(path.join(base, 'validity_before.xlsx')));
const sheet = workbook.worksheets.getItem(item.sheet);
if (Number(sheet.getRange(`A${item.row}`).values[0][0]) !== 827) throw new Error('Case row mismatch');
if (sheet.getRange(item.workbook_cell).values[0][0] !== item.validity_before) throw new Error('Original validity mismatch');
console.log((await workbook.inspect({ kind: 'table', range: `${item.sheet}!A85:D89`, include: 'values,formulas', tableMaxRows: 5, tableMaxCols: 4, maxChars: 2000 })).ndjson);
const before = await workbook.render({ sheetName: item.sheet, range: 'A85:D89', scale: 1.5, format: 'png' });
await fs.writeFile(path.join(base, 'validity_before.png'), new Uint8Array(await before.arrayBuffer()));
if (process.argv.includes('--edit')) {
  sheet.getRange(item.workbook_cell).values = [['p']];
  workbook.recalculate();
  if (sheet.getRange(item.workbook_cell).values[0][0] !== 'p') throw new Error('P update failed');
  const after = await workbook.render({ sheetName: item.sheet, range: 'A85:D89', scale: 1.5, format: 'png' });
  await fs.writeFile(path.join(base, 'validity_after.png'), new Uint8Array(await after.arrayBuffer()));
  await (await SpreadsheetFile.exportXlsx(workbook)).save(path.join(base, 'validity_updated.xlsx'));
  console.log(`Updated ${item.sheet}!${item.workbook_cell} to p.`);
}
