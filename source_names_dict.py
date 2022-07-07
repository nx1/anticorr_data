
source_names_dict = {'ESO_243-49_HLX-1'             : 'ESO243-49',
                     'NAME_Holmberg_IX_X-1'         : 'Holmberg_IX',
                     'Holmberg_II_X-1'              : 'Holmberg_II',
                     'M31_ULX-1'                    : 'M31',
                     '[LM2005]_NGC_598_ULX1'        : 'M33',         # AKA M33 X-8
                     'RX_J133001+47137'             : 'M51',         # M51 ULX-7
                     '[LM2005]_NGC_3031_ULX1'       : 'M81',         # AKA M81
                     'M82_X-2'                      : 'M82',
                     '[LM2005]_NGC_1042_ULX1'       : 'NGC1042',
                     'NAME_NGC_1313_X-1'            : 'NGC1313',
                     'NAME_NGC_1313_X-2'            : 'NGC1313',
                     '[LM2005]_NGC_247_ULX1'        : 'NGC247',
                     '[LB2005]_NGC_253_X2'          : 'NGC253',       # Near AGN source
                     '[LB2005]_NGC_253_X9'          : 'NGC253',       # SE gal
                     'NAME_NGC_300_ULX1'            : 'NGC300',
                     '[LM2005]_NGC_4395_ULX1'       : 'NGC4395',
                     '[LM2005]_NGC_5204_ULX1'       : 'NGC5204',
                     '[LM2005]_NGC_5408_ULX1'       : 'NGC5408',
                     '[SRW2006b]_NGC_55_ULX'        : 'NGC55',
                     '[SST2011]_J141939.39+564137.8': 'NGC5585',       # NGC 5585 ULX (overlapping sources)
                     'NAME_NGC_5907_ULX'            : 'NGC5907',
                     '[LB2005]_NGC_6946_ULX1'       : 'NGC6946',       # Southern Source
                     '[LB2005]_NGC_6946_ULX3'       : 'NGC6946',       # Northern Source
                     'NAME_NGC_7090_ULX3'           : 'NGC7090',       # NGC 7090
                     'NAME_NGC_7793_P13'            : 'NGC7793',
                     'NAME_NGC_925_ULX-1'           : 'NGC925',
                     'NAME_NGC_925_ULX-2'           : 'NGC925',
                     'SMC_X-3'                      : 'SMC_X-3',
                     'SS433'                        : 'SS433',
                     'SWIFT_J0243.6+6124'           : 'Swift_J0243.6+6124',
                     'NAME_UGC_6456_ULX'            : 'UGC6456',
                     'NOVA_Cyg_1989'                : 'V404Cyg',       # v404 Cygni
                     '[LB2005]_NGC_5236_X11'        : 'M83',           # Outer ULX M83
                     'NAME_M83_ULX-1'               : 'M83',           # Inner ULX M83
                     'NAME_NGC_1365-X1'             : 'NGC1365',       # 1365 X-1
                     '[SK2009]_X2'                  : 'NGC1365',       # 1365 X-2
                     'NAME_IC_10_X-1'               : 'IC10',
                     '[WMR2006]_NGC4945_XMM1'       : 'NGC4945',
                     '[LM2005]_NGC_4559_ULX1'       : 'NGC4559',
                     'NAME_M101-ULX1'               : 'M101'}


