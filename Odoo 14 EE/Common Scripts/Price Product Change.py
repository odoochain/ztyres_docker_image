"""Price Product change
    
    Allows change recordset product informatión of list_price field

    Parameters example
    new_prices_list = [('03504580000',1299.97),('15485630000',1179.67)]
    """
def price_product_change(self,new_prices_list):
    product_template = self.env['product.template']
    for product in new_prices_list:
        product_to_change = product_template.search([('default_code','in',[product[0]])])
        product_to_change.ensure_one()
        product_to_change.list_price = product[1]


new_prices_list = [('03504580000',1299.97),('15485630000',1179.67)]

price_product_change(self,new_prices_list)