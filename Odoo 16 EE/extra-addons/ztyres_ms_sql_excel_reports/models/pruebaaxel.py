import pandas as pd
import numpy as np


#pip install pyodbc sqlalchemy
#apt-get install unixodbc
from odoo import api, fields, models
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

class MyModel(models.TransientModel):
    _name = 'ztyres_ms_sql_excel_reports_pruebaaxel'

    # Configuramos la semilla para la reproducibilidad
    def genererate_pruebaaxel_report(self):
        n = 100
        df = pd.DataFrame({
            'id': range(1, n + 1),
            'edad': np.random.randint(18, 61, n),  # Edades aleatorias entre 18 y 60
            'puntaje': np.random.randint(0, 101, n),  # Puntajes aleatorios entre 0 y 100
            'categoria': np.random.choice(["A", "B", "C", "D"], n)  # Categorías aleatorias
        })
        print(df)
        reports_core = self.env['ztyres_ms_sql_excel_core']
        reports_core.action_insert_dataframe(df,'reporte_pruebaaxel')