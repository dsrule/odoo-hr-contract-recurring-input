# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    from_recurringinput = fields.Boolean(string='From Recurring-Input', default=False)


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.onchange('employee_id', 'struct_id', 'contract_id', 'date_from', 'date_to')
    def _onchange_employee(self):
        res = super(HrPayslip, self)._onchange_employee()
        if self.contract_id and self.date_from and self.date_to:
            other_input_list = []
            self.input_line_ids = False
            for each in self.contract_id.recurringinput_ids.filtered(lambda x:x.active_recurringinput == True):
                input_line_ids = self.input_line_ids.filtered(lambda x:x.from_recurringinput == True and x.input_type_id == each.input_type_id)
                if each.end_date and each.start_date <= self.date_from and each.end_date >= self.date_to:
                    other_input_list.append((0, 0, {
                        'input_type_id': each.input_type_id.id,
                        'amount': each.amount,
                        'from_recurringinput': True}
                        ))
                if not each.end_date and each.start_date <= self.date_from:
                    other_input_list.append((0, 0, {
                        'input_type_id': each.input_type_id.id,
                        'amount': each.amount,
                        'from_recurringinput': True}
                        ))
            self.input_line_ids = other_input_list
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
