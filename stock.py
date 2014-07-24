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

from openerp.osv import osv, fields
from openerp import tools
from openerp.tools.translate import _

class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    '''
    classdocs >
    '''
    
    
    def onchange_location_id(self, cr, uid, ids, location_id, picking_type, move_lines, context):
        if not move_lines or len(move_lines)==0:
            return {}
        res = {'value':{'move_lines': move_lines}}
        for move in move_lines:
            if not move[2]:
                move[2] = {}
            move[2]['location_id'] = location_id
        return res

    def onchange_location_dest_id(self, cr, uid, ids, location_dest_id, picking_type, move_lines, context):
        if not move_lines or len(move_lines)==0:
            return {}
        res = {'value':{'move_lines': move_lines}}
        for move in move_lines:
            if not move[2]:
                move[2] = {}
            move[2]['location_dest_id'] = location_dest_id
        return res
    
    
    
    def onchange_address_id(self, cr, uid, ids, address_id=None, context={}):
        """
        This method replace the bad formed 'onchange_partner_in' method, but
        to prevent compatibility problems, in the first line is invoked
        """
        res = self.onchange_partner_in(cr,uid,context,address_id)
        if 'value' not in res:
            value = {}
            res['value'] = value
        else:
            value = res['value']
        location_id = self._default_location_source(cr, uid, context=context)
        if location_id:
            value['location_id'] = location_id
        location_dest_id = self._default_location_destination(cr, uid, context=context)
        if location_dest_id:
            value['location_dest_id'] = location_dest_id
        return res

    def write(self, cr, uid, ids, vals, context={}):
        if not context or not context.get('no_upd_move_locs', False):
            vals2 = {}
            if 'location_id' in vals:
                vals2['location_id'] = vals['location_id']
            if 'location_dest_id' in vals:
                vals2['location_dest_id'] = vals['location_dest_id']
            if vals2 != {}:
                for pick in self.browse(cr,uid,ids,context):
                    move_ids = [move.id for move in pick.move_lines]
                    self.pool.get('stock.move').write(cr,uid,move_ids,vals2,context)
        return super(stock_picking, self).write(cr, uid, ids, vals, context)

    def copy(self, cr, uid, _id, default=None, context=None):
        if default is None:
            default = {}
        if context is None:
            context = {}
        default = default.copy()
        picking = self.browse(cr, uid, _id, context=context)
        # (src location, dest location) <=> (dest location, src location) in returns
        if '-return' in default.get('name', '') or context.get('return', False):
            if 'location_id' not in default:
                default['location_id'] = picking.location_dest_id.id
            if 'location_dest_id' not in default:
                default['location_dest_id'] = picking.location_id.id
        res = super(stock_picking, self).copy(cr, uid, _id, default, context)
        return res
    
    
    
    '''
    < classdocs
    '''
    def _default_location_source(self, cr, uid, context=None):
        location_id = context.get('location_id', False)
        if location_id:
            return location_id
        else:
            return self.pool.get("stock.move")._default_location_source(cr, uid, context=context)

    def _default_location_destination(self, cr, uid, context=None):
        location_dest_id = context.get('location_dest_id', False)
        if location_dest_id:
            return location_dest_id
        else:
            return self.pool.get("stock.move")._default_location_destination(cr, uid, context=context)
    
    _columns = {
        'location_id': fields.many2one('stock.location', 'Source Location',
                                required=True, select=True,
                                states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
                                help="Sets a location if you produce at a fixed location. "
                                     "This can be a partner location if you subcontract the manufacturing operations. "
                                     "This will be the default of the asociated stock moves."),
        'location_dest_id': fields.many2one('stock.location', 'Destination Location',
                                required=True, select=True,
                                states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
                                help="Location where the system will stock the finished products. "
                                     "This will be the default of the asociated stock moves."),
    }

    _defaults = {
        'location_id': _default_location_source,
        'location_dest_id': _default_location_destination,
    }

stock_picking()        