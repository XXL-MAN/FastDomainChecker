# FastDomainChecker (Domain Availability Checker)
Fast Domain Checker - Orphan Domain investigation - @TheXXLMAN

Este repositorio contiene un script en Python que permite verificar si dominios o dominios extraídos de correos electrónicos están registrados, utilizando consultas DNS y verificaciones `whois`. Es ideal para obtener rápidamente la disponibilidad de dominios en masa.

## Funcionalidades

1. **Entrada de datos**:
   - Lee un archivo que contiene dominios, palabras clave o correos electrónicos, uno por línea.
   - Si se detecta un correo electrónico, se extrae el dominio.
   - Si se ingresa una palabra clave sin TLD (por ejemplo, `example`), el script combina esa palabra clave con TLDs de un archivo opcional o usa TLDs predeterminados (`com`, `net`, `org`, `info`, `biz`).

2. **Verificación DNS**:
   - Para cada dominio, realiza una verificación rápida de DNS buscando registros `MX` y `NS` para determinar si el dominio está activo.
   - Los dominios sin registros DNS se agregan a una lista para una verificación adicional.

3. **Verificación de Registro (WHOIS)**:
   - Los dominios en la lista sin registros DNS se verifican mediante `whois` para determinar si están registrados.
   - Los dominios que no tienen información `whois` se consideran no registrados y se almacenan en una lista final.

4. **Salida de resultados**:
   - Los dominios no registrados se imprimen en pantalla y se guardan en un archivo con un nombre basado en la fecha y hora de ejecución (`output_YYYYMMDDHHMMSS.txt`).

## Requisitos

- **Python 3.x**
- **Módulos de Python**:
  - `whois`
  - `dnspython`

## Instalación

Instala los módulos ejecutando:
- pip install python-whois dnspython

## Uso
Para ejecutar el script, utiliza el siguiente comando en la terminal:
python script.py archivo_dominio.txt [extensions.txt]
-archivo_dominio.txt: Archivo de entrada con dominios, palabras clave o correos electrónicos, uno por línea.
-extensions.txt: (Opcional) Archivo con una lista de TLDs, uno por línea. Si no se proporciona, se usarán TLDs predeterminados (com, net, org, info, biz).

## Ejemplo
Supón que tienes un archivo entrada.txt con el siguiente contenido:

example
test@example.com
website.net

Y un archivo extensions.txt con:
com
org
co

La salida se imprimirá en pantalla y se guardará en un archivo de texto llamado output_YYYYMMDDHHMMSS.txt, donde YYYYMMDDHHMMSS representa la fecha y hora de ejecución del script. El archivo de salida incluirá únicamente los dominios no registrados, en el siguiente formato:

example.com está DISPONIBLE
example.org está DISPONIBLE
website.net está DISPONIBLE

## Notas
Delay: El script introduce un retardo aleatorio en la verificación whois para evitar sobrecargar los servidores y cumplir con las políticas de uso de whois.
Compatibilidad: Este script está diseñado para sistemas basados en UNIX/Linux. Si deseas ejecutarlo en Windows, pueden ser necesarios ajustes adicionales.
Limitación para dominios .es: Debido a restricciones del módulo whois, este script puede no funcionar de manera confiable para dominios .es.

## Contribuciones
¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar el proyecto, no dudes en abrir un issue o enviar un pull request.

Creado por Andrés Naranjo @TheXXLMAN '2024 - [Contacta conmigo en MyPublicInbox](https://mypublicinbox.com/thexxlman)
