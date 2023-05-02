Supplementary Data for Long-Term X-Ray/UV Variability in ULXs
-------------------------------------------------------------

============
INTRODUCTION
============
This readme is best read with a fixed-width font.

More information, source code and additional data can be found at https://github.com/nx1/anticorr_data/
The code for the irradiated companion model may be found at https://github.com/nx1/anticorr_data/model/area.py

Contact : Norman Khan - norman1000@gmail.com

This supplementary data contains the following data:

    1. Lightcurves
    2. Tables

IMPORTANT NOTE:
    The source names used in the paper are often separate from
    the SIMBAD identifiers used in the codebase.
    
    The SIMBAD identifiers and the names given in the paper are provided
    as follows:

SIMBAD_NAME                      READABLE NAME
----------------------------------------------------
'ESO_243-49_HLX-1'             : 'ESO 243-49 HLX-1',
'NAME_Holmberg_IX_X-1'         : 'Holmberg IX X-1',
'Holmberg_II_X-1'              : 'Holmberg II X-1',
'M31_ULX-1'                    : 'M31 ULX-1',
'[LM2005]_NGC_598_ULX1'        : 'M33 ULX-1',
'RX_J133001+47137'             : 'M51 ULX-7',
'[LM2005]_NGC_3031_ULX1'       : 'M81 X-6',         
'M82_X-2'                      : 'M82 X-2',
'[LM2005]_NGC_1042_ULX1'       : 'NGC1042 ULX-1',
'NAME_NGC_1313_X-1'            : 'NGC1313 X-1',
'NAME_NGC_1313_X-2'            : 'NGC1313 X-2',
'[LM2005]_NGC_247_ULX1'        : 'NGC247 ULX-1',
'[LB2005]_NGC_253_X2'          : 'NGC253 X-2',
'[LB2005]_NGC_253_X9'          : 'NGC253 X-9',
'NAME_NGC_300_ULX1'            : 'NGC300 ULX-1',
'[LM2005]_NGC_4395_ULX1'       : 'NGC4395 ULX-1',
'[LM2005]_NGC_5204_ULX1'       : 'NGC5204 ULX-1',
'[LM2005]_NGC_5408_ULX1'       : 'NGC5408 ULX-1',
'[SRW2006b]_NGC_55_ULX'        : 'NGC55 ULX',
'[SST2011]_J141939.39+564137.8': 'NGC5585 ULX',
'NAME_NGC_5907_ULX'            : 'NGC5907 ULX',
'[LB2005]_NGC_6946_ULX1'       : 'NGC6946 ULX-1',
'[LB2005]_NGC_6946_ULX3'       : 'NGC6946 ULX-3',
'NAME_NGC_7090_ULX3'           : 'NGC7090 ULX-3',
'NAME_NGC_7793_P13'            : 'NGC7793 P13',
'NAME_NGC_925_ULX-1'           : 'NGC925 ULX-1',
'NAME_NGC_925_ULX-2'           : 'NGC925 ULX-2',
'SMC_X-3'                      : 'SMC X-3',
'SS433'                        : 'SS433',
'SWIFT_J0243.6+6124'           : 'Swift J0243.6+6124',
'NAME_UGC_6456_ULX'            : 'UGC6456 ULX',
'NOVA_Cyg_1989'                : 'V404Cyg',
'[LB2005]_NGC_5236_X11'        : 'M83 ULX-2',
'NAME_M83_ULX-1'               : 'M83 ULX-1',
'NAME_NGC_1365-X1'             : 'NGC1365 X-1',
'[SK2009]_X2'                  : 'NGC1365 X-2',
'NAME_IC_10_X-1'               : 'IC10 X-1',
'[WMR2006]_NGC4945_XMM1'       : 'NGC4945 XMM-1',
'[LM2005]_NGC_4559_ULX1'       : 'NGC4559 ULX-1',
'NAME_M101-ULX1'               : 'M101 ULX-1',
'[LM2005]_IC_342_ULX1'         : 'IC342 ULX-1',
'[BBL2003b]_IC_342_X-2'        : 'IC342 ULX-2'}




===============
1.0 Lightcurves
===============

1.1 : XRT Lightcurves (csv format)
----------------------------------
    For more information on XRT lightcurves see
    https://www.swift.ac.uk/user_objects/docs.php

    path : lightcurves/xrt/csv/[simbad_name],[xrt_lc_type].csv

    Contains processed .csv files of two xrt_lc_type
        - curve_nosys_join : Contains full band data with upper limits
        - hardrat_join     : Contains soft/hard/hardness ratio bands without upper limits


