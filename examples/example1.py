import numpy as np
import seriesview as sev

def main():
    n = 100
    x = np.arange(0, n, dtype=np.float32) / n
    y = x ** 2
    X = sev.SVSeries.from_numpy(
        type='continuous',
        sampling_frequency=1/n,
        start_time=0,
        end_time=1,
        segment_duration=0.3,
        timestamps=x,
        values=y
    )
    Y = sev.SVSeries.from_uri(X.to_uri())
    t, v = Y.get_samples(start=0.1, end=0.5)
    print(Y.to_dict())
    print(t)
    print(v)
    # F = ts.figurl()
    # url = F.url(label='Test seriesview')
    # print(url)

if __name__ == '__main__':
    main()