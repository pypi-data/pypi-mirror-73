import os
import sys


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    print("This is the main routine.")
    print("It should do something interesting.")

    # Do argument parsing here (eg. with argparse) and anything else

    # you want your project to do.


def download_sample_data():
    from xrspatial.datasets import crater_lake_dem
    os.system('wget http://oe.oregonexplorer.info/craterlake/products/dem/dems_10m.zip')



    pass


def remove_sample_data():
    pass



if __name__ == "__main__":
    main()
