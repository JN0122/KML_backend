import logging

from delivery.model import Delivery as DeliveryModel
from forecast.winters.Winters import Winters
from forecast.winters.WintersDataConverter import WintersDataConverter
from helpers.ConsoleLogger import ConsoleLogger


class RunWinters:
    def __init__(self):
        self.logger = ConsoleLogger()

    def for_every_fuel(self, delivery_models: list[DeliveryModel]):
        data_converter = WintersDataConverter(delivery_models)
        forecasts = {}

        for key in data_converter.series_dict.keys():
            self.logger.log(level=logging.INFO, msg=f"Starting Winters for series \"{key}\".")

            model = Winters(data_converter.series_dict[key])
            coefs = [model.alpha, model.beta, model.gamma, model.season]

            forecasts[key] = model.forecast.get(coefs)

            self.logger.log(level=logging.INFO, msg="Winters run successfully!")

        return data_converter.cast_forecasts_to_forcast_models(forecasts)
