import numpy as np
import kachery_client as kc
import hither2 as hi
from seriesview.config import job_cache, job_handler
from seriesview.serialize_wrapper import serialize_wrapper
from seriesview.timeseries import Timeseries

@hi.function('get_seriesview_timeseries_info', '0.1.3')
@serialize_wrapper
def get_seriesview_timeseries_info(timeseries_object: dict):
    x = Timeseries(timeseries_object)
    return {
        'object': x.object,
        'channelProperties': x.channel_properties,
        'channelNames': x.channel_names,
        'numSamples': x.num_samples,
        'startTime': x.start_time,
        'samplingFrequency': x.sampling_frequency,
        'endTime': x.end_time,
        'type': x.type
    }

@kc.taskfunction('seriesview.get_timeseries_info.3', type='pure-calculation')
def task_get_timeseries_info(timeseries_object):
    with hi.Config(job_handler=job_handler.misc, job_cache=job_cache):
        return hi.Job(get_seriesview_timeseries_info, {'timeseries_object': timeseries_object})