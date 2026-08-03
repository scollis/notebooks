"""Extend the KLOT volume set back to 13:30 UTC (8:30 am CDT) to capture pre-convective conditions."""
import os, re, requests

Q = ("https://thredds.ucar.edu/thredds/radarServer/nexrad/level2/IDD?stn=KLOT"
     "&time_start=2026-07-27T13:30:00Z&time_end=2026-07-27T16:20:00Z")
BASE = "https://thredds.ucar.edu/thredds/fileServer/nexrad/level2/IDD/"
DEST = "nexrad_scans"; os.makedirs(DEST, exist_ok=True)

names = re.findall(r'<dataset[^>]*name="([^"]+)"[^>]*urlPath="([^"]+)"',
                   requests.get(Q, timeout=90).text)
todo = [(n, u) for n, u in sorted(names) if not os.path.exists(os.path.join(DEST, n))]
print(f"{len(names)} in catalog, {len(todo)} to fetch", flush=True)

for i, (n, u) in enumerate(todo):
    out = os.path.join(DEST, n)
    r = requests.get(BASE + u, timeout=300)
    if r.status_code != 200 or len(r.content) < 100_000:
        print("  skip", n, r.status_code, len(r.content), flush=True); continue
    open(out, "wb").write(r.content)
    if i % 8 == 0 or i == len(todo) - 1:
        print(f"  {i+1}/{len(todo)} {n} {len(r.content)/1e6:.1f} MB", flush=True)
print("DONE", len([f for f in os.listdir(DEST) if f.endswith('.ar2v')]))
