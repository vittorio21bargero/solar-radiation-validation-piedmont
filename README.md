# Validazione del dato di radiazione solare in Piemonte

Codice della tesi di laurea triennale di **Vittorio Bargero** (Università degli Studi di Torino), svolta in collaborazione con **ARPA Piemonte** e **Regione Piemonte**.

- Relatore: Claudio Cassardo
- Correlatore: Federico Spanna

## Obiettivo

Valutare la qualità delle misure di radiazione solare globale orizzontale (**GHI**, *Global Horizontal Irradiance*) della rete di radiometri ARPA Piemonte, confrontandole con due riferimenti indipendenti:

- **ERA5**: rianalisi ECMWF (`shortwave_radiation`, copertura nuvolosa bassa/media/alta);
- **modello clear-sky** calcolato con [pvlib](https://pvlib-python.readthedocs.io/) per le coordinate e l'altitudine di ciascuna stazione.

Il confronto serve a individuare le stazioni con misure anomale e a stimare il **deterioramento dei sensori** nel tempo. Sono state analizzate 29 stazioni (Alba, Alessandria, Asti, Avigliana, Basaluzzo, Borgofranco d'Ivrea, Borgomanero, Buttigliera d'Asti, Bra, Candia Canavese, Carmagnola, Casale Monferrato, Costigliole Saluzzo, Cumiana, Cuneo, Fossano, Isola Sant'Antonio, Mombaldone, Mombarcaro, Moncalieri, Novi Ligure, Pino Torinese, Ponzone, Saliceto, Torino, Treiso, Vercelli, Verolengo, Villanova Solaro).

## Procedimento

1. **Preparazione dei dati**
   - conversione degli orari da ora locale (Europe/Rome) a UTC (`UTC_converter`);
   - aggregazione dei dati orari in giornalieri (`hourly_to_daily`, `Untitled2`);
   - unione delle misure di stazione con ERA5 e con la radiazione clear-sky (`stazioni_ERA5_combined`, `stazioni_GHI_ERA5`).
2. **Radiazione clear-sky**: calcolo orario con pvlib per ogni stazione (`PVLIB_orari_min_refresh`).
3. **Selezione delle giornate serene** tramite una *effective cloudiness* ricavata da ERA5,
   `0.70·cloud_low + 0.25·cloud_mid + 0.05·cloud_high` (`selezionatore_clearsky`).
4. **Confronto stazioni / modelli**
   - regressioni lineari orarie, giornaliere e annuali stazione vs clear-sky ed ERA5, con coefficiente R² (`fit_*`, `R_2_orario_clearsky_stazione_PV_anno`);
   - scarto percentuale tra stazioni ed ERA5 con media mobile pesata (`scarto_percentuale_ERA_stazioni_totale_giornaliero`, `pianura`);
   - deviazione standard percentuale tra le stazioni giorno per giorno (`dev_std_stazioni`, `dev_std_stazioni_era`, `errore_PV_dev_std_clearsky`).
5. **Deterioramento**: andamento nel tempo dello scarto rispetto ai riferimenti per ogni stazione (`deterioramento_stazioni`).

## Struttura del repository

```
notebooks/            Notebook principali dell'analisi (vedi sopra)
data/hourly/          Notebook di conversione dei dati orari e radiazione extraterrestre
altro/ARPA/           Notebook esplorativi sui dati ARPA
altro/RAM/            Analisi preliminari: correlazioni lineari per stazione (corlin),
                      fit orari e confronti con pvlib su singole stazioni
```

## Dati

I dati **non sono inclusi** nel repository per motivi di dimensione (circa 1,9 GB, con singoli file oltre i 100 MB) e di licenza. Le fonti utilizzate sono:

- misure orarie dei radiometri della rete **ARPA Piemonte**;
- rianalisi **ERA5** (ECMWF / Copernicus Climate Change Service).

I notebook si aspettano file CSV come `ERA_PV_stazioni.csv`, `ERA_PV_stazioni_clearsky.csv` e `PV.csv` nella cartella di lavoro. Alcuni percorsi sono assoluti e vanno adattati alla propria macchina.

## Requisiti

Python 3 con Jupyter e le librerie:

```
pandas numpy scipy scikit-learn statsmodels matplotlib pvlib pytz
```

```bash
pip install pandas numpy scipy scikit-learn statsmodels matplotlib pvlib pytz jupyter
```
