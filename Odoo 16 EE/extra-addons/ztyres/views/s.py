product_template = self.env['product.template'].with_context(lang='es_MX').search([])
for product in product_template:
    try:
        product.unlink()
        print("BORRADO")
    except:
        print("No borrado")
    


