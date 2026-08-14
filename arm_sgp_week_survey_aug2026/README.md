# ARM SGP week survey, 6-13 August 2026

Southern Great Plains observatory, one week, 46 live datastreams. Built from ARM Live + ACT,
with one NEXRAD Level II frame from the Unidata IDD. All colormaps from `cmweather`.

## The finding

**The week had one weather event and five days of nothing.** All measurable rain fell on
6-7 August; 8-12 August were five consecutive cloud-free days. The value of a
multi-instrument site is that surface radiation, cloud radar, ceilometer, microwave
radiometer and the surface energy balance each resolve that same break independently.

| | Wet regime (Aug 6-7) | Dry regime (Aug 8-12) |
|---|---|---|
| Daily insolation at C1 | 8.9-12.2 MJ m-2 (33-45 % of clear-sky) | 25.5-26.3 MJ m-2 (95-99 %) |
| Diffuse fraction | 0.82 | 0.21 |
| KAZR cloud fraction > 5 km | 0.52 | 0.00-0.02 |
| Median cloud top | 9.6-9.8 km | 3.5-3.9 km |
| Ceilometer cloudy fraction | 0.40-0.43 | 0.00-0.02 |
| Daily p99 reflectivity | +22 to +27 dBZ | -4.6 to -10.2 dBZ |
| Midday Bowen ratio | 0.31 (Aug 7) | 3.90 by Aug 11 |

## Precipitation was convective and patchy

Weekly totals ranged from **13.09 mm at E32** to **exactly zero at E33 and E37** — facilities
51 km apart. Any single-gauge weekly total for "SGP" would be wrong by an order of magnitude
depending on which gauge you picked.

| Facility | Range/bearing from C1 | Weekly precip |
|---|---|---|
| E13 | 0.3 km SE | 5.67 mm |
| E32 | 37.8 km NW | 13.09 mm |
| E33 | 50.6 km NE | 0.00 mm |
| E37 | 51.3 km SW | 0.00 mm |
| E39 | 45.6 km SE | 1.59 mm |

Peak 1-min rain rate at C1 was **57.33 mm/hr at 17:18 UTC on 7 August**; the last tip
anywhere was 18:34 UTC the same day. Convective outflow gusted to 19.97 m/s at E32.

The four collocated C1 sensors span **2.15 mm** over the week (weighing pluvio 7.62, laser
disdrometer 7.93, video disdrometer 9.77 mm) — the instrumental uncertainty on a ~8 mm point
total, worth knowing before comparing gauges 50 km apart.

## The surface responds with a multi-day lag

Midday Bowen ratio is 1.40 on 6 August, drops to **0.31** on the rain day as latent heat
dominates (H/LE = 64/207 W m-2), then climbs monotonically over the following **four** days
— 1.16, 2.02, 3.17, **3.90** by 11 August (H/LE = 246/63) — as the soil dries out. Only E32,
the wettest facility, shows a soil-moisture response (8.6 -> 20.6 % volumetric); E37 (+0.25)
and E39 (+0.81) stay flat, consistent with the patchy rainfall.

Column vapour never left: PWV stayed at 2.8-4.8 cm all week, so the dry days were suppressed
by subsidence rather than by a dry airmass. Cloud liquid water was confined to the two wet days.

## The rain event, from two radars

KAZR resolves convective shafts to 12 km with a melting layer at 3.5 km, but **Ka-band is
extinguished inside heavy rain**: at the 17:18 peak the apparent echo top collapses to 2529 m
against a median of 10,593 m in light or no rain. That is why the event needs S-band.

The KVNX volume at **17:15:45 UTC** (Unidata IDD, 58.9 km WNW of C1) shows a **50 dBZ**
convective core directly over the site, Z_DR +1.4 dB and rho_HV 0.975 — oblate, uniform large
rain drops, no hail signature. Marshall-Palmer gives 48.6 mm/hr at the nearest gate and
67.9 mm/hr over a 2 km footprint, bracketing the disdrometer's 57.33 mm/hr. The agreement is
within a factor of ~1.2 despite three known biases: M-P (Z = 200 R^1.6) is a stratiform
relation that over-reads at 50 dBZ in convection; the 0.48 deg beam centre is 1104 m MSL
(~790 m above ground), not a surface measurement; and the sweep crosses the C1 azimuth at
17:15:53, ~2.5 min before the gauge peak.

## Artifacts that are instruments, not weather

Three features in these data would be over-read if taken at face value:

- **Doppler velocity folds below the melting layer.** KAZR Nyquist is +/-5.96 m/s but rain
  fall speeds reach 8-9 m/s, so they alias to large *positive* (apparently upward) values.
- **The dry-day echo above 3 km is insects and clear-air Bragg scatter**, peaking near
  2.3-2.6 km. The >3 km echo fraction stays at 0.63-0.95 all week and would tell the
  opposite story to the >5 km cloud fraction (0.00-0.02). Use the latter for cloud claims.
- **The 46.3 dBZ weekly maximum is a single ray at 6 km on Aug 11 in otherwise clear air** —
  an aircraft or bird. The p99 column is the meteorological statistic.

## Data gaps

- `qcrad1long` and `mfrsr7nch`: 6-10 August only (5 files/facility); radiation falls back to SIRS after.
- `vdis`, `ldquants`, ECOR fluxes end 11 August, so the 12 August Bowen ratio is null.
- Ceilometer's last file is 11 August (no cloudy fraction for Aug 12).
- **No ARSCL VAP** for this window — value-added products lag real time, so all cloud
  boundaries come from raw KAZR `a1` moments plus the ceilometer.
- KAZR: all 336 hourly files (both modes, 3.6 GB) staged; general mode plotted, medium mode
  staged but not shown. One volume only for KVNX, so no storm tracking.

## Reproducing

`ARM_SGP_Week_Survey.ipynb` runs the whole survey end to end. Two ARM-specific traps are
documented inline because both fail *silently*:

1. **The CF time decoder drops the time of day.** ARM `time_offset` units read
   `seconds since 2026-08-08 02:00:13 0:00`; the trailing `0:00` defeats xarray's decoder,
   collapsing every hourly file onto midnight. Build the axis from
   `base_time + time_offset` by hand.
2. **ECOR flux QC is a graded 1-8 scale**, not the usual 0=good — masking on `qc == 0`
   discards every flux value. Other streams do use 0=good, so check per stream.

ARM Live credentials are read from `os.environ` / `getpass`, never hardcoded.
