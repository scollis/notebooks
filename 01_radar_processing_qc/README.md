# Radar Data Processing & Quality Control

Dealiasing, differential-phase (PHIDP/KDP) processing, attenuation correction, CMAC, gridding, gate filtering, dual-pol corrections, and radar I/O — the core Py-ART processing chain.

**45 notebooks** &nbsp;·&nbsp; 7 featured, 37 solid, 1 work-in-progress

[← Back to collection index](../README.md)

## Start here

- **[advection_interpolation/Radar_Volume_Advection_Interpolation.ipynb](advection_interpolation/Radar_Volume_Advection_Interpolation.ipynb)** — Temporal interpolation of radar volumes by optical-flow advection morphing, on native gate geometry (C-SAPR / MC3E)
- **[AGU_analysis.ipynb](AGU_analysis.ipynb)** — Phase processing and attenuation correction using linear programming for ARM X-band radars
- **[Demonstration of Py-ART for the Computation Instutute .ipynb](Demonstration%20of%20Py-ART%20for%20the%20Computation%20Instutute%20.ipynb)** — Py-ART tutorial: radar I/O, dual-pol fields, smoothing, map display
- **[LP processing of PHIDP.ipynb](LP%20processing%20of%20PHIDP.ipynb)** — Linear programming phase unwrapping for differential phase PHIDP
- **[nexrad/Quick Slice.ipynb](nexrad/Quick%20Slice.ipynb)** — Quick 2D slicing and visualization of NEXRAD radar data for rapid laptop exploration
- **[nexrad_echo_area_timeseries.ipynb](nexrad_echo_area_timeseries.ipynb)** — Compute 24-hour NEXRAD echo-area timeseries above reflectivity threshold
- **[xarray pyart integration.ipynb](xarray%20pyart%20integration.ipynb)** — Fetch NEXRAD from AWS, grid with Py-ART, visualize with xarray and MetPy

## All notebooks

