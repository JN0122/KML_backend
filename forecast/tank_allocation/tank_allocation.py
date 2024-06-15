from datetime import datetime, timedelta
from forecast import dto
import pandas as pd

def allocate_tanks(dane: dict[pd.Series], tank_residual: dto.TankResidualCreate, iteration=1):
    # Sprawdzenie, czy iteracja nie przekracza dostępnych danych
    if iteration >= len(dane["ulg95"]):
        return [], dto.TankResidualBase(
            station_id=tank_residual.station_id,
            delivery_date=tank_residual.delivery_date,
            ulg95=tank_residual.ulg95,
            dk=tank_residual.dk,
            ultdk=tank_residual.ultdk,
            ultsu=tank_residual.ultsu
        )

    # Przygotowanie danych wejściowych na podstawie inicjalizowanych wartości paliw
    paliwa = [
        ("ulg95", tank_residual.ulg95 + dane["ulg95"].iloc[iteration]),
        ("dk", tank_residual.dk + dane["dk"].iloc[iteration]),
        ("ultsu", tank_residual.ultsu + dane["ultsu"].iloc[iteration]),
        ("ultdk", tank_residual.ultdk + dane["ultdk"].iloc[iteration])
    ]

    dt = datetime.combine(tank_residual.delivery_date, datetime.min.time()) + timedelta(days=iteration)
    date = dt.date()

    # Zbiorniki zawsze te same
    pojemniki = [7400, 6100, 8500, 10000, 4000]

    def przydziel_paliwo(paliwa, pojemniki, przypisanie=None):
        if przypisanie is None:
            przypisanie = []

        if not paliwa or not pojemniki:
            residual = dto.TankResidualBase(
                station_id=tank_residual.station_id,
                delivery_date=date,
                ulg95=0,
                dk=0,
                ultdk=0,
                ultsu=0
            )
            residual.add_tank_residual_from_list(paliwa)
            return przypisanie, residual

        # Sortujemy paliwa i pojemniki w kolejności malejącej
        paliwa.sort(reverse=True, key=lambda x: x[1])
        pojemniki.sort(reverse=True)

        # Wybieramy największe paliwo i największy pojemnik
        najw_paliwo = paliwa.pop(0)
        najw_pojemnik = pojemniki.pop(0)

        paliwo_typ, paliwo_ilosc = najw_paliwo

        tank_data = {
            "station_id": tank_residual.station_id,
            "date": date,
            "capacity": najw_pojemnik,
            "ulg95": 0,
            "dk": 0,
            "ultsu": 0,
            "ultdk": 0,
            "tank_id": len(przypisanie) + 1
        }

        # Jeśli pojemnik może pomieścić całe paliwo
        if paliwo_ilosc <= najw_pojemnik:
            tank_data[paliwo_typ] = paliwo_ilosc
        else:
            tank_data[paliwo_typ] = najw_pojemnik
            # Dodajemy pozostałe paliwo z powrotem do listy paliw
            paliwa.append((paliwo_typ, paliwo_ilosc - najw_pojemnik))

        przypisanie.append(tank_data)

        # Rekurencyjnie wywołujemy funkcję dla pozostałych paliw i pojemników
        return przydziel_paliwo(paliwa, pojemniki, przypisanie)

    # Wywołanie funkcji
    przypisanie, nieprzydzielone_paliwa = przydziel_paliwo(paliwa, pojemniki)

    # Dodanie warunku zakończenia rekurencji
    if not any(paliwo[1] > 0 for paliwo in paliwa):
        return przypisanie, dto.TankResidualBase(
            station_id=tank_residual.station_id,
            delivery_date=date,
            ulg95=tank_residual.ulg95,
            dk=tank_residual.dk,
            ultdk=tank_residual.ultdk,
            ultsu=tank_residual.ultsu
        )

    # Wynikowa struktura danych
    wynik = []
    for tank in przypisanie:
        wynik.append(tank)

    # Sprawdzenie, czy iteracja nie przekracza dostępnych danych
    if iteration + 1 < len(dane["ulg95"]):
        return allocate_tanks(dane, tank_residual, iteration + 1)

    return wynik, nieprzydzielone_paliwa

# Ensure that przydziel_paliwo has a proper termination condition
def przydziel_paliwo(paliwa, pojemniki, przypisanie=None):
    if przypisanie is None:
        przypisanie = []

    if not paliwa or not pojemniki:
        residual = dto.TankResidualBase(
            station_id=tank_residual.station_id,
            delivery_date=date,
            ulg95=0,
            dk=0,
            ultdk=0,
            ultsu=0
        )
        residual.add_tank_residual_from_list(paliwa)
        return przypisanie, residual

    # Sortujemy paliwa i pojemniki w kolejności malejącej
    paliwa.sort(reverse=True, key=lambda x: x[1])
    pojemniki.sort(reverse=True)

    # Wybieramy największe paliwo i największy pojemnik
    najw_paliwo = paliwa.pop(0)
    najw_pojemnik = pojemniki.pop(0)

    paliwo_typ, paliwo_ilosc = najw_paliwo

    tank_data = {
        "station_id": tank_residual.station_id,
        "date": date,
        "capacity": najw_pojemnik,
        "ulg95": 0,
        "dk": 0,
        "ultsu": 0,
        "ultdk": 0,
        "tank_id": len(przypisanie) + 1
    }

    # Jeśli pojemnik może pomieścić całe paliwo
    if paliwo_ilosc <= najw_pojemnik:
        tank_data[paliwo_typ] = paliwo_ilosc
    else:
        tank_data[paliwo_typ] = najw_pojemnik
        # Dodajemy pozostałe paliwo z powrotem do listy paliw
        paliwa.append((paliwo_typ, paliwo_ilosc - najw_pojemnik))

    przypisanie.append(tank_data)

    # Rekurencyjnie wywołujemy funkcję dla pozostałych paliw i pojemników
    if not paliwa or not pojemniki:
        return przypisanie, dto.TankResidualBase(
            station_id=tank_residual.station_id,
            delivery_date=date,
            ulg95=0,
            dk=0,
            ultdk=0,
            ultsu=0
        )

    return przydziel_paliwo(paliwa, pojemniki, przypisanie)
