from eventLogic.expressions import Primitive



class Visible(Primitive):
    def __init__(self, figure, landmark):
        Primitive.__init__(self, figure, landmark)
        
        
class Following(Primitive):
    def __init__(self, figure, landmark):
        Primitive.__init__(self, figure, landmark)


class Close(Primitive):
    def __init__(self, figure, landmark):
        Primitive.__init__(self, figure, landmark)
                