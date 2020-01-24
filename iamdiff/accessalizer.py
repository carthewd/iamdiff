from iamdiff import iam_diff_lib
from iamdiff.helpers import timeout
from iamdiff import helpers
import concurrent.futures


def get_service_diff(iam_client, **kwargs):
    account_id = kwargs.get('account_id')
    principal_type = kwargs.get('principal_type')
    name = kwargs.get('name')

    job = gen_access_details(iam_client, principal_type, name, account_id)
    report = get_access_details(iam_client, job)

    raw_diff = iam_diff_lib.service_diff(report)
    final_diff = iam_diff_lib.create_diff(raw_diff)
    
    print(final_diff)

def get_unused_roles(iam_client, **kwargs):
    account_id = kwargs.get('account_id')
    
    role_report = {}
    role_report['allowed'] = []
    role_report['accessed'] = []

    unused_roles = []

    roles = iam_client.list_roles()

    for role in roles['Roles']: 
        if 'service-role' not in role['Path']:
            role_report['allowed'].append(role['RoleName'])
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor: 
        futures = {
            executor.submit(find_unused_roles, iam_client, role): role for role in role_report['allowed']
        }

        for fut in concurrent.futures.as_completed(futures, timeout=60):
            if fut.result():
                unused_roles.append(fut.result())

    for role in role_report['allowed']:
        if role not in unused_roles:
            role_report['accessed'].append(role)

    final_diff = iam_diff_lib.create_diff(role_report)

    print (final_diff)
    
def find_unused_roles(iam_client, role):
    job = gen_access_details(iam_client, 'role', role)
    access_details = get_access_details(iam_client, job)

    services_accessed = 0
    for svc in access_details:
        services_accessed += svc['TotalAuthenticatedEntities']
    
    if services_accessed == 0:
        return role
    else:
        return None

def gen_access_details(iam_client, principal_type, entity_name, account_id=None):
    if account_id is None:
        account_id = helpers.check_user()

    resource_arn = f'arn:aws:iam::{account_id}:{principal_type}/{entity_name}'
    return iam_client.generate_service_last_accessed_details(
        Arn=resource_arn
    )['JobId']

@timeout(60)
def get_access_details(iam_client, job_id):
    job_status = None
    while job_status != 'COMPLETED':
        resp = iam_client.get_service_last_accessed_details(
            JobId=job_id
        )

        job_status = resp['JobStatus']
    
    return resp['ServicesLastAccessed']
