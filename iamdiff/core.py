from pprint import pprint
#from helpers import timeout
import argparse
import sys
from botocore.exceptions import ClientError

# from iamdiff import *
from iamdiff import accessalizer
import iamdiff.helpers as helpers
from iamdiff import iam_diff_lib

def main():
    argv = sys.argv[1:]

    parser = argparse.ArgumentParser(usage=('%(prog)s'))

    def add_common_arguments(parser):
        parser.add_argument('--principal_type', '-p',
                            dest='principal_type',
                            type=str,
                            default='role',
                            help='The type of IAM principal to review')

        parser.add_argument('--name', '-n',
                            dest='name',
                            type=str,
                            help='The name of the IAM entity to review')

        parser.add_argument('--account_id', '-a',
                            dest='account_id',
                            type=str,
                            default=None,
                            help='The account ID for the owner of the IAM resources (defaults to current)')

    subparsers = parser.add_subparsers()

    # service
    service_parser = subparsers.add_parser('svc', description='Get services that have not been accessed for a threshold (default: 90 days)')
    service_parser.set_defaults(func='get_service_diff')
    add_common_arguments(service_parser)

    # role
    role_parser = subparsers.add_parser('roles', description='Get access information related to roles')
    role_parser.set_defaults(func='get_unused_roles')

    options, args = parser.parse_known_args(argv)

    if not hasattr(options, 'func'):
        parser.print_help()
        return 1

    client = helpers.get_iam_client()
    try:
        getattr(sys.modules['iamdiff.accessalizer'], options.func)(client, **vars(options))
    except ClientError as e:
        ret = err_handler(e.response['Error']['Code'], options, parser)
        return ret

def err_handler(error_code, options, parser):
    if error_code == 'NoSuchEntity':
        print(f'A {options.principal_type} for {options.name} does not exist - verify the name and entity type.\n' )
        parser.print_help()
        return 4

if __name__ == '__main__':
    main()
