// Copyright (c) 2020 [Your Name]. All rights reserved.

#define CATCH_CONFIG_MAIN

#include <exception>
#include <iostream>
#include <numeric>

#include <catch2/catch.hpp>

extern "C" {
#include <lrcalc/vector.h>
}
#include <nlnum/nlnum.h>
#include <nlnum/partitions_in.h>

TEST_CASE("Create a vector from an iterable", "[iterable_to_vector]") {
  const std::vector<int> vec = {1, 2, 3, 4};
  vector* v = nlnum::to_vector(vec);

  REQUIRE(v->length == 4);
  for (size_t i = 0; i < v->length; i++) {
    REQUIRE(v->array[i] == vec[i]);
  }

  v_free(v);
}

TEST_CASE("Littlewood-Richardson coefficient", "[lrcoef]") {
  SECTION("Test 1") {
    const int64_t lr = nlnum::lrcoef({3, 2, 1}, {2, 1}, {2, 1});
    REQUIRE(lr == 2);
  }
  SECTION("Test 2") {
    const int64_t lr = nlnum::lrcoef({3, 3}, {2, 1}, {2, 1});
    REQUIRE(lr == 1);
  }
  SECTION("Test 3") {
    const int64_t lr = nlnum::lrcoef({2, 1, 1, 1, 1}, {2, 1}, {2, 1});
    REQUIRE(lr == 0);
  }
}

TEST_CASE("Newell-Littlewood number Slow", "[nlcoef_slow]") {
  SECTION("Test 1") {
    const int64_t nl = nlnum::nlcoef_slow({2, 1}, {2, 1}, {4, 2});
    REQUIRE(nl == 1);
  }
  SECTION("Test 2") {
    const int64_t nl = nlnum::nlcoef_slow({8, 4, 4}, {8, 4, 4}, {8, 4, 4});
    REQUIRE(nl == 141);
  }
}

TEST_CASE("Newell-Littlewood number", "[nlcoef]") {
  SECTION("Test 0") {
    const int64_t nl = nlnum::nlcoef({1}, {1}, {1});
    // The total sum is odd.
    REQUIRE(nl == 0);
  }
  SECTION("Test 1") {
    const int64_t nl = nlnum::nlcoef({2, 1}, {2, 1}, {4, 2});
    REQUIRE(nl == 1);
  }
  SECTION("Test 1a") {
    const int64_t nl = nlnum::nlcoef({1, 1}, {1}, {1});
    REQUIRE(nl == 1);
  }
  SECTION("Test 2") {
    const int64_t nl = nlnum::nlcoef({8, 4, 4}, {8, 4, 4}, {8, 4, 4});
    REQUIRE(nl == 141);
  }
  SECTION("Test 3") {
    const int64_t nl = nlnum::nlcoef({12, 6, 6}, {12, 6, 6}, {12, 6, 6});
    REQUIRE(nl == 676);
  }
  SECTION("Test 4") {
    const int64_t nl = nlnum::nlcoef({24, 12, 12}, {24, 12, 12}, {24, 12, 12});
    REQUIRE(nl == 16366);
  }
  SECTION("Test 5") {
    const int64_t nl = nlnum::nlcoef({96, 48, 48}, {60, 50, 50}, {50, 40, 40});
    REQUIRE(nl == 47146);
  }
  SECTION("Test 6") {
    const int64_t nl = nlnum::nlcoef({120, 70, 70}, {80, 50, 50}, {80, 40, 40});
    REQUIRE(nl == 972380);
  }
  SECTION("Test 7") {
    const int64_t nl = nlnum::nlcoef({120, 70, 70}, {2, 1, 1}, {3, 2, 1});
    // Sizes don't satisfy the triangle inequality.
    REQUIRE(nl == 0);
  }
}

TEST_CASE("Partitions In", "[partitions-in]") {
  SECTION("Normal") {
    const nlnum::Partition limit = {24, 12, 12};
    const size_t size = 24;
    nlnum::PartitionsIn pi(limit, size);

    int sum = 0;
    for (const nlnum::Partition& partition : pi) {
      REQUIRE(std::accumulate(partition.begin(), partition.end(), 0) == size);
      REQUIRE(partition.size() <= limit.size());
      for (size_t i = 0; i < partition.size(); ++i) {
        REQUIRE(partition[i] <= limit[i]);
      }
      ++sum;
    }
    REQUIRE(sum == 61);
  }
  SECTION("Zero") {
    const nlnum::Partition& zero = {0};
    const nlnum::PartitionsIn pi({2}, 0);

    size_t sum = 0;
    // Iterator loop written explicitly.
    for (auto it = pi.begin(); it != pi.end(); ++it) {
      const nlnum::Partition& partition = *it;
      REQUIRE(partition == zero);
      ++sum;
    }
    REQUIRE(sum == 1);
  }
}

TEST_CASE("Test bad partitions.", "[bad-partitions]") {
  SECTION("Test 0") {
    REQUIRE_NOTHROW(nlnum::ValidatePartitions(
        {{}, {0}, {1, 0}, {1, 1}, {0, 0}, {3, 2, 1}}));
  }
  SECTION("Test 0a") {
    REQUIRE_THROWS_AS(nlnum::ValidatePartitions({{-1}}), std::invalid_argument);
  }
  SECTION("Test 1") {
    REQUIRE_THROWS_AS(nlnum::nlcoef({2, 1, 2}, {2, 1}, {4, 2}),
                      std::invalid_argument);
  }
  SECTION("Test 2") {
    REQUIRE_THROWS_AS(nlnum::nlcoef({2, 1, -1}, {2, 1}, {4, 2}),
                      std::invalid_argument);
  }
}

TEST_CASE("Test positivity.", "[bad-partitions]") {
  SECTION("Test 1") {
    const int64_t positive = nlnum::nlcoef({1}, {1}, {1}, true);
    REQUIRE(positive == 0);
  }
  SECTION("Test 2") {
    const int64_t positive = nlnum::nlcoef({120, 70, 70}, {80, 50, 50}, {80, 40, 40}, true);
    REQUIRE(positive == 1);
  }
  SECTION("Test 3") {
    const int64_t nl = nlnum::nlcoef({8, 4, 4}, {8, 4, 4}, {8, 4, 4}, false);
    REQUIRE(nl == 141);
  }
  SECTION("Test 4") {
    const int64_t positive = nlnum::nlcoef({2}, {2}, {2}, true);
    REQUIRE(positive == 1);
  }
}
