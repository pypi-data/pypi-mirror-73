"""timecast: a library for online time series analysis"""
from timecast.api import tscan
from timecast.modules import Module
from timecast.utils.experiment import experiment

__all__ = ["experiment", "tscan", "Module"]
