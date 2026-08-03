"""GFS 0.25deg analysis fields for moisture-source diagnosis of the 27 Jul 2026 event.

Domain spans the Gulf of Mexico to the Great Lakes so integrated vapour transport
(IVT) and back trajectories can attribute the moisture to a source region.
Window runs 23 Jul -> 28 Jul at 6-h analysis steps: four days of upstream history
is enough to trace parcels back to the Gulf at typical 850 hPa speeds.
"""
import os, pickle, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
SAVE = os.path.join(os.getcwd(), "herbie_data")
from herbie import Herbie

# continental domain: Gulf coast + Caribbean edge up through the Great Lakes
LAT0, LAT1 = 15.0, 52.0
LON0, LON1 = -110.0, -70.0

# levels for the moisture-flux integral (surface -> 300 hPa carries ~all vapour)
LEVS = [1000, 975, 950, 925, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300]

TIMES = pd.date_range("2026-07-23 00:00", "2026-07-28 00:00", freq="6h")

def sub_ll(ds):
    """GFS is 0..360 lon, ascending lat. Return (lat2d, lon2d, slices)."""
    la = ds.latitude.values
    lo = ds.longitude.values
    lo180 = np.where(lo > 180, lo - 360, lo)
    ji = np.where((la >= LAT0) & (la <= LAT1))[0]
    ii = np.where((lo180 >= LON0) & (lo180 <= LON1))[0]
    return ji, ii, la[ji], lo180[ii]

out = {"levels": np.array(LEVS, dtype="float32"), "times": [str(t) for t in TIMES]}
geo_done = False

for t in TIMES:
    try:
        H = Herbie(t, model="gfs", product="pgrb2.0p25", fxx=0, save_dir=SAVE, verbose=False)
        rec = {}
        for key, srch in [("q", r":SPFH:(%s) mb:" % "|".join(str(L) for L in LEVS)),
                          ("u", r":UGRD:(%s) mb:" % "|".join(str(L) for L in LEVS)),
                          ("v", r":VGRD:(%s) mb:" % "|".join(str(L) for L in LEVS))]:
            res = H.xarray(srch, remove_grib=False)
            ds = res[0] if isinstance(res, list) else res
            var = [v for v in ds.data_vars][0]
            lev = ds.isobaricInhPa.values
            order = [int(np.where(lev == L)[0][0]) for L in LEVS]
            if not geo_done:
                ji, ii, lat1d, lon1d = sub_ll(ds)
                out["lat"] = lat1d.astype("float32")
                out["lon"] = lon1d.astype("float32")
                out["_ji"], out["_ii"] = ji, ii
                geo_done = True
            arr = ds[var].values[order][:, out["_ji"], :][:, :, out["_ii"]]
            rec[key] = arr.astype("float32")
        # column PWAT for context
        res = H.xarray(":PWAT:entire atmosphere", remove_grib=False)
        dsp = res[0] if isinstance(res, list) else res
        vp = [v for v in dsp.data_vars][0]
        rec["pwat"] = dsp[vp].values[out["_ji"], :][:, out["_ii"]].astype("float32")
        out[str(t)] = rec
        print(f"{t:%m-%d %HZ} ok  q{rec['q'].shape}", flush=True)
    except Exception as e:
        print(f"{t:%m-%d %HZ} FAIL {type(e).__name__} {str(e)[:70]}", flush=True)

pickle.dump(out, open("gfs_moisture.pkl", "wb"))
print("saved gfs_moisture.pkl | grid", out["lat"].shape, out["lon"].shape)
