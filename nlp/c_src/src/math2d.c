#ifdef NDEBUG
#undef NDEBUG
#endif

#include "math2d.h"
#include <stdlib.h>
#include <assert.h>
#include <math.h>
#include <stdio.h>

double threshold = 0.0001;

void setThreshold(double t) 
{
  threshold = t;
}

double getThreshold() 
{
  return threshold;
}

double dist(const point p1, const point p2)
{
  return pow((p2.y - p1.y) * (p2.y - p1.y) + 
	      (p2.x - p1.x) * (p2.x - p1.x), 0.5);

}

double squareDist(const point p1, const point p2)
{
  return ((p2.y - p1.y) * (p2.y - p1.y) + 
	  (p2.x - p1.x) * (p2.x - p1.x));
}

point pointOnSegment(const segment s, const double distance) 
{
  double segmentLength = dist(s.start, s.end);
  double cosAngle = (s.end.x - s.start.x)/segmentLength;
  double sinAngle = (s.end.y - s.start.y)/segmentLength;
  
  point result;
  result.x = s.start.x + cosAngle * distance;
  result.y = s.start.y + sinAngle * distance;
  return result;
  
}

boolean segmentEqual(const segment s1, const segment s2) 
{
  
  return (pointEqual(s1.start, s2.start) &&
	  pointEqual(s1.end, s2.end));
}

boolean pointEqual(const point p1, const point p2) 
{
  return sorta_eq(p1.x, p2.x) && sorta_eq(p1.y, p2.y);
}



boolean sorta_eq(const double d1, const double d2)
{
  return fabs(d1 - d2) < threshold;
}

boolean isVertical(const segment s) 
{
  return (sorta_eq(s.start.x, s.end.x) && 
	  !sorta_eq(s.start.y, s.end.y));
}

boolean isDegenerate(const segment s) 
{
  return pointEqual(s.start, s.end);
}

boolean between(const double bound1, const double bound2, const double d)
{

  return (((bound1 <= d || sorta_eq(bound1, d)) && 
	   (d <= bound2 || sorta_eq(bound2, d))) || 
	   ((bound2 <= d || sorta_eq(bound2, d)) && 
	    (d <= bound1 || sorta_eq(bound1, d))));

    }

double slope(const segment s)
{
  return (s.end.y - s.start.y) / (s.end.x - s.start.x); // POSSIBLE DIVIDE BY ZERO
}


boolean isOnSegment(const segment s, const point p)
{
  if (isDegenerate(s)) {
    return pointEqual(s.start, p);
  } else if (isVertical(s)) {
    if (sorta_eq(p.x, s.start.x) && between(s.start.y, s.end.y, p.y)) {
      return TRUE;
    } else {
      return FALSE;
    }
  } else {
    double m = slope(s);
    double b = s.start.y - s.start.x * m;
    if (!sorta_eq(p.x*m + b, p.y)) {
      return FALSE;
    } 
    return between(s.start.x, s.end.x, p.x);
  }
}

point lineEquation(segment s) {
  if (isVertical(s)) {
      printf("cmath2d vertical segment in slope.\n");
  }
  point r;
  r.x = (s.end.y - s.start.y) / (s.end.x - s.start.x);
  r.y = s.start.y - s.start.x * r.x;
  return r;
}


point closestPointOnLine(const line l, const point p) // DANGER
{
  double bestSquareDist = -1;
  assert(l.length>0);
  point bestPoint = l.points[0];
  segment s;
  int i;

  for (i = 0; i < l.length - 1; i++) {
    const point p1 = l.points[i];
    const point p2 = l.points[i+1];
    s.start = p1;
    s.end = p2;
    point tmpPoint = closestPointOnSegment(s, p);
    double squareDistToSegment = dist(tmpPoint, p);
    if (bestSquareDist == -1 || squareDistToSegment < bestSquareDist) {
      bestSquareDist = squareDistToSegment;
      bestPoint = tmpPoint;
    }
  }
  return bestPoint;
}

point closestPointOnPolygon(const line polygon, const point p) // DANGER
{
  double bestSquareDist = -1;
  assert(polygon.length>0);
  point bestPoint = polygon.points[0];
  segment s;
  int i;

  for (i = 0; i < polygon.length; i++) {
    int j = (i + 1) % polygon.length;
    const point p1 = polygon.points[i];
    const point p2 = polygon.points[j];
    s.start = p1;
    s.end = p2;
    point tmpPoint = closestPointOnSegment(s, p);
    double squareDistToSegment = dist(tmpPoint, p);
    if (bestSquareDist == -1 || squareDistToSegment < bestSquareDist) {
      bestSquareDist = squareDistToSegment;
      bestPoint = tmpPoint;
    }
  }
  return bestPoint;
}


point closestPointOnSegment(const segment s, const point p)
{
  point candidate = closestPointOnSegmentLine(s, p);

  //  if (between(s.start.x, s.end.x, candidate.x)) {
  if (isOnSegment(s, candidate)) {
    return candidate;
  } else {
    double d1 = squareDist(s.start, p);
    double d2 = squareDist(s.end, p);
    if (d1 > d2) {
      return s.end;
    } else {
      return s.start;
    }
  }
}

