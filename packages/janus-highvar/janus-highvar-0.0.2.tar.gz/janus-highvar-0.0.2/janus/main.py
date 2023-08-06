from __future__ import print_function
from argparse import ArgumentParser

from .dice import HighVarianceD4, HighVarianceD6, HighVarianceD8, HighVarianceD10, HighVarianceD12, HighVarianceD20,\
                  HighVarianceD100

DIE_MAPPING = {
    "d4": HighVarianceD4(),
    "d6": HighVarianceD6(),
    "d8": HighVarianceD8(),
    "d10": HighVarianceD10(),
    "d12": HighVarianceD12(),
    "d20": HighVarianceD20(),
    "d100": HighVarianceD100()
}
VALID_DIE_OPTIONS = sorted(DIE_MAPPING.keys(), key=lambda x: int(x[1:]))


def parse_args():
    parser = ArgumentParser("input arguments")
    required = parser.add_argument_group("required arguments")
    required.add_argument("die_type", help="Type of dice to roll. One of {}".format(
        ", ".join(VALID_DIE_OPTIONS))
                          )
    args = parser.parse_args()

    if args.die_type not in VALID_DIE_OPTIONS:
        raise ValueError("Die type must be one of {}".format(", ".join(VALID_DIE_OPTIONS)))

    return args


def roll_die():
    args = parse_args()
    print(DIE_MAPPING[args.die_type].roll)
