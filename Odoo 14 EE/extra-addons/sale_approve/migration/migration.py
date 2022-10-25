"""
Fields Studio                     Type
x_studio_val_ventas               Boolean
x_studio_val_credito              Boolean
x_studio_val_pago                 Boolean
x_studio_solicitud_de_embarques   Selection['Si']

Fields Code                     Type
Please see sale_approve/models/sale.py
"""

all_sale_objects = self.env['sale.order'].search([])
count = 0
total = len(all_sale_objects)

for record in all_sale_objects:
    if record.x_studio_val_ventas:
        record.approve_state='draft'
    if record.x_studio_val_credito:
        record.approve_state='done'
    if record.x_studio_val_pago:
        record.approve_state='confirm'
    if record.x_studio_solicitud_de_embarques in ['Si']:
        record.shipment_state='done'
    count = count +1
    print('%s de %s'%(count,total))

##  python3 -m ptvsd --host localhost --port 5678 /usr/bin/odoo --config /etc/odoo/odoo.conf --xmlrpc-port=8001 --workers=0 -u sale_approve
##  /usr/bin/odoo shell -d Z_TEST --config /etc/odoo/odoo.conf --xmlrpc-port=8001