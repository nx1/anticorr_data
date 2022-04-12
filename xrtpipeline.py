from swifttools.xrt_prods import XRTProductRequest, countActiveJobs



class Job(XRTProductRequest):

class XRTProductRequestManager():
    def __init__(self):
        self.email = 'nk7g14@soton.ac.uk'
        self.requests = []
        self.n_max_jobs = 5
        self.n_submitted_jobs = 0
        self.n_completed_jobs = 0
        # self.n_active_jobs    = 0
        self.n_jobs           = 0

    def __repr__(self):
        string = f"""XRTProductRequestManager
                     max_jobs = {self.n_max_jobs}
                  """
        return string 

    @property
    def n_active_jobs(self):
        return countActiveJobs(self.email)

    def add_request(XRTProductRequest):
        self.requests.append(XRTProductRequest)

    def job_is_submittable(self):
        if self.n_active_jobs < self.n_max_jobs:
            return True
        else:
            return False

    def submit_all(self):
        while self.n_submitted_jobs < self.n_jobs:
            if self.job_is_submittable():
               job.submit()

           



if __name__ == "__main__":
    mgr = XRTProductRequestManager()
    print(mgr)

