invoices = self.env['account.move'].search([
    ('invoice_date','>=','2022-10-01'),
    ('invoice_date','<=','2022-10-31'),
    ('move_type','in',['out_invoice']),
    # ('state','in',['posted']),

    # ('move_type','in',['out_invoice','out_refund'])
])

sum(invoices.mapped('balance'))