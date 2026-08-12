# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StudentEnrollment(models.Model):
    """
    Enrollment Model mapping a Student to a Course.
    Tracks overall course progress.
    """
    _name = 'student.enrollment'
    _description = 'Student Enrollment'
    _order = 'enrollment_date desc, id desc'

    name = fields.Char(string='Enrollment Number', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    enrollment_date = fields.Date(string='Enrollment Date', default=fields.Date.context_today)
    state = fields.Selection([
        ('enrolled', 'Enrolled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='enrolled', tracking=True)
    
    student_id = fields.Many2one('student.student', string='Student', required=True, ondelete='cascade')
    course_id = fields.Many2one('student.course', string='Course', required=True, ondelete='cascade')
    
    progress_ids = fields.One2many('student.module.progress', 'enrollment_id', string='Module Progress')
    attempt_ids = fields.One2many('student.quiz.attempt', 'enrollment_id', string='Quiz Attempts')
    attendance_ids = fields.One2many('student.attendance', 'enrollment_id', string='Attendance Records')

    total_modules = fields.Integer(string='Total Modules', compute='_compute_progress', store=True)
    completed_modules = fields.Integer(string='Completed Modules', compute='_compute_progress', store=True)
    progress_percentage = fields.Float(string='Progress (%)', compute='_compute_progress', store=True)
    attendance_percentage = fields.Float(string='Attendance Rate (%)', compute='_compute_attendance_percentage', store=True)

    _sql_constraints = [
        ('unique_student_course', 'unique(student_id, course_id)', 'A student cannot be enrolled in the same course more than once!')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('student.enrollment') or _('New')
        return super(StudentEnrollment, self).create(vals_list)

    @api.depends('course_id.module_ids', 'progress_ids.is_completed')
    def _compute_progress(self):
        for record in self:
            if not record.course_id:
                record.total_modules = 0
                record.completed_modules = 0
                record.progress_percentage = 0.0
                continue
                
            total = len(record.course_id.module_ids)
            # Count how many of those modules have a completed progress record for this enrollment
            completed = len(record.progress_ids.filtered(lambda p: p.is_completed))
            
            record.total_modules = total
            record.completed_modules = completed
            if total > 0:
                record.progress_percentage = (completed / total) * 100.0
                if record.progress_percentage >= 100.0 and record.state in ['enrolled', 'in_progress']:
                    record.state = 'completed'
                elif record.progress_percentage > 0.0 and record.state == 'enrolled':
                    record.state = 'in_progress'
            else:
                record.progress_percentage = 0.0

    @api.depends('attendance_ids.state')
    def _compute_attendance_percentage(self):
        for record in self:
            total = len(record.attendance_ids)
            if total > 0:
                present_or_late = len(record.attendance_ids.filtered(lambda a: a.state in ['present', 'late']))
                record.attendance_percentage = (present_or_late / total) * 100.0
            else:
                record.attendance_percentage = 0.0
