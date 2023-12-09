# Copyright: (C) 2017 iCub Facility - Istituto Italiano di Tecnologia
# Authors: Giulia Pasquale
# CopyPolicy: Released under the terms of the GNU GPL v2.0.
cmake_minimum_required(VERSION 3.5)

project(classify_image_list_vvv)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR})

option(CPU_ONLY "Use CPU only for Caffe" ON)
option(USE_CUDNN "Use CuDNN library for Caffe" OFF)

find_package(OpenCV REQUIRED)
find_package(Caffe REQUIRED)

set(Boost_USE_STATIC_LIBS OFF) 
set(Boost_USE_MULTITHREADED ON)  
set(Boost_USE_STATIC_RUNTIME OFF) 
find_package(Boost COMPONENTS filesystem)

include_directories(${Boost_INCLUDE_DIRS}) 
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${Caffe_INCLUDE_DIRS})

include_directories(${PROJECT_SOURCE_DIR})

set ( CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g" )

add_executable(${PROJECT_NAME} ${PROJECT_NAME}.cpp)
target_compile_definitions(${PROJECT_NAME} PRIVATE ${Caffe_DEFINITIONS})

target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})
target_link_libraries(${PROJECT_NAME} ${Caffe_LIBRARIES})
target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})
