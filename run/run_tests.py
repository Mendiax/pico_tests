import argparse
import logging
import sys

import dep.run_local as run_local
import dep.run_ssh as run_ssh
from dep.config import Config


def get_arg_data():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, help='Path to config file')
    args = parser.parse_args()


    print(f"Config file path: {args.config}")

    return args


def main():
    arguments = get_arg_data()
    config = Config.from_yaml(arguments.config)

    connection = config.get_connection_type()
    print(f"connection={connection}")
    result = 0
    if connection == 'local':
        result = run_local.run(config)
    elif connection == 'ssh':
        result = run_ssh.run(config)
    else:
        raise Exception('Wrong connection parameter')

    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())

