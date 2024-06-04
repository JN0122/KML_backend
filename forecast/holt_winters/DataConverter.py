import pandas as pd

from delivery.dto import Delivery as DeliveryDto
from delivery.model import Delivery as DeliveryModel
from helpers.ModelDtoCasting import ModelDtoCasting


class DataConverter:
    @staticmethod
    def delivery_models_to_delivery_dtos(delivery_models: list[DeliveryModel]) -> list[DeliveryDto]:
        result = []

        for delivery_model in delivery_models:
            result.append(ModelDtoCasting.delivery_model_to_delivery_dto(delivery_model))

        return result

    @staticmethod
    def get_series_for_every_fuel(delivery_dtos: list[DeliveryDto]) -> dict[str, pd.Series]:
        fuels = delivery_dtos[0].get_delivery_for_every_fuel().keys()
        result = {key: pd.Series() for key in fuels}

        for i in range(len(delivery_dtos)):
            single_delivery = delivery_dtos[i]
            delivery_for_every_fuel = single_delivery.get_delivery_for_every_fuel()

            for fuel in fuels:
                result[fuel] = pd.concat([result[fuel], pd.Series(delivery_for_every_fuel[fuel])],
                          axis=0, ignore_index=True)
        return result

    @staticmethod
    def convert_zeros_to_small_floats(series: pd.Series) -> pd.Series:
        return series.map(lambda x: float(1e-4) if x == 0 else x)
