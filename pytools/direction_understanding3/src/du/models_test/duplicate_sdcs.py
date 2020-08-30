import min_entropy

class model(min_entropy.model):

    """
    Make extra keyword sdcs.
    """
    def get_usable_sdc(self, sdcs):
        output_sdcs = []
        for sdc in min_entropy.model.get_usable_sdc(self, sdcs):
            if not sdc["kwsdc"]:
                output_sdcs.append(sdc)
                output_sdcs.append(sdc)
                output_sdcs.append(sdc)
        return output_sdcs
