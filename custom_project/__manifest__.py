{
    'name': 'Custom Project',
    'version': '1.0',
    'description': 'Custom Project',
    'author': 'Jhon Jairo Rojas Ortiz',
    'license': 'LGPL-3',
    'depends': [
        'sale', 'project', 'base_automation'
    ],
    'data': [
        'data/project_project.xml',
        'data/project_task_type.xml',
        'data/base_automation.xml',
        'views/project_task.xml',
        'views/sale.xml'
    ],
    'auto_install': False,
    'application': False,
}
