import config

from argparse import ArgumentParser
from Manual import Manual
from Auto import Auto


if __name__ == '__main__':

    parser = ArgumentParser(description='Start the vehicle in manual or fully autonomous mode')

    parser.add_argument("-n", "--nocapture", help="disable capturing of training data",
                                             action="store_false",
                                             dest="capture",
                                             default=True)

    parser.add_argument("-a", "--auto", help="enable fully autonomous driving mode",
                                        action="store_true",
                                        dest="autonomous",
                                        default=False)

    args = parser.parse_args()

    vehicle = Auto() if args.autonomous else Manual(capture=args.capture)
    vehicle.drive()
