from environ_vars import TKLIB_HOME
from du.plot_utils import plot_distance_curve_random
from du import dir_util
import pylab as mpl

def main():
    from sys import argv
    model = dir_util.load(argv[1])
    d8="%s/data/directions/direction_floor_8_full/" % TKLIB_HOME
    plot_distance_curve_random(model, 
                               "%s/nlp/data/Direction understanding subjects Floor 8 (Final).ods" % TKLIB_HOME,
                               "%s/regions/df8full_gtruth_regions.tag" % d8,
                               "%s/direction_floor_8_full_filled.cmf.gz" % d8,
                               color="b", marker="p", label="Random")
    mpl.show()
if __name__ == "__main__":
    main()
