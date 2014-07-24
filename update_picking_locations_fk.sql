/*    OpenERP, Stock Picking Simple Locations
 *    Copyright (C) 2013 Mariano Ruiz <mrsarm@gmail.com>
 *    Enterprise Objects Consulting (<http://www.eoconsulting.com.ar>)
 *
 *    Script to update new FKs in Stock Picking when install this module.
 */

UPDATE stock_picking SET location_id = (
    SELECT m.location_id 
      FROM stock_move m
      WHERE m.picking_id = stock_picking.id
      GROUP BY m.location_id
      ORDER BY COUNT(m.location_id) DESC
      LIMIT 1
    )
  WHERE location_id IS NULL;

UPDATE stock_picking SET location_dest_id = (
    SELECT m.location_dest_id
      FROM stock_move m
      WHERE m.picking_id = stock_picking.id
      GROUP BY m.location_dest_id
      ORDER BY COUNT(m.location_dest_id) DESC
      LIMIT 1
    )
  WHERE location_dest_id IS NULL;
