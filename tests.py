import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/1"
ENDPOINT = ""

URL = BASE_URL + ENDPOINT

data = json.dumps({
    "parts": ["swiatła", "bolesne"]
})

requests.post(url=BASE_URL, data=data)

# ROSARY = {
#     "radosne" : [
#         "Zwiastowanie Najswietszej Marii Pannie",
#         "Nawiedzenie Swietej Elzbiety",
#         "Narodzenie Jezusa Chrystusa",
#         "Ofiarowanie Jezusa w Swiatyni",
#         "Odnalezienie Jezusa w Swiatyni"
#     ],
#     "bolesne": [
#         "Modlitwa w Ogrojcu",
#         "Biczowanie Pana Jezusa",
#         "Cierniem Ukoronowanie Pana Jezusa",
#         "Droga Krzyzowa",
#         "Smierc na Krzyzu"
#     ],
#     "chwalebne": [
#         "Zmartwychwstanie Pana Jezusa",
#         "Wniebowstapienie Pana Jezusa",
#         "Zeslanie Ducha Swietego na Maryje i apostolow",
#         "Wniebowziecie Najswietszej Marii Panny",
#         "Ukoronowanie Najswietszej Marii Panny"
#     ],
#     "swatla": [
#         "Chrzest Pana Jezusa",
#         "Wesele w Kanie Galilejskiej",
#         "Gloszenie Krolewstwa Bozego i wzywanie do nawrocenia",
#         "Przemienienie na gorze Tabor",
#         "Ustanowienie Eucharystii"
#     ]
# }
#
