import sys
import getopt
import requests
import subprocess

#Tarea02-Torres-Bello-Brandon
#Rut : 25.714.131-4
#brandon.torres@alumnos.uv.cl

# URL de la API para consultar fabricantes a partir de la dirección MAC
API_URL = "https://api.maclookup.app/v2/macs/"

# Función para consultar el fabricante de una MAC en la API
def buscar_mac(mac_address):
    try:
        response = requests.get(f"{API_URL}{mac_address}")
        data = response.json()
        if 'company' in data:
            print(f"MAC address: {mac_address}")
            print(f"Fabricante: {data['company']}")
        else:
            print(f"MAC address: {mac_address}")
            print("Fabricante: Not found")
    except Exception as e:
        print(f"Error al consultar la API: {e}")

# Función para consultar la tabla ARP en macOS y obtener los fabricantes
def leer_tabla_arp():
    try:
        # Ejecuta el comando `arp -a` para obtener la tabla ARP
        result = subprocess.run(['arp', '-a'], stdout=subprocess.PIPE)
        arp_output = result.stdout.decode('utf-8')

        # Divide la salida en líneas
        lines = arp_output.splitlines()

        # Recorre cada línea y extrae las direcciones MAC
        for line in lines:
            if 'at' in line:
                # Extrae la dirección MAC (usualmente entre "at" y "[ethernet]")
                parts = line.split()
                ip_address = parts[1].strip("()")
                mac_address = parts[3]

                # Consulta el fabricante de la MAC en la API
                print(f"\nConsultando dirección IP: {ip_address}")
                buscar_mac(mac_address)
    except Exception as e:
        print(f"Error al consultar la tabla ARP: {e}")

# Función principal para procesar los parámetros de línea de comandos
def main(argv):
    mac_address = None
    try:
        # Parseo de los parámetros con getopt
        opts, args = getopt.getopt(argv, "", ["mac=", "arp", "help"])
    except getopt.GetoptError:
        print("Usage: OUILookup.py --mac <mac> | --arp | --help")
        sys.exit(2)

    # Procesamiento de las opciones ingresadas por el usuario
    for opt, arg in opts:
        if opt == "--help":
            print("Usage: OUILookup.py --mac <mac> | --arp | --help")
            sys.exit()
        elif opt == "--mac":
            mac_address = arg
        elif opt == "--arp":
            # Si se pasa el parámetro --arp, se consulta la tabla ARP
            leer_tabla_arp()
            sys.exit()

    # Si se pasó un parámetro --mac, se consulta la API
    if mac_address:
        buscar_mac(mac_address)

# Punto de entrada del programa
if __name__ == "__main__":
    main(sys.argv[1:])