"""
Loop over all xrt_region files and create requests on
UKSSDC website for the source.
"""
from glob import glob
from swifttools.xrt_prods import XRTProductRequest


max_jobs = 5
email = 'nk7g14@soton.ac.uk'

requests = []


source_dirs = glob('download_scripts/*/')
for s in source_dirs:
    source_name = s.split('/')[-1]
    print(s, source_name)

req = XRTProductRequest(email)
global_pars = {'name': 'NGC 300 ULX-1',
               'targ': '00095672',
               'T0': None,
               'SinceT0': None,
               'RA': None,
               'Dec': None,
               'centroid': True,
               'centMeth': 'simple',
               'maxCentTries': None,
               'posErr': 1,
               'sss': None,
               'useSXPS': False,
               'wtPupRate': None,
               'pcPupRate': None,
               'notify': True,
               'getCoords': True,
               'getTargs': None,
               'getT0': None}




req.setGlobalPars(name='NGC 300 ULX-1',
                  targ='00095672',
                  getCoords=True,
                  centroid=True,
                  centMeth='simple',
                  useSXPS=False,
                  posErr=1)
req.addLightCurve(binMeth='obsid', timeType='m')
req.addSpectrum(hasRedshift=False)

assert req.isValid()[0]
#req.submit()
#req.submitError

while not req.complete:
    print('a')
    time.sleep(10)

print(req.getAllPars())
