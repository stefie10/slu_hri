/*
    This file is part of Orange.

    Orange is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Orange is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Orange; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

    Authors: Janez Demsar, Blaz Zupan, 1996--2002
    Contact: janez.demsar@fri.uni-lj.si
*/

#include "strings.hpp"

string trim(const string &s)
{ 
  string::const_iterator si(s.begin()), se(s.end());
  
  while ((si!=se) && (*si==' '))
    si++;
  while ((si!=se) && (se[-1]==' '))
    se--;
  
  return string(si, se);
}


void trim(char *s)
{ 
  char *si = s, *se = s + strlen(s);

  while (*si && (*si==' '))
    si++;
  while ((si!=se) && (se[-1]==' '))
    se--;

  while(si!=se)
    *(s++) = *(si++);
  *s = 0;
}


void split(const string &s, TSplits &atoms)
{
  atoms.clear();

  for(string::const_iterator si(s.begin()), se(s.end()), sii; si != se;) {
    while ((si != se) && (*si <= ' '))
      si++;
    if (si == se)
      break;
    sii = si;
    while ((si != se) && (*si > ' '))
      si++;
    atoms.push_back(make_pair(sii, si));
  }
}