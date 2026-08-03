"""Extract HRRR severe-weather fields over Chicagoland for the 27 Jul 2026 event.

Uses F01 from each hourly cycle: gives the 'max in previous hour' diagnostics
(MXUPHL, MAXUVV, APCP) that the F00 analysis does not carry, while staying
close to the analysis state.
"""
import os, pickle, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")

SAVE = os.path.join(os.getcwd(), "herbie_data"); os.makedirs(SAVE, exist_ok=True)
from herbie import Herbie

# Valid times 12Z 27 Jul -> 06Z 28 Jul  (cycle = valid - 1h, fxx=1)
VALID = pd.date_range("2026-07-27 12:00", "2026-07-28 06:00", freq="1h", tz=None)

# Sub-domain kept for maps
LAT0, LAT1, LON0, LON1 = 39.8, 43.8, -92.0, -85.0

# (name, search string, [(varname, typeOfLevel, level) -> outkey])
GROUPS = [
    ("bulk", ":(CAPE|CIN):(surface|180-0 mb above ground):|:PWAT:|:MSLMA:|:GUST:surface:"
             "|:HPBL:surface:|:(TMP|DPT):2 m above ground:|:[UV]GRD:10 m above ground:"
             "|:APCP:surface:0-1 hour acc fcst:|:HGT:level of adiabatic condensation from sfc:"
             "|:(REFC|VIL|LTNG):|:RETOP:cloud top:",
     {("cape", "surface"): "cape_sfc", ("cin", "surface"): "cin_sfc",
      ("cape", "pressureFromGroundLayer"): "cape_ml", ("cin", "pressureFromGroundLayer"): "cin_ml",
      ("pwat", "atmosphereSingleLayer"): "pwat", ("mslma", "meanSea"): "mslp",
      ("gust", "surface"): "gust", ("blh", "surface"): "pblh",
      ("t2m", "heightAboveGround"): "t2m", ("d2m", "heightAboveGround"): "d2m",
      ("u10", "heightAboveGround"): "u10", ("v10", "heightAboveGround"): "v10",
      ("tp", "surface"): "apcp1h", ("gh", "adiabaticCondensation"): "lcl_agl",
      ("refc", "atmosphere"): "refc", ("veril", "atmosphere"): "vil",
      ("ltng", "atmosphere"): "ltng", ("unknown", "cloudTop"): "echotop"}),
    ("cape03", ":CAPE:0-3000 m above ground:", {("cape", "heightAboveGroundLayer"): "cape_03km"}),
    ("srh",    ":HLCY:", {("hlcy", "heightAboveGroundLayer", 3000.0): "srh_03km",
                          ("hlcy", "heightAboveGroundLayer", 1000.0): "srh_01km"}),
    ("shr6",   ":(VUCSH|VVCSH):0-6000 m above ground:",
     {("vucsh", "heightAboveGroundLayer"): "ushr_06km", ("vvcsh", "heightAboveGroundLayer"): "vshr_06km"}),
    ("shr1",   ":(VUCSH|VVCSH):0-1000 m above ground:",
     {("vucsh", "heightAboveGroundLayer"): "ushr_01km", ("vvcsh", "heightAboveGroundLayer"): "vshr_01km"}),
    ("stm",    ":[UV]STM:0-6000 m above ground:",
     {("ustm", "heightAboveGroundLayer"): "ustm", ("vstm", "heightAboveGroundLayer"): "vstm"}),
    ("uh25",   ":MXUPHL:2000-0 m above ground:", {("unknown", "heightAboveGroundLayer"): "uh_02km"}),
    ("uh52",   ":MXUPHL:5000-2000 m above ground:", {("unknown", "heightAboveGroundLayer"): "uh_25km"}),
    ("uvv",    ":MAXUVV:", {("unknown", "pressureFromGroundLayer"): "maxuvv"}),
]


def harvest(ds, mapping, out):
    for v in ds.data_vars:
        tol = ds[v].attrs.get("GRIB_typeOfLevel", "?")
        lev = float(ds[tol].values) if tol in ds.coords and ds[tol].size == 1 else None
        key = mapping.get((v, tol, lev)) or mapping.get((v, tol))
        if key:
            out[key] = ds[v].values.astype("float32")


rows, maps, geo = [], {}, {}
for ti, vt in enumerate(VALID):
    cycle = vt - pd.Timedelta(hours=1)
    H = Herbie(cycle, model="hrrr", product="sfc", fxx=1, save_dir=SAVE, verbose=False)
    flds = {}
    for name, search, mapping in GROUPS:
        try:
            res = H.xarray(search, remove_grib=False)
            for ds in (res if isinstance(res, list) else [res]):
                harvest(ds, mapping, flds)
                if "lat" not in geo:
                    la = ds.latitude.values
                    lo = np.where(ds.longitude.values > 180, ds.longitude.values - 360, ds.longitude.values)
                    geo["lat"], geo["lon"] = la, lo
        except Exception as e:
            print(f"  {vt:%H}Z {name} FAIL {type(e).__name__} {str(e)[:90]}", flush=True)
    if "lat" in geo and "jy" not in geo:
        la, lo = geo["lat"], geo["lon"]
        m = (la >= LAT0) & (la <= LAT1) & (lo >= LON0) & (lo <= LON1)
        yy, xx = np.where(m)
        geo["j0"], geo["j1"], geo["i0"], geo["i1"] = yy.min(), yy.max() + 1, xx.min(), xx.max() + 1
        geo["jy"] = True
    j0, j1, i0, i1 = geo["j0"], geo["j1"], geo["i0"], geo["i1"]
    for k, a in flds.items():
        maps.setdefault(k, []).append(a[j0:j1, i0:i1])
    print(f"{vt:%Y-%m-%d %HZ} ok  nfields={len(flds)}", flush=True)

out = dict(valid=VALID, maps={k: np.stack(v) for k, v in maps.items()},
           lat=geo["lat"][geo["j0"]:geo["j1"], geo["i0"]:geo["i1"]],
           lon=geo["lon"][geo["j0"]:geo["j1"], geo["i0"]:geo["i1"]])
pickle.dump(out, open("hrrr_chicago_20260727.pkl", "wb"))
print("saved", {k: v.shape for k, v in list(out["maps"].items())[:3]}, "nfields", len(out["maps"]))
