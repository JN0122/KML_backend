from delivery.model import Delivery as DeliveryModel
from forecast.winters.WintersDataConverter import WintersDataConverter
from forecast.winters.Winters import Winters
from helpers.ConsoleLogger import ConsoleLogger


class RunWinters:
    @staticmethod
    def for_every_fuel(delivery_models: list[DeliveryModel]):
        data_converter = WintersDataConverter(delivery_models)
        forecasts = {}

        for key in data_converter.series_dict.keys():
            ConsoleLogger.log_info(f"Starting Winters for series \"{key}\".")

            model = Winters(data_converter.series_dict[key])
            coefs = [model.alpha, model.beta, model.gamma, model.season]

            forecasts[key] = model.forecast.get(coefs)

            ConsoleLogger.log_info("Winters run successfully!")

        return forecasts