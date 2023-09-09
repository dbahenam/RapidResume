from datetime import datetime, date

def datestr_to_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()

def date_to_datestr(date_obj):
    return date_obj.isoformat()