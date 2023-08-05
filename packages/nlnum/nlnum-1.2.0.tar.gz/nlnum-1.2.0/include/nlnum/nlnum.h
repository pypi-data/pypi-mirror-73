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

typedef std::map<Partition, int64_t> Coefficients;

// Converts a C++ vector into a C vector defined by lrcalc.
vector* to_vector(const Partition&);

// Converts a C vector defined by lrcalc into a C++ vector.
bool to_cppvec(const vector*, Partition*);

// Converts a C hashtable defined by lrcalc to a C++ map
// (of resulting coefficients).
bool to_map(hashtab*, Coefficients*);

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

// Computes the skew-Schur polynomial of the given skew-shape.
Coefficients skew(const Partition& outer, const Partition& inner);

// Computes the skew-Schur polynomial of the given skew-shape.
// If max_rows is positive, then only partitions with at most
// `max_rows` number of rows are included in the result.
Coefficients skew(const Partition& outer, const Partition& inner,
                  const size_t max_rows);

}  // namespace nlnum

#endif  // NLNUM_NLNUM_H_
