import datetime
from delivery.dto import DeliveryCreate


class TankAllocationConverter:
    @staticmethod
    def get_delivery_create_from_tank_allocation(allocation_data) -> DeliveryCreate:
        fuels = {"ulg95": 0, "dk": 0, "ultsu": 0, "ultdk": 0}

        for data in allocation_data:
            for fuel_type in fuels.keys():
                if data[fuel_type] != 0:
                    fuels[fuel_type] += int(round(data[fuel_type], 0))

        now = datetime.datetime.now()

        return DeliveryCreate(
            station_id=allocation_data[0]["station_id"],
            date=allocation_data[0]["date"],
            time=now.strftime("%H:%M"),
            ulg95=fuels["ulg95"],
            dk=fuels["dk"],
            ultsu=fuels["ultsu"],
            ultdk=fuels["ultdk"]
        )
