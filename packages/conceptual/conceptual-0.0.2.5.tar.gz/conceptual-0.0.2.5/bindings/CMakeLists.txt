cmake_minimum_required(VERSION 3.10.1)
project(conceptual::bindings LANGUAGES CXX)

##find_package(OpenCV REQUIRED)
##find_package(Python3 COMPONENTS Interpreter Development)

pybind11_add_module(conceptual SHARED
  conceptual.cpp)
##  pybind11_opencv.hpp)

target_compile_features(conceptual PRIVATE
  cxx_std_17)

target_link_libraries(conceptual
        PRIVATE
        pybind11_json
        nlohmann_json::nlohmann_json
        conceptual::core)

##target_link_libraries(conceptual
##  PRIVATE
##  ${OpenCV_LIBS}
##  pybind11_json
##  conceptual::core)

#cp conceptual.cpython-36m-x86_64-linux-gnu.so ~/.pyenv/versions/3.6.9/lib/python3.6/site-packages
