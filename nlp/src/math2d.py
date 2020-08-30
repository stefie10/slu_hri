import math
import numpy as na
import numpy.linalg as la


from scipy import stats
from scipy import optimize
import cMath2d
import convexhull   

threshold = cMath2d.getThreshold()


"""
Compute the derivative 
"""
def derivative(x, y):
    lst = zip(x,y)
    d1 = []
    for (x1, y1), (x2, y2) in zip(lst, lst[1:]):
        xdiff = x2 - x1
        ydiff = y2 - y1
        d1.append(ydiff / xdiff)
    return d1

    
        
def segments(path):
    for p, p1 in zip(path, path[1:]):
        yield [p, p1]


def squaredistP(p, p2=[0,0]):
    return pow(p[0] - p2[0],2) + pow(p[1] - p2[1],2)
squaredist = cMath2d.squareDist
#squaredist = squaredistP

def squareDistancesP(p1lst, p2lst):
    return [squaredist(p1, p2) for p1, p2 in zip(p1lst, p2lst)]
squareDistances = cMath2d.numpySquareDistances
#squareDistances = squareDistancesP        



def distP(p, p2=[0,0]):
    return pow(pow(p[0] - p2[0],2) + pow(p[1] - p2[1],2), 0.5)
#return pow(squaredist(p, p2), 0.5)
#distP = cMath2d.dist
dist = cMath2d.dist

def component(direction, point):
    """
    Returns the magnitude of point along that direction.
    Direction must be a unit vector.
    """
    return na.dot(direction, point)

def radiusFromArea(area):
    return math.pow(area/math.pi, 0.5)

def slope(segment):
    p1, p2 = segment
    denominator = p2[0] - p1[0]
    if isDegenerate(segment) or isVertical(segment):
        raise VerticalSegmentError("Segment:" + `segment`)
    else:
        return float(p2[1] - p1[1]) / (p2[0] - p1[0])

def lineEquation(segment):
    (x1, y1), (x2, y2) = segment
    m = slope(segment)
    b = y1 - x1 * m
    return m, b

def lineEquationToPoints(m, b):
    def line(x):
        return m*x + b

    return [(0, line(0)), (1, line(1))]

def normalizeAngle(theta):
    if theta <= 0:
        theta += 2*math.pi
    elif theta >= 2*math.pi:
        theta -= 2*math.pi
    return theta

def normalizeAngleMinusPiToPi(theta):
    theta1 = normalizeAngle(theta)

    if theta1 >= math.pi:
        theta1 -= 2*math.pi

    assert -math.pi <= theta1
    assert math.pi >= theta1
    return theta1

def angleBetweenLines(l1, l2):
    """
    Always returns an angle between 0 ando pi/2
    """
    if isDegenerate(l1) or isDegenerate(l2):
        return 0
    elif isVertical(l1) and isVertical(l2):
        return 0
    elif isVertical(l1) or isVertical(l2):
        if isVertical(l2):
            l2,l1 = l1,l2
        return math.pi/2 - angleBetweenLines(l2, [(0, 0), (1, 0)])
    m1 = slope(l1)
    m2 = slope(l2)
    angle = math.fabs(math.atan2(m2 - m1,1 + m1*m2))
    if angle > math.pi/2:
        angle = math.pi - angle
    assert 0 <= angle
    assert angle <= math.pi/2
    return angle



def angleBetweenSegments(s1, s2):
    """
    The angle between two segments. 
    s1[0] must equal s2[0]
    """
    assert s1[0] == s2[0]
    if isDegenerate(s1) or isDegenerate(s2):
        return 0
    p1, p2 = s1
    p3 = s2[-1]
    
    numerator = squaredist(p1, p2) + squaredist(p1, p3) - squaredist(p2, p3)
    denom = 2 * dist(p1, p2) * dist(p1, p3)

    fraction = numerator / denom
    if sorta_eq(fraction, 1):
        fraction = 1
    if sorta_eq(fraction, -1):
        fraction = -1
    return math.acos(fraction)

"""
Determine if a point is inside a polygon
"""
def isInteriorPointP(polygon, point):
    x, y = point
    c = False
    for (x1, y1), (x2, y2) in allSegments(polygon):
        if x == x1 and y == y1:
            return True
        if ((((y1 <= y) and (y < y2)) or
             ((y2 <= y) and (y < y1))) and
            (x < ((x2 - x1) * (y - y1)) / float(y2 - y1) + x1)):
            c = not c
    return c
isInteriorPoint = cMath2d.isInteriorPoint
        
def isParallel(segment1, segment2):
    if isVertical(segment1) or isVertical(segment2):
        if isVertical(segment1) and isVertical(segment2):
            return True
        else:
            return False
    else:
        m1, b1 = lineEquation(segment1)
        m2, b2 = lineEquation(segment2)
        return sorta_eq(m1, m2)

def isVertical(segment):
    (x1, y1), (x2, y2) = segment
    return sorta_eq(x1, x2) and not (sorta_eq(y1,y2))

