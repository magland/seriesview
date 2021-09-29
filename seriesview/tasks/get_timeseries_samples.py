import numpy as np
import kachery_client as kc
import hither2 as hi
from seriesview.config import job_cache, job_handler
from seriesview.serialize_wrapper import serialize_wrapper
from seriesview.timeseries import Timeseries

@hi.function('get_seriesview_timeseries_samples', '0.1.3')
@serialize_wrapper
def get_seriesview_timeseries_samples(timeseries_object: dict, channel_name: str, ds_factor: int, segment_num: int, segment_duration_sec: float):
    t1 = segment_num * segment_duration_sec
    t2 = (segment_num + 1) * segment_duration_sec
    x = Timeseries(timeseries_object)
    timestamps, values = x.get_samples(start=t1, end=t2, channels=[channel_name])
    values = values.ravel()
    if ds_factor > 1:
        N = len(timestamps)
        N2 = int(N / ds_factor)
        timestamps = timestamps[:N2 * ds_factor]
        values = values[:N2 * ds_factor]
        timestamps_reshaped = timestamps.reshape((N2, ds_factor))
        values_reshaped = values.reshape((N2, ds_factor))
        values_min = np.min(values_reshaped, axis=1)
        values_max = np.max(values_reshaped, axis=1)        
        values = np.zeros((N2 * 2,))
        values[0::2] = values_min
        values[1::2] = values_max
        timestamps = timestamps_reshaped[:, 0].ravel()
    return {
        'timestamps': timestamps.astype(np.float32),
        'values': values.astype(np.float32)
    }
    

@kc.taskfunction('seriesview.get_timeseries_samples.3', type='pure-calculation')
def task_get_timeseries_samples(timeseries_object, channel_name: str, ds_factor: int, segment_num: int, segment_duration_sec: float):
    with hi.Config(job_handler=job_handler.timeseries, job_cache=job_cache):
        return hi.Job(get_seriesview_timeseries_samples, {'timeseries_object': timeseries_object, 'channel_name': channel_name, 'ds_factor': ds_factor, 'segment_num': segment_num, 'segment_duration_sec': segment_duration_sec})