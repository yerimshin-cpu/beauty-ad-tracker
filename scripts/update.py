"""Refresh public Meta ad library snapshots from Apify. Requires APIFY_TOKEN secret."""
import json, os, pathlib, time, urllib.request, urllib.error
ROOT = pathlib.Path(__file__).resolve().parents[1]
TOKEN = os.environ['APIFY_TOKEN']
ACTOR = os.environ.get('APIFY_ACTOR_ID', 'juh6OwzcsI0sdSFsn')
SEARCH = ['SKIN1004_Indonesia', 'Skintific Indonesia', 'Glad2Glow Indonesia', 'LANEIGE Indonesia', 'COSRX Indonesia', 'Wardah Indonesia', 'Garnier Indonesia']
PAYLOAD = {'activeStatus':'active','adType':'all','country':'ID','exactPhrase':False,'includeAdDetails':False,'maxAds':5,'platforms':['facebook','instagram'],'proxyConfiguration':{'useApifyProxy':True,'apifyProxyGroups':['RESIDENTIAL']},'searchTerms':SEARCH,'mediaType':'all','sortBy':'default'}
def api(path, data=None):
    req = urllib.request.Request('https://api.apify.com/v2/'+path, data=None if data is None else json.dumps(data).encode(), headers={'Authorization':'Bearer '+TOKEN,'Content-Type':'application/json'}, method='POST' if data is not None else 'GET')
    with urllib.request.urlopen(req, timeout=90) as res: return json.load(res)
run = api(f'acts/{ACTOR}/runs', PAYLOAD)['data']
run_id = run['id']
for i in range(60):
    state = api(f'actor-runs/{run_id}')['data']
    if state['status'] in ('SUCCEEDED','FAILED','ABORTED','TIMED-OUT'): break
    time.sleep(10)
else: raise RuntimeError('Apify run exceeded 10-minute polling window')
if state['status'] != 'SUCCEEDED': raise RuntimeError('Apify run status: '+state['status'])
items = api(f'datasets/{state["defaultDatasetId"]}/items?clean=true&limit=1000')
if not isinstance(items,list) or not items: raise RuntimeError('No ads collected; keeping last good data.json')
# Exclude unrelated keyword matches using advertiser page names, not text mentions.
allow = ('skin1004','skintific','glad2glow','glad 2 glow','laneige','cosrx','wardah','garnier')
items = [x for x in items if any(k in (x.get('pageName') or '').lower() for k in allow)]
if not items: raise RuntimeError('No matching advertisers; keeping last good data.json')
unique={str(x.get('adArchiveId') or x.get('url')):x for x in items}
(ROOT/'data.json').write_text(json.dumps(list(unique.values()),ensure_ascii=False),encoding='utf-8')
print('Updated public ads:',len(unique))
