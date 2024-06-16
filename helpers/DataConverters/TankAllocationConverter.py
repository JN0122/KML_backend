import datetime
from delivery.dto import DeliveryCreate
from forecast.dto import TankPartition  


class TankAllocationConverter:
    @staticmethod
    def get_delivery_create_from_tank_allocation(allocation_data: list[TankPartition]) -> DeliveryCreate:
        fuels = {"ulg95": 0, "dk": 0, "ultsu": 0, "ultdk": 0}

        for data in allocation_data:
            fuels["ulg95"] += round(data.ulg95, 0)
            fuels["dk"] += round(data.dk, 0)
            fuels["ultsu"] += round(data.ultsu, 0)
            fuels["ultdk"] += round(data.ultdk, 0)

        now = datetime.datetime.now()

        return DeliveryCreate(
            station_id=allocation_data[0].station_id,
            date=allocation_data[0].delivery_date,
            time=now.strftime("%H:%M"),
            ulg95=fuels["ulg95"],
            dk=fuels["dk"],
            ultsu=fuels["ultsu"],
            ultdk=fuels["ultdk"]
        )
