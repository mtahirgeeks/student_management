# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StudentAttendance(models.Model):
    """
    Model to track student attendance for courses they are enrolled in.
    """
    _name = 'student.attendance'
    _description = 'Student Attendance'
    _order = 'date desc, student_id'

    student_id = fields.Many2one('student.student', string='Student', required=True, ondelete='cascade')
    course_id = fields.Many2one('student.course', string='Course', required=True, ondelete='cascade')
    enrollment_id = fields.Many2one(
        'student.enrollment', 
        string='Enrollment', 
        compute='_compute_enrollment_id', 
        store=True, 
        ondelete='cascade'
    )
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    state = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused')
    ], string='Status', required=True, default='present')
    remarks = fields.Text(string='Remarks')

    _sql_constraints = [
        ('unique_student_course_date', 'unique(student_id, course_id, date)', 'Attendance record for this student and course on this date already exists!')
    ]

    @api.model
    def default_get(self, fields_list):
        res = super(StudentAttendance, self).default_get(fields_list)
        enrollment_id = res.get('enrollment_id') or self._context.get('default_enrollment_id')
        if enrollment_id:
            enrollment = self.env['student.enrollment'].browse(enrollment_id)
            if enrollment:
                res.update({
                    'student_id': enrollment.student_id.id,
                    'course_id': enrollment.course_id.id,
                })
        return res

    @api.depends('student_id', 'course_id')
    def _compute_enrollment_id(self):
        for record in self:
            if record.student_id and record.course_id:
                enrollment = self.env['student.enrollment'].search([
                    ('student_id', '=', record.student_id.id),
                    ('course_id', '=', record.course_id.id)
                ], limit=1)
                record.enrollment_id = enrollment
            else:
                record.enrollment_id = False

    @api.constrains('student_id', 'course_id')
    def _check_enrollment(self):
        for record in self:
            if record.student_id and record.course_id:
                enrollment = self.env['student.enrollment'].search([
                    ('student_id', '=', record.student_id.id),
                    ('course_id', '=', record.course_id.id)
                ], limit=1)
                if not enrollment:
                    raise ValidationError(_("The student %s is not enrolled in the course %s.") % (record.student_id.name, record.course_id.name))

    @api.onchange('student_id')
    def _onchange_student_id(self):
        """Limit course selection to student's enrollments."""
        if self.student_id:
            enrolled_course_ids = self.student_id.enrollment_ids.mapped('course_id').ids
            return {'domain': {'course_id': [('id', 'in', enrolled_course_ids)]}}
        return {'domain': {'course_id': []}}

    @api.onchange('course_id')
    def _onchange_course_id(self):
        """Limit student selection to course's enrollments."""
        if self.course_id:
            enrolled_student_ids = self.course_id.enrollment_ids.mapped('student_id').ids
            return {'domain': {'student_id': [('id', 'in', enrolled_student_ids)]}}
        return {'domain': {'student_id': []}}
