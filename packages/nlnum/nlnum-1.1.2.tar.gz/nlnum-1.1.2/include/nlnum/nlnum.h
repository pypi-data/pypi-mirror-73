// Copyright (c) 2020 ICLUE @ UIUC. All rights reserved.

#ifndef NLNUM_NLNUM_H_
#define NLNUM_NLNUM_H_

#include <cstdint>
#include <map>
#include <vector>

#include <nlnum/partitions_in.h>

extern "C" {
#include <lrcalc/hashtab.h>
#include <lrcalc/vector.h>
}

namespace nlnum {
// Converts a C++ vector into a C vector defined by lrcalc.
vector* to_vector(const Partition&);

// Converts a C vector defined by lrcalc into a C++ vector.
bool to_cppvec(const vector*, Partition*);

// Converts a C hashtable defined by lrcalc to a C++ map.
bool to_map(hashtab*, std::map<Partition, int>*);

// Computes the Littlewood-Richardson coefficient.
int64_t lrcoef(const Partition& outer, const Partition& inner1,
               const Partition& inner2);

// Computes the Newell-Littlewood coefficient using Proposition 2.3.
int64_t nlcoef_slow(const Partition& mu, const Partition& nu,
                    const Partition& lambda);

// Computes the Newell-Littlewood coefficient using the definition 1.1.
int64_t nlcoef(const Partition& mu, const Partition& nu,
               const Partition& lambda);

// If check_positivity is true, then the output will either be 0 or 1,
// depending if the NL number is positive or not. This will save time
// if only positivity is needed.
int64_t nlcoef(const Partition& mu, const Partition& nu,
               const Partition& lambda, const bool check_positivity);
}  // namespace nlnum

#endif  // NLNUM_NLNUM_H_
