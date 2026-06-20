{
    'name': 'HMS',
    'version': '1.0',
    'summary': 'Hospitals Management System',
    'description': 'Hospitals Management System (HMS)',
    'category': 'Health',
    'depends': ['base', 'crm'],
    'data': [
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/customer_views.xml',
        'views/menus.xml',
        'reports/patient_report.xml',
    ],
}
