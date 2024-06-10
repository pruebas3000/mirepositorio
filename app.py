from flask import Flask, render_template, send_from_directory, flash, request, jsonify
import requests
import subprocess

app = Flask(__name__)

# Ruta para servir archivos estáticos
@app.route('/static/<path:path>')

def send_static(path):
    return send_from_directory('static', path)

global numero_dni_global
def consultar_dni(numero_dni, token, proxy=None):
    url = "https://api.apis.net.pe/v2/reniec/dni"
    params = {"numero": numero_dni}
    headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}
    if proxy:
        response = requests.get(url, params=params, headers=headers, proxies=proxy)
    else:
        response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error en la solicitud:", response.status_code)
        return None

def consultar_en_hoja(numero_dni):
    spreadsheet_id = '1zmBtk5DP2QqdXUgslS5KCVVouAvrwggYkzAalmB-SgY'
    range_name = 'Activos!A1:N'
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}"
    params = {'key': 'AIzaSyCp4E2tTUQfOOdi3UkXNZ9bjSyu_lQHa-0'}

    response = requests.get(url, params=params)

    mensajes = []

    if response.status_code == 200:
        data = response.json()
        values = data.get('values', [])
        if values:
            print('Datos obtenidos:')
            found = False
            for row in values:
                if numero_dni in row:
                    mensajes.append("¡El DNI existe en la hoja!")
                    found = True
                    break
            if not found:
                mensajes.append("No se encontraron datos en la hoja.")
        else:
            mensajes.append('No se encontraron datos en la hoja.')
    else:
        mensajes.append('Error al obtener datos de la hoja:', response.text)

    return mensajes

@app.route('/', methods=['GET', 'POST'])
def index():
    
    resultado = None
    mensajes=[]
    if request.method == 'POST':
        token = "apis-token-7718.Y799VUMW6sswqLB9el5b7B98xG5eMkn6"
        proxy = {
            'http': 'http://Administrator:RenAu4568@192.168.2.1:3128',
            'https': 'http://Administrator:RenAu4568@192.168.2.1:3128'
        }
        numero_dni = request.form['dni']
        resultado = consultar_dni(numero_dni, token, proxy)
        numero_dni_global = numero_dni
        print(numero_dni)
        if resultado:
            print(f"Se encontró el dato en la variable global: {numero_dni_global}")
            mensajes = consultar_en_hoja(numero_dni_global)
    return render_template('index.html', resultado=resultado, mensajes=mensajes)


@app.route('/ejecutar-script', methods=['POST'])
def ejecutar_script():
    # Aquí puedes ejecutar tu script Python
    # Cambia 'ruta/al/script.py' por la ruta de tu script
    try:
        subprocess.run(['python', 'D:/_sistemas/Python cpt/Carga_Automatica_Entel/CargaAutEntelv1/CargaAutomaticaEntel.py'])
        #subprocess.run(['python', 'D:/_sistemas/Python cpt/Crear Correos Aut/cPanel-crearCorreos.py'])
        return 'Script ejecutado correctamente'
    except Exception as e:
        return f'Error al ejecutar el script: {str(e)}'

if __name__ == '__main__':
    app.run(host='192.168.2.193',debug=True)


"""
import requests

def consultar_dni(numero_dni, token, proxy=None):
    # URL de la API
    url = "https://api.apis.net.pe/v2/reniec/dni"

    # Parámetros de la solicitud
    params = {
        "numero": numero_dni
    }

    # Cabeceras de la solicitud
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Realizar la solicitud GET con o sin proxy, según se haya proporcionado
    if proxy:
        response = requests.get(url, params=params, headers=headers, proxies=proxy)
    else:
        response = requests.get(url, params=params, headers=headers)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Convertir la respuesta a formato JSON
        data = response.json()
        return data
    else:
        print("Error en la solicitud:", response.status_code)
        return None

# Definir el token
token = "apis-token-7718.Y799VUMW6sswqLB9el5b7B98xG5eMkn6"

# Definir el número de DNI a consultar
numero_dni = "75106370"

# Definir el proxy
proxy = {
    'http': 'http://Administrator:RenAu4568@192.168.2.1:3128',
    'https': 'http://Administrator:RenAu4568@192.168.2.1:3128'
}

# Llamar a la función para consultar el DNI
resultado = consultar_dni(numero_dni, token, proxy)

# Imprimir el resultado
print(resultado)
"""