# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json
#curl -X POST -H "Content-Type: application/json" -d '{}' http://192.168.1.126:8001/reporte_direccion
class ZtyresMsSqlExcelReports(http.Controller):
#http://your_odoo_domain_or_ip/reportes_ztyreshome?db=your_database_name


    @http.route('/reporte_direccion', auth='public', methods=['GET'], website=True)
    def insert_dataframe_2(self):
        request.env['ztyres_ms_sql_excel_reports'].sudo().genererate_direccion_report()
        data = {"message": "Dataframe inserted successfully"}
        return Response(json.dumps(data), content_type='application/json;charset=utf-8', status=200)
    
    
    @http.route('/reporte_pruebaaxel', auth='public', methods=['GET'], website=True)
    def insert_dataframe_3(self):
        request.env['ztyres_ms_sql_excel_reports_pruebaaxel'].sudo().genererate_pruebaaxel_report()
        data = {"message": "Dataframe inserted successfully"}
        return Response(json.dumps(data), content_type='application/json;charset=utf-8', status=200)
