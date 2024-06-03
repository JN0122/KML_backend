import logging

from delivery.model import Delivery as DeliveryModel
from forecast.winters.HoltWinters import HoltWinters
from forecast.winters.DataConverter import DataConverter
from helpers.ConsoleLogger import ConsoleLogger


class RunModels:
    def __init__(self):
        self.logger = ConsoleLogger()

    def holt_winters_for_every_fuel(self, delivery_models: list[DeliveryModel], forecast_len: int):
        data_converter = DataConverter(delivery_models)

        forecasts = {}

        for fuel in data_converter.series_dict.keys():
            self.logger.log(level=logging.INFO, msg=f"Starting HoltWinters for series \"{fuel}\".")

            holt_winters = HoltWinters(data_converter.series_dict[fuel])
            holt_winters.fit()

            forecasts[fuel] = holt_winters.get_forecast(forecast_len)

            # self.logger.log(level=logging.INFO, msg="HoltWinters run successfully!")

        return data_converter.cast_forecasts_to_forcast_models(forecasts)
