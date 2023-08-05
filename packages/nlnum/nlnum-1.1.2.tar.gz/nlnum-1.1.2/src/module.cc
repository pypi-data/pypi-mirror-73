// Copyright 2020 ICLUE @ UIUC. All rights reserved.

#include <cstdint>
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <nlnum/nlnum.h>

namespace py = pybind11;

PYBIND11_MODULE(nlnum, m) {
  m.doc() = R"pbdoc(
    Pybind11 example plugin
    -----------------------
    .. currentmodule:: cmake_example
    .. autosummary::
       :toctree: _generate
       lrcoef
       nlcoef
       nlcoef_slow
    )pbdoc";

  m.def("nlcoef_slow", &nlnum::nlcoef_slow, R"pbdoc(
    Compute a single Newell-Littlewood coefficient using Proposition 2.3.
    INPUT:
    - ``mu`` -- a partition (weakly decreasing list of non-negative integers).
    - ``nu`` -- a partition.
    - ``lambda`` -- a partition.
    EXAMPLES::
        python: from nlnum import nlcoef_slow
        python: nlcoef_slow([2,1], [2,1], [4, 2])
        0
  )pbdoc");

  m.def(
      "nlcoef",
      py::overload_cast<
          const std::vector<int>&,
          const std::vector<int>&,
          const std::vector<int>&,
          const bool>(&nlnum::nlcoef),
        R"pbdoc(
    Compute a single Newell-Littlewood coefficient using the definition (1.1).
    INPUT:
    - ``mu`` -- a partition (weakly decreasing list of non-negative integers).
    - ``nu`` -- a partition.
    - ``lambda`` -- a partition.
    EXAMPLES::
        python: from nlnum import nlcoef
        python: nlcoef([8, 4, 4], [8, 4, 4], [8, 4, 4])
        141
        python: nlcoef([8, 4, 4], [8, 4, 4], [8, 4, 4], check_positivity=True)
        1
        python: nlcoef([2, 1], [2, 1], [4, 2])
        0
        python: nlcoef([2, 1], [2, 1], [4, 2], check_positivity=True)
        0
    NOTES::
        If you want check_positivity to be heavily optimized, the environment
        variable `OMP_CANCELLATION` needs to be set to `true` BEFORE importing
        this module.
  )pbdoc",
  py::arg("mu"), py::arg("nu"), py::arg("lambda"), py::arg("check_positivity") = false);

  m.def("lrcoef", &nlnum::lrcoef, R"pbdoc(
    Compute a single Littlewood-Richardson coefficient.
    Return the coefficient of ``outer`` in the product of the Schur
    functions indexed by ``inner1`` and ``inner2``.
    INPUT:
    - ``outer`` -- a partition (weakly decreasing list of non-negative integers).
    - ``inner1`` -- a partition.
    - ``inner2`` -- a partition.
    EXAMPLES::
        python: from nlnum import lrcoef
        python: lrcoef([3,2,1], [2,1], [2,1])
        2
        python: lrcoef([3,3], [2,1], [2,1])
        1
        python: lrcoef([2,1,1,1,1], [2,1], [2,1])
        0
  )pbdoc");

  py::class_<nlnum::PartitionsIn>(m, "PartitionsIn")
      .def(py::init<const nlnum::Partition&, const size_t>())
      // Keep this class alive while the returned iterator is alive.
      .def("__iter__", [](nlnum::PartitionsIn& p) {
        return py::make_iterator(p.begin(), p.end());
      }, py::keep_alive<0, 1>());

  #ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
  #else
  m.attr("__version__") = "dev";
  #endif
}