"""
Computed following this web page: 
http://local.wasp.uwa.edu.au/~pbourke/geometry/polyarea/
"""
def signedArea(polygon):
    area = 0
    for i in range(0, len(polygon)):
        j = (i + 1) % len(polygon)
        area = area + \
            float(polygon[i][0]*polygon[j][1]) - \
            float(polygon[j][0]*polygon[i][1])
    area = 0.5 * area
    return area


def area(polygon):
    return math.fabs(signedArea(polygon))

"""
Computed following this web page: 
http://local.wasp.uwa.edu.au/~pbourke/geometry/polyarea/
"""
def centroid(polygon):
    cx = 0.0
    cy = 0.0
    a = signedArea(polygon)
    if a == 0:
        X = [x for x, y in polygon]
        Y = [y for x, y in polygon]
        return mean(X), mean(Y)
    #raise ValueError("Polygon with zero area." + `polygon`)
    for i in range(0, len(polygon)):
        j = (i + 1) % len(polygon)
        
        
        multiplier = \
            polygon[i][0]*polygon[j][1] - \
            polygon[j][0]*polygon[i][1]
        cx += multiplier * (polygon[i][0] + polygon[j][0])
        cy += multiplier * (polygon[i][1] + polygon[j][1])

    cx = cx / (6.0*a)
    cy = cy / (6.0*a)
    return cx, cy



def centerOfMass(points):
    xsum = 0.0
    ysum = 0.0
    for p in points:
        xsum = xsum + p[0]
        ysum = ysum + p[1]
    l = len(points)
    return xsum/l, ysum/l

"""        
Find the intersection point of two lines defined as segments.
The intersection point might not be on the two segments. 
Implemented following
http://local.wasp.uwa.edu.au/~pbourke/geometry/lineline2d/
"""
def intersectSegment(segment1, segment2, bound=True):
    try:
        x1, y1 = segment1[0]
        x2, y2 = segment1[1]
        x3, y3 = segment2[0]
        x4, y4 = segment2[1]
    except:
        print "segment1", segment1
        print "segment2", segment2
        raise



    denom = ((y4 - y3)*(x2 - x1) - (x4 - x3)*(y2 - y1))
    if denom == 0:
        # parallel.
        return None
    else:
        ua = float(((x4 - x3)*(y1 - y3) - (y4 - y3)*(x1 - x3))) / denom
        ix = x1 + ua*(x2 - x1)
        iy = y1 + ua*(y2 - y1)
        p = ix, iy
        if not bound or isOnSegment(segment1, p) and isOnSegment(segment2, p):
            return ix, iy
        else:
            return None

def polygonToLine(polygon):
    if len(polygon) == 0:
        return []
    else:
        return list(polygon) + [polygon[0]]

def interiorPointsPython(polygon, pointList):
    return [p for p in pointList if isInteriorPoint(polygon, p)]
interiorPoints = cMath2d.interiorPoints

def intersectSegmentAnalytic(segment, m, b):
    return intersectSegment(segment, [(0, b), (1, m*1+b)], bound=False)

def intersectPolygonAnalytic(polygon, m, b):
    line = polygonToLine(polygon)
    results = set()

    for p1, p2 in zip(line, line[1:]):
        p = intersectSegmentAnalytic([p1, p2], m, b)
        if p and isOnSegment([p1, p2], p):
            results.add(p)
    return list(results)

def contains(poly1, poly2):
    for v in poly2:
        if not isInteriorPoint(poly1, v):
            return False
    return True
def intersectPolygons(poly1, poly2):
    for p1, p2 in allSegments(poly1):
        for m1, m2 in allSegments(poly2):
            if len(intersectLines([p1, p2], [m1, m2])) != 0:
                return True

    return contains(poly1, poly2) or contains(poly2, poly1)
def intersectLines(line1, line2):
    results = []
    last = None
    for p1, p2 in zip(line1, line1[1:]):
        for m1, m2 in zip(line2, line2[1:]):
            p = intersectSegment([p1, p2], [m1, m2])

            if (p != None and
                isOnSegment([p1, p2], p) and
                isOnSegment([m1, m2], p)):
                if not array_equal(p, last):
                    results.append(p)
                    last = p
                assert isOnLine(line1, p), p
                assert isOnLine(line2, p), p
    return results
            
def betweenP(bound1, bound2, d):
    return (((bound1 <= d or sorta_eq(bound1, d)) and (d <= bound2 or sorta_eq(bound2, d)) or 
             ((bound2 <= d or sorta_eq(bound2, d)) and (d <= bound1 or sorta_eq(bound1, d)))))
between = cMath2d.between
#between = betweenP

def isOnLine(line, point):
    for p1, p2 in zip(line, line[1:]):
        if isOnSegment([p1, p2], point):
            return True
    return False

#@memoize.memoize

def isOnSegmentP(segment, point):
    (x1, y1), (x2, y2) = segment
    if isDegenerate(segment):
        return pointEqual(segment[0], point)
    elif isVertical(segment):
        x,y = point
        if sorta_eq(x,x1) and between(y1, y2, y):
            return True
        else:
            return False
    else:
        m, b = lineEquation(segment)
        x,y = point
        if not sorta_eq(x * m + b, y):
            return False

        if between(x1, x2, x):
            return True
        else:
            return False
