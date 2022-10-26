
import pandas as pd 

# select * from res_lang rl 
# select * from ir_translation it 

fields = self.env['ir.model.fields'].search([('model_id.model','in',['res.partner'])])
data = []
for field in fields:
    record = \
        {   'Etiqueta de campo' :field.field_description.translate(''),
            'Tipo':field.ttype,
            'Requerido':field.required,
            'Solo Lectura':field.readonly,
            'Tipo Nativo':field.state,
            'Nombre Técnico':field.name
        }
    data.append(record)
# Creates DataFrame.  
df = pd.DataFrame(data)  
# Print the data  
print(df)  
