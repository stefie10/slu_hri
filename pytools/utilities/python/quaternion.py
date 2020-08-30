import math

class Quaternion:
    def __init__ (self, *args):
        if len(args) == 4:
            self.q = list (args[:])
        elif len(args) == 1 and len(args[0]) == 4:
            self.q = args[0][:]
        else:
            raise TypeError ("invalid initializer")
        self.conjugate = [ self.q[0], -self.q[1], -self.q[2], -self.q[3] ]

    def __mul__ (self, other):
        a = self.q
        b = other.q
        return Quaternion (a[0]*b[0] - a[1]*b[1] - a[2]*b[2] - a[3]*b[3],
                           a[0]*b[1] + a[1]*b[0] + a[2]*b[3] - a[3]*b[2],
                           a[0]*b[2] - a[1]*b[3] + a[2]*b[0] + a[3]*b[1],
                           a[0]*b[3] + a[1]*b[2] - a[2]*b[1] + a[3]*b[0])

    def __getitem__ (self, i):
        return self.q[i]

    def __repr__ (self):
        return repr (self.q)
    
    def rotate (self, vector):
        b = Quaternion (0, vector[0], vector[1], vector[2])
        a = self * b
        b.q[0] = self.q[0]
        b.q[1] = - self.q[1]
        b.q[2] = - self.q[2]
        b.q[3] = - self.q[3]
        c = a * b
        return c[1:]

    @staticmethod
    def from_roll_pitch_yaw (roll, pitch, yaw):
        halfroll = roll / 2;
        halfpitch = pitch / 2;
        halfyaw = yaw / 2;
        sin_r2 = math.sin (halfroll)
        sin_p2 = math.sin (halfpitch)
        sin_y2 = math.sin (halfyaw)
        cos_r2 = math.cos (halfroll)
        cos_p2 = math.cos (halfpitch)
        cos_y2 = math.cos (halfyaw)
        return Quaternion (cos_r2 * cos_p2 * cos_y2 + sin_r2 * sin_p2 * sin_y2,
                 sin_r2 * cos_p2 * cos_y2 - cos_r2 * sin_p2 * sin_y2,
                 cos_r2 * sin_p2 * cos_y2 + sin_r2 * cos_p2 * sin_y2,
                 cos_r2 * cos_p2 * sin_y2 - sin_r2 * sin_p2 * cos_y2)

    def to_roll_pitch_yaw (self):
        roll_a = 2 * (self.q[0]*self.q[1] + self.q[2]*self.q[3])
        roll_b = 1 - 2 * (self.q[1]*self.q[1] + self.q[2]*self.q[2])
        roll = math.atan2 (roll_a, roll_b)

        pitch_sin = 2 *  (self.q[0]*self.q[2] - self.q[3]*self.q[1])
        pitch = math.asin (pitch_sin)

        yaw_a = 2 * (self.q[0]*self.q[3] + self.q[1]*self.q[2])
        yaw_b = 1 - 2 * (self.q[2]*self.q[2] + self.q[3]*self.q[3])
        yaw = math.atan2 (yaw_a, yaw_b)
        return roll, pitch, yaw

if __name__ == "__main__":
    q = Quaternion.from_roll_pitch_yaw (0, 0, 2 * math.pi / 16)
    v = [ 1, 0, 0 ]
    print v
    for i in range (16):
        v = q.rotate (v)
        print v
