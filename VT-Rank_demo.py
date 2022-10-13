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