1.2 UVOT Lightcurves
--------------------
1.2.1 : Processed lightcurves (split by filter)
    path : lightcurves/uvot/fits/[simbad_name],[uvot_filter].fits



1.3 Joined Lightcurves
----------------------
1.3.1 : Joined XRT/UVOT lightcurves split by UVOT filter and XRT band
    path : lightcurves/joined/fits/[simbad_name],[uvot_filter],[xrt_lc_type],[xrt_band].fits

    The lightcurves here are provided as .fits format
    and are the result of joining the files in (1.1) with (1.2)

    The files joined with the _hardrat_ files as described in (1.1)
    are further split at this stage into each of the three xrt bands:
    SOFT/HARD/HR 

1.3.2 : Joined XRT/UVOT lightcurves complete join (format .csv)
    path : lightcurves/joined/all/[simbad_name].csv

    These lightcurves contain joined count rates across all bands and UVOT filters
    the UVOT count rates are those given by COI_SRC_RATE and COI_SRC_RATE_ERR
    (see https://heasarc.gsfc.nasa.gov/lheasoft/ftools/headas/uvotsource.html)

    These lightucurves may contain missing values but may be suitable for machine learning
    models where each filter and X-ray band is treated as a feature.

==========
2.0 Tables
==========
The tables provided in this section include various intermediary steps in our
analysis. As such, they may not be fully documented here and certain properties
such as column names and units may not be immediately clear.

Although we do not expect that an author using the lightcurves provided in this
paper will use these extensively, we provide them with the intention of
completeness that anyone working with our data may be able to quickly gain insight
into certain areas of interest. 

If you do have any questions regarding these, please do not hesitate to contact
me at norman1000@gmail.com

tables/csv/
- UVOT_FLUX.csv
    Number of source observations and detections in each UVOT band
    N_obs (N_detections) where N_detection is defined as >3 sig from 
    the `uvotsource' command see: https://heasarc.gsfc.nasa.gov/lheasoft/ftools/headas/uvotsource.html

- UVOT_obs_rates.csv
    Average count rate and standard deviation for each source in each UVOT band.

- XRT_obs_rates.csv
    Average count rate and standard deviation for each source in each XRT band.

- closest_srcreg.csv
    summary of source and background extraction regions used for the UVOT as well
    as their separation from the SIMBAD coordinates.

- correlation_N_datapoints.csv
    Columns : 
        name        : Name of dataset subset, one of:
            tab              : Original data with no filters applied
            tab_5_sig        : dataset with a +-5 sigma cut applied to both XRT and UVOT count rates
            tab_UL           : dataset containing only upper limits
            tab_no_UL        : Dataset containing no upper limits
            tab_BAD          : Dataset containing BAD XRT values
            tab_no_BAD       : Dataset without BAD XRT values
            tab_UL_no_bad    : Dataset with upper limits and without BAD XRT values
            tab_no_UL_no_bad : Dataset without upper limit and without BAD XRT values

        length      : Length of Dataset (should be identical to N_obs)
        N_obs       : Number of unique observations in dataset
        N_bad       : Number of bad datapoints in dataset
        N_good      : Number of NOT bad datapoints in dataset
        N_UL        : Number of Upper XRT datapoints in dataset
        simbad_name : SIMBAD identifier
        xrt_curve   : X-ray band, one of: FULL, HARD, SOFT or HR
        uvot_filter : UVOT filter, one of: U, B, V, UVW1, UVM2, UVW2

- correlation_fit_values.csv:
    mean and standard deviation values for correlation coefficient r
    slope m and intercept c for the correlation simulation run

- earnshaw_summary.csv
    Swift catalogue crossmatched against each source in Earnshaw catalogue
    https://ui.adsabs.harvard.edu/abs/2019MNRAS.483.5554E/abstract

- hecarte_summary.csv
    Swift catalogue crossmatched against each source in HECATE catalogue
    https://ui.adsabs.harvard.edu/abs/2021MNRAS.506.1896K/abstract

- source_with_hosts.csv
    RA, DEC, distance and references crossmatched via SIMBAD for sources

- swiftmaster_all_tables.csv
    Swift observation list for all sources.

- swiftmaster_summary.csv
    Total number of observations as well as total exposure time for all sources

- uvot_lc_info.csv
    Number of observation, src exposure, average gapsize and mean count rate
    for each uvot filter over all sources

- walton_summary.csv
    crossmatching results, number of observations and total exposure for sources
    in Walton catalogue https://ui.adsabs.harvard.edu/abs/2022MNRAS.509.1587W/abstract

- xrt_centroids.csv
    xrt centroid positions for each observation ID, from swift XRT pipeline.