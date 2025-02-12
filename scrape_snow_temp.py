import requests
from bs4 import BeautifulSoup

# URL till sidan
url = "https://www.piteenergi.se/snotemperatur/"

# Proxy-inställningar (använd en gratis eller betald proxy)
proxies = {
    "http": "http://24.49.117.86:80",  # Ersätt med en giltig proxy
    "https": "http://24.49.117.86:80",  # Ersätt med en giltig proxy
}

# Lägg till en User-Agent i headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Hämta sidans innehåll med headers och proxy
try:
    response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
    response.raise_for_status()  # Kasta ett fel om statuskod inte är 200
except requests.exceptions.RequestException as e:
    print(f"Fel vid hämtning av sidan: {e}")
    exit()

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Hitta det specifika m-snow-card-elementet med data-id
    snow_card = soup.find('div', {'data-id': 'e62e4e60-5774-11ec-868f-ab20b6d69604'})
    
    if snow_card:
        # Hitta snötemperaturen
        snow_temp_element = snow_card.find('div', {'class': 'm-snow-card__temp-sensor-value'})
        snow_temp = snow_temp_element.text.strip() if snow_temp_element else "Ej tillgänglig"
        
        # Hitta lufttemperaturen
        air_temp_element = snow_card.find_all('div', {'class': 'm-snow-card__temp-sensor-value'})[1]
        air_temp = air_temp_element.text.strip() if air_temp_element else "Ej tillgänglig"
        
        # Hitta tiden för senaste uppdatering
        update_time_element = snow_card.find('div', {'class': 'm-snow-card__temp-time'})
        update_time = update_time_element.text.strip() if update_time_element else "Ej tillgänglig"
        
        # Skriv ut värdena
        print(f"Snötemperatur: {snow_temp}")
        print(f"Lufttemperatur: {air_temp}")
        print(f"Senast uppdaterad: {update_time}")
        
        # Spara resultatet i en fil (valfritt)
        with open("output.txt", "w") as file:
            file.write(f"Snötemperatur: {snow_temp}\n")
            file.write(f"Lufttemperatur: {air_temp}\n")
            file.write(f"Senast uppdaterad: {update_time}\n")
    else:
        print("Kunde inte hitta 'm-snow-card'-elementet med det angivna data-id.")
else:
    print(f"Kunde inte hämta sidan. Statuskod: {response.status_code}")