isOnSegment = cMath2d.isOnSegment
#isOnSegment = isOnSegmentP

    

            
"""
Returns the bounding box of a set of points as a 4 tuple. 

returns minX, minY, width, height
"""
def boundingBox(pointlist,noscale=False):
    firstPoint = pointlist[0]
    
    maxX, maxY = firstPoint
    minX, minY = firstPoint
    for x,y in pointlist:
        if x > maxX:
            maxX = x
        if y > maxY:
            maxY = y
        if x < minX:
            minX = x
        if y < minY:
            minY = y

    scaleX = maxX - minX
    scaleY = maxY - minY
    assert scaleX >= 0
    assert scaleY >= 0
    if noscale:
        return (minX,minY),(maxX,maxY)
    else:
        return (minX, minY), (scaleX, scaleY)

def boundLine(pointlist,numboxes=2,scaling=0.5):
    rectlist = []
    for w in pointlist[::len(pointlist)/(numboxes-1)]:
        xmin = w[0]-scaling
        xmax = w[0]+scaling
        ymin = w[1]-scaling
        ymax = w[1]+scaling
        rect = [(xmin,ymin),(xmin,ymax),(xmax,ymax),(xmax,ymin)]
        rectlist.append(rect)
    xmin = pointlist[len(pointlist)-1][0]-scaling
    xmax = pointlist[len(pointlist)-1][0]+scaling
    ymin = pointlist[len(pointlist)-1][1]-scaling
    ymax = pointlist[len(pointlist)-1][1]+scaling
    rect = [(xmin,ymin),(xmin,ymax),(xmax,ymax),(xmax,ymin)]
    rectlist.append(rect)
    return rectlist

def angle(point):
    #return math.acos(point[0] / dist((0, 0), point))
    return math.atan2(point[1], point[0])

def stepAlongLineP(line, stepSize):
    return [x for x in stepAlongLineIter(line, stepSize)]
#stepAlongLine = stepAlongLineP

def stepAlongLine(line, stepSize):
    # if you don't remove duplicates, the c library seg faults.
    # at least it did in direction understanding land.
    return cMath2d.stepAlongLine(removeDuplicates(line), stepSize)
#stepAlongLineP = stepAlongLine


def stepAlongLineIter(line, stepSize):
    distAlongStep = 0.0
    if len(line) == 0:
        raise ValueError("Line has no length" + `line`)
    yield line[0]
    if sorta_eq(stepSize, 0):
        return
    for p1, p2 in zip(line, line[1:]):


        # go to next point
        # find distance and yield, and stay at this point.
        startP = p1
        while True:
            newDistAlongStep = distAlongStep + dist(startP, p2)
            if newDistAlongStep >= stepSize:
                yieldP = pointOnSegment([startP, p2], stepSize - distAlongStep)
                yield yieldP

                startP = yieldP
                distAlongStep = 0
            else:
                distAlongStep = newDistAlongStep
                break

    
"""
Find a point the given distance along the line. 
"""    
def pointOnLine(line, distance):
    distAlongLine = 0.0
    for p1, p2 in zip(line, line[1:]):
        d = dist(p1, p2)
        distAlongLine += d
        if distAlongLine > distance:
            return pointOnSegment([p1, p2], d - (distAlongLine - distance))
        elif sorta_eq(distAlongLine, distance):
            return p2
    raise ValueError("Distance " + `distance` + " longer than line " + 
                     `line` + " length of line: " + `length(line)`)

        
"""
Find a point a given distance along a line segment
"""                                
def pointOnSegmentPython(line, distance):
    if len(line) != 2:
        raise ValueError("Segment must contain two points: " + `line`)
    if length(line) == 0:
        raise ValueError("Degenerate line: " + `line`)
    (x1, y1), (x2, y2) = line
    p1, p2 = line
    cosAngle = (x2 - x1)/dist(p1, p2)
    sinAngle = (y2 - y1)/dist(p1, p2)

    xdist = cosAngle * distance
    ydist = sinAngle * distance

    return x1 + xdist, y1 + ydist

pointOnSegment = cMath2d.pointOnSegment
#pointOnSegment = pointOnSegmentPython


def closestPointOnSegmentLineP(line, point):
    """ 
    Closest point on the line defined by two points.
    http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/ 
    """
    if squaredist(line[0], line[1]) == 0:
        # line contains exactly one point. 
        return line[0]
    if line[0][0] < line[1][0]: 
        (x1, y1), (x2, y2) = line
    else:
        (x2, y2), (x1, y1) = line
    x3, y3 = point
    u = ((x3 - x1) * (x2 - x1) + (y3 - y1) * (y2 - y1)) / \
        squaredist(line[0], line[1])
    x = x1 + u * (x2 - x1)
    y = y1 + u * (y2 - y1)
    return x, y
closestPointOnSegmentLine = cMath2d.closestPointOnSegmentLine
#closestPointOnSegmentLine = closestPointOnSegmentLineP



def closestPointOnSegmentP(line, point):
    """
    If the closest point on the segment defined by the line isn't on
    the segment, returns whichever endpoint is closest.
    http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/
    """
    x, y = closestPointOnSegmentLine(line, point)
    if isOnSegment(line, (x, y)):
        return (x, y)
    else:
        p1, p2 = line
        d1 = squaredist(p1, point)
        d2 = squaredist(p2, point)
        if d1 > d2:
            return p2
        else:
            return p1