point closestPointOnSegmentLine(const segment s, const point p)
{
  if (isDegenerate(s)) {
    return s.start;
  }
  double x1, y1, x2, y2;
  if (s.start.x < s.end.x) {
    x1 = s.start.x;
    y1 = s.start.y;
    x2 = s.end.x;
    y2 = s.end.y;
  } else {
    x2 = s.start.x;
    y2 = s.start.y;
    x1 = s.end.x;
    y1 = s.end.y;
  }
  double u = (((p.x - x1) * (x2 - x1) + (p.y - y1) * (y2 - y1)) / 
	      squareDist(s.start, s.end));
  point ret;
  ret.x = x1 + u * (x2 - x1);
  ret.y = y1 + u * (y2 - y1);
  return ret;
}


void squareDistances(const line l1, const line l2, double* out, const int dim)  // DANGER
{
  assert(l1.length == l2.length);
  assert(l1.length == dim);

  int i;

  for (i = 0; i < l1.length; i++) {
    out[i] = squareDist(l1.points[i], l2.points[i]);
  }

}

double length(line l)  // DANGER
{
  int i;
  double d = 0;
  for (i = 0; i < l.length - 1; i++) {
    d += dist(l.points[i], l.points[i+1]);
  }
  return d;
}

void printLine(line l) {
  int i;
  printf("[");
  for (i = 0; i < l.length; i++) {
    printf("(%f, %f),", l.points[i].x, l.points[i].y);
  }
  printf("]\n");
}

line stepAlongLine(line l, double stepSize)  // DANGER
{
  int i;
  double lineLength = length(l);
  line out;
  //assert(stepSize>0);
  //assert(lineLength>0);
  if (lineLength <= 0 || sorta_eq(stepSize, 0) || l.length <= 1) {
    out = l;
    out.points = (point *) malloc(sizeof(point) * l.length);
    for (i = 0; i < l.length; i++) {
      out.points[i] = l.points[i];
    }
    return out;
  }
  int maxOutLength = (lineLength / stepSize) + 1;
  assert(maxOutLength >= 1);
  out.length = 0;
  out.points = (point *) malloc(sizeof(point) * (maxOutLength+1));
  double distAlongStep = 0.0;
  out.points[out.length++] = l.points[0];


  point yieldP;
  for (i = 0; i < l.length - 1; i++) {
    point p1 = l.points[i];
    point p2 = l.points[i+1];
    point startP = p1;
    while (1) {
      double newDistAlongStep = distAlongStep + dist(startP, p2);
      if (newDistAlongStep >= stepSize) {
	segment s;
	s.start = startP;
	s.end = p2;
	yieldP = pointOnSegment(s, stepSize - distAlongStep);
	assert(out.length <= maxOutLength);
	out.points[out.length++] = yieldP;
	startP = yieldP;
	distAlongStep = 0;
      } else {
	distAlongStep = newDistAlongStep;
	break;
      }
    }
  }
  return out;
}



pose interpolate(double t1, pose p1, double t2, pose p2, double offset) {
  segment s;
  s.start.x = p1.x;
  s.start.y = p1.y;
  s.end.x = p2.x;
  s.end.y = p2.y;
  pose r;



  double fraction = (offset -t1) / (t2 - t1);
  r.theta = p1.theta + (p2.theta - p1.theta) * fraction;

  if (isDegenerate(s)) {
    return p1;
  }
  else if (isVertical(s)) {
    r.x = p1.x;
    r.y = p1.y + fraction * (p2.y - p1.y);
    return r;
  }
  else {
    point mb = lineEquation(s);
    r.x = p1.x + fraction *  (p2.x - p1.x);
    r.y = mb.x * r.x + mb.y;
    return r;
  }

  
}


boolean isInteriorPoint(line polygon, point p) {
  boolean c = FALSE;
  int i;
  for (i = 0; i < polygon.length; i++) {
    point p1 = polygon.points[i];
    int j = (i + 1) % polygon.length;
    point p2 = polygon.points[j];
    
    if (p.x == p1.x && p.y == p1.y) {
      return TRUE;
    }
    if ((((p1.y <= p.y) && (p.y < p2.y)) ||
         ((p2.y <= p.y) && (p.y < p1.y))) &&
        (p.x < ((p2.x - p1.x) * (p.y - p1.y)) / (p2.y - p1.y) + p1.x)) {
      c = !c;
    }
  }
  return c;
}


line interiorPoints(line polygon, line points) {
  line out;
  out.points = (point *) malloc(sizeof(point) * points.length);  
  int i = 0;
  int pointIdx = 0;
  for (i = 0; i < points.length; i++) {
    if (isInteriorPoint(polygon, points.points[i])) {
      out.points[pointIdx] = points.points[i];
      pointIdx++;
    }
  }
  out.length = pointIdx;
  return out;
}
