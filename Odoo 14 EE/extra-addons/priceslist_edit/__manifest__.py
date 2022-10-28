
{
    "name": "Change the field price_list_id",
    "summary": "Change the field price_list_id to be readonly until accessed by authorized user",
    "version": "14.0.1.1.0",
    "category": "Sales",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
    ],
    "data": [
        "views/list_prices_edit.xml",
    ],
}
