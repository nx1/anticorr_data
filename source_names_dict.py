
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
                     '[LM2005]_NGC_4559_ULX1'       : 'NGC4559'}


source_names_readable = {'ESO_243-49_HLX-1'             : 'ESO_243-49 HLX-1',
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
                         'SWIFT_J0243.6+6124'           : 'Swift_J0243.6+6124',
                         'NAME_UGC_6456_ULX'            : 'UGC6456 ULX',
                         'NOVA_Cyg_1989'                : 'V404Cyg',           # v404 Cygni
                         '[LB2005]_NGC_5236_X11'        : 'M83 ULX-2',         # Outer ULX M83
                         'NAME_M83_ULX-1'               : 'M83 ULX-1',         # Inner ULX M83
                         'NAME_NGC_1365-X1'             : 'NGC1365 X-1',       # 1365 X-1
                         '[SK2009]_X2'                  : 'NGC1365 X-2',       # 1365 X-2
                         'NAME_IC_10_X-1'               : 'IC10 X-1',
                         '[WMR2006]_NGC4945_XMM1'       : 'NGC4945 XMM-1',
                         '[LM2005]_NGC_4559_ULX1'       : 'NGC4559 ULX-1'}




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


if __name__ == "__main__":
    print(f'{len(source_names)} {len(source_names_readable)}')
    for simbad_name, readable_name in source_names_dict.items():
        if simbad_name not in list(source_names_readable.keys()):
             print(f'{simbad_name} not in readable source_names dict')

    for simbad_name in source_names_w_counterparts:
        if simbad_name not in list(source_names_dict.keys()):
            print(f'{simbad_name} not in readable source_names dict')

