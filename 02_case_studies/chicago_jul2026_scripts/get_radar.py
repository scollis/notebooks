"""Download KLOT Level II volumes for the 27 Jul 2026 tornado window from AWS."""
import os, re, datetime as dt, xml.etree.ElementTree as ET, requests

BUCKET = "https://noaa-nexrad-level2.s3.amazonaws.com"
SITE, Y, M, D = "KLOT", 2026, 7, 27
T0, T1 = dt.datetime(2026,7,27,16,15), dt.datetime(2026,7,27,18,30)   # UTC
DEST = "nexrad_scans"; os.makedirs(DEST, exist_ok=True)

def list_keys():
    keys, token = [], None
    prefix = f"{Y}/{M:02d}/{D:02d}/{SITE}/"
    while True:
        p = {"list-type":"2", "prefix":prefix, "max-keys":"1000"}
        if token: p["continuation-token"] = token
        r = requests.get(BUCKET, params=p, timeout=90); r.raise_for_status()
        root = ET.fromstring(r.text)
        ns = {"s3":"http://s3.amazonaws.com/doc/2006-03-01/"}
        for c in root.findall("s3:Contents", ns):
            keys.append(c.find("s3:Key", ns).text)
        tok = root.find("s3:NextContinuationToken", ns)
        if tok is None: break
        token = tok.text
    return keys

def ktime(k):
    m = re.search(r"(\d{8})_(\d{6})", k)
    return dt.datetime.strptime(m.group(1)+m.group(2), "%Y%m%d%H%M%S") if m else None

keys = [k for k in list_keys() if "_MDM" not in k]
sel = sorted([k for k in keys if ktime(k) and T0 <= ktime(k) <= T1], key=ktime)
print(f"{len(keys)} volumes on {Y}-{M:02d}-{D:02d}; {len(sel)} in window", flush=True)

paths = []
for i, k in enumerate(sel):
    out = os.path.join(DEST, os.path.basename(k))
    if not os.path.exists(out) or os.path.getsize(out) < 100_000:
        r = requests.get(f"{BUCKET}/{k}", timeout=300); r.raise_for_status()
        open(out, "wb").write(r.content)
    paths.append(out)
    if i % 5 == 0 or i == len(sel)-1:
        print(f"  {i+1}/{len(sel)} {os.path.basename(k)} {os.path.getsize(out)/1e6:.1f} MB", flush=True)
print("DONE", len(paths))
