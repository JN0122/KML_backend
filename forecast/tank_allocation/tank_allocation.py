from forecast import dto
import pandas as pd


def process_tank_data(dane: dict[pd.Series], tank_residual: dto.TankResidualCreate):
    # Przygotowanie danych wejściowych na podstawie inicjalizowanych wartości paliw
    paliwa = [
        ("ulg95", tank_residual.ulg95 + dane["ulg95"].iloc[0]),
        ("dk", tank_residual.dk + dane["dk"].iloc[0]),
        ("ultsu", tank_residual.ultsu + dane["ultsu"].iloc[0]),
        ("ultdk", tank_residual.ultdk + dane["ultdk"].iloc[0])
    ]

    # Zbiorniki zawsze te same
    pojemniki = [7400, 6100, 8500, 10000, 4000]

    def przydziel_paliwo(paliwa, pojemniki, przypisanie=None):
        if przypisanie is None:
            przypisanie = []

        if not paliwa or not pojemniki:
            residual = dto.TankResidualBase(station_id=tank_residual.station_id, delivery_date=tank_residual.delivery_date, ulg95=0, dk=0, ultdk=0, ultsu=0)
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
            "date": tank_residual.delivery_date,
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

    # Wynikowa struktura danych
    wynik = []
    for tank in przypisanie:
        wynik.append(tank)

    return wynik, nieprzydzielone_paliwa
