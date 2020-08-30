
from du.dialogue_util import combine
    
def combine_fixed():

    topN_N = 15
    wronged_sn = [16, 25, 31, 36, 46, 48, 57, 84, 89, 96, 98, 101, 104, 111, 112, 138, 139, 143, 148]

    file_lst = ["dialog_SN_"+str(SN)+"_obj_deltaH_askd_2_gend_50_N_"+str(topN_N)+".pck" for SN in range(150)]
#    file_lst = ["dialog_SN_"+str(SN)+"_obj_deltaH_askd_2_gend_50_N_"+str(topN_N)+".pck" for SN in wronged_sn]
        
    from environ_vars import TKLIB_HOME
    dirname = TKLIB_HOME+"/data/directions/direction_floor_8_full/dialog/"

    file_lst = [dirname+W for W in file_lst]
    combine(file_lst,dirname)

combine_fixed()

