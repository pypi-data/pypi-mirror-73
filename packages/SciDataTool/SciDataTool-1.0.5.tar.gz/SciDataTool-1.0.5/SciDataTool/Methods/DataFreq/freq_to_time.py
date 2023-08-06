# -*- coding: utf-8 -*-
from SciDataTool import Data1D
from SciDataTool.Functions import AxisError

def freq_to_time(self):
    """Performs the inverse Fourier Transform and stores the resulting field in a DataTime object.
    Parameters
    ----------
    self : DataFreq
        a DataFreq object
    Returns
    -------
    a DataTime object
    """
    
    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes.DataTime", fromlist=["DataTime"])
    DataTime = getattr(module, "DataTime")
    
    axes_str = [axis.name for axis in self.axes]
    axes_str = ["time" if axis_name == "freqs" else axis_name for axis_name in axes_str]
    axes_str = ["angle" if axis_name == "wavenumber" else axis_name for axis_name in axes_str]
    
    if axes_str == [axis.name for axis in self.axes]:
        raise AxisError(
            "ERROR: No available axis is compatible with fft (should be time or angle)"
        )
    else:
        results = self.get_along(*axes_str)
        values = results.pop(self.symbol)
        Axes = []
        for axis in results.keys():
            if next((ax.is_components for ax in self.axes if ax.name==axis),False): # components axis
                is_components = True
                axis_values = next((ax.values for ax in self.axes if ax.name==axis))
            else:
                is_components = False
                axis_values = results[axis]
            Axes.append(Data1D(name=axis, values=axis_values, is_components=is_components))
        return DataTime(
            name=self.name,
            unit=self.unit,
            symbol=self.symbol,
            axes=Axes,
            values=values,
        )