closestPointOnSegment = cMath2d.closestPointOnSegment
#closestPointOnSegment = closestPointOnSegmentP


        
    

def closestPointOnPolygonP(polygon, point):
    return closestPointOnLine(polygonToLine(polygon), point)
closestPointOnPolygon = cMath2d.closestPointOnPolygon
"""    
   Closest point on a line (made up of a list of points./
"""
def closestPointOnLine(line, point):
    minPoint = line[0]
    minDist = dist(minPoint, point)
    for p1, p2 in zip(line, line[1:]):
        p = closestPointOnSegment([p1, p2], point)
        distToSegment = dist(p, point)
        if distToSegment < minDist:
            minDist = distToSegment
            minPoint = p


    return minPoint
closestPointOnLine = cMath2d.closestPointOnLine
#closestPointOnLine = closestPointOnLine


def distAlongSegment(seg, point):
    p1, p2 = seg
    if not isOnSegment(seg, point):
        raise ValueError("Point " + `point` + " not on segment " + `seg`)
    return dist(p1, point)
    

    
def distAlongLine(line, point):
    distAlongLine = 0.0
    for p1, p2 in zip(line, line[1:]):
        if isOnSegment([p1, p2], point):
            return distAlongLine + dist(p1, point)
        distAlongLine += dist(p1, p2)
    raise ValueError("Point " + `point` + " not on line " + `line`)

"""
The distance between p1 and p2, along the line.  p1 and p2 must be on
the line.
"""
def distBetweenPointsAlongLine(line, p1, p2):
    return distAlongLine(line, p2) - distAlongLine(line, p1)

def distBetweenPointsAlongPolygon(polygon, p1, p2):
    per = perimeter(polygon)
    s1 = math.fabs(distBetweenPointsAlongLine(polygonToLine(polygon), p1, p2))
    s2 = per - s1
    return min(s1, s2)

def lengthP(line):
    distAlongLine = 0.0
    for p1, p2 in zip(line, line[1:]):
        distAlongLine += dist(p1, p2)
    return distAlongLine

length = cMath2d.length
#lengthP = cMath2d.length


def midpointLine(line):
    l = length(line)
    return pointOnLine(line, l/2.0)

def midpoint(segment):
    (x1, y1), (x2, y2) = segment
    if isDegenerate(segment):
        return segment[0]
    elif isVertical(segment):
        assert sorta_eq(x1, x2)
        return (x1, (y1 + y2 ) / 2.0)
    else:
        m, b = lineEquation(segment)
        x =     (x1 + x2) * 0.5
        y = x * m + b
        return x, y

def perimeter(polygon):
    return length(polygonToLine(polygon))
"""
Returns a segment perpendicular to a given segment, through the
specified point, which must be on the segment.  If no point is
specified, it uses the segment's midpoint.
"""
def perpendicular(segment, startPoint=None):
    (x1, y1), (x2, y2) = segment
    if startPoint == None:
        startPoint = midpoint(segment)

    startX, startY = startPoint
    segmentLength = length(segment)
    if isDegenerate(segment):
        return segment
    elif isVertical(segment):
        return [(x1 - segmentLength/2.0, startY), 
                (x1 + segmentLength/2.0, startY)] 
    else:
        m, b = lineEquation(segment)

        if not sorta_eq(m, 0.0):
            newM = -1.0/m
            newB = startY - startX * newM
            offset = math.fabs(x2 - x1) / 2
            newX1 = startX - offset
            newX2 = startX + offset
            
            return [(newX1, newM * newX1 + newB),
                    (newX2, newM * newX2 + newB)]
        else:

            #assert_sorta_eq(y1, y2)
            return [(startX, y1 - segmentLength/2.0), 
                    (startX, y1 + segmentLength/2.0)]



def stdDeviation(lst):
    return math.pow(variance(lst), 0.5)
def variance(lst):
    avg = mean(lst)
    sum = 0.0
    for x in lst:
        sum += math.pow(x - avg, 2)
    return sum / len(lst)
    
def mean(lst):
    sum = 0.0
    cnt = 0
    for x in lst:
        cnt += 1
        sum += x
    return sum / cnt

def harmonic_mean(lst):
    return len(lst) / sum([1.0/a for a in lst])

def geometric_mean(lst):
    sum = 0.0
    for x in lst:
        sum += math.log(x)
    return math.exp((1.0/len(lst)) * sum)


"""
Idea for this from Blissard 08, and skubic/coyote work.
Following http://en.wikipedia.org/wiki/Principal_components_analysis
"""

def eigenvectorsOGrid(polygon, resolution=100):
    gridPointList = polygonToOccupancyGrid(polygon, resolution)
    X = na.transpose(na.array(gridPointList))
    M, N = na.shape(X)
    u = na.mean(X, 1)

    uh = na.transpose(na.multiply(u, na.ones((N, M))))

    B = X - uh
    assert M == 2
    assert N == len(gridPointList), N
    C = (1./N) * na.dot(B, na.transpose(B))
    return la.eig(C)

