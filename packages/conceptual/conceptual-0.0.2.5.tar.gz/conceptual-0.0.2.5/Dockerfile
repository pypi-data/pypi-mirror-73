FROM danielkoudouna/vision-environment:latest

WORKDIR /conceptual/build

## Build dependencies
COPY external /conceptual/external
RUN cmake ../external
RUN rm -rf CMakeCache.txt CMakeFiles Makefile cmake_install.cmake

## Build application
COPY library /conceptual/library
COPY bindings /conceptual/bindings
COPY tests /conceptual/tests
COPY CMakeLists.txt /conceptual
RUN cmake ..
RUN make

COPY . /conceptual

WORKDIR /conceptual
