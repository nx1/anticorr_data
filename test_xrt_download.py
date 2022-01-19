from swifttools.xrt_prods import XRTProductRequest, listOldJobs

email = 'nk7g14@soton.ac.uk'

req = XRTProductRequest(email)

global_pars = {'name': 'abitrary_source',
               'centroid': True,
               'centMeth': 'simple',
               'posErr': 1,
               'useSXPS': False,
               'notify': True,
               'getCoords': False,
               'getTargs': True,
               'RA' : 49.560990,
               'Dec' : -66.490645}
 
req.setGlobalPars(**global_pars)
req.addLightCurve(binMeth='obsid',
                  timeType='m',
                  minEnergy=0.3,
                  maxEnergy=10.0,
                  softLo=0.3,
                  softHi=1.5,
                  hardLo=1.5,
                  hardHi=10.0,
                  allowUL='no')
                  
req.submit()
print(req.submitError)
print(listOldJobs('nk7g14@soton.ac.uk')[0])
