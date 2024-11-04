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
import whois
import time
import sys
import dns.resolver
from datetime import datetime

def check_domain(domain_name):
    """
    Comprueba si un dominio tiene registros DNS (MX o NS) y verifica su registro con WHOIS si no tiene registros DNS.
    Devuelve una tupla (disponible, registrado).
    """
    try:
        # Primero intenta resolver registros MX
        dns.resolver.query(domain_name, 'MX')
        return False, True  # El dominio tiene registros, no está disponible, está registrado
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        pass  # No hay respuesta, continuamos a NS
    except Exception as e:
        print(f"Error resolviendo {domain_name}: {e}")

    try:
        # Intenta resolver registros NS
        dns.resolver.query(domain_name, 'NS')
        return False, True  # El dominio tiene registros, no está disponible, está registrado
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        pass  # No hay respuesta
    except Exception as e:
        print(f"Error resolviendo {domain_name}: {e}")

    # No se encontraron registros DNS, intentamos whois
    try:
        w = whois.whois(domain_name)
        if w is None or not w.domain_name:
            return True, False  # Dominio disponible, no está registrado
        return False, True  # Dominio no disponible, está registrado
    except Exception as e:
        print(f"Error consultando WHOIS para {domain_name}")
        return True, False  # Suponemos que está disponible si hay un error en WHOIS

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

# Contador de progreso
total_domains = len(domains_to_check)
domains_to_check = set(domains_to_check)			            # elimina duplicados
print(f"Total de dominios a analizar: {total_domains}")

# Verificación DNS y WHOIS con contador de progreso
unregistered_domains = []
for index, domain in enumerate(domains_to_check, start=1):
    print(f"Analizando {domain} ({index}/{total_domains})...")
    
    is_available, is_registered = check_domain(domain)
    
    if is_available:
        unregistered_domains.append(domain)
        print(f"{domain} está DISPONIBLE")

# Generar archivo de salida
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
output_file = f"output_{timestamp}.txt"
with open(output_file, 'w') as outfile:
    for domain in unregistered_domains:
        outfile.write(f"{domain}\n")

print(f"\nArchivo de salida generado: {output_file}")
print(f"Número total de dominios analizados: {total_domains}")
print(f"Número de dominios disponibles: {len(unregistered_domains)}")
