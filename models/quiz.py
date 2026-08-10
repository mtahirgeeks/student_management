# -*- coding: utf-8 -*-
from odoo import models, fields

class StudentQuizQuestion(models.Model):
    """
    Quiz Question Model for a module's MCQ test.
    """
    _name = 'student.quiz.question'
    _description = 'Quiz Question'
    _order = 'sequence, id'

    name = fields.Text(string='Question Text', required=True, help="The actual question.")
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(string='Active', default=True)
    
    module_id = fields.Many2one(
        'student.course.module', 
        string='Module', 
        required=True, 
        ondelete='cascade'
    )
    
    option_ids = fields.One2many(
        'student.quiz.option',
        'question_id',
        string='Options',
        help="Multiple choice options for this question."
    )

class StudentQuizOption(models.Model):
    """
    Quiz Option Model for an MCQ question.
    """
    _name = 'student.quiz.option'
    _description = 'Quiz Option'
    _order = 'id'

    name = fields.Char(string='Option Text', required=True)
    is_correct = fields.Boolean(string='Is Correct Answer', default=False)
    
    question_id = fields.Many2one(
        'student.quiz.question', 
        string='Question', 
        required=True, 
        ondelete='cascade'
    )
