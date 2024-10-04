import argparse
from .data import TData

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('tdata', type=str, help='Path to tdata directory')
    parser.add_argument('--password', type=str, help='Local key encryption password', default='', required=False)
    args = parser.parse_args()

    for account in TData.read_accounts(args.tdata, args.password).accounts.values():
        print(f'Account {account.index}:')

        print(f'\tUser ID: {account.mtp_data.user_id}')
        print(f'\tMain DC ID: {account.mtp_data.main_dc_id}')

        for dc_id, key in account.mtp_data.keys_to_destroy.items():
            print(f'\tKey TD DC {dc_id}: {key.hex(" ")}')

        for dc_id, key in account.mtp_data.keys.items():
            print(f'\tKey DC {dc_id}: {key.hex(" ")}')