"""
Following levin02principal.pdf, which is in doc/analytical-eigen-axes/
Idea for eigen axes still from Blissard, but the algorithm is from levin.
"""
def eigenvectorsRecursive(polygon):
    A = na.transpose(na.array(polygon))
    n, d = A.shape
    assert n == 2
    assert d == len(polygon)
    I = na.identity(d)
    E = na.ones((d,d))

    cov = (1. / (d * (d + 1))) * na.dot(na.dot( A, I+E),
                                        na.transpose(A))
    return la.eig(cov)
    
    
def eigenvectors(polygon, resolution=100):
    #return eigenvectorsOGrid(polygon, resolution)
    return eigenvectorsRecursive(polygon)



    

def eigenAxes(polygon, resolution=100):
    u, v = eigenvectors(polygon, resolution)
    a0 = v[:, 0] * u[0]
    a1 = v[:, 1] * u[1]
    c = centroid(polygon)
    if u[0] > u[1]:
        major, minor = a0, a1
    else:
        major, minor = a1, a0
        
    return [c-major , c+major], [c-minor, c+minor]


"""
Polygon is a list of points.  Grid is a really long list of points.
Each point is "on" in the grid.  I guess.

Resolution is the number of points from the bounding box we'll test. 
"""
def polygonToOccupancyGrid(polygon, resolution = 100):
    a = area(polygon)
    (minX, minY), (width, height) = boundingBox(polygon)
    stepSize = math.pow(width * height / float(resolution), 0.5)
    pointList = []
    for x in na.arange(minX+stepSize/2, minX + width, stepSize):
        for y in na.arange(minY+stepSize/2, minY + height, stepSize):
            p = x, y
            if isInteriorPoint(polygon, (x, y)):
                pointList.append(p)
    return pointList


def pointLstToXlstAndYlst(pointLst):
    xlst = [x for x, y in pointLst]
    ylst = [y for x, y in pointLst]
    return xlst, ylst

def sorta_eq(v1, v2, threshold=threshold):
    return math.fabs(v1 - v2) < threshold
def array_equal(arr1, arr2):
    if arr1 == None or arr2 == None:
        return False
    if len(arr1) != len(arr2):
        return False
    else:
        return (na.fabs(na.array(arr1) - na.array(arr2)) < threshold).all()
def assert_sorta_eq(v1, v2):
    assert sorta_eq(v1, v2), (v1, v2)

def assert_array_equal(arr1, arr2):
    try:
        for a1, a2 in zip(arr1, arr2):
            if hasattr(a1, "__iter__") and hasattr(a2, "__iter__"):
                assert_array_equal(a1, a2)
            else:
                assert_sorta_eq(a1, a2)            
        assert len(arr1) == len(arr2), (arr1, arr2)
    except:
        print "arr1", arr1
        print "arr2", arr2
        raise
    #assert array_equal(arr1, arr2), (arr1, arr2)


"""
Returns a subset of the line that starts at p1 and ends at p2.
p1 and p2 have to be on the line. 

Returns the line itself if p1 and p2 aren't on the line. 
"""
def trimLine(line, p1, p2):
    if not isOnLine(line, p1) or not isOnLine(line, p2):
        return line
    if distAlongLine(line, p1) < distAlongLine(line, p2):
        startPoint, endPoint = p1, p2
    else:
        startPoint, endPoint = p2, p1
    trimmedLine = []
    state = "before"
    for p1, p2 in zip(line, line[1:]):
        if state == "before" and isOnSegment([p1, p2], startPoint):
            trimmedLine.append(startPoint)
            state = "during"
        if isOnSegment([p1, p2], endPoint):
            trimmedLine.append(endPoint)
            return trimmedLine
        if state == "during":
            trimmedLine.append(p2)
    assert False, "never get here"


"""
Returns a subsequence of points from the polygon, starting at p1, and
ending at p2.  p1 and p2 do not have to be vertices, but all other
points in the list will be vertices of the polygon.
p1 and p2 have to be on the polygon. 
"""
def trimPolygon(polygon, p1, p2):
    l1 = trimLine(polygon, p1, polygon[-1])
    return trimLine(l1 + polygon, p1, p2)

    
def fitLine(points):
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    return slope, intercept

def averageDistance(path1, path2, resolution=100):
    sum = 0.0
    for p1 in stepAlongLine(path1, length(path1) / resolution):
        p2 = closestPointOnLine(path2, p1)
        sum += dist(p1, p2)
    return sum / resolution

def pathsToPolygon(p1, p2):
    if ((dist(p1[0], p2[0]) + dist(p1[-1], p2[-1])) >= 
        (dist(p1[0], p2[-1]) + dist(p1[-1], p2[0]))):
        return p1 + p2
    else:
        return p2 + p1
    

def approxAreaComplexPolygon(polygon):
    (minX, minY), (width, height) = boundingBox (polygon)
    area = 0.0
    scale = 100
    boxW = width/ 100.0
    boxH = height / 100.0
    boxA = boxW * boxH
    for x in na.arange(minX, minX + width, boxW):
        for y in na.arange(minY, minY + height, boxH):
            if isInteriorPoint(polygon, (x, y)):
                area += boxA
    return area

