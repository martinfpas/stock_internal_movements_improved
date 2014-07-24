# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Stock Internal Movements Improved
#    Copyright (C) 2014 Martin Pascualon <martinfpas@gmail.com>
#    Enterprise Objects Consulting (<http://www.sysfe.com.ar>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name'          : 'Stock Internal Movements Improved',
    'version'       :'1.14',
    'author'        : 'Martin Pascualon : Sysfe',
    'description'   : """
Move the *Location* and *Destiny Location* fields from Moves to Stock Picking.
When stock moves are created they are taken by default.

Also add a new "Picking" report, with a more simple layout:

 - Move the locations fields to the head
 - Add "Notes" field to the head
 - Add support to "serial_ids" field from the **stock_serial_number**
   module (optional)

If you have installed the following modules (left), you should be install (right):

 - **purchase**: stock_picking_simple_locations_purchase
 - **sale**: stock_picking_simple_locations_sale
 - **mrp**: stock_picking_simple_locations_mrp
    """,
    'category'      : 'Warehouse Management',
    'website'       : 'http://www.sysfe.com.ar',
    'depends'       : ['stock'],
    'init_xml'      : [],
    'update_xml': [
        'update_picking_locations_fk.sql',
        'stock_view.xml',
        'report/stock_report.xml',
    ],
    'installable': True,
}