"""GFS land-surface fields along the 27 Jul 2026 moisture advection path.

Two questions:
 1. Was the soil wet along the trajectory (so parcels lost little moisture to a
    thirsty surface, and could even gain from evapotranspiration)?
 2. How was surface energy partitioned - latent (evaporative) vs sensible heat?
    A high evaporative fraction means the land was ADDING vapour to the parcel.

Soil moisture (SOILW) comes from the fxx=0 analysis; turbulent fluxes are
time-averaged so they come from the 0-6 h forecast of the preceding cycle.
"""
import os, pickle, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
SAVE = os.path.join(os.getcwd(), "herbie_data")
from herbie import Herbie

LAT0, LAT1 = 15.0, 52.0
LON0, LON1 = -110.0, -70.0
DAYS = pd.date_range("2026-07-23", "2026-07-27", freq="1D")

out = {"days": [str(d.date()) for d in DAYS]}
geo = False

def clip(ds, key):
    global geo
    la = ds.latitude.values
    lo = ds.longitude.values
    lo180 = np.where(lo > 180, lo - 360, lo)
    ji = np.where((la >= LAT0) & (la <= LAT1))[0]
    ii = np.where((lo180 >= LON0) & (lo180 <= LON1))[0]
    if not geo:
        out["lat"] = la[ji].astype("float32")
        out["lon"] = lo180[ii].astype("float32")
        out["_ji"], out["_ii"] = ji, ii
        geo = True
    v = [x for x in ds.data_vars][0]
    a = ds[v].values
    if a.ndim == 3:                      # (level, lat, lon) - SOILW comes stacked
        return a[:, out["_ji"], :][:, :, out["_ii"]].astype("float32")
    return a[out["_ji"], :][:, out["_ii"]].astype("float32")

for d in DAYS:
    rec = {}
    # --- analysis at 12Z: soil moisture (4 layers) + land mask ---
    Ha = Herbie(d + pd.Timedelta(hours=12), model="gfs", product="pgrb2.0p25",
                fxx=0, save_dir=SAVE, verbose=False)
    res = Ha.xarray(":SOILW:", remove_grib=False)
    dss = res if isinstance(res, list) else [res]
    sm = {}
    for ds in dss:
        arr = clip(ds, "soilw")                       # (level, lat, lon) or (lat, lon)
        tops = np.atleast_1d(ds.depthBelowLandLayer.values).astype(float)
        if arr.ndim == 3:
            for k, t in enumerate(tops):
                sm[round(float(t), 2)] = arr[k]
        else:
            sm[round(float(tops[0]), 2)] = arr
    rec["soilw"] = sm
    for key, srch in [("land", ":LAND:surface:"), ("veg", ":VEG:surface:")]:
        try:
            r = Ha.xarray(srch, remove_grib=False)
            rec[key] = clip(r[0] if isinstance(r, list) else r, key)
        except Exception as e:
            print(f"  {d.date()} {key} skip {type(e).__name__}")

    # --- 0-6 h averaged fluxes from the 06Z cycle (covers midday heating) ---
    Hf = Herbie(d + pd.Timedelta(hours=6), model="gfs", product="pgrb2.0p25",
                fxx=6, save_dir=SAVE, verbose=False)
    for key, srch in [("lhtfl", ":LHTFL:surface:"), ("shtfl", ":SHTFL:surface:"),
                      ("apcp", ":APCP:surface:")]:
        try:
            r = Hf.xarray(srch, remove_grib=False)
            ds = r[0] if isinstance(r, list) else r
            rec[key] = clip(ds, key)
        except Exception as e:
            print(f"  {d.date()} {key} FAIL {type(e).__name__} {str(e)[:60]}")
    out[str(d.date())] = rec
    print(f"{d.date()} ok  soil layers {sorted(sm)}  keys {sorted(rec)}", flush=True)

pickle.dump(out, open("gfs_land.pkl", "wb"))
print("saved gfs_land.pkl | grid", out["lat"].shape, out["lon"].shape)