"""
DOES NOT WORK RIGHT. Comment in test cases and fix before using. 
"""
def areaBetweenPaths(path1, path2):
    if ((dist(path1[0], path2[0]) + dist(path1[-1], path2[-1])) >= 
        (dist(path1[0], path2[-1]) + dist(path1[-1], path2[0]))):
        path2.reverse()
    
    import plot2d
    n1 = [path2[0]] + path1
    n2 = path2 + [path1[-1]]
    plot2d.plotLine(n1, "r")
    plot2d.plotLine(n2, "g")
    ipoints = intersectLines(n1, n2)
    totalArea = 0.0
    for p1, p2 in zip(ipoints, ipoints[1:]):
        trimmed1 = trimLine(n1, p1, p2)
        trimmed2 = trimLine(n2, p1, p2)
        trimmed2.reverse()
        polygon =  trimmed1 + trimmed2 
        plot2d.plotLine(polygon, "b")
        totalArea += area(polygon)
    return totalArea
        

def arrayToLine(arr):
    return [(arr[0], arr[1]), (arr[2], arr[3])]
def lineToArray(line):
    return [line[0][0], line[0][1], line[1][0], line[1][1]]
    
def fitLineToPath(path):

    def score(xArr):
        line = arrayToLine(xArr)
        return (areaBetweenPaths(path, line) +  
                math.pow(averageDistance(path, line), 2) * 100) 
    
    xopt = optimize.fmin(score, 
                      lineToArray(path))
    return arrayToLine(xopt)


def isConvex(polygon):
    return not isConcave(polygon)
def isConcave(polygon):
    startSign = None
    for i in range(0, len(polygon)):
        lastx, lasty = polygon[i-1]
        thisx, thisy = polygon[i]
        nextIdx = (i + 1) % len(polygon)
        nextx, nexty = polygon[nextIdx]
        
        cross = ((thisx-lastx)*(nexty-thisy) - \
                     (thisy-lasty)*(nextx-thisx))
        if cross == 0:
            continue
        thisSign = cross / math.fabs(cross)
        if not startSign:
            startSign = thisSign
        else:
            if startSign != thisSign:
                return True
    return False



"""
Returns the first subset of the line that is inside the polygon.

If there are more than two intersection points, it just returns the
part between the first two.  If the line is contained inside the
polygon, it returns the whole thing.  If the line is completely
outside the polygon, it returns the empty list.

"""
def clip(line, polygon):
    try:
        ipoints = intersectLines(line, polygonToLine(polygon))[0:2]
    except:
        print "line", line
        print "polygon", polygon
        raise

    if len(ipoints) == 0:
        if isInteriorPoint(polygon, line[0]):
            return line
        else:
            return []
    else:
        newline = []

        if not isInteriorPoint(polygon, line[0]):
            newline.append(ipoints[0])
        started = False
        lastPoint = None
        for p in line:
            if isInteriorPoint(polygon, p):
                if not array_equal(p, ipoints[0]):
                    newline.append(p)
                    started = True
            else:
                if started:
                    lastPoint = p
                    break

        if not started or lastPoint != None:
            newline.append(ipoints[-1])

        return  newline

def clipPoint(path, startP, endP):
    clippedPath = []
    started = False
    for segment in segments(path):
        if isOnSegment(segment, startP):
            started = True
            clippedPath.append(startP)
        if isOnSegment(segment, endP):
            clippedPath.append(endP)
            break
        if started:
            # ugly for speed (profiled on 8-26-2009 for robotic understanding
            # with tk.  - stefie10
            # it said array_equal is slow, and this looks like the only place
            # that's calling it. 
            if not (sorta_eq(segment[0][0], startP[0]) and
                    sorta_eq(segment[0][1], startP[1])):
                clippedPath.extend(segment)
            else:
                clippedPath.append(segment[-1])
    return clippedPath
        
    
"""
Returns the convex hull of a set of points.
"""
def convexHull(points):
    return list(convexhull.convexHull(points))




def powerset(s):
    d = dict(zip(
            (1<<i for i in range(len(s))),
            (set([e]) for e in s)
             ))
    subset = set()
    yield subset
    for i in xrange(1, 1<<len(s)):
        subset = subset ^ d[i & -i]
        yield subset

"""
Returns two new polygons formed by cutting the existing polygon
at the segment (or extension of segment)

The two new polygons are subsets of the points on the original
polygons, and the connecting segment is the absent point on the list
of points.  This is important if you just want the border for the cut.
"""
def cutPolygon(polygon, segment):
    lPolygon = polygonToLine(polygon)
    intersectPoints = intersectLines(lPolygon, segment)
    if len(intersectPoints) != 2:
        raise ValueError("Must call with a segment that intersects the polygon exactly twice! polygon:" + `polygon` + " segment:" + `segment`)
    i1, i2 = intersectPoints
    
    onHalf1 = True

    half1 = []
    half2 = []
    for p1, p2 in zip(lPolygon, lPolygon[1:]):
        if onHalf1:
            half1.append(p1)
            if isOnSegment([p1, p2], i2):
                tmp = i1
                i1 = i2
                i2 = tmp
            if isOnSegment([p1, p2], i1):
                half1.append(i1)
             
                secondHalfOfHalf1 = half1
                half1 = []
                half1.append(i2)
                half2.append(i1)
                onHalf1 = False
        else:
            half2.append(p1)
            if isOnSegment([p1, p2], i2):
                half2.append(i2)
                onHalf1 = True
    half1 = half1 + secondHalfOfHalf1

    return half1, half2

