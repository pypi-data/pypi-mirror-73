#include <pybind11/pybind11.h>
#include "pybind11_json/pybind11_json.hpp"
#include <pybind11/stl.h>
#include <pybind11/iostream.h>
#include <string>
#include <vector>

#include <conceptual/core.hpp>

PYBIND11_MODULE(conceptual, m) {
    m.doc() = "Conceptual space bindings";

    //    m.def("bar", &conceptual::core::bar, "does some stuff.");
};
