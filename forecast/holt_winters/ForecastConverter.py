import datetime

from forecast.dto import Forecast as ForecastDto
from delivery.model import Delivery as DeliveryModel


class ForecastConverter:
    @staticmethod
    def forecasts_to_forecast_dtos(forecasts: dict, delivery_models: list[DeliveryModel]) -> list[ForecastDto]:
        result = []

        forecast_len = ForecastConverter.__get_forecast_len(forecasts)
        prepared_forecasts = ForecastConverter.__fillna_in_forecasts(forecasts)
        newest_delivery_date = max([delivery.date for delivery in delivery_models])

        for i in range(forecast_len):
            forecast_dto = ForecastConverter.__create_forecast_dto(
                station_id=delivery_models[0].station_id,
                date=newest_delivery_date + datetime.timedelta(days=i+1),
                forecasts=prepared_forecasts,
                i=i
            )
            result.append(forecast_dto)

        return result

    @staticmethod
    def __get_forecast_len(forecasts: dict):
        result = len(forecasts[list(forecasts.keys())[0]])

        for key in forecasts.keys():
            if result != len(forecasts[key]):
                raise Exception("Different number of forecasts for fuels")

        return result

    @staticmethod
    def __fillna_in_forecasts(forecasts: dict):
        for fuel in forecasts.keys():
            forecasts[fuel] = forecasts[fuel].fillna(0)
        return forecasts

    @staticmethod
    def __create_forecast_dto(station_id: int, date: datetime.date, forecasts: dict, i):
        return ForecastDto(
            station_id=station_id,
            date=date.strftime("%Y-%m-%d"),
            ulg95_forecast=forecasts["ulg95"].iloc[i],
            dk_forecast=forecasts["dk"].iloc[i],
            ultsu_forecast=forecasts["ultsu"].iloc[i],
            ultdk_forecast=forecasts["ultdk"].iloc[i],
            id=i
        )
