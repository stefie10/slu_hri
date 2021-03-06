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


#ifdef _MSC_VER
  #pragma warning (disable : 4290)
#endif

#include <stdio.h>
#include "statexceptions.hpp"

#ifndef _MSC_VER
statexception::statexception(const string &desc)
  : err_desc(desc)
  {}

const char* statexception::what () const throw()
  { return err_desc.c_str(); };

statexception::~statexception() throw()
{}
#endif



exception StatException(const string &anerr)
{ return statexception(anerr.c_str()); }

exception StatException(const string &anerr, const string &s)
{ char buf[255];
  sprintf(buf, anerr.c_str(), s.c_str());
  return statexception(buf);
}

exception StatException(const string &anerr, const string &s1, const string &s2)
{ char buf[255];
  sprintf(buf, anerr.c_str(), s1.c_str(), s2.c_str());
  return statexception(buf);
}

exception StatException(const string &anerr, const string &s1, const string &s2, const string &s3)
{ char buf[255];
  sprintf(buf, anerr.c_str(), s1.c_str(), s2.c_str(), s3.c_str());
  return statexception(buf);
}

exception StatException(const string &anerr, const long i)
{ char buf[255];
  sprintf(buf, anerr.c_str(), i);
  return statexception(buf);
}

