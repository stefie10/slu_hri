


void setThreshold(double t);
double getThreshold(void);

enum FOOLEAN {FALSE=0,TRUE=1};
typedef enum FOOLEAN boolean;

struct poseStruct{
  double x;
  double y;
  double theta;
};
typedef struct poseStruct pose;

struct pointStruct {
  double x;
  double y;
};
typedef struct pointStruct point;

struct segmentStruct {
  point start;
  point end;
};
typedef struct segmentStruct segment;

struct lineStruct {
  point * points;
  int length;
};
typedef struct lineStruct line;


double dist(point p1, point p2);
double squareDist(point p1, point p2);
void squareDistances(line l1, line l2, double * out, int dim);


point pointOnSegment(segment s, double distance);


boolean segmentEqual(const segment s1, const segment s2);
boolean pointEqual(const point p1, const point p2);
boolean sorta_eq(const double d1, const double d2);

boolean between(double bound1, double bound2, double d);

boolean isOnSegment(const segment s, const point p);
double slope(segment s);

point closestPointOnLine(line l, point p);
point closestPointOnSegment(segment s, point p);
point closestPointOnSegmentLine(segment s, point p);

double length(line l);


line stepAlongLine(line l, double stepSize);

pose interpolate(double t1, pose p1, double t2, pose p2, double offset);

boolean isInteriorPoint(line polygon, point p);

line interiorPoints(line polygon, line points);

point closestPointOnPolygon(const line polygon, const point p);
