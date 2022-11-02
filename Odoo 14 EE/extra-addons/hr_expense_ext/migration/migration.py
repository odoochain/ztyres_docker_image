expenses = self.env['hr.expense.sheet'].search([])

# expenses = self.env['hr.expense.sheet'].browse(1444)
# expenses = self.env['hr.expense.sheet'].search([('id','in',[1374])])
expenses = self.env['hr.expense.sheet'].search([])
for record in expenses:
    messages = self.env['mail.message'].search([('model','in',['hr.expense.sheet']),('res_id','in',[record.id])])
    print(messages)
    
    for message in messages:
        for track in message.tracking_value_ids:            
            for rec in track:                
                if rec.field_desc == 'Estado' and rec.field_type == 'selection' and rec.old_value_char == 'Publicado' and rec.new_value_char == 'Pagado':
                    record.payment_date = rec.create_date
                    print('Cambiado'+str(record.id))
                    print(record.payment_date)
        if message.message_type == 'notification' and message.subtype_id.id == 21:
            record.payment_date = message.date
            print('Cambiado'+str(record.id))
            print(record.payment_date)                    
                        


