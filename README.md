#Run once as sudo

mkdir -p /ZTYRES/DB
chmod 777 -R /ZTYRES/DB



mkdir -p /ZTYRES/FILESTORE
chmod 777 -R /ZTYRES/FILESTORE

Actualizar en el siguiente orden

ztyres


Eliminar de la vista  /web?debug=1#id=1807&menu_id=4&cids=1&action=28&model=ir.ui.view&view_type=form 
    <field name="x_studio_nombre_paqueteria" string="Nombre Paquetería" readonly="False"/>

/web?debug=1#id=1216&menu_id=4&cids=1&action=28&model=ir.ui.view&view_type=form
 <button name="fix_weigth" type="object" string="Solucionar Peso en 0"/>


 /web#id=1807&cids=1&menu_id=4&action=28&model=ir.ui.view&view_type=form

  <xpath expr="//button[@name='action_cancel']" position="replace"/>
  <xpath expr="//field[@name='partner_id']" position="attributes">
    <attribute name="attrs">{"readonly": [["state","in",["sale","done","cancel"]]]}</attribute>
  </xpath>


Actualizar lista de aplicaciones

Actualizar en el siguiente orden

ztyres_sale
sale_management


