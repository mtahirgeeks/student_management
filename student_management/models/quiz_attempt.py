# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StudentQuizAttempt(models.Model):
    """
    Quiz Attempt Model representing a student taking a quiz for a module.
    """
    _name = 'student.quiz.attempt'
    _description = 'Quiz Attempt'
    _order = 'attempt_date desc'

    name = fields.Char(string='Attempt Number', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    student_id = fields.Many2one(related='enrollment_id.student_id', string='Student', store=True)
    enrollment_id = fields.Many2one('student.enrollment', string='Enrollment', required=True, ondelete='cascade')
    module_id = fields.Many2one('student.course.module', string='Module', required=True, ondelete='cascade')
    attempt_date = fields.Datetime(string='Attempt Date', default=fields.Datetime.now)
    
    answer_ids = fields.One2many('student.quiz.answer', 'attempt_id', string='Answers')
    
    total_questions = fields.Integer(string='Total Questions', compute='_compute_score', store=True)
    correct_answers = fields.Integer(string='Correct Answers', compute='_compute_score', store=True)
    score_percentage = fields.Float(string='Score (%)', compute='_compute_score', store=True)
    passed = fields.Boolean(string='Passed', compute='_compute_score', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted')
    ], string='Status', default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('student.quiz.attempt') or _('New')
        return super(StudentQuizAttempt, self).create(vals_list)

    @api.depends('answer_ids.is_correct')
    def _compute_score(self):
        passing_percentage = 70.0 # Default business rule
        
        for record in self:
            total = len(record.answer_ids)
            correct = len(record.answer_ids.filtered(lambda a: a.is_correct))
            
            record.total_questions = total
            record.correct_answers = correct
            
            if total > 0:
                record.score_percentage = (correct / total) * 100.0
                record.passed = record.score_percentage >= passing_percentage
            else:
                record.score_percentage = 0.0
                record.passed = False

    def action_submit_quiz(self):
        """ Mark the attempt as submitted and update module progress if passed. """
        for record in self:
            if record.state == 'submitted':
                raise UserError(_("This attempt is already submitted."))
            
            record.state = 'submitted'
            
            if record.passed:
                # Find or create progress record for this enrollment & module
                progress_env = self.env['student.module.progress']
                progress = progress_env.search([
                    ('enrollment_id', '=', record.enrollment_id.id),
                    ('module_id', '=', record.module_id.id)
                ], limit=1)
                
                if not progress:
                    progress = progress_env.create({
                        'enrollment_id': record.enrollment_id.id,
                        'module_id': record.module_id.id,
                        'is_completed': True,
                        'completion_date': fields.Datetime.now()
                    })
                elif not progress.is_completed:
                    progress.write({
                        'is_completed': True,
                        'completion_date': fields.Datetime.now()
                    })

    @api.onchange('module_id')
    def _onchange_module_id(self):
        """ Automatically generate answer records for the module's questions when creating an attempt. """
        if self.module_id:
            # Clear existing answers
            self.answer_ids = [(5, 0, 0)]
            # Add new answers based on module questions
            new_answers = []
            for question in self.module_id.question_ids:
                new_answers.append((0, 0, {
                    'question_id': question.id
                }))
            self.answer_ids = new_answers


class StudentQuizAnswer(models.Model):
    """
    Quiz Answer Model tracking what the student selected for a question.
    """
    _name = 'student.quiz.answer'
    _description = 'Quiz Answer'

    attempt_id = fields.Many2one('student.quiz.attempt', string='Attempt', required=True, ondelete='cascade')
    question_id = fields.Many2one('student.quiz.question', string='Question', required=True, ondelete='cascade')
    selected_option_id = fields.Many2one('student.quiz.option', string='Selected Option')
    is_correct = fields.Boolean(string='Is Correct', compute='_compute_is_correct', store=True)

    @api.depends('selected_option_id')
    def _compute_is_correct(self):
        for record in self:
            if record.selected_option_id:
                record.is_correct = record.selected_option_id.is_correct
            else:
                record.is_correct = False
