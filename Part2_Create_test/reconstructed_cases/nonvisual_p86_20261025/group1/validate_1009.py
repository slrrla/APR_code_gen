from pathlib import Path
import json
import run_group

rows = []
for version in ('0_25_0', '0_46_3'):
    for variant in ('fixed', 'buggy'):
        row = run_group.run(({'case':'issue_1009', 'version':version}, variant))
        # Preserve version-specific evidence because run_group's usual paths are single-version pilots.
        source = Path(row['log'])
        destination = source.with_name(version+'_'+variant+'.log')
        destination.write_bytes(source.read_bytes())
        row['log'] = str(destination)
        rows.append(row)
(Path(__file__).parent/'results_1009.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