| Notebook | Description | Status | Last updated |
|---|---|---|---|
| [advection_interpolation/Radar_Volume_Advection_Interpolation.ipynb](advection_interpolation/Radar_Volume_Advection_Interpolation.ipynb) | Temporal interpolation of radar volumes by optical-flow advection morphing on native gate geometry; leave-one-out validated on C-SAPR / MC3E | ⭐ featured | 2026 |
| [AGU_analysis.ipynb](AGU_analysis.ipynb) | Phase processing and attenuation correction using linear programming for ARM X-band radars | ⭐ featured | 2012 |
| [Demonstration of Py-ART for the Computation Instutute .ipynb](Demonstration%20of%20Py-ART%20for%20the%20Computation%20Instutute%20.ipynb) | Py-ART tutorial: radar I/O, dual-pol fields, smoothing, map display | ⭐ featured | 2014 |
| [LP processing of PHIDP.ipynb](LP%20processing%20of%20PHIDP.ipynb) | Linear programming phase unwrapping for differential phase PHIDP | ⭐ featured | 2013 |
| [nexrad/Quick Slice.ipynb](nexrad/Quick%20Slice.ipynb) | Quick 2D slicing and visualization of NEXRAD radar data for rapid laptop exploration | ⭐ featured | 2014 |
| [nexrad_echo_area_timeseries.ipynb](nexrad_echo_area_timeseries.ipynb) | Compute 24-hour NEXRAD echo-area timeseries above reflectivity threshold | ⭐ featured | 2026 |
| [xarray pyart integration.ipynb](xarray%20pyart%20integration.ipynb) | Fetch NEXRAD from AWS, grid with Py-ART, visualize with xarray and MetPy | ⭐ featured | 2017 |
| [BAMS RHI Dualpol.ipynb](BAMS%20RHI%20Dualpol.ipynb) | RHI dual-pol processing: phase correction, KDP retrieval, attenuation correction | solid | 2019 |
| [Barrow X-SAPR Investigation.ipynb](Barrow%20X-SAPR%20Investigation.ipynb) | X-SAPR dual-polarization radar visualization at Barrow, Alaska site | solid | 2015 |
| [canned_sapr_investigations/C-SAPR RHIs.ipynb](canned_sapr_investigations/C-SAPR%20RHIs.ipynb) | Parallel processing of C-SAPR RHI radar sweeps with reflectivity visualization | solid | 2016 |
| [canned_sapr_investigations/C-SAPR back up investigation.ipynb](canned_sapr_investigations/C-SAPR%20back%20up%20investigation.ipynb) | Investigates C-SAPR receiver calibration and radar equation power calculations | solid | 2014 |
| [COD_demo.ipynb](COD_demo.ipynb) | Radar data I/O and dual-pol PPI mapping for COD case study | solid | 2015 |
| [canned_sapr_investigations/CSAPR right now.ipynb](canned_sapr_investigations/CSAPR%20right%20now.ipynb) | Real-time SGP radar PPI visualization and animation pipeline | solid | 2015 |
| [DLCombo.ipynb](DLCombo.ipynb) | Converts StreamLine Doppler lidar .hpl files to Py-ART radar objects and visualizes RHI plots | solid | 2022 |
| [DVN.ipynb](DVN.ipynb) | NEXRAD Level-2 retrieval and PPI/RHI visualization for KDVN radar | solid | 2025 |
| [Fetch And Grid Multiple Radars.ipynb](Fetch%20And%20Grid%20Multiple%20Radars.ipynb) | Fetches multiple NEXRAD radars from AWS, grids them, and plots rainfall fields. | solid | 2022 |
| [gap_anal/Gap storm ZDR and KDP in hail.ipynb](gap_anal/Gap%20storm%20ZDR%20and%20KDP%20in%20hail.ipynb) | Dual-pol analysis of CP2 radar data during Gap Storm hail event | solid | 2014 |
| [Hail.ipynb](Hail.ipynb) | Hail event radar processing: SNR filtering, velocity dealiasing, PPI visualization | solid | 2015 |
| [canned_sapr_investigations/I6 right now rhi.ipynb](canned_sapr_investigations/I6%20right%20now%20rhi.ipynb) | RHI animation and phase texture QC for SAPR radar | solid | 2015 |
| [KLOT_qvp.ipynb](KLOT_qvp.ipynb) | Extract QVPs from radar files using Py-ART with distributed computing | solid | 2015 |
| [KTLX_qvp.ipynb](KTLX_qvp.ipynb) | Extract QVP retrievals from radar files using Py-ART and distributed computing | solid | 2015 |
| [NBpresent.ipynb](NBpresent.ipynb) | Py-ART RadarDisplay tutorial plotting reflectivity from MDV file | solid | 2016 |
| [NSA dealias.ipynb](NSA%20dealias.ipynb) | Velocity dealiasing and SNR filtering on NSA SAPR radar data | solid | 2015 |
| [Notebook for User XSAPR.ipynb](Notebook%20for%20User%20XSAPR.ipynb) | XSAPR radar file I/O and reflectivity PPI map visualization | solid | 2016 |
| [nexrad/OKSC.ipynb](nexrad/OKSC.ipynb) | NEXRAD radar data I/O and dual-pol differential reflectivity mapping | solid | 2014 |
| [scipy2014/Part 1 Reading and correcting.ipynb](scipy2014/Part%201%20Reading%20and%20correcting.ipynb) | C-SAPR radar I/O, phase processing, and dual-pol corrections | solid | 2014 |
| [scipy2014/Part 2 Mapping to cartesian space and meshing.ipynb](scipy2014/Part%202%20Mapping%20to%20cartesian%20space%20and%20meshing.ipynb) | Grid multiple radars to Cartesian mesh, visualize with cross-sections | solid | 2014 |
| [scipy2014/Part 3 Morphological Analysis.ipynb](scipy2014/Part%203%20Morphological%20Analysis.ipynb) | Morphological analysis of radar reflectivity and rainfall fields from scipy2014 campaign | solid | 2014 |
| [Radar demo.ipynb](Radar%20demo.ipynb) | Loads and visualizes radar reflectivity and velocity PPI scans | solid | 2015 |
| [canned_sapr_investigations/Retrieving dBm from Reflectivity.ipynb](canned_sapr_investigations/Retrieving%20dBm%20from%20Reflectivity.ipynb) | Convert radar reflectivity to received power using Doviak-Zrnic equation | solid | 2014 |
| [canned_sapr_investigations/SGP CSAPR PPI elevation check.ipynb](canned_sapr_investigations/SGP%20CSAPR%20PPI%20elevation%20check.ipynb) | Inspects CSAPR radar elevation angles and azimuth timing across sweeps | solid | 2014 |
| [canned_sapr_investigations/SGP CSAPR PPI plots.ipynb](canned_sapr_investigations/SGP%20CSAPR%20PPI%20plots.ipynb) | SGP CSAPR radar PPI visualization with clutter filtering and power calculations | solid | 2014 |
| [canned_sapr_investigations/SGP CSAPR PPI sector missing.ipynb](canned_sapr_investigations/SGP%20CSAPR%20PPI%20sector%20missing.ipynb) | Investigates missing PPI sector in SGP CSAPR radar data from April 2014 | solid | 2014 |
| [gap_anal/Synthetic RHI development.ipynb](gap_anal/Synthetic%20RHI%20development.ipynb) | Constructs synthetic RHI data from radar scans, quality checks output | solid | 2015 |
| [Thai mdv.ipynb](Thai%20mdv.ipynb) | Reads MDV radar file, displays PPI reflectivity map with geographic overlay | solid | 2014 |
| [X-SAPR Co-Pol.ipynb](X-SAPR%20Co-Pol.ipynb) | Loads and visualizes SGP X-SAPR co-pol radar data with rayplots and PPIs | solid | 2013 |
| [XSAPR2-2018.ipynb](XSAPR2-2018.ipynb) | XSAPR2 radar data ingest, quality correction, and quicklook plotting | solid | 2018 |
| [concatinate_file (2).ipynb](concatinate_file%20%282%29.ipynb) | Concatenates radar sweeps across files using Py-ART and Dask parallelization | solid | 2022 |
| [demo for lrose.ipynb](demo%20for%20lrose.ipynb) | LROSE kick-off demo: read IRIS radar file, map PPI display, vertical profiles | solid | 2017 |
| [elegant QVP.ipynb](elegant%20QVP.ipynb) | Retrieves radar data from AWS S3 and computes quasi-vertical profiles | solid | 2018 |
| [canned_sapr_investigations/location checks.ipynb](canned_sapr_investigations/location%20checks.ipynb) | Reads and verifies geographic coordinates of ARM SAPR radar sites | solid | 2015 |
| [quick x-array ingest from PyART.ipynb](quick%20x-array%20ingest%20from%20PyART.ipynb) | Ingest PyART radar objects into xarray Datasets from AWS S3 | solid | 2018 |
| [region block.ipynb](region%20block.ipynb) | Py-ART radar I/O, geolocation correction, and Cartopy map display | solid | 2019 |
| [tweet_my_radar.ipynb](tweet_my_radar.ipynb) | Fetch NEXRAD radar from AWS S3, process with Py-ART, tweet radar imagery | solid | 2016 |
| [canned_sapr_investigations/noise_harmonics.ipynb](canned_sapr_investigations/noise_harmonics.ipynb) | Radial velocity texture via complex-plane calculations, signal-noise analysis | wip | 2015 |

---
*Index generated from notebook content analysis. Descriptions and maturity tiers are automated assessments — see the [top-level README](../README.md) for methodology.*