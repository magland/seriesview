import numpy as np
import seriesview as sev

def main():
    x = np.arange(0, 100, dtype=np.float32) / 100
    y1 = x
    y2 = x ** 2
    y3 = x ** 3
    ts: sev.Timeseries = sev.Timeseries.from_numpy(
        channel_names=['1', '2', '3'],
        timestamps=x,
        values=np.stack([y1, y2, y3]).T,
        type='continuous'
    )
    F = ts.figurl()
    url = F.url(label='Test seriesview')
    print(url)

if __name__ == '__main__':
    main()