"""
Returns the half of the polygon pointed to by the unit vector.

First cuts the polygon in half through the centroid using the vector
perpendicular to the unit vector.  Then returns the appropriate half,
in the direction of the vector.

"""
    
def xHalf(polygon, unitVector):
    c = centroid(polygon)
    direction = (unitVector[1], -unitVector[0])
    
    l = perimeter(polygon)
    s0 = [c, (c[0] + direction[0],
              c[1] + direction[1])]
    startP = pointOnSegment(s0, -l)
    endP = pointOnSegment(s0, l)
    p1, p2 = cutPolygon(polygon, [startP, endP])
    c1 = centroid(p1)
    c2 = centroid(p2)
    target = (c[0] + unitVector[0], c[1] + unitVector[1])

    if dist(c1, target) < dist(c2, target):
        return p1
    else:
        return p2

def cartesianToPolar(point):
    x, y = point
    return dist((0, 0), point), math.atan2(y, x)

    

def argMin(lst):    
    value = None
    idx = None
    for i, x in enumerate(lst):
        if value is None:
            value = x
            idx = i
        else:
            if x < value:
                value = x
                idx = i
    return idx, value
        
def argMax(lst):
    value = None
    idx = None
    for i, x in enumerate(lst):
        if value is None:
            value = x
            idx = i
        else:
            if x > value:
                value = x
                idx = i
    return idx,value
                
def pathToPolygon(path, delta = (0.3, 0.3)):
    translatedPath = []
    for p in path:
        translatedPath.append((p[0] + delta[0],
                              p[1] + delta[1]))
    polygon = path + list(reversed(translatedPath))
    return polygon

def slideWindowAlongPath(path, stepSize, absoluteSize=None, fractionSize=None):
    if absoluteSize == None:
        assert fractionSize != None, "Must pass absolute size or fraction size"
        absoluteSize = length(path) * fractionSize
    distSoFar = 0
    for startP in stepAlongLine(path, stepSize):
        try:
            endP = pointOnLine(path, distSoFar + absoluteSize)
        except ValueError:
            break
        yield clipPoint(path, startP, endP)
        distSoFar += stepSize



def isDegenerate(segment):
    return pointEqual(segment[0], segment[1])

def pointEqualP(p1, p2):
    return array_equal(p1, p2)
pointEqual = cMath2d.pointEqual
#pointEqual = pointEqualP


def segmentEqualP(s1, s2):
    return array_equal(s1, s2)
segmentEqual = cMath2d.segmentEqual
#segmentEqual = segmentEqualP



class VerticalSegmentError(ValueError):
    def __init__(self, segment):
        ValueError.__init__(self, `segment`)

class DegenerateSegmentError(ValueError):
    def __init__(self, segment):
        ValueError.__init__(self, `segment`)

        
def boxToPolygon(lowerLeft, dimensions):
    x0,y0 = lowerLeft
    width, height = dimensions
    return [(x0, y0), (x0+width, y0), 
            (x0+width, y0+height), (x0, y0+height)]

    

def smallestWindow(lst, windowSize):

    windowTotal = sum(lst[0:windowSize]) 

    minWindow = windowTotal
    maxIdx = 0, windowSize


    idx = (0,windowSize)
    for i in range(1, len(lst) - windowSize + 1):
        startIdx = i
        endIdx = startIdx + windowSize - 1
        windowTotal -= lst[startIdx - 1]
        windowTotal += lst[endIdx]
        if windowTotal < minWindow:
            minWindow = windowTotal
            maxIdx = startIdx, endIdx + 1 


    return maxIdx


def rotatePoint(p1, angle, aboutPoint=(0,0)):
    def rotatePointOrigin(p1, angle):
        sinval = math.sin(angle)
        cosval = math.cos(angle)
        x,y = p1
        nx = x * cosval  - y * sinval
        ny = y * cosval + x * sinval
        return nx, ny
    x,y = p1
    ax, ay = aboutPoint
    nx, ny = rotatePointOrigin((x - ax, y - ay), angle)
    return nx + ax, ny + ay
            
    
def rotate(points,  angle, aboutPoint=(0,0)):
    outpoints = [rotatePoint(p, angle, aboutPoint)  for p in points]
    return outpoints
    
def unitVector(theta):
    return math.cos(theta), math.sin(theta)


def allSegments(polygon):
    for i, p1 in enumerate(polygon):
        j= (i + 1) % len(polygon)
        p2 = polygon[j]
        yield p1, p2


def regression(line):
    x = [p[0] for p in line]
    y = [p[1] for p in line]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    return slope, intercept, r_value, p_value, std_err





def subSample(array, target):
    return na.take(na.array(array), na.arange(0, len(array), len(array)/target), axis=0)


def removeDuplicates(line):
    newLine = []
    lastPoint = None
    for p1 in line:
        if lastPoint is None or not pointEqual(p1, lastPoint):
            lastPoint = p1
            newLine.append(p1)
    return newLine

