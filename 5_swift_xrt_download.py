"""
Loop over all xrt_region files and create requests on
UKSSDC website for the source.
"""
from glob import glob
from swifttools.xrt_prods import XRTProductRequest


max_jobs = 5
email = 'nk7g14@soton.ac.uk'


sources_names = ['ESO 243-49 HLX-1',
                 'Ho IX X-1',
                 'Holmberg II X-1',
                 'M31 ULX-1',
                 'J013350.8+303937' # M33 X-8
                 'RX J133001+47137' # M51 ULX-7
                 '[LM2005] NGC 3031 ULX1',
                 'M82 X-2',
                 'J024025.6-082428' # NGC 1042 ULX1
                 'NGC1313 X-1',
                 'NGC1313 X-2',
                 'J004703.9-204743', # NGC 247 ULX1
                 '[LB2005] NGC 253 X20', # NGC 253 ULX1
                 'NGC 300 ULX1',
                 '[LM2005] NGC 4395 ULX1',
                 '[LM2005] NGC 5204 ULX1',
                 '[LM2005] NGC 5408 ULX1',
                 '[SRW2006b] NGC 55 ULX',
                 'J141939.3+564137', # NGC 5585 ULX (overlapping sources)
                 'NAME NGC 5907 ULX',
                 '[LB2005] NGC 6946 ULX1',
                 'J213631.9-543357', # NGC 7090
                 'NGC7793 P13',
                 'NAME NGC 925 ULX-1',
                 'NAME NGC 925 ULX-2',
                 'SMC X-3',
                 'SS433',
                 'SWIFT J0243.6+6124',
                 'NAME UGC 6456 ULX',



                 '
requests = []


source_dirs = glob('download_scripts/*/')
for s in source_dirs:
    source_name = s.split('/')[-1]
    print(s, source_name)

req = XRTProductRequest(email)

global_pars = {'name': 'sourcename',
               #'targ': None,
               #'T0': None,
               #'SinceT0': None,
               'RA': 359.462083,
               'Dec': -32.624056,
               'centroid': True,
               'centMeth': 'simple',
               #'maxCentTries': None,
               'posErr': 1,
               #'sss': None,
               'useSXPS': False,
               #'wtPupRate': None,
               #'pcPupRate': None,
               'notify': True,
               'getCoords': False,
               'getTargs': False}
               #'getT0': None}




req.setGlobalPars(**global_pars)

req.addLightCurve(binMeth='obsid', timeType='m')
req.addSpectrum(hasRedshift=False)

assert req.isValid()[0]
#req.submit()
print(req.submitError)

while not req.complete:
    time.sleep(10)

print(req.getAllPars())
