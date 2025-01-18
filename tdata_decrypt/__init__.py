import argparse
import base64
from .data import TData

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('tdata', type=str, help='Path to tdata directory')
    parser.add_argument(
        '--password', type=str, help='Local key encryption password',
        default='', required=False
    )
    args = parser.parse_args()

    data = TData(args.tdata, args.password)
    display_accounts(data)


def display_accounts(data: TData):
    for account in data.read_accounts().values():
        print(f'Account {account.index}:')

        print(f'\tUser ID: {account.mtp_data.user_id}')
        print(f'\tMain DC: {account.mtp_data.main_dc_id}')

        print(f'\tKeys to destroy:')
        for dc_id, key in account.mtp_data.keys_to_destroy.items():
            print(f'\t\tDC {dc_id}: {base64.b64encode(key)}')

        print(f'\tAuth Keys:')
        for dc_id, key in account.mtp_data.keys.items():
            print(f'\t\tDC {dc_id}: {base64.b64encode(key)}')
