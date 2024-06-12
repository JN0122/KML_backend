import json
from datetime import datetime


def przydziel_paliwo_z_danych(dane, station_id, date, inicjalizowane_paliwa):
    # Przygotowanie danych wejściowych na podstawie inicjalizowanych wartości paliw
    paliwa = [
        ("ulg95", inicjalizowane_paliwa.get("ulg95", 0) + list(dane["ulg95"].values())[0]),
        ("dk", inicjalizowane_paliwa.get("dk", 0) + list(dane["dk"].values())[0]),
        ("ultsu", inicjalizowane_paliwa.get("ultsu", 0) + list(dane["ultsu"].values())[0]),
        ("ultdk", inicjalizowane_paliwa.get("ultdk", 0) + list(dane["ultdk"].values())[0])
    ]

    # Zbiorniki zawsze te same
    pojemniki = [7400, 6100, 8500, 10000, 4000]

    def przydziel_paliwo(paliwa, pojemniki, przypisanie=None):
        if przypisanie is None:
            przypisanie = []

        if not paliwa or not pojemniki:
            return przypisanie, paliwa

        # Sortujemy paliwa i pojemniki w kolejności malejącej
        paliwa.sort(reverse=True, key=lambda x: x[1])
        pojemniki.sort(reverse=True)

        # Wybieramy największe paliwo i największy pojemnik
        najw_paliwo = paliwa.pop(0)
        najw_pojemnik = pojemniki.pop(0)

        paliwo_typ, paliwo_ilosc = najw_paliwo

        tank_data = {
            "station_id": station_id,
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

    # Wynikowa struktura danych
    wynik = []
    for tank in przypisanie:
        wynik.append(tank)

    return wynik, nieprzydzielone_paliwa


# # Przykładowe użycie
# dane = {
#     "ulg95": {
#         "350": 6997.56043222195,
#         "351": 5844.313394669532,
#         "352": 6052.106291684175,
#         # reszta danych...
#     },
#     "dk": {
#         "350": 21118.426570731488,
#         "351": 21960.348532182128,
#         "352": 21945.841965587282,
#         # reszta danych...
#     },
#     "ultsu": {
#         "350": 1839.1537610906341,
#         "351": 779.8585222001146,
#         "352": 815.0604329295747,
#         # reszta danych...
#     },
#     "ultdk": {
#         "350": 3427.8802117939235,
#         "351": 2820.2442109332887,
#         "352": 2867.279306824674,
#         # reszta danych...
#     }
# }
#
# station_id = 0
# date = "2024-05-27"
# inicjalizowane_paliwa = {
#     "ulg95": 0,
#     "dk": 0,
#     "ultsu": 0,
#     "ultdk": 0
# }
#
# wynik, nieprzydzielone_paliwa = przydziel_paliwo_z_danych(dane, station_id, date, inicjalizowane_paliwa)
#
# print("Przypisanie paliwa do pojemników:")
# for tank in wynik:
#     print(tank)
#
# if nieprzydzielone_paliwa:
#     print("\nNieprzydzielone paliwo:")
#     for typ_paliwa, ilosc_paliwa in nieprzydzielone_paliwa:
#         print(f'{ilosc_paliwa:.2f} jednostek paliwa typu {typ_paliwa}')
# else:
#     print("\nWszystkie paliwa zostały przydzielone.")