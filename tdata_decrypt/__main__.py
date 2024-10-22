import argparse
from . import display_accounts
from .data import TData

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tdata', type=str, help='Path to tdata directory')
    parser.add_argument(
        '--password', type=str, help='Local key encryption password',
        default='', required=False
    )
    args = parser.parse_args()

    data = TData(args.tdata, args.password)
    display_accounts(data)
