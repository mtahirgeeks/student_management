# -*- coding: utf-8 -*-
from odoo import models, fields

class StudentModuleProgress(models.Model):
    """
    Module Progress Model tracking if an enrollment has completed a specific module.
    """
    _name = 'student.module.progress'
    _description = 'Module Progress'

    enrollment_id = fields.Many2one('student.enrollment', string='Enrollment', required=True, ondelete='cascade')
    module_id = fields.Many2one('student.course.module', string='Module', required=True, ondelete='cascade')
    is_completed = fields.Boolean(string='Completed', default=False)
    completion_date = fields.Datetime(string='Completion Date')

    _sql_constraints = [
        ('unique_enrollment_module', 'unique(enrollment_id, module_id)', 'Progress record already exists for this module and enrollment!')
    ]
