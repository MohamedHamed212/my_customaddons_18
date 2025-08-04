{
    'name': 'HR Attendance Geofence',
    'version': '18.0.1.0.0',
    'summary': 'Adds geofencing to HR Attendance check-in/out',
    'description': 'Restricts attendance to within a configurable geofence around work locations.',
    'author': 'Your Company',
    'depends': ['hr_attendance'],
    'data': [
        'views/hr_work_location_views.xml',
    ],
    'installable': True,
    'application': False
}

