# TODO: make automatic pricefactor ranges based on the fact that you shouldn't be generating a
# level 10 gun from a level 9 default

import yaml
import sys
import random
import numpy as np

# number of decimal points for your stats
PRECISION = 2


def random_histogram(N):
    """
    Returns random list of floats in the interval [0, 1) of length N that sum to 1.
    """
    out = []
    remaining = 1
    for i in range(N - 1):
        # scale down the random float
        proportion = random.random() * remaining
        remaining -= proportion

        out.append(proportion)
    out.append(remaining)
    return out


def generate(level):
    """
    Print random data for a gun of a certain level,
    with the degree of randomness depending on the pricefactor.

    A pricefactor of 1.4 means that if the base price
    is 100, the price range would be between 100 and 140.
    """

    with open("levels.yaml") as f:
        data = yaml.full_load(f)

        # find the appropriate pricefactor to stay within level
        pricefactor = data[level + 1]["price"] / data[level]["price"]

        # getting multipliers to multiply the average weapon stats
        actual_pricefactor = 1 + random.random() * (pricefactor - 1)

        # 4 gun stats over which we have to distribute the histogram
        histogram = np.array(random_histogram(4))

        # using the histogram to make multipliers for weapon stats
        multipliers = [actual_pricefactor]
        multipliers.extend(1 + (actual_pricefactor - 1) * histogram)
        multipliers = np.array(multipliers)
        rounded_multipliers = np.round(multipliers, 2)

        default_gun = data[level]
        gundata = np.round(np.multiply(
            multipliers, list(default_gun.values())), PRECISION)

        gundata_dict = dict(zip(list(default_gun.keys()), gundata))

        # print what gun level and price variance we are generating
        # and the gun data
        print("----------")

        print(
            f"Generating level {level} gun...")

        print(f"Maximum pricefactor of {pricefactor}")

        print(f"Actual pricefactor of {rounded_multipliers[0]}")

        i = 0
        for key in default_gun:
            print(
                f"{rounded_multipliers[i]:.2f}x {key} \t{default_gun[key]} -> {gundata_dict[key]}")
            i += 1


generate(int(sys.argv[1]))
