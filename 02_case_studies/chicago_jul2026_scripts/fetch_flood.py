"""HRRR fields for the 31 Jul - 1 Aug 2026 Chicagoland flooding event."""
import os, pickle, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
SAVE = os.path.join(os.getcwd(), "herbie_data")
from herbie import Herbie

VALID = pd.date_range("2026-07-31 00:00", "2026-08-01 21:00", freq="1h")
LAT0, LAT1, LON0, LON1 = 39.8, 43.8, -92.0, -85.0

GROUPS = [
    ("bulk", ":(CAPE|CIN):(surface|180-0 mb above ground):|:PWAT:|:MSLMA:"
             "|:(TMP|DPT):2 m above ground:|:[UV]GRD:10 m above ground:"
             "|:APCP:surface:0-1 hour acc fcst:|:HGT:level of adiabatic condensation from sfc:"
             "|:REFC:|:GUST:surface:",
     {("cape","surface"):"cape_sfc", ("cin","surface"):"cin_sfc",
      ("cape","pressureFromGroundLayer"):"cape_ml", ("cin","pressureFromGroundLayer"):"cin_ml",
      ("pwat","atmosphereSingleLayer"):"pwat", ("mslma","meanSea"):"mslp",
      ("t2m","heightAboveGround"):"t2m", ("d2m","heightAboveGround"):"d2m",
      ("u10","heightAboveGround"):"u10", ("v10","heightAboveGround"):"v10",
      ("tp","surface"):"apcp1h", ("gh","adiabaticCondensation"):"lcl_agl",
      ("refc","atmosphere"):"refc", ("gust","surface"):"gust"}),
    ("shr6", ":(VUCSH|VVCSH):0-6000 m above ground:",
     {("vucsh","heightAboveGroundLayer"):"ushr_06km", ("vvcsh","heightAboveGroundLayer"):"vshr_06km"}),
    ("stm",  ":[UV]STM:0-6000 m above ground:",
     {("ustm","heightAboveGroundLayer"):"ustm", ("vstm","heightAboveGroundLayer"):"vstm"}),
]

def harvest(ds, mapping, out):
    for v in ds.data_vars:
        tol = ds[v].attrs.get("GRIB_typeOfLevel","?")
        key = mapping.get((v,tol))
        if key: out[key] = ds[v].values.astype("float32")

maps, geo = {}, {}
for vt in VALID:
    H = Herbie(vt - pd.Timedelta(hours=1), model="hrrr", product="sfc", fxx=1, save_dir=SAVE, verbose=False)
    flds = {}
    for name, search, mapping in GROUPS:
        try:
            res = H.xarray(search, remove_grib=False)
            for ds in (res if isinstance(res,list) else [res]):
                harvest(ds, mapping, flds)
                if "lat" not in geo:
                    la = ds.latitude.values
                    lo = np.where(ds.longitude.values>180, ds.longitude.values-360, ds.longitude.values)
                    m = (la>=LAT0)&(la<=LAT1)&(lo>=LON0)&(lo<=LON1)
                    yy,xx = np.where(m)
                    geo["j0"],geo["j1"],geo["i0"],geo["i1"] = yy.min(),yy.max()+1,xx.min(),xx.max()+1
                    geo["lat"]=la[geo["j0"]:geo["j1"], geo["i0"]:geo["i1"]]
                    geo["lon"]=lo[geo["j0"]:geo["j1"], geo["i0"]:geo["i1"]]
        except Exception as e:
            print(f"  {vt:%m-%d %H}Z {name} FAIL {type(e).__name__} {str(e)[:70]}", flush=True)
    j0,j1,i0,i1 = geo["j0"],geo["j1"],geo["i0"],geo["i1"]
    for k,a in flds.items(): maps.setdefault(k, []).append(a[j0:j1, i0:i1])
    print(f"{vt:%m-%d %HZ} ok n={len(flds)}", flush=True)

out = dict(valid=VALID, maps={k: np.stack(v) for k,v in maps.items()},
           lat=geo["lat"], lon=geo["lon"])
pickle.dump(out, open("hrrr_flood.pkl","wb"))
print("saved", len(out["maps"]), "fields", out["lat"].shape)
