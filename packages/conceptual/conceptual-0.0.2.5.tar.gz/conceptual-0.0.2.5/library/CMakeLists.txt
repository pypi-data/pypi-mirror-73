cmake_minimum_required(VERSION 3.10.1)
project(conceptual-core LANGUAGES CXX)

find_package(OpenCV REQUIRED)
add_library(${PROJECT_NAME} SHARED
  space.cpp
  graph.cpp)

target_compile_features(${PROJECT_NAME} PRIVATE
  cxx_std_17)

target_link_libraries(${PROJECT_NAME}
  ${OpenCV_LIBS})


target_include_directories(${PROJECT_NAME} PUBLIC
  ${OpenCV_INCLUDE_DIRS}
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include/>
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

add_library(conceptual::core ALIAS ${PROJECT_NAME})
