
#pip install pyodbc sqlalchemy
#apt-get install unixodbc
from odoo import api, fields, models
import pandas as pd

class MyModel(models.TransientModel):
    _name = 'ztyres_ms_sql_excel_reports'
    
    def genererate_direccion_report(self):
        reports_direccion = self.env['ztyres_ms_sql_excel_reports_direccion']
        x = reports_direccion.dict_to_df(reports_direccion.get_all_products())
        t = reports_direccion.last_six_months_details()
        res = reports_direccion.add_month(x,'out_invoice','out_refund',t)
        res = reports_direccion.add_transit(res)
        res = reports_direccion.add_price_list(res,1,'MAYOREO')
        res = reports_direccion.add_price_list(res,7,'PROMO')
        res = reports_direccion.add_price_list(res,21,'ESPECIAL')
        res = reports_direccion.add_ucf(res)
        res = reports_direccion.add_upf(res)
        res = reports_direccion.add_backorder(res)
        reports_core = self.env['ztyres_ms_sql_excel_core']
        reports_core.action_insert_dataframe(res,'reporte_direccion')
        
        