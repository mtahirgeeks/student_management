# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class StudentStudent(models.Model):
    """
    Student Model to manage student personal and academic enrollment details.
    """
    _name = 'student.student'
    _description = 'Student'
    _order = 'name'

    name = fields.Char(string='Student Name', required=True, help="Full name of the student.")
    roll_number = fields.Char(string='Student Number', required=True, copy=False, readonly=True, default=lambda self: _('New'), help="Unique identification number of the student.")
    email = fields.Char(string='Email', help="Primary email address.")
    phone = fields.Char(string='Phone', help="Contact phone number.")
    date_of_birth = fields.Date(string='Date of Birth', help="Date of birth of the student.")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender', help="Gender of the student.", default="male")
    active = fields.Boolean(string='Active', default=True, help="Is the student active?")
    
    enrollment_ids = fields.One2many(
        'student.enrollment',
        'student_id',
        string='Enrollments',
        help="Courses the student is enrolled in."
    )
    
    attendance_ids = fields.One2many(
        'student.attendance',
        'student_id',
        string='Attendance Records',
        help="Attendance history of the student."
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('roll_number', _('New')) == _('New'):
                vals['roll_number'] = self.env['ir.sequence'].next_by_code('student.student') or _('New')
        return super(StudentStudent, self).create(vals_list)