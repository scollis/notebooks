"""HRRR pressure-level fields: point soundings + synoptic forcing maps."""
import os, pickle, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
SAVE = os.path.join(os.getcwd(), "herbie_data")
from herbie import Herbie

TIMES = [pd.Timestamp("2026-07-27 12:00"), pd.Timestamp("2026-07-27 15:00"),
         pd.Timestamp("2026-07-27 17:00"), pd.Timestamp("2026-07-27 21:00")]
LAT0, LAT1, LON0, LON1 = 38.5, 45.0, -95.0, -83.0   # wider for synoptic

out = {}
for vt in TIMES:
    H = Herbie(vt, model="hrrr", product="prs", fxx=0, save_dir=SAVE, verbose=False)
    got = {}
    for key, search in [("gh",  ":HGT:\\d+ mb:"), ("t", ":TMP:\\d+ mb:"),
                        ("dpt", ":DPT:\\d+ mb:"), ("u", ":UGRD:\\d+ mb:"),
                        ("v",   ":VGRD:\\d+ mb:"), ("w", ":VVEL:\\d+ mb:"),
                        ("absv",":ABSV:\\d+ mb:"), ("q", ":SPFH:\\d+ mb:")]:
        try:
            res = H.xarray(search, remove_grib=False)
            ds = res[0] if isinstance(res, list) else res
            v = [x for x in ds.data_vars][0]
            got[key] = ds[v]
            if "lat" not in out:
                la = ds.latitude.values
                lo = np.where(ds.longitude.values > 180, ds.longitude.values-360, ds.longitude.values)
                m = (la>=LAT0)&(la<=LAT1)&(lo>=LON0)&(lo<=LON1)
                yy,xx = np.where(m)
                out["j0"],out["j1"],out["i0"],out["i1"] = yy.min(),yy.max()+1,xx.min(),xx.max()+1
                out["lat"]=la[out["j0"]:out["j1"], out["i0"]:out["i1"]]
                out["lon"]=lo[out["j0"]:out["j1"], out["i0"]:out["i1"]]
                out["levels"]=ds.isobaricInhPa.values
        except Exception as e:
            print(f"  {vt:%H}Z {key} FAIL {type(e).__name__} {str(e)[:80]}", flush=True)
    j0,j1,i0,i1 = out["j0"],out["j1"],out["i0"],out["i1"]
    out[str(vt)] = {k: da.values[:, j0:j1, i0:i1].astype("float32") for k,da in got.items()}
    print(f"{vt:%HZ} ok {list(got)} levels={len(out['levels'])}", flush=True)

pickle.dump(out, open("hrrr_prs.pkl","wb"))
print("saved. levels:", out["levels"][:5], "...", out["levels"][-5:], "grid", out["lat"].shape)