def heading(segment):
    (x1, y1), (x2, y2)  = segment
    if isDegenerate(segment):
        return 0
    elif isVertical(segment):
        if y1 < y2:
            return math.pi/2
        elif y2 < y1:
            return 3*math.pi/2
        else:
            raise ValueError("Should never get here, because it is degenerate:" +
                             `segment`)
    else:
        m, b = lineEquation(segment)
        p = (1, m)
        r, theta = cartesianToPolar(p)
        if (x2 < x1):
            theta = theta + math.pi
        return theta
        
def deltaHeading(s1, s2):
    """
    Returns 0 if s1 and s2 are on the same heading.
    Returns a number between 0 and -pi if it represents a right turn.
    Returns a number between 0 and pi if it represents a left turn.
    If it's going backwards, it will either be pi or -pi - there is a 
    discontiunity there.
    """
    if isDegenerate(s1) or isDegenerate(s2):
        return 0
    else:
        theta1 = heading(s1)
        theta2 = heading(s2)
        rTheta1 = theta1 - theta1
        rTheta2 = theta2 - theta1
        rTheta2 = normalizeAngleMinusPiToPi(rTheta2)
        return rTheta2

def ratioLengthByCrow(line):
    if length(line) == 0:
        return 0
    else:
        return dist(line[0], line[-1]) / length(line)




def derive_transform(a1, a2, b1, b2):
    """ Given two pairs of features, return a 2D transformation
        function that will convert the first pair to the second.
        from http://mike.teczno.com/img/qrgoyles/matchup.py
    """
    a1x, a1y = a1
    a2x, a2y = a2
    b1x, b1y = b1
    b2x, b2y = b2

    affine = na.identity(3)
    
    # translate A point to (0, 0)
    affine = na.dot(na.array([[1, 0, -a1x], [0, 1, -a1y], [0, 0, 1]]), affine)
    
    # scale to B size
    scale = math.hypot(b2x - b1x, b2y - b1y) / math.hypot(a2x - a1x, a2y - a1y)
    affine = na.dot(na.array([[scale, 0, 0], [0, scale, 0], [0, 0, 1]]), affine)
    
    # rotate to B orientation
    #theta = math.atan2(a2x - a1x, a2y - a1y) - math.atan2(b2x - b1x, b2y - b1y)
    theta = math.pi/2
    print "theta", math.degrees(theta)
    affine = na.dot(na.array([[math.cos(theta), -math.sin(theta), 0], 
                              [math.sin(theta), math.cos(theta), 0], 
                              [0, 0, 1]]), affine)

    affine = na.dot(na.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                    affine)

    
    # translate back to B point
    affine = na.dot(na.array([[1, 0, b1x], [0, 1, b1y], [0, 0, 1]]), affine)
    
    return make_transform(affine)

def make_transform(affine):
    """ Given an affine transformation matrix return the associated 2D transform function.
    """
    ax, bx, cx, ay, by, cy = affine[0,0], affine[0,1], affine[0,2], affine[1,0], affine[1,1], affine[1,2]
    return lambda x, y: (ax * x + bx * y + cx, ay * x + by * y + cy)



def points_to_xy(points):
    X = []
    Y = []
    for x, y in points:
        X.append(x)
        Y.append(y)
    return X, Y


def direction(p1, p2):
    """
    The angle you have to face if you want to face p2 when standing on p1.
    """
    return angle((p2[0] - p1[0], p2[1] - p1[1]))


def interpolate(time1, position1, time2, position2, offset):
    return cMath2d.interpolate(float(time1), position1, float(time2), position2, float(offset))

def pyinterpolate(time1, position1, time2, position2, offset):
    assert time1 <= offset <= time2, (time1, offset, time2)
    x1, y1, theta1 = position1
    x2, y2, theta2 = position2
    segment = [(x1, y1), (x2, y2)]
    fraction = float(offset - time1) / (time2 - time1)

    dtheta = (theta2 - theta1)* fraction
                
    if isDegenerate(segment):
        return position1
    elif isVertical(segment):
        x = x1
        y = y1 + fraction * (y2 - y1) 
    else:
        m,b = lineEquation(segment)
        x = (x1 + fraction * (x2 - x1))
        y = m*x + b
    return x, y, theta1 + dtheta




def xyToXyth(fig_xy):
    fig_xy = na.array(fig_xy)
    Xst, Yst = fig_xy[:,:-1]
    Xend, Yend = fig_xy[:,1:]
   
    Theta = na.arctan2(Yend-Yst, Xend-Xst);
    Theta = list(Theta)
    Theta.append(Theta[-1])
    return na.array([fig_xy[0], fig_xy[1], Theta])




def computeBoundaryLine(landmarkGeom, figureGeom):
    startG = closestPointOnLine(landmarkGeom, figureGeom[0])
    endG = closestPointOnLine(landmarkGeom, figureGeom[-1])
    
    l1 = trimPolygon(landmarkGeom, startG, endG)
    l2 = trimPolygon(landmarkGeom, endG, startG)
    if length(l1) <= length(l2):
        return l1
    else:
        return l2


    

