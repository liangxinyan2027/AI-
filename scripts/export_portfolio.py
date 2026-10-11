"""Export the approved synthetic analysis for the static portfolio."""
import json
import urllib.request
from pathlib import Path
BASE = 'http://127.0.0.1:8000/api'
OUT = Path(__file__).resolve().parents[1] / 'frontend/public/demo'
def get(path):
    with urllib.request.urlopen(BASE + path, timeout=30) as response:
        return response.read()
def data(path):
    return json.loads(get(path))
OUT.mkdir(parents=True, exist_ok=True)
summary = data('/dataset/summary')
if summary['name'] != 'beauty_ad_campaign_5000.csv':
    raise RuntimeError('Only the approved synthetic portfolio dataset may be exported')
first = data('/model/predictions?page=1')
rows = first['rows']
for page in range(2, (first['total']+29)//30+1):
    rows.extend(data('/model/predictions?page='+str(page))['rows'])
assert len(rows) == summary['rows'] == 5000
snapshot = dict(summary=summary, quality=data('/data-quality'), model=data('/model/summary'), predictions=rows, groups=first['groups'])
(OUT/'snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
for endpoint, filename in [('data','campaign.csv'), ('predictions','predictions.csv'), ('report','validation_report.json')]:
    (OUT/filename).write_bytes(get('/download/'+endpoint))
print('Exported', len(rows), 'synthetic users')
