# -*- coding: utf-8 -*-
{
    'name': "Student Management",
    'summary': "Manage students and courses.",
    'description': """
Student Management Module
==========================
A clean, production-grade custom module for Odoo 18 Community.
Features:
- Student profile management (CRUD)
- Course details & curriculum mapping
- Many2one / One2many database relationships for course enrollment
    """,
    'author': "Hamza Khan Lodhi",
    'website': "https://www.example.com",
    'category': 'Education',
    'version': '18.0.1.0.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/course_views.xml',
        'views/student_views.xml',
        'views/course_module_views.xml',
        'views/quiz_views.xml',
        'views/enrollment_views.xml',
        'views/quiz_attempt_views.xml',
        'views/attendance_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
