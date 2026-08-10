# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class StudentCourse(models.Model):
    """
    Course Model to manage educational courses.
    """
    _name = 'student.course'
    _description = 'Course'
    _order = 'name'

    name = fields.Char(string='Course Name', required=True, help="Name of the course.")
    code = fields.Char(string='Course Code', required=True, copy=False, readonly=True, default=lambda self: _('New'), help="Unique code for the course.")
    duration = fields.Integer(string='Duration (Weeks)', help="Duration of the course in weeks.")
    fee = fields.Float(string='Course Fee', help="Tuition fee for the course.")
    short_description = fields.Char(string='Short Description', help="Brief summary of the course.")
    description = fields.Text(string='Description', help="Detailed syllabus or details of the course.")
    active = fields.Boolean(string='Active', default=True, help="Is the course active?")
    
    module_ids = fields.One2many(
        'student.course.module',
        'course_id',
        string='Modules',
        help="Modules included in this course."
    )

    enrollment_ids = fields.One2many(
        'student.enrollment', 
        'course_id', 
        string='Enrollments', 
        help="Students enrolled in this course."
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('student.course') or _('New')
        return super(StudentCourse, self).create(vals_list)
