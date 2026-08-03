"""July precipitable-water climatology from observed radiosondes.

Computes PWAT by integrating the observed moisture profile for every July
sounding at the Chicagoland-relevant upper-air sites, so the 27 Jul 2026 value
can be placed as a percentile of the real observed distribution rather than
against a model.

PWAT = (1/(rho_w * g)) * integral of q dp, surface -> 300 hPa.
"""
import io, os, pickle, warnings, numpy as np, pandas as pd, requests, time
warnings.filterwarnings("ignore")

STNS = ["KILX", "KDVN", "KGRB"]      # Lincoln IL (upstream), Quad Cities, Green Bay
YEARS = range(2000, 2027)
G = 9.80665
RHOW = 1000.0

def esat_hpa(tc):
    """Saturation vapour pressure, Bolton (1980), hPa."""
    return 6.112 * np.exp(17.67 * tc / (tc + 243.5))

def pwat_mm(p_hpa, tc, tdc, ptop=300.0):
    """Integrate specific humidity over pressure. Returns mm."""
    m = np.isfinite(p_hpa) & np.isfinite(tc) & np.isfinite(tdc)
    p, td = p_hpa[m], tdc[m]
    if p.size < 5:
        return np.nan
    o = np.argsort(-p)                     # surface first
    p, td = p[o], td[o]
    keep = p >= ptop
    p, td = p[keep], td[keep]
    if p.size < 5 or p[0] < 800:           # need a real surface-based profile
        return np.nan
    e = esat_hpa(td)                       # actual vapour pressure from dewpoint
    w = 0.622 * e / (p - e)                # mixing ratio (kg/kg)
    q = w / (1.0 + w)                      # specific humidity
    # integral q dp with p in Pa, descending -> negate
    return float(-np.trapezoid(q, p * 100.0) / (RHOW * G) * 1000.0)

rows = []
for stn in STNS:
    for yr in YEARS:
        u = ("https://mesonet.agron.iastate.edu/cgi-bin/request/raob.py?"
             f"station={stn}&sts={yr}-07-01T00:00Z&ets={yr}-08-01T00:00Z&fmt=csv")
        for attempt in range(3):
            try:
                txt = requests.get(u, timeout=300).text
                d = pd.read_csv(io.StringIO(txt), na_values=["M", ""])
                break
            except Exception as e:
                if attempt == 2:
                    print(f"  {stn} {yr} FAIL {type(e).__name__}", flush=True)
                    d = None
                time.sleep(5)
        if d is None or not len(d) or "validUTC" not in d.columns:
            continue
        d["validUTC"] = pd.to_datetime(d.validUTC)
        n = 0
        for t, g in d.groupby("validUTC"):
            pw = pwat_mm(g.pressure_mb.values, g.tmpc.values, g.dwpc.values)
            if np.isfinite(pw):
                rows.append(dict(station=stn, valid=t, pwat_mm=pw))
                n += 1
        print(f"{stn} {yr}: {n} soundings", flush=True)

PW = pd.DataFrame(rows)
PW.to_csv("pwat_climatology_july.csv", index=False)
print("total soundings:", len(PW))
print(PW.groupby("station").pwat_mm.describe().round(1).to_string())
