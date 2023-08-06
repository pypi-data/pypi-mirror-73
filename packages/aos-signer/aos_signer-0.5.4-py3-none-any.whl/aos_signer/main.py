#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import argparse
import sys

from aos_signer.signer.signer import Signer
from aos_signer.signer.bootstrapper import run_bootstrap
from aos_signer.signer.uploader import run_upload
from colorama import init, Fore

_COMMAND_INIT = 'init'
_COMMAND_SIGN = 'sign'
_COMMAND_UPLOAD = 'upload'


def run_init_signer():
    print(Fore.GREEN + "Starting SERVICE UPLOAD process")
    run_bootstrap()


def run_upload_service():
    try:
        run_upload()
    except OSError:
        print(Fore.RED + str(sys.exc_info()[1]))


def run_sign():
    print(Fore.GREEN + "Starting SERVICE SIGNING process")
    try:
        s = Signer(src_folder='src', package_folder='.')
        s.process()
    except OSError:
        print(Fore.RED + str(sys.exc_info()[1]))


def main():
    from colorama import init
    init()
    parser = argparse.ArgumentParser(
        prog='Aos Signer Tool',
        description='This tool will help you to prepare, sign and upload service to Aos Cloud'
    )
    parser.set_defaults(which=None)

    sub_parser = parser.add_subparsers(title='Commands')

    init = sub_parser.add_parser(
        _COMMAND_INIT,
        help='Generate required folders and configuration file. If you don\'t know where to start type aos-signer init'
    )
    init.set_defaults(which=_COMMAND_INIT)

    sign = sub_parser.add_parser(
        _COMMAND_SIGN,
        help='Sign Service'
    )
    sign.set_defaults(which=_COMMAND_SIGN)

    upload = sub_parser.add_parser(
        _COMMAND_UPLOAD,
        help='Upload Service to the Cloud. Address, security credentials and service UID is taken from config.yaml in meta folder'
    )
    upload.set_defaults(which=_COMMAND_UPLOAD)

    args = parser.parse_args()
    if args.which is None:
        run_sign()

    if args.which == _COMMAND_INIT:
        run_init_signer()

    if args.which == _COMMAND_SIGN:
        run_sign()

    if args.which == _COMMAND_UPLOAD:
        run_upload_service()


if __name__ == '__main__':
    main()
