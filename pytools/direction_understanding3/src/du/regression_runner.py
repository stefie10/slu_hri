from environ_vars import TKLIB_HOME
import traceback
import smtplib
import os
from email.mime.text import MIMEText
from subprocess import Popen
import subprocess
import datetime
from socket import gethostname


lastrun_file = "%s/regression.lastrun" % TKLIB_HOME

def sh(cmd):
    process = Popen(cmd, shell=True, stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise ValueError("command failed!" + `cmd`)
    return stdout

def current_svn_revision():
    return 1
    global_rev =  sh("svn info").split("\n")[4]
    revision, revno = global_rev.split()
    return int(revno)

def has_diffs(lastrev, currentrev):
    if lastrev == None:
        return True
    diff = sh("svn diff -r%d:%d --summarize" % (lastrev, currentrev))
    if len(diff) != 0:
        return True
    else:
        return False

def save_last_run():
    f = open(lastrun_file, "w")
    f.write(`datetime.datetime.now()`)
    f.write("\n")
    f.write(`current_svn_revision()`)
    f.write("\n")
    f.close()
    
def get_last_run():
    if os.path.exists(lastrun_file):
        f = open(lastrun_file, "r")
        date = eval(f.readline())
        svnrevno = eval(f.readline())
        return date, svnrevno
    else:
        return None, None

def main():
    lockfile = "%s/regression.lock" % TKLIB_HOME
    if os.path.exists(lockfile):
        return
    else:
        open(lockfile, "w").close()
        try:
            failed, msgBody, log = runtests()
        except:
            failed = True
            msgBody = traceback.format_exc()
            log = None
        finally:
            os.remove(lockfile)
            if failed != None:
                send_email(failed, msgBody, log)


def runtests():

    last_run_datetime, last_svn_revno = get_last_run()

    log = ""
    os.chdir(TKLIB_HOME)
    #log += sh("svn up") # happens in cron
    svn_revno = current_svn_revision()
    diffs = has_diffs(last_svn_revno, svn_revno)
    log += sh("rake build_cutilities")

    os.chdir("%s/pytools/direction_understanding3/" % TKLIB_HOME)
    if False:
        log += sh("rake build_slimd_cutilities")
        #log += sh("rake create_min_entropy_d8")
        #log += sh("rake create_min_entropy_srel_mat_d8")

        log += sh("rake create_min_entropy_extended_d8_full")
        log += sh("rake create_min_entropy_extended_srel_mat_d8_full")
        log += sh("rake create_min_entropy_grandchildren_d8_full")
        
        #log += sh("rake create_min_entropy_extended_d1")
        #log += sh("rake create_min_entropy_extended_srel_mat_d1")

    log += "\n\n"

    if last_run_datetime != None:
        time_delta = datetime.datetime.now() - last_run_datetime
    else:
        time_delta = None
    time_delta_passes = last_run_datetime == None or  time_delta >= datetime.timedelta(minutes=10)
    print "revno", svn_revno, "(last run on", last_svn_revno, ")", "has_diffs:", diffs, "time delta:", time_delta, time_delta_passes
    if diffs and time_delta_passes:
        failed, msgBody = actually_run()
        return failed, msgBody, log
    else:
        return None, None, log
        

class Dataset:
    def __init__(self, rake_suffix, corpus_fn, gtruth_tag_fn, map_fn, dir):
        self.rake_suffix = rake_suffix
        self.corpus_fn = corpus_fn
        self.gtruth_tag_fn = gtruth_tag_fn
        self.map_fn = map_fn
        self.dir = dir

def makeDatasets():
    dir8 = '%s/data/directions/direction_floor_8' % TKLIB_HOME
    dir1 = '%s/data/directions/direction_floor_1' % TKLIB_HOME
    d8_full = "%s/data/directions/direction_floor_8_full" % TKLIB_HOME
    d1_3d = "%s/data/directions/direction_floor_1_3d" % TKLIB_HOME
    datasets = {"d8":Dataset(rake_suffix="d8", 
                             corpus_fn="%s/nlp/data/Direction understanding subjects Floor 8 (Final).ods" % TKLIB_HOME,
                             gtruth_tag_fn="%s/regions/df8_small_filled_regions_gtruth.tag" % (dir8),
                             map_fn="%s/df8_small_filled.cmf.gz" % dir8,
                             dir=dir8,
                             ),
                "d8_full":Dataset(rake_suffix="d8_full", 
                             corpus_fn="%s/nlp/data/Direction understanding subjects Floor 8 (Final).ods" % TKLIB_HOME,
                             gtruth_tag_fn="%s/regions/df8full_gtruth_regions.tag" % (d8_full),
                             map_fn="%s/direction_floor_8_full_filled.cmf.gz" % d8_full,
                             dir=d8_full,
                             ),
                "d1":Dataset(rake_suffix="d1",
                             corpus_fn="%s/nlp/data/Direction understanding subjects Floor 1 (Final).ods" % TKLIB_HOME,
                             gtruth_tag_fn="%s/regions/df1_small_groundtruth.tag" % (dir1),
                             map_fn="%s/direction_floor_1_small.cmf" % (dir1),
                             dir=dir1,
                             ),
                "d1_3d":Dataset(rake_suffix="d1_3d",
                             corpus_fn="%s/nlp/data/Direction understanding subjects Floor 1 (Helicopter).ods" % TKLIB_HOME,
                             gtruth_tag_fn="%s/regions/df13d_small_groundtruth.tag" % (d1_3d),
                             map_fn="%s/direction_floor_1_small.cmf" % (d1_3d),
                             dir=d1_3d,
                             ),
                }
    return datasets
def actually_run():
    models = [
        ("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=False, quadrant_number=1), 16),
        ("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=True, quadrant_number=1), 14),
        ("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=False, inference="greedy", quadrant_number=1), 2),
        ("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=True, inference="greedy", quadrant_number=1), 0),

        ("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=False, quadrant_number=3), 0),
        ("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=True, quadrant_number=3), 22),
        ("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=False, inference="greedy", quadrant_number=3), 3),
        ("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=True, inference="greedy", quadrant_number=3), 5),
        ]
    modelsWithRevision16992_change_to_keyword_extraction = [
        ("min_entropy_grandchildren", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=False,
                                                      inference="greedy"), 38),
        ("min_entropy_grandchildren", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                                      inference="greedy"), 21),                                                       
        ("min_entropy_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=False,
                                                 inference="last_sdc"), 22),
        ("min_entropy_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=False,
                                                 inference="global"), 69),                                                       
        ("min_entropy_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True), 65),                                                                                                      
        ("hri2010_wei_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=False), 55),
        ]
    models = [
        ("min_entropy_grandchildren", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=False,
                                                      inference="greedy"), 34),
        ("min_entropy_grandchildren", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True,
                                                      inference="greedy"), 19),                                                       
        ("min_entropy_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=False,
                                                 inference="last_sdc"), 29),
        ("min_entropy_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=False,
                                                 inference="global"), 60),                                                       
        ("min_entropy_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True), 64),
        ("hri2010_wei_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=False), 70),
        ]
    
    [
        ("min_entropy_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=False), 71),
        ("min_entropy_extended", "d8_full", dict(evaluation_mode="specialized", no_spatial_relations=True), 61),

        ("min_entropy", "d8", dict(evaluation_mode="max_prob", no_spatial_relations=False), 51),

        #("min_entropy_extended", "d1", dict(evaluation_mode="specialized", no_spatial_relations=False), 56),


        ("min_entropy", "d8", dict(evaluation_mode="specialized", no_spatial_relations=False), 55),

        ("hri2010_global", "d8", dict(evaluation_mode="specialized", no_spatial_relations=False), 49),
        ("hri2010_greedy_2step", "d8", dict(evaluation_mode="specialized", no_spatial_relations=False), 22), 
        ("hri2010_wei", "d8", dict(evaluation_mode="specialized", no_spatial_relations=False), 37),
        ("hri2010_lastSDC", "d8", dict(evaluation_mode="specialized", no_spatial_relations=False), 24),
        ("min_entropy", "d8", dict(evaluation_mode="specialized", no_spatial_relations=True), 44),
        ("duplicate_landmarks", "d8", dict(evaluation_mode="specialized", no_spatial_relations=True), 52),
        ("hri2010_global", "d8", dict(evaluation_mode="specialized", no_spatial_relations=True), 47),
        ("hri2010_greedy_2step", "d8", dict(evaluation_mode="specialized", no_spatial_relations=True), 22), 
        ("hri2010_wei", "d8", dict(evaluation_mode="specialized", no_spatial_relations=True), 37),
        ("hri2010_lastSDC", "d8", dict(evaluation_mode="specialized", no_spatial_relations=True), 24),

        ]
    return do_run(models)
def do_run(models):
    start_time = datetime.datetime.now()
    save_last_run()    
    msgBody = ""        
    log = ""

    failed = False
    datasets = makeDatasets()
    for m, dataset, args, expected in models:
        try:
            ds = datasets[dataset]
            log += sh("rake create_model_%s_%s" % (m, ds.rake_suffix))
            log += "\n\n"

            msgBody += "**********************************\n"
            msgBody += "%s  %s "  % (m, args)

            import evaluate_model
            eval_start = datetime.datetime.now()
            actual, out_fname = evaluate_model.evaluate(run_description=str(args), corpus_fn=ds.corpus_fn, 
                                                        model_fn="%s/models/%s.pck" % (ds.dir, m),
                                                        output_dir="%s/output" % ds.dir,
                                                        gtruth_tag_fn=ds.gtruth_tag_fn,
                                                        map_fn=ds.map_fn,
                                                        **args)
            eval_stop = datetime.datetime.now()
            msgBody += "\n(outfile: %s)\n" % out_fname
            if expected != None:
                assert actual == expected, (actual, expected)
                msgBody += "got %d, as expected, in %s\n" % (actual, str(eval_stop - eval_start))
            else:
                msgBody += "Didn't check expected.  got %d\n" % (actual)

        except:
            stackTrace = traceback.format_exc()
            failed = True
            msgBody += "failed with %s!\n\n"
            msgBody += stackTrace
    end_time = datetime.datetime.now()
    msgBody =  "Ran %d tests in " % len(models) + str(end_time - start_time) + "\n"  + msgBody 
    return failed, msgBody
def send_email(failed, msgBody, log):
        to = [
            "stefie10@media.mit.edu", 
            "tkollar@csail.mit.edu",
            "mitko@csail.mit.edu",
            ]

 

        if not failed:
            msgBody += "\n\nEverything passed!\n"
            subject_str = "Passed"
        else:
            now = datetime.datetime.now()
            log_fname = now.strftime(TKLIB_HOME + "/regression.%Y-%m-%d-%H-%M-%S.log")
            log_file = open(log_fname, 'w')
            if log != None:
                log_file.write(log)
            msgBody += "\n\nLog written to %s\n" % log_fname
            subject_str = "Failed"
            #to.append("tkollar@csail.mit.edu")


        msg = MIMEText(msgBody)
        svn_revno = current_svn_revision()
        msg['Subject'] = "Direction Understanding Regression Tests on %s for -r%d (%s)" % (gethostname(), svn_revno, subject_str)
        msg['From'] = "stefie10@media.mit.edu"
        msg['To'] = ", ".join(to)



        server = smtplib.SMTP("outgoing.media.mit.edu")
        server.sendmail(msg['From'], to, msg.as_string())
        server.quit()
        print msg.as_string()
        #log_file.write("\n\n\n\n******************** stdout\n" + open("regression.log").read())
        #log_file.close()

if __name__== "__main__":
    main()


# old runs
        #("hri2010_global", dict(evaluation_mode="best_path", no_spatial_relations=False), 61),
        #("hri2010_global", dict(evaluation_mode="best_path", no_spatial_relations=True), 55),
        #("hri2010_global", dict(evaluation_mode="best_path", no_spatial_relations=True), 55), 
        #("hri2010_greedy_2step", dict(evaluation_mode="best_path", no_spatial_relations=False), 35),
        #("hri2010_greedy_2step", dict(evaluation_mode="best_path", no_spatial_relations=True), 26),
        #("hri2010_wei", dict(evaluation_mode="best_path", no_spatial_relations=False), 37),             
        #("hri2010_wei", dict(evaluation_mode="best_path", no_spatial_relations=True), 37), 
        #("hri2010_lastSDC", dict(evaluation_mode="best_path", no_spatial_relations=False), 23), 
        #("hri2010_lastSDC", dict(evaluation_mode="best_path", no_spatial_relations=True), 23), 
        #("min_entropy", dict(evaluation_mode="best_path", no_spatial_relations=False), 64), 
        #("min_entropy", dict(evaluation_mode="best_path", no_spatial_relations=True), 48), 
        #("duplicate_landmarks", dict(evaluation_mode="best_path", no_spatial_relations=False), 64),
#         ("min_entropy", dict(evaluation_mode="max_prob", no_spatial_relations=False), 51),
#         ("duplicate_landmarks", dict(evaluation_mode="max_prob", no_spatial_relations=False), 53),
#         ("hri2010_global", dict(evaluation_mode="max_prob", no_spatial_relations=False), 44),
#         ("hri2010_greedy_2step", dict(evaluation_mode="max_prob", no_spatial_relations=False), 24), 
#         ("hri2010_wei", dict(evaluation_mode="max_prob", no_spatial_relations=False), 37),
#         ("hri2010_lastSDC", dict(evaluation_mode="max_prob", no_spatial_relations=False), 24),

#         ("min_entropy", dict(evaluation_mode="max_prob", no_spatial_relations=True), 43),
#         ("duplicate_landmarks", dict(evaluation_mode="max_prob", no_spatial_relations=True), 52),
#         ("hri2010_global", dict(evaluation_mode="max_prob", no_spatial_relations=True), 46),
#         ("hri2010_greedy_2step", dict(evaluation_mode="max_prob", no_spatial_relations=True), 24), 
#         ("hri2010_wei", dict(evaluation_mode="max_prob", no_spatial_relations=True), 37),
#         ("hri2010_lastSDC", dict(evaluation_mode="max_prob", no_spatial_relations=True), 24),
#        ("min_entropy", dict(evaluation_mode="best_path", no_spatial_relations=False), 65), 
#        ("lda", dict(evaluation_mode="specialized", no_spatial_relations=False), 58),
#        ("duplicate_landmarks", dict(evaluation_mode="specialized", no_spatial_relations=False), 55),
