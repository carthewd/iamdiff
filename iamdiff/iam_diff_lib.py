import difflib 
import os

def service_diff(access_report): 
    service_report = {}
    service_report['allowed'] = []
    service_report['accessed'] = []
    
    for svc in access_report:
        if svc['TotalAuthenticatedEntities'] > 0:
            service_report['accessed'].append(svc['ServiceName'])
        
        service_report['allowed'].append(svc['ServiceName'])
    
    return service_report

def create_diff(service_report):
    diff = difflib.unified_diff(service_report['allowed'], service_report['accessed'])

    formatted = '\n'.join(list(diff))

    final_output = os.linesep.join([s for s in formatted.splitlines() if s])

    return final_output
