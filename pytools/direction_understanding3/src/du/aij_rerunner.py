import regression_runner
from environ_vars import TKLIB_HOME
import os
def main():
    os.chdir("%s/pytools/direction_understanding3/" % TKLIB_HOME)

    runspec = [
        
        ("min_entropy_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                                 inference="last_sdc"), None),

        ("min_entropy_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                                 inference="global", do_exploration=True), None),

        ("min_entropy_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                                 inference="greedy"), None),
        ("min_entropy_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                                 inference="global"), None),
        ("min_entropy_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                                 inference="global", wizard_of_oz_sdcs="stefie10"), None),


        
        ("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                            inference="greedy"), None),
        ("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                            inference="global"), None),
        ("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                            inference="last_sdc"), None),
        ("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                            inference="global", wizard_of_oz_sdcs="stefie10"), None),

        ("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                            inference="global", do_exploration=True), None),

        #("min_entropy_extended", "d1_3d", dict(evaluation_mode="specialized", no_spatial_relations=True,
        #                                       inference="greedy"), None),
        ("min_entropy_extended", "d1_3d", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                               inference="global"), None),
        #("min_entropy_extended", "d1_3d", dict(evaluation_mode="specialized", no_spatial_relations=True,
        #                                       inference="last_sdc"), None),
        



        ("naive_bayes", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                        inference="greedy"), None),
        ("naive_bayes", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                        inference="global"), None),
        ("naive_bayes", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                        inference="last_sdc"), None),
        ("naive_bayes", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                        inference="global", do_exploration=True), None),
        
        ("naive_bayes", "d1", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                   inference="greedy"), None),
        ("naive_bayes", "d1", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                   inference="global"), None),
        ("naive_bayes", "d1", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                   inference="last_sdc"), None),
        ("naive_bayes", "d1", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                   inference="global", do_exploration=True), None),
        
        
        ("helicopter_offline", "d1_3d", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                             inference="greedy"), None),
        ("helicopter_offline", "d1_3d", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                             inference="global"), None),
        ("helicopter_offline", "d1_3d", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                             inference="last_sdc"), None),
        ("helicopter_offline", "d1_3d", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                             inference="global", do_exploration=True), None),
        
        ("helicopter_offline_nb", "d1_3d", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                                inference="greedy"), None),
        ("helicopter_offline_nb", "d1_3d", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                                inference="global"), None),
        ("helicopter_offline_nb", "d1_3d", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                                inference="last_sdc"), None),
        ("helicopter_offline_nb", "d1_3d", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                                inference="global", do_exploration=True), None),
        ]

    failed, msgBody = regression_runner.do_run(runspec)
    print msgBody
         
if __name__== "__main__":
    main()
