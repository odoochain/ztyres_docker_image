# -*- coding: utf-8 -*-

from email.policy import default
from re import M
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta, date
import calendar
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import json
import io
from odoo.tools import date_utils
import base64
import logging 
_logger = logging.getLogger(__name__)

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class DirReport(models.Model): 
    _name = 'dir.report'


    def sql_queries(self):
        lines = []
        sql = ('''
            select pt.id, x_studio_medida_1 as medida, x_studio_cara as cara, x_studio_capas as capas, x_studio_ndice_de_velocidad as vel,x_studio_indice_carga as indCarga, x_studio_modelo_1 as modelo, x_studio_marca as marca,x_studio_fabricante as fabricante, x_studio_uso as uso,x_studio_segmento as segmento, x_studio_segmento_proveedor as segProv,(select name from res_country where id=x_studio_origen) as pais,x_studio_posicionamiento as tier,x_studio_e_mark as emark,x_studio_s_mark as smark,x_studio_ccc as ccc, pt.default_code as codigo
            from product_product pp inner join product_template pt on pp.product_tmpl_id=pt.id where pt.active = true 
        ''')
        self._cr.execute(sql)
        for row in self._cr.dictfetchall():
            lines.append(row)
        return lines
            

    def action_xlsx(self): 
        data = self.read()[0]
        #Initialize

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Dir Report')
        sheet.set_zoom(100)

        record = self.env['dir.report'].browse(data.get('id', [])) or False

        lines = self.sql_queries()
        #Formats
        sheet.set_column(0, 0, 12)
        sheet.set_column(1, 1, 10)
        sheet.set_column(2, 2, 10)
        sheet.set_column(3, 3, 10)
        sheet.set_column(4, 4, 25)
        sheet.set_column(5, 5, 12)
        sheet.set_column(6, 6, 15)
        sheet.set_column(7, 7, 10)
        sheet.set_column(8, 8, 15)
        sheet.set_column(9, 9, 13)
        sheet.set_column(10, 10, 15)
        sheet.set_column(11, 11, 10)
        sheet.set_column(12, 12, 20)
        sheet.set_column(13, 13, 15)
        sheet.set_column(14, 14, 15)
        sheet.set_column(15, 15, 15)
        sheet.set_column(16, 16, 15)
        sheet.set_column(17, 17, 15)
        sheet.set_column(18, 18, 15)
        sheet.set_column(19, 19, 15)
        sheet.set_column(20, 20, 15)
        sheet.set_column(21, 21, 15)
        sheet.set_column(22, 22, 15)
        sheet.set_column(23, 23, 15)
        sheet.set_column(24, 24, 15)
        sheet.set_column(25, 25, 15)
        sheet.set_column(26, 26, 15)
        sheet.set_column(27, 27, 15)
        sheet.set_column(28, 28, 15)
        sheet.set_column(29, 29, 15)
        sheet.set_column(30, 30, 15)
        sheet.set_column(31, 31, 15)
        sheet.set_column(32, 32, 15)
        sheet.set_column(33, 33, 15)
        sheet.set_column(34, 34, 15)
        sheet.set_column(35, 35, 15)
        sheet.set_column(36, 36, 15)
        sheet.set_column(37, 37, 15)
        sheet.set_column(38, 38, 15)
        sheet.set_column(39, 39, 15)
        sheet.set_column(40, 40, 15)
        sheet.set_column(41, 41, 15)
        sheet.set_column(42, 42, 15)
        sheet.set_column(43, 43, 15)
        sheet.set_column(44, 44, 15)
        sheet.set_column(45, 45, 15)
        sheet.set_column(46, 46, 15)
        sheet.set_column(47, 47, 15)
        sheet.set_column(48, 48, 15)
        sheet.set_column(49, 49, 15)
        sheet.set_column(50, 50, 15)
        sheet.set_column(51, 51, 15)


        sheet.freeze_panes(2, 0)

        format_header_green = workbook.add_format({
            'bold': True,
            'font_size': 11,
            'font': 'Geneva',
            'align': 'left',
            'bg_color': '3F9C19'
        })
        format_header_white = workbook.add_format({
            'bold': True, 
            'font_size': 11,
            'font': 'Geneva', 
            'align': 'left',
            'top' : True, 
            'bottom' : True,
        })
        format_header_black = workbook.add_format({
            'bold': True,
            'font_size': 11,
            'font': 'Geneva',
            'align': 'left',
            'bg_color': '000000',
            'font_color': 'white'
        })
        line_format = workbook.add_format({
            'font_size': 11,
            'font': 'Geneva',
            'align': 'left'
        })
        lang = self.env.user.lang
        lang_id = self.env['res.lang'].search([('code', '=', lang)])[0]
        
        #Write data

        current_time = fields.Date.from_string(str(datetime.now())).strftime(lang_id.date_format)
        row_pos = 0
        sheet.write(0, 0, current_time)

        row_pos+=1
        sheet.write_string(row_pos, 0, _('medida'), format_header_white)
        sheet.write_string(row_pos, 1, _('cara'), format_header_white)
        sheet.write_string(row_pos, 2, _('capas'), format_header_white)
        sheet.write_string(row_pos, 3, _('vel'), format_header_white)
        sheet.write_string(row_pos, 4, _('Indcarga'), format_header_white)
        sheet.write_string(row_pos, 5, _('modelo'), format_header_white)
        sheet.write_string(row_pos, 6, _('marca'), format_header_white)
        sheet.write_string(row_pos, 7, _('fabricante'), format_header_white)
        sheet.write_string(row_pos, 8, _('uso'), format_header_white)
        sheet.write_string(row_pos, 9, _('segmento'), format_header_white)
        sheet.write_string(row_pos, 10, _('segprov'), format_header_white)
        sheet.write_string(row_pos, 11, _('pais'), format_header_white)
        sheet.write_string(row_pos, 12, _('tier'), format_header_white)
        sheet.write_string(row_pos, 13, _('emark'), format_header_white)
        sheet.write_string(row_pos, 14, _('smark'), format_header_white)
        sheet.write_string(row_pos, 15, _('ccc'), format_header_white)
        sheet.write_string(row_pos, 16, _('codigo'), format_header_white)
        sheet.write_string(row_pos, 17, _('ene'), format_header_white)
        sheet.write_string(row_pos, 18, _('feb'), format_header_white)
        sheet.write_string(row_pos, 19, _('mar'), format_header_white)
        sheet.write_string(row_pos, 20, _('abr'), format_header_white)
        sheet.write_string(row_pos, 21, _('mayo'), format_header_white)
        sheet.write_string(row_pos, 22, _('junio'), format_header_white)
        sheet.write_string(row_pos, 23, _('julio'), format_header_white)
        sheet.write_string(row_pos, 24, _('agosto'), format_header_white)
        sheet.write_string(row_pos, 25, _('sep'), format_header_white)
        sheet.write_string(row_pos, 26, _('oct'), format_header_white)
        sheet.write_string(row_pos, 27, _('nov'), format_header_white)
        sheet.write_string(row_pos, 28, _('dic'), format_header_white)
        sheet.write_string(row_pos, 29, _('ene22'), format_header_white)
        sheet.write_string(row_pos, 30, _('feb22'), format_header_white)
        sheet.write_string(row_pos, 31, _('mar22'), format_header_white)
        sheet.write_string(row_pos, 32, _('abr22'), format_header_white)
        sheet.write_string(row_pos, 33, _('mayo22'), format_header_white)
        sheet.write_string(row_pos, 34, _('junio22'), format_header_white)
        sheet.write_string(row_pos, 35, _('julio22'), format_header_white)
        sheet.write_string(row_pos, 36, _('inv'), format_header_white)
        sheet.write_string(row_pos, 37, _('reser'), format_header_white)
        sheet.write_string(row_pos, 38, _('disp'), format_header_white)
        sheet.write_string(row_pos, 39, _('trans'), format_header_white)
        sheet.write_string(row_pos, 40, _('may'), format_header_white)
        sheet.write_string(row_pos, 41, _('promo'), format_header_white)
        sheet.write_string(row_pos, 42, _('esp'), format_header_white)
        sheet.write_string(row_pos, 43, _('upf'), format_header_white)
        sheet.write_string(row_pos, 44, _('promo'), format_header_white)
        sheet.write_string(row_pos, 45, _('cstfinal'), format_header_white)
        sheet.write_string(row_pos, 46, _('pedidocomp'), format_header_white)
        sheet.write_string(row_pos, 47, _('cstpedido'), format_header_white)
        sheet.write_string(row_pos, 48, _('presup'), format_header_white)
        sheet.write_string(row_pos, 49, _('cstpresup'), format_header_white)
        sheet.write_string(row_pos, 50, _('dot'), format_header_white)
        sheet.write_string(row_pos, 51, _('suma'), format_header_white)

        for line in lines: 
            if line.get('medida') != None and line.get('marca') != None and line.get('modelo') != None: 
                row_pos+=1
                sheet.write(row_pos, 0, line.get('medida'), line_format)
                sheet.write(row_pos, 1, line.get('cara'), line_format)
                sheet.write(row_pos, 2, line.get('capas'), line_format)
                sheet.write(row_pos, 3, line.get('vel'), line_format)
                sheet.write(row_pos, 4, line.get('indCarga'), line_format)
                sheet.write(row_pos, 5, line.get('modelo'), line_format)
                sheet.write(row_pos, 6, line.get('marca'), line_format)
                sheet.write(row_pos, 7, line.get('fabricante'), line_format)
                sheet.write(row_pos, 8, line.get('uso'), line_format)
                sheet.write(row_pos, 9, line.get('segmento'), line_format)
                sheet.write(row_pos, 10, line.get('segprov'), line_format)
                sheet.write(row_pos, 11, line.get('pais'), line_format)
                sheet.write(row_pos, 12, line.get('tier'), line_format)
                sheet.write(row_pos, 13, line.get('emark'), line_format)
                sheet.write(row_pos, 14, line.get('smark'), line_format)
                sheet.write(row_pos, 15, line.get('ccc'), line_format)
                sheet.write(row_pos, 16, line.get('codigo'), line_format)

        #Close and return
        workbook.close()
        output.seek(0)
        result = base64.b64encode(output.read())

        report_id = self.env['common.xlsx.out'].sudo().create({'filedata': result, 'filename': 'GL.xlsx'})
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=common.xlsx.out&field=filedata&id=%s&filename=%s.xlsx' % (
            report_id.id, 'DirReport'),
            'target': 'new',
        }

        output.close()

