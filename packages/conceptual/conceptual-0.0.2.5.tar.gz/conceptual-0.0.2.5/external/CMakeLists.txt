cmake_minimum_required(VERSION 3.14.1)
project(conceptual-deps LANGUAGES CXX)

## Dependencies
include(FetchContent)

## Google Test
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG        release-1.8.0
)

## JSON
FetchContent_Declare(
  json
  GIT_REPOSITORY https://github.com/nlohmann/json.git
  GIT_TAG        v3.8.0
)

## Pybind11
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v2.5.0
)

## Pybind11_Json
FetchContent_Declare(
  pybind11_json
  GIT_REPOSITORY https://github.com/pybind/pybind11_json.git
  GIT_TAG        0.2.6
)

set(JSON_BuildTests OFF CACHE INTERNAL "")
FetchContent_MakeAvailable(json)
FetchContent_MakeAvailable(pybind11)
FetchContent_MakeAvailable(pybind11_json)

if(PACKAGE_TESTS)
  FetchContent_MakeAvailable(googletest)
endif()
