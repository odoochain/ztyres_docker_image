
#pip install pyodbc sqlalchemy
#apt-get install unixodbc
from odoo import api, fields, models
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

class MyModel(models.TransientModel):
    _name = 'ztyres_ms_sql_excel_reports_direccion'

    def get_transit_qty(self,product_tmpl_ids):
        query = """
        SELECT  
            pp.product_tmpl_id as id,
            SUM(sq.quantity) AS transito 
        FROM stock_quant sq
        JOIN
            product_product AS pp ON sq.product_id = pp.id
        WHERE location_id in (53, 24686, 24687) AND
        pp.product_tmpl_id IN %s 
        GROUP BY
            pp.product_tmpl_id
        """
        params = (tuple(product_tmpl_ids),)
        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()
        return results


    def get_purchase_backorder_qty(self):
        query = """
        SELECT 
            pp.product_tmpl_id as id,
            pol.product_qty - pol.qty_invoiced as purchase_backorder 
        FROM 
            purchase_order_line pol
        JOIN 
            product_product AS pp ON pol.product_id = pp.id
        WHERE 
            pol.order_id IN (
                SELECT id 
                FROM purchase_order po 
                WHERE 
                    po.state IN ('purchase') AND
                    po.invoice_status NOT IN ('invoiced', 'cancel')
            ) 
            AND (pol.product_qty - pol.qty_invoiced) > 0;
            """
        self.env.cr.execute(query)
        results = self.env.cr.dictfetchall()
        return results


    def get_origin_name(self,product_tmpl_ids):
        query = """
        select pt.id ,rc."name"->>'es_ES' as x_studio_origen from product_template pt
        join res_country rc on pt.x_studio_origen = rc.id where active = true
        and pt.id IN %s
        """
        params = (tuple(product_tmpl_ids),)
        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()
        return results

    def get_upf(self,product_tmpl_ids):
        query = """
        WITH OldestRecords AS (
            SELECT 
                pp.product_tmpl_id,
                MIN(aml.create_date) AS oldest_date
            FROM account_move_line AS aml
            JOIN product_product AS pp ON aml.product_id = pp.id
            JOIN account_move AS am ON aml.move_id = am.id
            WHERE am.state IN ('posted') 
            AND aml.display_type = 'product'
            AND am.move_type = 'out_invoice'
            AND pp.product_tmpl_id = 49055
            GROUP BY pp.product_tmpl_id
        )

        SELECT
            pp.product_tmpl_id as id,
            aml."date" as fecha_upf,
            aml.price_unit as upf
        FROM account_move_line AS aml
        JOIN product_product AS pp ON aml.product_id = pp.id
        JOIN account_move AS am ON aml.move_id = am.id
        JOIN OldestRecords AS o ON o.product_tmpl_id = pp.product_tmpl_id AND o.oldest_date = aml.create_date
        WHERE am.state IN ('posted') 
        AND pp.product_tmpl_id = %s
        AND aml.display_type = 'product'
        AND am.move_type = 'out_invoice';

        """
        params = (tuple(product_tmpl_ids),)
        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()
        return results



    def get_upf(self,product_tmpl_ids):
        query = """
        WITH OldestRecords AS (
            SELECT 
                pp.product_tmpl_id,
                MIN(aml.create_date) AS oldest_date
            FROM account_move_line AS aml
            JOIN product_product AS pp ON aml.product_id = pp.id
            JOIN account_move AS am ON aml.move_id = am.id
            WHERE am.state IN ('posted') 
            AND aml.display_type = 'product'
            AND am.move_type = 'out_invoice'
            AND pp.product_tmpl_id in %s
            GROUP BY pp.product_tmpl_id
        )

        SELECT
            pp.product_tmpl_id as id,
            aml."date" as fecha_upf,
            aml.price_unit as upf
        FROM account_move_line AS aml
        JOIN product_product AS pp ON aml.product_id = pp.id
        JOIN account_move AS am ON aml.move_id = am.id
        JOIN OldestRecords AS o ON o.product_tmpl_id = pp.product_tmpl_id AND o.oldest_date = aml.create_date
        WHERE am.state IN ('posted') 
        AND pp.product_tmpl_id in %s
        AND aml.display_type = 'product'
        AND am.move_type = 'out_invoice';

            """
        params = (tuple(product_tmpl_ids),tuple(product_tmpl_ids))
        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()
        return results


    def get_avg_cost_inv(self,product_tmpl_ids):
        query = """
        WITH RankedRecords AS (
            SELECT 
                pp.product_tmpl_id as id,
                aml."date" as fecha_ucf,
                aml.price_unit ucf_final,
                ROW_NUMBER() OVER(PARTITION BY pp.product_tmpl_id ORDER BY aml."date" ASC) AS rn
            FROM 
                account_move_line AS aml
            JOIN 
                product_product AS pp ON aml.product_id = pp.id
            JOIN 
                account_move AS am ON aml.move_id = am.id
            WHERE 
                am.state IN ('posted') AND
                pp.product_tmpl_id IN %s AND
                aml.display_type = 'product' AND
                am.move_type = 'in_invoice')

        SELECT
        id,fecha_ucf,ucf_final
        FROM 
            RankedRecords
        WHERE 
            rn = 1;
        """
        params = (tuple(product_tmpl_ids), )
        self.env.cr.execute(query, params)
        print(query)
        results = self.env.cr.dictfetchall()
        return results


    def get_ucf(self,product_tmpl_ids):
        query = """
        WITH RankedRecords AS (
            SELECT 
                pp.product_tmpl_id as id,
                aml."date" as fecha_ucf,
                aml.price_unit ucf_final,
                ROW_NUMBER() OVER(PARTITION BY pp.product_tmpl_id ORDER BY aml."date" ASC) AS rn
            FROM 
                account_move_line AS aml
            JOIN 
                product_product AS pp ON aml.product_id = pp.id
            JOIN 
                account_move AS am ON aml.move_id = am.id
            WHERE 
                am.state IN ('posted') AND
                pp.product_tmpl_id IN %s AND
                aml.display_type = 'product' AND
                am.move_type = 'in_invoice')

        SELECT
        id,fecha_ucf,ucf_final
        FROM 
            RankedRecords
        WHERE 
            rn = 1;
        """
        params = (tuple(product_tmpl_ids), )
        self.env.cr.execute(query, params)
        print(query)
        results = self.env.cr.dictfetchall()
        return results

    def get_price_list(self,product_tmpl_ids, price_list_id,name):
        query = """
        SELECT 
            product_tmpl_id AS id, 
            fixed_price AS "%s" 
        FROM 
            product_pricelist_item ppi  
        WHERE 
            applied_on = '1_product'
            AND pricelist_id = %s 
            AND product_tmpl_id IN %s;
            """
        params = (name,price_list_id, tuple(product_tmpl_ids))
        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()
        return results

    def get_last_invoice_product_price(self,product_tmpl_id,move_type):
        domain = [
            ('product_id.product_tmpl_id', '=', product_tmpl_id),
            ('move_id.state', 'in', ['posted']),
            ('display_type','=','product'),
            ('move_id.move_type', 'in', [move_type])
        ]
        return self.env['account.move.line'].search(domain)

    def get_last_invoice_product_cost(self,product_tmpl_id):
        return self.get_last_invoice_product_price(product_tmpl_id,'in_invoice').x_studio_costo_final
