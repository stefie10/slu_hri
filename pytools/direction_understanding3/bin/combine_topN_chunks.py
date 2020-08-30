from evaluate_model import *
import cPickle


file_lst_50 = [
    "topN.output_6.pck",
    "topN.output_7.pck",
    "topN.output_8.pck",
    "topN.output_9.pck",
    "topN.output_10.pck",
    "topN.output_11.pck",
    "topN.output_12.pck",
    "topN.output_13.pck",
    "topN.output_50.pck",
    "topN.output_51.pck",
    "topN.output_14.pck",
    "topN.output_15.pck",
    "topN.output_16.pck",
    "topN.output_17.pck",
    "topN.output_18.pck",
    "topN.output_19.pck"]

# Attention: this was to run only on my home computer. Modify if needed to run on another machine.
dirname = "/home/stevend/Desktop/code/tklib/data/directions/direction_floor_8_full/output/specialized/"

output_fname_50 = dirname+"topN_50_combined.pck"
output_fname_30 = dirname+"topN_30_combined.pck"
output_fname_15 = dirname+"topN_15_combined.pck"


file_lst_30 = ["topN.output_"+str(i)+".pck" for i in range(20,35)]
file_lst_15 = ["topN.output_"+str(i)+".pck" for i in range(1,16)]


file_lst = file_lst_15
file_lst = [dirname+W for W in file_lst]
output_fname = output_fname_15

output_data = initialize_save_data()

# Initialize Aggregate Save Data:

for f_name in file_lst:
    save_data = cPickle.load(open(f_name,"r"))
    # for every sentence information which is not None:
    # add the sentence information in the aggregate Save Data:
    for key in output_data.keys():
        if key == "do_exploration":
            continue
        for SN in range(len(save_data[key])):
            if save_data[key][SN] != None:# and key in output_data.keys():
                if output_data[key]==None:
                    print key
                while len(output_data[key]) <= SN:
                    output_data[key].append(None)
                output_data[key][SN] = save_data[key][SN]

# Add the other useful stuff from the first file
save_data = cPickle.load(open(file_lst[0],"r"))
output_data["tmap"] = save_data["tmap"]
output_data["tmap_locs"] = save_data["tmap_locs"]
output_data["tmap_graph_D"] = save_data["tmap_graph_D"]
output_data["region_to_topology"] =save_data["region_to_topology"]
output_data["corpus_fname"] = save_data["corpus_fname"]
output_data["run_description"] = save_data["run_description"]
output_data["options"] = save_data["options"]
 
# save the data as specified
cPickle.dump(output_data, open(output_fname, "w") )