source_names_readable = {'ESO_243-49_HLX-1'             : 'ESO 243-49 HLX-1',
                         'NAME_Holmberg_IX_X-1'         : 'Holmberg IX X-1',
                         'Holmberg_II_X-1'              : 'Holmberg II X-1',
                         'M31_ULX-1'                    : 'M31 ULX-1',
                         '[LM2005]_NGC_598_ULX1'        : 'M33 ULX-1',         # AKA M33 X-8
                         'RX_J133001+47137'             : 'M51 ULX-7',         # M51 ULX-7
                         '[LM2005]_NGC_3031_ULX1'       : 'M81 X-6',         # AKA M81
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
                         '[SST2011]_J141939.39+564137.8': 'NGC5585 ULX',       # NGC 5585 ULX (overlapping sources)
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
                         'NOVA_Cyg_1989'                : 'V404Cyg',           # v404 Cygni
                         '[LB2005]_NGC_5236_X11'        : 'M83 ULX-2',         # Outer ULX M83
                         'NAME_M83_ULX-1'               : 'M83 ULX-1',         # Inner ULX M83
                         'NAME_NGC_1365-X1'             : 'NGC1365 X-1',       # 1365 X-1
                         '[SK2009]_X2'                  : 'NGC1365 X-2',       # 1365 X-2
                         'NAME_IC_10_X-1'               : 'IC10 X-1',
                         '[WMR2006]_NGC4945_XMM1'       : 'NGC4945 XMM-1',
                         '[LM2005]_NGC_4559_ULX1'       : 'NGC4559 ULX-1',
                         'NAME_M101-ULX1'               : 'M101 ULX-1'}




source_names = list(source_names_dict.keys())

source_names_w_counterparts = ['RX_J133001+47137',
                               'NAME_NGC_1313_X-2',
                               '[SK2009]_X2',
                               '[LB2005]_NGC_6946_ULX3',
                               'NAME_NGC_300_ULX1',
                               'SWIFT_J0243.6+6124',
                               'Holmberg_II_X-1',
                               'NOVA_Cyg_1989',
                               '[LM2005]_NGC_4559_ULX1',
                               'NAME_NGC_7793_P13',
                               'NAME_NGC_925_ULX-2',
                               'NAME_NGC_925_ULX-1',
                               '[LM2005]_NGC_5204_ULX1',
                               'SS433',
                               'SMC_X-3',
                               '[LM2005]_NGC_598_ULX1']



