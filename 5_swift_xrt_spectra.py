"""
Extract Spectra for all sources in the sample.
"""
import time
from glob import glob
from pathlib import Path
from swifttools.xrt_prods import XRTProductRequest, countActiveJobs

from source_names_dict import source_names_dict

source_names = list(source_names_dict.keys())
email = 'nk7g14@soton.ac.uk'
max_jobs = 10
n_jobs = len(source_names)
reqs = [XRTProductRequest(email) for i in range(n_jobs)]

print('Swift XRT ULX script')
print(f'email: {email} max_jobs={max_jobs} n_jobs={n_jobs}')

# Fix glob square bracket issue
to_replace = {'[':'[[]',
              ']':'[]]'}



# Set up all jobs
for i in range(n_jobs):
    source_name = source_names[i]
    req         = reqs[i]

    global_pars = {'name': source_name,
                   'centroid': True,
                   'centMeth': 'simple',
                   'posErr': 1,
                   'useSXPS': False,
                   'notify': True,
                   'getCoords': True,
                   'getTargs': True}
    
    spec_pars = {"hasRedshift": False,
                 "useObs":"all",
                 "whichData": "all",
                 "grades": "all",
                 "doNotFit":True}

    req.setGlobalPars(**global_pars)
    req.addSpectrum(**spec_pars)

    req.savedir = f'UKSSDC_spec/{source_name}'

    savedir_esc = req.savedir.translate(str.maketrans(to_replace)) # Used to fix globbing square brackets

   

    req.is_downloaded = False
    req.is_submitted  = False
    
    for f in glob(f'{savedir_esc}/*'):
        if 'tar.gz' in f:
            print(f'File found: {f}, assuming request is downloaded')
            req.is_downloaded = True
    assert req.isValid()[0]
    print(f'{i:<4} {source_name}')

print('-'*50)
print(f'{n_jobs} jobs to run, press any key to submit...')
input()


n_submitted = 31
while n_submitted < n_jobs:
    while (countActiveJobs(email) <= max_jobs) and (n_submitted < n_jobs):
        req = reqs[n_submitted]

        print(f'Active Jobs = {countActiveJobs(email)} <= {max_jobs} {req.savedir}')
        if req.is_downloaded==False:
            print(f'submitting job {n_submitted}/{n_jobs} {req.getAllPars()["name"]}')
            submitted = req.submit()
            if submitted:
                req.is_submitted = True
            time.sleep(5) # wait a bit for the job to be submitted
        n_submitted+=1


    for r in reqs:
        if r.is_submitted:
            if r.is_downloaded==False:
                if r.complete:
                    source_name = r.getAllPars()["name"]
                    print(f'Request for {source_name} is complete!')
                    Path(r.savedir).mkdir(parents=True, exist_ok=True)
                    print(f'Saving to {r.savedir}, stem={source_name}')
                    try:
                        dl = r.downloadProducts(r.savedir, stem=source_name)
                        print(dl)
                        r.is_downloaded = True
                    except RuntimeError:
                        print('Runtime Error, probably already saved')


        print(f"I have submitted {n_submitted} / {n_jobs} jobs, active={countActiveJobs(email)}")
        print('sleeping 2 min...')
        time.sleep(120)

