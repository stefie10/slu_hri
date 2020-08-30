import datetime
from regression_runner import CommandLogger
import regression_runner
from environ_vars import TKLIB_HOME
import traceback

def run_tests():
    start_time = datetime.datetime.now()
    log = CommandLogger()

    directory_names = ["forklift", "du_crf3", "esdcs", "stanford-parser",
                       "spatial_features", "nlu_navigation", "gis"]

    log.sh("cd cutilities && rake build")
    log.sh("cd cutilities && rake build")
    log.sh("cd pytools/du_crf3 && rake train_forklift")
    log.sh("cd pytools/du_crf3 && rake train_esdcs")
    log.sh("cd pytools/du_crf3 && rake train_sr")


    for directory_name in directory_names:

        cmd = "cd %s/pytools/%s && rake tests" % (TKLIB_HOME, directory_name)
        log.sh(cmd)


    end_time = datetime.datetime.now()


    log.append("Ran %d tests in " % len(directory_names) + 
               str(end_time - start_time))
    return log.failed_count, log.run_count, log.log

def main():
    regression_runner.run(run_tests)

if __name__ == "__main__":
    main()
