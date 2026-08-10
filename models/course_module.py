# -*- coding: utf-8 -*-
from odoo import models, fields

class StudentCourseModule(models.Model):
    """
    Module Model to represent a single learning unit inside a course.
    """
    _name = 'student.course.module'
    _description = 'Course Module'
    _order = 'sequence, id'

    name = fields.Char(string='Module Title', required=True, help="Title of the learning module.")
    sequence = fields.Integer(string='Sequence', default=10, help="Order of the module in the course.")
    description = fields.Text(string='Module Description', help="Short description of this module.")
    content = fields.Html(string='Learning Content', help="Text-based learning content for the student.")
    active = fields.Boolean(string='Active', default=True)
    
    course_id = fields.Many2one(
        'student.course', 
        string='Course', 
        required=True, 
        ondelete='cascade',
        help="Course this module belongs to."
    )
    
    question_ids = fields.One2many(
        'student.quiz.question',
        'module_id',
        string='Quiz Questions',
        help="Questions for this module's quiz."
    )
