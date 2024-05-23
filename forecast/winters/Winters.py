import numpy as np
from scipy.optimize import least_squares

from forecast.winters.WintersForecast import WintersForecast


class Winters:
    def __init__(self, series):
        self.alpha = 0.05
        self.beta = 0.05
        self.gamma = 0.05
        self.season = 3

        self.series = series
        self.series_size = len(self.series)

        self.forecast = WintersForecast(self.series, self.series_size)

    def loss(self):
        ys = np.array(list(self.series.values())[self.season + 1:])
        fs = np.array(list(self.forecast.get([self.alpha, self.beta, self.gamma, self.season], 0).values()))
        return 0.5 * ((ys - fs) ** 2).sum()

    def fit_coefs(self):
        ys = np.array(list(self.series.values())[self.season + 1:])

        def residuals(coefs):
            coefs = np.append(coefs, self.season)
            return np.array(list(self.forecast.get(coefs, 0).values())) - ys

        self.alpha, self.beta, self.gamma = least_squares(
            fun=residuals,
            x0=np.array([self.alpha, self.beta, self.gamma]),
            bounds=([0.0, 0.0, 0.0], [1.0, 1.0, 1.0])).x

    def fit_coefs_season(self):
        def residuals(coefs):
            fs = list(self.forecast.get(coefs, 0).values())
            fsize = len(fs)
            ys = np.array(list(self.series.values())[-fsize:])
            return np.array(fs) - ys

        res = least_squares(fun=residuals,
                            x0=np.array([self.alpha, self.beta, self.gamma, self.season]),
                            bounds=([0, 0, 0, 1], [1, 1, 1, int(self.series_size / 2)]))

        self.alpha, self.beta, self.gamma, self.season = res.x[0], res.x[1], res.x[2], int(res.x[3])
