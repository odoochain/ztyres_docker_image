from odoo import api, fields, models
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

def get_unique_by_id(self,lst):
    seen = set()
    unique_lst = []
    for d in lst:
        if d['ID'] not in seen:
            seen.add(d['ID'])
            unique_lst.append(d)
    return unique_lst
def sacar_reporte(self):
    report_dataAccMov = []
    account_move = self.env['account.move']
    domainAccMov = [('move_type', 'in', ['out_invoice']),
                    ('state', 'in', ['posted'])]
    resAccMov = account_move.search(domainAccMov, order='date desc')
    for recAccMov in resAccMov:
        if (recAccMov.partner_id.sale_order_count > 0
            and recAccMov.partner_id.purchase_order_count == 0
            and recAccMov.partner_id.type == 'contact'):
            for recAccMovline in recAccMov.invoice_line_ids:
                valsAccMovline = {
                    'ID': recAccMovline.product_id.id or '',
                    'CostoUnitario': recAccMovline.price_unit or '',
                    'fechaUnitari': recAccMov.date.strftime("%Y/%m/%d") or ''
                }
                report_dataAccMov.append(valsAccMovline)

    lista_distinct = get_unique_by_id(report_dataAccMov)

    report_dataAccMovProv = []
    account_moveProv = self.env['account.move']
    domainAccMovProv = [('move_type', 'in', ['out_invoice']),
                        ('state', 'in', ['posted'])]
    resAccMovProv = account_moveProv.search(domainAccMovProv, order='date desc')
    for recAccMovProv in resAccMovProv:
        if (recAccMovProv.partner_id.sale_order_count == 0
            and recAccMovProv.partner_id.purchase_order_count > 0
            and recAccMovProv.partner_id.type == 'contact'):
            for recAccMovline in recAccMovProv.invoice_line_ids:
                valsAccMovline = {
                    'ID': recAccMovline.product_id.id or '',
                    'Costo Unitario': recAccMovline.price_unit or '',
                    'fecha': recAccMovProv.date.strftime("%Y/%m/%d") or ''
                }
                report_dataAccMovProv.append(valsAccMovline)

    lista_distinctprov = get_unique_by_id(report_dataAccMovProv)

    puchase_order = self.env['purchase.order']
    domainPO = []
    resPO = puchase_order.search(domainPO, order='date_approve desc')
    report_dataPO = []
    for recPO in resPO:
        for recline in recPO.order_line:
            if (recline.qty_received > 0 and (recline.x_studio_costo_final > 0 or recline.price_unit > 0)
                and recline.price_unit > 0):
                vals = {
                    'ID': recline.product_id.id,
                    'PrecioUnitario': recline.price_unit,
                    'CostoFinal': recline.x_studio_costo_final
                }
                report_dataPO.append(vals)

    lista_distinctpo = get_unique_by_id(report_dataPO)

    report_data = []
    product_template = self.env['product.template']
    product_pricelist = self.env['product.pricelist']
    domain = [('default_code', '!=', False),
            ('x_studio_posicionamiento', '!=', False)]
    res = product_template.search(domain)
    resPricelist = product_pricelist.search([])
    vals = {}
    for rec in res:
        vals = {
            'ID': rec.id,
            'codigo': rec.default_code or '',
            'medida': rec.x_studio_medida_1 or '',
            'cara': rec.x_studio_cara or '',
            'capas': rec.x_studio_capas or '',
            'vel': rec.x_studio_ndice_de_velocidad or '',
            'indcarga': rec.x_studio_indice_carga or '',
            'modelo': rec.x_studio_modelo_1 or '',
            'marca': rec.x_studio_marca or '',
            'fabricante': rec.x_studio_fabricante or '',
            'seg': rec.x_studio_segmento or '',
            'uso': rec.x_studio_uso or '',
            'tier': rec.x_studio_posicionamiento or '',
            'pais': rec.x_studio_origen.name or '',
            'Abril': '',
            'Mayo': '',
            'Junio': '',
            'Julio': '',
            'Agosto': '',
            'Septiembre':'',
            'inv': rec.qty_available or '',
            'resev': rec.product_variant_id.outgoing_qty or '',
            'Disp': rec.product_variant_id.free_qty or '',
            'Tran': '',
            'may': '',
            'promo': '',
            'esp': '',
            'upf': '',
            'fechaUpf': '',
            'UCFact': '',
            'UCFinal': '',
            'CPFact': '',
            'CPFinal': '',
            'BO': '',
            'CBO': ''
        }
        valorID = rec.id
        product_product_id = rec.product_variant_id.id
        for recPricelist in resPricelist:
            for id_price in recPricelist.item_ids:
                value = id_price.product_tmpl_id.id
                if value == valorID:
                    precios = {
                        'PromoID': recPricelist.id,
                        'idProducto': value,
                        'precio': id_price.fixed_price
                    }
                    if recPricelist.id == 21:
                        vals.update({'esp': id_price.fixed_price})
                    if recPricelist.id == 1:
                        vals.update({'may': id_price.fixed_price})
                    if recPricelist.id == 7:
                        vals.update({'promo': id_price.fixed_price})
        for PrecioUnitario in lista_distinct:
            if PrecioUnitario['ID'] == product_product_id:
                vals.update({'upf': PrecioUnitario['CostoUnitario']})
                vals.update({'fechaUpf': PrecioUnitario['fechaUnitari']})
        for PrecioUnitarioPO in lista_distinctpo:
            if PrecioUnitarioPO['ID'] == product_product_id:
                vals.update({'UCFact': PrecioUnitarioPO['PrecioUnitario']})
                vals.update({'UCFinal': PrecioUnitarioPO['CostoFinal']})
        if vals['inv'] != '' or vals['upf'] != '' or vals['UCFact'] != '':
            report_data.append(vals)

    # ventas netas mensuales

    mesesNum = [ 4, 5, 6, 7, 8, 9]
    account_moveVN = self.env['account.move']
    meses = [ 0,0,0,0,'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre']
    mesesLastDay = [0, 0, 0, 0, 30, 31, 30, 31, 31, 30]

    for i in mesesNum:
        domainMes = []
        desde = '2023-0%s-01' % (str(i))
        hasta = '2023-0%s-%s' % (str(i), str(mesesLastDay[i]))
        domainMes.append(('invoice_date', '>=', desde))
        domainMes.append(('invoice_date', '<=', hasta))
        domainMes.append(('move_type', 'in', ['out_invoice', 'out_refund']))
        domainMes.append(('state', 'in', ['posted']))
        resVN = account_moveVN.search(domainMes)
        cantidad_productoVN = {}
        for recVN in resVN:
            for line in recVN.invoice_line_ids.filtered(lambda line: line.product_id.detailed_type == 'product'):
                cantidad = line.quantity
                id_producto = line.product_id.product_tmpl_id.id
                if id_producto in cantidad_productoVN:
                    if recVN.move_type in ['out_refund']:
                        cantidad_productoVN[id_producto] -= cantidad
                    else:
                        cantidad_productoVN[id_producto] += cantidad
                else:
                    if recVN.move_type in ['out_refund']:
                        cantidad_productoVN[id_producto] = -cantidad
                    else:
                        cantidad_productoVN[id_producto] = cantidad
        resultadosVN = [{'idProducto': id_producto, 'suma_cantidades': suma_cantidades}
                                for id_producto, suma_cantidades in cantidad_productoVN.items()]
        for producto in report_data:
            for recP in resultadosVN:
                if recP['idProducto'] == producto['ID']:
                    producto[meses[i]] = recP['suma_cantidades']

    report_data_fob_cif=[]

    for dato in report_data:
        if dato['marca'] in ['KUMHO','CONTINENTAL','GOODYEAR','MASTERCRAFT','FIRESTONE','DUNLOP','PIRELLI','COOPER','BRIDGESTONE']:
            if dato ['Disp'] != False and dato['Disp'] != '' : 
                report_data_fob_cif.append(dato)

    df1 = pd.DataFrame(report_data_fob_cif)
    df = pd.DataFrame(report_data)

    ruta_archivo_excel = '/mnt/extra-addons/reporteDireccion_4.xlsx'
    # Se crea el archivo Excel y se guarda el DataFrame en una hoja llamada 'Facturas'
    with pd.ExcelWriter(ruta_archivo_excel) as writer:
        df1.to_excel(writer, sheet_name='Data_Fob_Cif')
        df.to_excel(writer, sheet_name='Data_Direccion')
        
    

