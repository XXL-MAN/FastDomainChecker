"""
Este script en Python consulta la API de VirusTotal para obtener información de popularidad sobre dominios de correo electrónico extraídos de un archivo de entrada.

### Descripción del funcionamiento:

1. **Importación de librerías**: 
   Se utilizan librerías como `sys` para argumentos de línea de comandos, `time` para controlar el tiempo entre consultas y `virustotal_python` para interactuar con la API de VirusTotal.

2. **Lectura del archivo de entrada**: 
   El archivo debe pasarse como argumento al ejecutar el script. Cada línea debe contener un email en el formato `usuario@dominio.com`. Si el archivo no se especifica, el script mostrará un mensaje de error y se detendrá.

3. **Extracción de dominios**: 
   Para cada línea del archivo, el script extrae la parte del dominio después del símbolo `@` y evita duplicados agregando solo dominios únicos a una lista.

4. **Consulta a la API de VirusTotal**:
   Para cada dominio único, el script consulta la API de VirusTotal y extrae los datos de popularidad, si están disponibles. Si no se puede realizar la consulta o no se obtienen datos, el valor por defecto para `popularity` es una lista vacía.

5. **Impresión de resultados**:
   Imprime el nombre de cada dominio y su popularidad en formato `Dominio - [Datos de popularidad]`.

6. **Control de tiempo**:
   Incluye una pausa de un segundo entre consultas para evitar exceder los límites de la API.

### Ejecución del script:

```bash
python nombre_del_script.py archivo_de_entrada.txt
"""

import sys,time
import virustotal_python
from pprint import pprint



#domain = "virustotal.com"

VirusTotalAPIKey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

try:
    file = sys.argv[1]
except:
    print("ERROR: Utiliza el fichero de entrada como argumento")
    sys.exit(0)

domains_list = []

f = open(file)
for linea in f:
    domain = linea.strip()
    #print(domain)
    domain = domain.split("@")[1]
    if not domain in domains_list:
        domains_list.append(domain)

for domain in domains_list:
    with virustotal_python.Virustotal(VirusTotalAPIKey) as vtotal:
        try:
            resp = vtotal.request(f"domains/{domain}")
            popularity = resp.data['attributes']['popularity_ranks']
        except:
            popularity = []
            pass

    print('Dominio {} - {}'.format(domain, popularity))
    time.sleep(1)






