import time
from glob import glob
from swifttools.xrt_prods import XRTProductRequest, countActiveJobs

from source_names import source_names

email = 'nk7g14@soton.ac.uk'
max_jobs = 5
n_jobs = len(source_names)

reqs = [XRTProductRequest(email) for i in range(n_jobs)]


print('Swift XRT ULX script')
print(f'email: {email} max_jobs={max_jobs} n_jobs={n_jobs}')


# Set up all jobs
for i in range(n_jobs):
    source_name = source_names[i]
    req         = reqs[i]
    savedir = f'UKSSDC/{source_name}/'

    global_pars = {'name': source_name,
                   'centroid': True,
                   'centMeth': 'simple',
                   'posErr': 1,
                   'useSXPS': False,
                   'notify': True,
                   'getCoords': True,
                   'getTargs': True}

    req.setGlobalPars(**global_pars)
    req.addLightCurve(binMeth='obsid', timeType='m')
    req.addSpectrum(hasRedshift=False)

    

    while countActiveJobs(email) < max_jobs:


    assert req.isValid()[0]

#req.submit()
print(req.submitError)

while not req.complete:
    time.sleep(10)

print(req.getAllPars())
