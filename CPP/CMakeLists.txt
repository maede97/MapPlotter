cmake_minimum_required(VERSION 3.1)
project(CXX_MapPlotter_Plot)

set(CMAKE_MODULE_PATH ${CXX_MapPlotter_Plot_SOURCE_DIR})

message(${CMAKE_MODULE_PATH})
find_package(MathGL)
include_directories(${MathGL_INCLUDE_DIRS})

add_executable(main main.cpp)

target_link_libraries(main ${MathGL_LIBRARIES})