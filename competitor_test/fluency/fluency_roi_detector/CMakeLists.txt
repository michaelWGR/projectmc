cmake_minimum_required(VERSION 2.8)
project( fluency_roi_detector )
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -DDEBUG")

find_package( OpenCV REQUIRED )

add_executable( fluency_roi_detector cpp/main.cpp)
target_link_libraries( fluency_roi_detector ${OpenCV_LIBS} )
