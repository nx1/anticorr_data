class Model:
    def __init__(self):
        self.name       = 'ulxlc'
        self.parameters  = ModelParams()
        self.input_data  = ModelData()
        self.model_data  = ModelData()
        self.output_data = ModelData()

    def run(self):


class ModelParameter:
    def __init__(self_):
        

class ModelParams:
    def __init__(self):
    
    def add_param(
        

class ModelData:
    def __init__(self):
        self.y
        self.z
        self.F_var
        self.lc_xrt
        self.lc_uvot
    
    @classmethod
    def load_xrt(cls, simbad_name):
        return cls

    @classmethod
    def load_uvot(cls, simbad_name):
        return cls




# models.py
from model import Model


class correlate(Model):
    a = 
    v = 
    np.correlate(a, v)
     np.corr(model.input_data.lc[0], model.input_data.c[1]) 
            
class DCF(Model):

class ACF(Model):
class redfit(Model):
class ulxlc(Model):
class physical1(Model):
class physical2(Model):



#from models import corr, DCF, ACF, redfit, ulxlc, physical1, physical2
from models import Corr
models = [corr, dcf, acf, redfit, ulxlc, physical1, physical2]


uv_xrt_linear_correlations = Model()
xrt_ulxlc                  = Model()
redfix_x                   = Model()


for model in models:
    model.run()
