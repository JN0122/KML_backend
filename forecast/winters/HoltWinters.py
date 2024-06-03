from statsmodels.tsa.holtwinters import ExponentialSmoothing


class HoltWinters:
    def __init__(self, series):
        self.model = None
        self.series = series

    def fit(self):
        self.model = ExponentialSmoothing(
            self.series, trend='mul', seasonal='mul', seasonal_periods=12).fit(optimized=True)

    def get_forecast(self, forecast_len: int):
        if self.model is None:
            return

        return self.model.forecast(forecast_len)
