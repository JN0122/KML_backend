from delivery.dto import Delivery as DeliveryDto
from delivery.model import Delivery as DeliveryModel


class WintersDataConverter:
    def __init__(self, delivery_models: list[DeliveryModel]):
        self.delivery_models: list[DeliveryModel] = delivery_models
        self.deliveries: list[DeliveryDto] = []
        self.cast_delivery_models_to_deliveries()
        self.deliveries.sort(key=lambda d: d.date)

        self.series_count = 0
        self.set_series_count()

        self.series_dict = {}
        self.set_series_dict_from_deliveries()

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

    def set_series_dict_from_deliveries(self):
        fuel_keys = self.deliveries[0].get_delivery_for_every_fuel().keys()
        self.series_dict = {key: {} for key in fuel_keys}

        for i in range(len(self.deliveries)):
            single_delivery = self.deliveries[i]
            delivery_for_every_fuel = single_delivery.get_delivery_for_every_fuel()

            for key in fuel_keys:
                self.series_dict[key][i + 1] = delivery_for_every_fuel[key]
