from delivery.model import Delivery as DeliveryModel
from delivery.dto import Delivery as DeliveryDto


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
