import min_entropy

class model(min_entropy.model):

    """
    Make extra keyword sdcs.
    """
    def get_usable_sdc(self, sdcs):
        output_sdcs = []
        for sdc in min_entropy.model.get_usable_sdc(self, sdcs):
            output_sdcs.append(sdc)
            if len(sdc["landmarks"]) == 1:
                kw = sdc["landmark"]
                mysdc = {"figure":None, "sr":None, "verb":"straight", "landmark":kw, 
                         "kwsdc":True, "landmarks":[kw]}
                output_sdcs.append(mysdc)
        return output_sdcs
