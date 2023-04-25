"""
         |\                               |               |                    /          
         | \                              |-h_emit        |                   /           
         |  \                             |               |                  /            
         |   \                            |               |                 /             
         |    \                           |               |                /              
         |theta\                          |               |               /               
         | /2   \                         |               |              /                
         |       \                        |               |             /                 
         |        \                       |               |            / 
         |         \                      |               |           /
         |          \                     |               |          /
         |           \                    |               |         /
         |            \                   |               |        /  
         |             \                  |               |       /
         |              \                 |               |      /
         |               \theta           |               |     /
         |                \ /2            |               |    / 
         |                 \              |               |   /  
         |                  \             |               |  /    
         |                   \            |               | /     
_________|____________________\           |               |/       
       R_SPH                R_ISCO       R=0                      
     mdot0 = 1              1.25Rg
                            6.00Rg
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


class Parameter:
    def __init__(self, name=None, minimum=None, maximum=None, value=None):
        self.name    = name
        self.minimum = minimum
        self.maximum = maximum
        self.value   = value

class Model:
    def __init__(self):
        self.parameters = []

    def add_parameter(self, parameter):
        self.parameters.append(parameter)


class SliderWrapper(Slider):
    def __init__(self, axes=None, parameter=None):
        self.parameter = self.set_parameter(parameter)
        self.axes      = self.set_axes()
        self.slider    = self.set_slider()
        
    def set_parameter(self, parameter):
        self.parameter = parameter

    def set_axes(self):
        self.axes = axes

    def set_slider(self, parameter):
        self.slider = Slider(ax=self.axes,
                             label=parameter.name,
                             valmin=parameter.minimum,
                             valmax=parameter.maximum,
                             valinit=parameter.value)

class ULX(Model):
    def __init__(self):
        self.r_isco = Parameter(name='r_isco', minimum=0, maximum=None, value=1.25)
        self.r_sph  = Parameter(name='r_sph',  minimum=0, maximum=None, value=3.00)
        self.theta  = Parameter(name='theta',  minimum=0, maximum=180,  value=45)

    def plot(self, axes=None):
        SliderWrapper(axes=axes, parameter=r_isco)
        SliderWrapper(axes=axes, parameter=r_sph)
        SliderWrapper(axes=axes, parameter=theta)



        def update(val):


            class Line:
                def __init__(self, xdata=None, ydata=None):
                    self.xdata = xdata
                    self.ydata = ydata

            
            class Photosphere:
                def __init__(self):
                    self.line = Line()

                def 
                    thetas = 
                    self.xdata = r_sph * np.cos(thetas)
                    self.ydata = 
                
            line.set_xdata(photosphere.xdata)
            line.sey_ydate(photosphere.ydate)

            line.set_ydata(y_photosphere(r_isco))
            fig.canvas.draw_idle()


        plot_points()
        plot_lines()
        plot_text()

        add_slider(self.r_isco)
        add_slider(self.r_sph)
        for parameter in self.parameters:
            parameter.plot()


        # The function to be called anytime a slider's value changes
        line.set_xdate()
        line.set_ydata()

        freq_slider.on_changed(update)
amp_slider.on_changed(update)

       


fig, ax = plt.subplots()
ulx = ULX()
ulx.plot(axes=ax)


ulx.r_isco.value = 1.25







# The parametrized function to be plotted
def f(t, amplitude, frequency):
    return amplitude * np.sin(2 * np.pi * frequency * t)

t = np.linspace(0, 1, 1000)

# Define initial parameters
init_amplitude = 5
init_frequency = 3

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = ax.plot(t, f(t, init_amplitude, init_frequency), lw=2)
ax.set_xlabel('Time [s]')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.
axfreq = fig.add_axes([0.25, 0.1, 0.65, 0.03])
freq_slider = Slider(
    ax=axfreq,
    label='Frequency [Hz]',
    valmin=0.1,
    valmax=30,
    valinit=init_frequency,
)

# Make a vertically oriented slider to control the amplitude
axamp = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
amp_slider = Slider(
    ax=axamp,
    label="Amplitude",
    valmin=0,
    valmax=10,
    valinit=init_amplitude,
    orientation="vertical"
)


# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata(f(t, amp_slider.val, freq_slider.val))
    fig.canvas.draw_idle()


# register the update function with each slider
freq_slider.on_changed(update)
amp_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    freq_slider.reset()
    amp_slider.reset()
button.on_clicked(reset)

plt.show()

---------------------------------------------------------------
 _____
|   /
|  /
| /
|/