############################################aqui esta ventas netas en linea 239
    def get_last_invoice_product_qty_by_period(self,month_name, product_tmpl_ids,move_type,reverse_move_type, date_from, date_to):
        query = """
            SELECT
                aml.product_id as id,
                SUM(CASE WHEN am.move_type = %s THEN aml.quantity ELSE -aml.quantity END) AS "%s"
            FROM
                account_move_line AS aml
            JOIN
                product_product AS pp ON aml.product_id = pp.id
            JOIN
                account_move AS am ON aml.move_id = am.id
            WHERE
                pp.product_tmpl_id IN %s AND
                am.state IN ('posted') AND
                aml.display_type = 'product' AND
                am.move_type IN (%s, %s) AND
                am.date >= %s AND
                am.date <= %s
            GROUP BY
                aml.product_id
            ORDER BY
                aml.product_id;
        """ 
        self.env.cr.execute(query, (move_type,month_name, tuple(product_tmpl_ids),move_type,reverse_move_type, date_from, date_to))
        results = self.env.cr.dictfetchall()
        return results

    def get_all_products(self):
        desired_fields = [
            'default_code',
            'x_studio_medida_1',
            'x_studio_cara',
            'x_studio_capas',
            'x_studio_ndice_de_velocidad',
            'x_studio_indice_carga',
            'x_studio_modelo_1',
            'x_studio_marca',
            'x_studio_fabricante',
            'x_studio_segmento',
            'x_studio_uso',
            'x_studio_posicionamiento',
            'qty_available',
            'outgoing_qty'
            ]
        return self.env['product.template'].search_read([('detailed_type','in',['product'])], fields=desired_fields)

    def dict_to_df(self,dict):
        df = pd.DataFrame(dict)
        return df

    def add_month(self,dataframe, move_type,reverse_move_type, details):
        ids = dataframe['id'].unique().tolist()
        dfs_to_merge = [pd.DataFrame(self.get_last_invoice_product_qty_by_period(item['month_name'], ids, move_type,reverse_move_type, item['start_date'], item['end_date'])) for item in details]
        for df in dfs_to_merge:
            try:
                if not df.empty:
                    dataframe = dataframe.merge(df, on='id', how='left')
            except:
                print('Hola')
        return dataframe

    def add_transit(self,dataframe):
        ids = dataframe['id'].unique().tolist()
        dfs_to_merge = pd.DataFrame(self.get_transit_qty(ids))
        return dataframe.merge(dfs_to_merge, on='id', how='left')

    def add_price_list(self,dataframe,pricelist_id,name):
        ids = dataframe['id'].unique().tolist()
        dfs_to_merge = pd.DataFrame(self.get_price_list(ids,pricelist_id,name))
        return dataframe.merge(dfs_to_merge, on='id', how='left')



    def add_ucf(self,dataframe):
        ids = dataframe['id'].unique().tolist()
        dfs_to_merge = pd.DataFrame(self.get_ucf(ids))
        return dataframe.merge(dfs_to_merge, on='id', how='left')

    def add_origin(self,dataframe):
        ids = dataframe['id'].unique().tolist()
        dfs_to_merge = pd.DataFrame(self.get_origin_name(ids))
        return dataframe.merge(dfs_to_merge, on='id', how='left')

    def add_upf(self,dataframe):
        ids = dataframe['id'].unique().tolist()
        dfs_to_merge = pd.DataFrame(self.get_upf(ids))
        return dataframe.merge(dfs_to_merge, on='id', how='left')


    def add_backorder(self,dataframe):
        dfs_to_merge = pd.DataFrame(self.get_purchase_backorder_qty())
        return dataframe.merge(dfs_to_merge, on='id', how='left')

    def last_six_months_details(self):
        MONTHS_IN_SPANISH = {
            1: 'ENERO',
            2: 'FEBRERO',
            3: 'MARZO',
            4: 'ABRIL',
            5: 'MAYO',
            6: 'JUNIO',
            7: 'JULIO',
            8: 'AGOSTO',
            9: 'SEPTIEMBRE',
            10: 'OCTUBRE',
            11: 'NOVIEMBRE',
            12: 'DICIEMBRE'
        }
        today = datetime.date.today()
        months_details = []
        for _ in range(6):
            first_day_of_month = datetime.date(today.year, today.month, 1)
            last_day_of_month = (first_day_of_month.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
            month_name = MONTHS_IN_SPANISH[today.month]
            months_details.append({
                'month_name': month_name,
                'start_date': first_day_of_month,
                'end_date': last_day_of_month
            })
            today -= relativedelta(months=1)
        return months_details