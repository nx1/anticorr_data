mport time
from glob import glob
from pathlib import Path
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

    global_pars = {'name': source_name,
                   'centroid': True,
                   'centMeth': 'simple',
                   'posErr': 1,
                   'useSXPS': False,
                   'notify': True,
                   'getCoords': True,
                   'getTargs': True}

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

    req.addSpectrum(hasRedshift=False)
    assert req.isValid()[0]

print('-'*50)
print(f'{n_jobs} jobs to run, press any key to submit...')
input()


n_submitted = 0
while n_submitted <= n_jobs:
    while countActiveJobs(email) <= max_jobs:
        req = reqs[n_submitted]

        print(f'Active Jobs = {countActiveJobs(email)} <= {max_jobs}, submitting job {n_submitted}/{n_jobs}')
        req.submit()
        time.sleep(5) # wait a bit for the job to be submitted
        n_submitted+=1


    for r in reqs[:n_submitted-1]:
        if r.complete:
            source_name = r.getAllPars()["name"]
            print(f'Request for {source_name} is complete!')
            savedir = f'UKSSDC/{source_name}'
            Path(savedir).mkdir(parents=True, exist_ok=True)

            print(f'Saving to {savedir}, stem={source_name}')
            try:
                dl = r.downloadProducts(savedir, stem=source_name)
                print(dl)
            except RuntimeError:
                print('Runtime Error, probably already saved')


    print(f"I have submitted {n_submitted} / {n_jobs} jobs, active={countActiveJobs(email)}")
    print('sleeping 2 min...')
    time.sleep(120)


