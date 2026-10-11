# Validation of solar radiation measurements in Piedmont

How reliable are the solar radiation measurements of a regional monitoring network? This project
compares 28 years of data from 29 pyranometers of **ARPA Piemonte** with two independent references,
the **ERA5-Land** reanalysis and a **clear-sky model**, to find stations with anomalous
measurements and to estimate the real uncertainty of the network.

*Bachelor's thesis in Physics, University of Turin, carried out during an internship with
ARPA Piemonte and Regione Piemonte (2023–2024). Supervisor: Claudio Cassardo;
co-supervisor: Federico Spanna.*

![Mean bias of each station with respect to ERA5-Land](docs/figures/station_bias.png)

*Mean difference between each station and ERA5-Land on clear-sky days. Most stations are within the
±5% accuracy of the instrument. The stations in red have large or very variable deviations; on-site
inspection and satellite images showed that their sensor is partly shaded (by trees in Borgomanero
and Mombaldone, by a telecommunication tower in Mombarcaro) or placed in an unrepresentative spot.*

## Method

The quantity measured is the **global horizontal irradiance** (GHI = direct normal irradiance ·
cos θ + diffuse horizontal irradiance), measured by thermopile pyranometers (CAE, WMO first class,
5% accuracy on the daily total).

1. **Data preparation.** Hourly data of 29 stations (1996–2023), conversion from local time to UTC,
   aggregation to daily totals, and matching with the nearest ERA5-Land grid point
   (0.07° ≈ 11 km resolution; hourly radiation and low/medium/high cloud cover).
2. **Clear-sky days.** Clouds make a point measurement and an 11 km grid cell hard to compare, so
   the comparison is restricted to clear-sky days. Each hour gets an effective cloudiness from ERA5,
   0.70·low + 0.25·mid + 0.05·high cloud cover, and a day is kept only if *all* its hours are below 10%
   (325 days).
3. **Is ERA5 a good reference?** On clear-sky hours ERA5-Land is compared with the Ineichen–Perez
   clear-sky model computed with [pvlib](https://pvlib-python.readthedocs.io/) for the coordinates
   and altitude of each station: for the stations tested, hourly linear fits give R² ≥ 0.97 and
   slopes between 0.96 and 1.01.
4. **Stations vs ERA5.** Percentage difference station − ERA5 for every station and day, its moving
   average over time and by season, and the day-by-day spread across stations.

## Results

**1. Most of the difference between stations and ERA5 is the stations' own variability.** On
clear-sky days the stations differ from ERA5-Land by 5.5% on average (4.1% in summer, 7.1% in winter).

![Mean absolute difference between stations and ERA5-Land](docs/figures/station_vs_era5.png)

**2. The network's uncertainty is compatible with the instrument specification.** On the same day
and under a clear sky, the stations disagree with each other by 4.7% (coefficient of variation),
while ERA5-Land at the same sites varies by only 1.4%. The difference, about 3.3%, is an estimate of
the measurement uncertainty of the network. It is below the 5% declared for the instruments.

![Spread across stations and across ERA5-Land grid points](docs/figures/spread_stations_vs_era5.png)

**3. Seasonal dependence.** The larger winter difference may come partly from the instruments
(low sun elevation) and partly from ERA5's cloud parameterisation, which can underestimate fog and
haze in the Po Valley in winter.

**4. Anomalous stations.** Six stations (Torino, Borgomanero, Mombaldone, Mombarcaro, Pino Torinese,
Ponzone) were flagged from their mean deviation and checked one by one; for those inspected on site
or on satellite images the cause is the siting of the sensor rather than its calibration. These
stations are excluded from the statistics above.

## Repository structure

```
notebooks/        main analysis
│   UTC_converter, hourly_to_daily, aggregate_9_15_to_daily,
│   merge_stations_era5, stations_ghi_era5                   data preparation
│   clearsky_pvlib_hourly                                    clear-sky radiation with pvlib
│   clearsky_day_selection                                   selection of clear-sky days
│   fit_*, r2_hourly_station_vs_clearsky_by_year             linear fits station / ERA5 / clear-sky
│   station_vs_era5_difference, percentage_difference_*      station - ERA5 differences
│   spread_stations*, station_error_spread_clearsky          spread across stations
│   station_degradation                                      bias of each station over time
data/hourly/      conversion of hourly data, extraterrestrial radiation
archive/          early exploration: ARPA data, regional agrometeorological network
                  (linear correlations per station, first pvlib comparisons)
scripts/          readme_figures.py: figures of this README
docs/figures/
```

The notebooks are written in Italian and were run interactively; file paths refer to the local
working copy and need to be adapted.

## Data

The data are **not included**, for size (about 2 GB) and licensing reasons:

- hourly GHI of the ARPA Piemonte pyranometer network;
- ERA5-Land hourly reanalysis (ECMWF / Copernicus Climate Change Service).

## Requirements

Python 3 with Jupyter and

```bash
pip install pandas numpy scipy scikit-learn statsmodels matplotlib pvlib pytz jupyter
```

## Author

Vittorio Bargero, BSc in Physics, University of Turin.
