import logging

from delivery.model import Delivery as DeliveryModel
from forecast.holt_winters.HoltWinters import HoltWinters
from forecast.holt_winters.DataConverter import DataConverter
from forecast.holt_winters.ForecastConverter import ForecastConverter
from helpers.ConsoleLogger import ConsoleLogger
from forecast.dto import Forecast as ForecastDto


class RunModels:
    def __init__(self, delivery_models: list[DeliveryModel]):
        self.logger = ConsoleLogger()
        self.delivery_models = delivery_models

    def for_every_fuel_as_dtos(self, forecast_len: int) -> list[ForecastDto]:
        forecasts = self.for_every_fuel(forecast_len)
        return ForecastConverter.forecasts_to_forecast_dtos(forecasts, self.delivery_models)

    def for_every_fuel(self, forecast_len: int) -> dict:
        result = {}

        delivery_dtos = DataConverter.delivery_models_to_delivery_dtos(self.delivery_models)
        delivery_dtos.sort(key=lambda d: d.date)

        series_for_every_fuel = DataConverter.get_series_for_every_fuel(delivery_dtos)
        fuels = series_for_every_fuel.keys()

        for fuel in fuels:
            self.logger.log(level=logging.INFO, msg=f"Starting HoltWinters for series \"{fuel}\".")

            series = series_for_every_fuel[fuel]
            series = DataConverter.convert_zeros_to_small_floats(series)

            holt_winters = HoltWinters(series)
            holt_winters.fit()

            result[fuel] = holt_winters.get_forecast(forecast_len)

            self.logger.log(level=logging.INFO, msg="Finished running HoltWinters")

        return result
