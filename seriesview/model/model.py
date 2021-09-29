from typing import Dict, List
from figurl import Figure
from ..timeseries import Timeseries

class Model:
    def __init__(self):
        self._timeseries: Dict[str, Timeseries] = {}
    def add_timeseries(self, name: str, t: Timeseries):
        self._timeseries[name] = t
    @property
    def timeseries_names(self):
        return sorted(list(self._timeseries.keys()))
    def timeseries(self, name: str):
        return self._timeseries[name]
    def figurl(self):
        a = {}
        for name in self.timeseries_names:
            a[name] = self._timeseries[name].object
        data = {
            'timeseries': a
        }
        return Figure(type='seriesview.model.1', data=data)
