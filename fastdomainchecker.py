import whois
import time
import sys
import random
import dns.resolver
from datetime import datetime

"""
Este script permite verificar si dominios (o dominios extraídos de correos electrónicos) están registrados o no, utilizando consultas DNS y verificaciones `whois`.

### Funcionalidad principal:
1. **Lectura de archivo de entrada**:
   - El archivo de entrada (`sys.argv[1]`) puede contener nombres de dominio, palabras clave, o correos electrónicos.
   - Si se detecta un correo electrónico, se extrae el dominio de éste.
   - Si el contenido es una palabra clave sin TLD (por ejemplo, "example"), el script genera combinaciones con TLDs de un archivo opcional (`sys.argv[2]`) o usa TLDs predeterminados (`com`, `net`, `org`, etc.).

2. **Verificación de DNS**:
   - Para cada dominio generado, se comprueba primero si existen registros DNS (tipos `MX` y `NS`) para determinar rápidamente si el dominio está activo.
   - Los dominios que no tienen registros DNS se agregan a la lista `domains_without_dns`.

3. **Verificación de registro (WHOIS)**:
   - Para los dominios en `domains_without_dns`, se realiza una consulta `whois` para verificar si están registrados.
   - Los dominios que no tienen información `whois` se consideran no registrados y se agregan a la lista `unregistered_domains`.

4. **Salida de resultados**:
   - La lista de dominios no registrados (`unregistered_domains`) se imprime en pantalla y se guarda en un archivo de salida con un nombre basado en la fecha y hora (`output_YYYYMMDDHHMMSS.txt`).

### Ejecución del script:
```bash
python script.py archivo_dominio.txt [extensions.txt]

"""

def fast_domain_checker(domain_name, delay=True):
    """
    Comprueba si un dominio tiene registros DNS (MX o NS).
    Si no encuentra estos registros, verifica con whois.
    """
    try:
        dns.resolver.resolve(domain_name, 'MX')
        return True
    except:
        try:
            dns.resolver.resolve(domain_name, 'NS')
            return True
        except:
            try:
                w = whois.whois(domain_name)
                if delay:
                    time.sleep(60)
            except Exception:
                return False
            else:
                return bool(w.domain_name)

def is_registered(domain_name):
    """
    Verifica si un dominio está registrado usando `whois`.
    """
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)

# Leer archivos de entrada
try:
    domain_file = sys.argv[1]
except IndexError:
    print("ERROR: Proporciona el archivo de entrada con dominios o emails como argumento.")
    sys.exit(1)

# Leer archivo de TLDs opcional o usar TLDs predeterminados
if len(sys.argv) > 2:
    extension_file = sys.argv[2]
    with open(extension_file, 'r') as ext_file:
        tlds = [line.strip() for line in ext_file if line.strip()]
else:
    tlds = ["com", "net", "org", "info", "biz"]  # TLDs predeterminados

domains_to_check = []

# Procesar dominios y emails en el archivo de entrada
with open(domain_file, 'r') as domains:
    for line in domains:
        line = line.strip()
        if "@" in line:  # Si es un email, extrae el dominio
            domain = line.split("@")[1]
        else:
            domain = line
        
        # Si es una palabra clave (sin TLD), combina con los TLDs
        if "." not in domain:
            for tld in tlds:
                full_domain = f"{domain}.{tld}"
                domains_to_check.append(full_domain)
        else:
            domains_to_check.append(domain)

# Verificación DNS
domains_without_dns = [domain for domain in domains_to_check if not fast_domain_checker(domain, delay=False)]

# Verificación WHOIS para dominios sin DNS
unregistered_domains = [domain for domain in domains_without_dns if not is_registered(domain)]

# Generar archivo de salida
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
output_file = f"output_{timestamp}.txt"
with open(output_file, 'w') as outfile:
    for domain in unregistered_domains:
        outfile.write(f"{domain} está DISPONIBLE\n")
        print(f"{domain} está DISPONIBLE")
        
print(f"\nArchivo de salida generado: {output_file}")
