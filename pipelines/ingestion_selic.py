import requests

codigo_serie = 11
dataInicial = "01/01/2026"
dataFinal = "30/01/2026"

url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json&dataInicial={dataInicial}&dataFinal={dataFinal}"

try:
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        for item in data:
            print(f"Values: {item['data']} : {item['valor']}\n")
            
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"A network error occurred: {e}")
