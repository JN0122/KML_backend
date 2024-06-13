from delivery.model import Delivery as DeliveryModel
from delivery.dto import Delivery as DeliveryDto
from forecast.dto import DeliveryForecast as DeliveryForecastDto, Forecast as ForecastDto
from datetime import date, timedelta


class ModelDtoCasting:
    @staticmethod
    def delivery_model_to_delivery_dto(delivery_model: DeliveryModel):
        return DeliveryDto(
            station_id=delivery_model.station_id,
            date=delivery_model.date,
            time=delivery_model.time,
            ulg95=delivery_model.ulg95,
            dk=delivery_model.dk,
            ultsu=delivery_model.ultsu,
            ultdk=delivery_model.ultdk,
            id=delivery_model.id,
            total=delivery_model.total
        )
    
    @staticmethod
    def delivery_models_to_delivery_dtos(delivery_models: list[DeliveryModel]):
        return [ModelDtoCasting.delivery_model_to_delivery_dto(delivery) for delivery in delivery_models]

    @staticmethod
    def forecast_and_delivery_model_to_deliveryforecast_dto(forecasts: list[ForecastDto], deliveries: list[DeliveryDto]) -> list[DeliveryForecastDto]:
        DeliveryForecast = []
        forecasts.sort(key=lambda d: d.date)
        deliveries.sort(key=lambda d: d.date)

        def is_out_of_deliveries_index(i: int):
            if i >= len(deliveries): return True
            return False

        for i in range(len(forecasts)):
            entry = DeliveryForecastDto(
                station_id=forecasts[i].station_id,
                date=forecasts[i].date,
                ulg95_forecast=forecasts[i].ulg95_forecast,
                dk_forecast=forecasts[i].dk_forecast,
                ultsu_forecast=forecasts[i].ultsu_forecast,
                ultdk_forecast=forecasts[i].ultdk_forecast,
                ulg95=None if is_out_of_deliveries_index(i) else deliveries[i].ulg95,
                dk=None if is_out_of_deliveries_index(i) else deliveries[i].dk,
                ultsu=None if is_out_of_deliveries_index(i) else deliveries[i].ultsu,
                ultdk=None if is_out_of_deliveries_index(i) else deliveries[i].ultdk,
                id=i+1)
            DeliveryForecast.append(entry)
        return DeliveryForecast

    @staticmethod
    def change_forecast_start_date(start_date: date, forecasts: list[ForecastDto]):
        forecasts.sort(key=lambda d: d.date)
        for i in range(len(forecasts)):
            forecasts[i].date = start_date + timedelta(days=i)
        return forecasts