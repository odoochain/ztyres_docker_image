import pandas as pd
import requests
from xmlrpc import client as xmlrpc_client
from decouple import config

"""
Modified Files


_get_csf_tables /home/isscjrmpacheco/.local/lib/python3.10/site-packages/pandas/io/html.py
read_csf "read_csf", /home/isscjrmpacheco/.local/lib/python3.10/site-packages/pandas/__init__.py
/home/isscjrmpacheco/.local/lib/python3.10/site-packages/pandas/io/api.py
from pandas.io.html import read_csf
pip install python-decouple
"""

# Disable warnings for urllib3
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'


def format_address(values):
    """Formats an address based on a provided dictionary."""
    
    road_type = values.get('Tipo de vialidad:', '')
    road_name = values.get('Nombre de la vialidad:', '')
    external_number = values.get('Número exterior:', '')
    internal_number = values.get('Número interior:', '')
    neighborhood = values.get('Colonia:', '')

    address = "{} {} NO. {}".format(road_type, road_name, external_number)
    if internal_number:
        address += " Int. " + internal_number
    if neighborhood:
        address += " COLONIA " + neighborhood

    return address


def get_csf_data_from_url(url):
    rfc = url.split('_')[1]
    page = requests.get(url, verify=False)
    html = page.content.decode("utf-8")
    all_tables = pd.read_csf(html)
    vals = {}
    regimes = []
    for table in all_tables:
        for row in table:
            if len(row) == 2 and row[0] and row[1]:
                if row[0] == "Régimen:":
                    regimes.append(row[1])
                    continue
                vals.update({row[0]: row[1]})
        
    vals.update({"Régimen:":list(set(regimes))})
    name = vals.get('Denominación o Razón Social:') or '%s %s %s' % (
        vals.get('Nombre:') or "",
        vals.get('Apellido Paterno:') or "",
        vals.get('Apellido Materno:') or ""
    )

    odoo_vals = {
        'name': name,
        'street': format_address(vals),
        'state_id': vals.get('Entidad Federativa:'),
        'city_id': vals.get('Municipio o delegación:'),
        'zip': vals.get('CP:'),
        'country_id': 156,
        'vat': rfc,
        'l10n_mx_edi_fiscal_regime': vals.get('Régimen:')
    }

    return odoo_vals
# url = "https://siat.sat.gob.mx/app/qr/faces/pages/mobile/validadorqr.jsf?D1=10&D2=1&D3=14040812593_CVR140214T41"

# print(get_csf_data_from_url(url))





    