simbad_ulxs_by_nbib = ["USNO-B1.0 1540-00162426",
                       "CXOU J092006.3+640738",
                       "[PMS2020] NGC 7456 ULX5",
                       "CXO J121345.2+363754",
                       "3XMM J141711.1+522541",
                       "CXOU J005953.3-073457",
                       "[RPS97] NGC 4258 2",
                       "RX J133719-29536",
                       "CXOU J122602.3+125951",
                       "RX J1230.5+4141",
                       "CXOU J005952.3-073447",
                       "CXOU J153730.8+055852",
                       "CXOU J092014.9+640436",
                       "[BWC2008] U31",
                       "[BWE2015] NGC 55 119",
                       "2E 756",
                       "NAME NGC 470 HLX1",
                       "CXOU J092032.1+640424",
                       "[SMM2013] NGC 2805 X-14",
                       "CXO J122611.8+125647",
                       "[SRW2012] Src. 9",
                       "[EHB2020] NGC 925 ULX-3",
                       "CXOU J103522.6-244503",
                       "CXO J020922.8-100824",
                       "RX J0333.5-3609",
                       "NAME NGC 5907 ULX",
                       "CXOU J153733.1+055756",
                       "CXOU J010511.3-061207",
                       "CXOU J092020.6+640607",
                       "CXOU J032242.5-371222",
                       "[OZV2014] 5",
                       "[BGK2008] S102",
                       "CXOU J005951.9-073458",
                       "[BWC2008] U28",
                       "CXOU J183351.5+491642",
                       "RX J1236.2+2558",
                       "USNO-B1.0 1392-00289633",
                       "SWIFT J004327.6+410452",
                       "IXO 5",
                       "[PCV2006] ULX 2",
                       "USNO-B1.0 1540-00162375",
                       "CXOU J103522.2-244513",
                       "[LM2005] NGC 1132 ULX2",
                       "CXOU J092019.5+640624",
                       "[OBM2019] ESO 338-4 X3",
                       "RX J004722.4-252051",
                       "NAME NGC 5907 ULX-2",
                       "NAME NGC 7793 P13",
                       "NAME NGC 7793 ULX-4",
                       "WISE J005950.64-073457.1",
                       "CXOU J005950.4-073454",
                       "CXOU J093402.0+551428",
                       "[SK2009] X2",
                       "[KCF2005] M82 G",
                       "[BWC2008] U33",
                       "[FK2005] 23",
                       "CXOU J032241.1-371235",
                       "CXOU J122518.6+144545",
                       "[PMS2020] NGC 7456 ULX3",
                       "[BWC2008] U17",
                       "SDSS J092013.63+640605.4",
                       "[PMS2020] NGC 7456 ULX2",
                       "2XMM J230457.6+122028",
                       "CXOU J010505.3-061148",
                       "EQ J120242.3+015808.5",
                       "[BWC2008] U22",
                       "USNO-B1.0 1392-00289637",
                       "[LM2005] NGC 1132 ULX1",
                       "RX J0957.9+6903",
                       "CXOU J183350.6+491558",
                       "[BWC2008] U46",
                       "NAME NGC 7319-X4",
                       "NAME M81-ULS1",
                       "RX J123551+27561",
                       "[BWC2008] U8",
                       "CXOU J203451.1+601043",
                       "CXOU J112803.0+785953",
                       "EQ J2320+0811",
                       "[BWC2008] U13",
                       "[SW2003b] J024224.5+000008",
                       "1SXPS J213629.1-543348",
                       "CXOU J010504.5-061323",
                       "USNO-B1.0 0959-00250298",
                       "[SST2011] J034555.61+680455.3",
                       "[PMS2020] NGC 7456 ULX1",
                       "3XMM J213631.9-543357",
                       "CXOU J092021.0+640617",
                       "[SST2011] J120922.18+295559.7",
                       "[MAJ2009] 5",
                       "CXOM31 J004253.1+411422",
                       "CXOU J005948.5-073457",
                       "[OBM2019] ESO 338-4 X1",
                       "[SRW2012] Src. 5",
                       "[MAJ2009] 4",
                       "CXOU J133705.1-295207",
                       "RX J132506.9-430402",
                       "[FWB2009] HLX-1",
                       "[PMS2020] NGC 7456 ULX4",
                       "[SST2011] J081929.00+704219.3",
                       "CXOU J092020.2+640409",
                       "[BWC2008] U14",
                       "CXOU J112635.7+534456",
                       "CXOU J223706.6+342620",
                       "CXOU J092018.6+640615",
                       "2XMM J034606.5+680705",
                       "[OZV2014] 13",
                       "[FK2005] 25",
                       "RX J004732.9-251748",
                       "NAME M51 XT-1",
                       "[LM2005] NGC 1566 ULX1",
                       "2XMM J125048.6+410743",
                       "[BWC2008] U35",
                       "CXOU J092033.2+640345",
                       "CXOU J103522.8-244632",
                       "USNO-B1.0 0652-00247945",
                       "[BWC2008] U16",
                       "[BWC2008] U24",
                       "CXOU J005949.5-073436",
                       "[ESC2002] NGC 4736 X-1",
                       "USNO-B1.0 0824-00013656",
                       "CXOU J153738.9+055845",
                       "CXOU J005947.5-073417",
                       "[OBM2019] ESO 338-4 X2",
                       "[FK2005] 6",
                       "CXOU J005949.5-073523",
                       "[BWC2008] U32",
                       "USNO-B1.0 1541-00162121",
                       "[OZV2014] 4",
                       "CXOU J032240.8-371224",
                       "[BWC2008] U47",
                       "CXO J133815.6+043255"]











if __name__ == "__main__":
    print(f'{len(source_names)} {len(source_names_readable)}')
    for simbad_name, readable_name in source_names_dict.items():
        if simbad_name not in list(source_names_readable.keys()):
             print(f'{simbad_name} not in readable source_names dict')

    for simbad_name in source_names_w_counterparts:
        if simbad_name not in list(source_names_dict.keys()):
            print(f'{simbad_name} not in readable source_names dict')

