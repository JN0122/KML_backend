import datetime
import pandas as pd

from delivery.dto import Delivery as DeliveryDto
from delivery.dto import Forecast as ForecastDto
from delivery.model import Delivery as DeliveryModel


class DataConverter:
    def __init__(self, delivery_models: list[DeliveryModel]):
        self.delivery_models: list[DeliveryModel] = delivery_models

        self.deliveries: list[DeliveryDto] = []
        self.cast_delivery_models_to_deliveries()
        self.deliveries.sort(key=lambda d: d.date)

        self.series_count = 0
        self.set_series_count()

        self.series_dict = {}
        self.set_series_dict()


    # This converts SQL_Alchemy model to DTO for later use
    def cast_delivery_models_to_deliveries(self):
        if len(self.deliveries) > 0:
            print(f"Deliveries dict is not empty, skipping...")
            return

        for delivery_model in self.delivery_models:
            delivery = DeliveryDto(
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
            self.deliveries.append(delivery)

    def set_series_count(self):
        self.series_count = len(self.deliveries[0].get_delivery_for_every_fuel())

    def set_series_dict(self):
        fuel_keys = self.deliveries[0].get_delivery_for_every_fuel().keys()
        self.series_dict = {key: pd.Series() for key in fuel_keys}

        for i in range(len(self.deliveries)):
            single_delivery = self.deliveries[i]
            delivery_for_every_fuel = single_delivery.get_delivery_for_every_fuel()

            for fuel in fuel_keys:
                self.series_dict[fuel] = (
                    pd.concat([self.series_dict[fuel], pd.Series(delivery_for_every_fuel[fuel])],
                          axis=0, ignore_index=True)
                )

    def convert_zeros_to_small_floats(self):
        for fuel in self.series_dict.keys():
            self.series_dict[fuel] = self.series_dict[fuel].map(lambda x: float(1e-4) if x == 0 else x)

    def cast_forecasts_to_forcast_models(self, forecasts: dict):
        forecast_len = len(forecasts["ulg95"])
        forecast_models = []
        for key in forecasts.keys():
            if forecast_len == len(forecasts[key]): continue
            raise Exception("Different number of predictions for fuels")

        date_newest_delivery = min([delivery.date for delivery in self.deliveries])

        forecasts = self.fillna_in_forecasts(forecasts)

        for i in range(forecast_len):
            date = date_newest_delivery + datetime.timedelta(days=i)
            forecast = ForecastDto(
                station_id=self.delivery_models[0].station_id,
                date=date.strftime("%Y-%m-%d"),
                ulg95_forecast=forecasts["ulg95"].iloc[i],
                dk_forecast=forecasts["dk"].iloc[i],
                ultsu_forecast=forecasts["ultsu"].iloc[i],
                ultdk_forecast=forecasts["ultdk"].iloc[i],
                id=i)
            forecast_models.append(forecast)
        return forecast_models

    @staticmethod
    def fillna_in_forecasts(forecasts: dict):
        for fuel in forecasts.keys():
            forecasts[fuel] = forecasts[fuel].fillna(0)

        return forecasts
