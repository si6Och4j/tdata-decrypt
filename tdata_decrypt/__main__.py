import argparse
from tdata_decrypt import TData, display_accounts

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
