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


count = 0
stock_picking = self.env['stock.picking'].search([])
total = len(stock_picking)
for record in stock_picking:
    if record.state in ['done']:
        if record.sale_id:
            if record.sale_id.shipment_state in ['done']:
                record.shipment_state = 'done'
        
        count = count +1
        print('%s de %s'%(count,total))

count = 0
sales_order = self.env['sale.order'].search([])
total = len(sales_order)
err = []
for record in sales_order:
    try:
        state = dict(record._fields['state'].selection).get(record.state)
        print(state)
        if state in ['Sales Order']:
            for rec in record.picking_ids:
                if rec.state  in ['done']:
                    record.shipment_state = 'done'
        if state in ['Locked']:
            record.action_unlock()
            print(record.state)
            if state in ['Sales Order']:
                for rec in record.picking_ids:
                    if rec.state  in ['done']:
                        record.shipment_state = 'done'   
            record.action_done()
            print(state)                    
        count = count +1
        print('%s de %s'%(count,total))
    except:
        count = count +1
        print('%s de %s'%(count,total))
        err.append(record.id)

                




##  python3 -m ptvsd --host localhost --port 5678 /usr/bin/odoo --config /etc/odoo/odoo.conf --xmlrpc-port=8001 --workers=0 -u sale_approve
##  /usr/bin/odoo shell -d SALE_APPROVE --config /etc/odoo/odoo.conf --xmlrpc-port=8001 --workers=8
