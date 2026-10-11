import json
import os
import sys
import threading
from pathlib import Path
import joblib
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response

SOURCE = Path(os.environ.get('AD_GROWTH_SOURCE', r'D:\PYTHON-project\APO-cdr'))
sys.path.insert(0, str(SOURCE / 'ad_growth_web'))
from data_io import read_csv, inspect_data
from modeling import train, cache_path, save_result

app = FastAPI(title='AI 广告增长优化助手')
lock = threading.Lock()
df, errors = inspect_data(read_csv((SOURCE / 'data/beauty_ad_campaign_5000.csv').read_bytes()))
if errors:
    raise ValueError('；'.join(errors))
cache = SOURCE / 'ad_growth_web/cache'
cached = cache_path(df, cache)
state = dict(df=df, name='beauty_ad_campaign_5000.csv', result=joblib.load(cached) if cached.exists() else None,
             status='ready' if cached.exists() else 'idle', error=None)

def records(frame):
    return json.loads(frame.to_json(orient='records', force_ascii=False))

def result():
    if state['result'] is None:
        raise HTTPException(409, '请先运行模型。')
    return state['result']

@app.get('/api/health')
def health():
    return dict(status=state['status'], error=state['error'], dataset=state['name'])

@app.get('/api/dataset/summary')
def summary():
    frame = state['df']
    arms = []
    for t, label in [(0, '未曝光组'), (1, '曝光组')]:
        g = frame[frame.ad_exposure == t]
        arms.append(dict(name=label, count=len(g), conversions=int((g.purchase_amount > 0).sum()), mean=float(g.purchase_amount.mean()),
                         purchase_rate=float((g.purchase_amount > 0).mean())))
    return dict(name=state['name'], rows=len(frame), columns=len(frame.columns),
                exposure_rate=float(frame.ad_exposure.mean()), arms=arms,
                raw_difference=arms[1]['mean']-arms[0]['mean'])

@app.get('/api/data-quality')
def quality():
    frame = state['df']
    return dict(rows=len(frame), missing=int(frame.isna().sum().sum()),
                duplicate_ids=int(frame.user_id.duplicated().sum()),
                fields=[dict(name=c, dtype=str(frame[c].dtype), missing=int(frame[c].isna().sum())) for c in frame])

@app.get('/api/model/summary')
@app.get('/api/model/validation')
def model_summary():
    r = result()
    counts, edges = np.histogram(r['holdout'].cate_cny, bins=24)
    hist = [dict(name=round(float((a+b)/2), 1), count=int(n)) for a,b,n in zip(edges[:-1],edges[1:],counts)]
    return dict(report=r['report'], curve=records(r['curve'].iloc[::max(1,len(r['curve'])//100)]), histogram=hist)

@app.get('/api/model/segments')
def segments():
    return result()['report']['groups']

@app.get('/api/model/predictions')
def predictions(group: str = '', search: str = '', page: int = 1):
    frame = result()['predictions']
    if group:
        frame = frame[frame.response_group == group]
    if search:
        frame = frame[frame.user_id.astype(str).str.contains(search, regex=False)]
    frame = frame.sort_values('cate_cny', ascending=False)
    start = max(0,page-1)*30
    groups = [dict(name=str(k), count=len(g), cate=float(g.cate_cny.mean()), cost=float(g.ad_cost.mean()),
                   net=float((g.cate_cny-g.ad_cost).mean())) for k,g in result()['predictions'].groupby('response_group')]
    return dict(rows=records(frame.iloc[start:start+30]), total=len(frame), groups=groups)

@app.get('/api/schema')
def schema():
    return dict(markdown=(SOURCE/'data/data_schema.md').read_text(encoding='utf-8-sig'))

@app.post('/api/dataset/upload')
async def upload(file: UploadFile = File(...)):
    raw = await file.read(20*1024*1024+1)
    if len(raw)>20*1024*1024:
        raise HTTPException(413, '文件需小于 20 MB。')
    try:
        new_df, errs = inspect_data(read_csv(raw))
    except Exception as exc:
        raise HTTPException(422, f'CSV 无法读取：{exc}')
    if errs:
        raise HTTPException(422, '；'.join(errs))
    with lock:
        if state['status']=='running':
            raise HTTPException(409, '模型正在运行，请完成后再上传。')
        cp = cache_path(new_df, cache)
        existing = joblib.load(cp) if cp.exists() else None
        state.update(df=new_df, name=Path(file.filename or 'upload.csv').name, result=existing,
                     status='ready' if existing else 'idle', error=None)
    return summary()

@app.post('/api/model/run', status_code=202)
def run_model():
    with lock:
        if state['status']=='running':
            raise HTTPException(409, '模型已经在运行。')
        state.update(status='running', error=None)
        snapshot = state['df'].copy()
    def work():
        try:
            trained = train(snapshot)
            save_result(snapshot, trained, cache)
            with lock:
                state.update(result=trained, status='ready')
        except Exception as exc:
            with lock:
                state.update(status='error', error=str(exc))
    threading.Thread(target=work, daemon=True).start()
    return dict(status='running')

@app.get('/api/download/predictions')
def download_predictions():
    return Response(result()['predictions'].to_csv(index=False).encode('utf-8-sig'), media_type='text/csv',
                    headers={'Content-Disposition':'attachment; filename=predictions.csv'})

@app.get('/api/download/report')
def download_report():
    return Response(json.dumps(result()['report'], ensure_ascii=False, indent=2), media_type='application/json',
                    headers={'Content-Disposition':'attachment; filename=validation_report.json'})

@app.get('/api/download/data')
def download_data():
    return Response(state['df'].to_csv(index=False).encode('utf-8-sig'), media_type='text/csv',
                    headers={'Content-Disposition':'attachment; filename=campaign.csv'})
