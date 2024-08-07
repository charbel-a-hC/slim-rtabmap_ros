cmake_minimum_required(VERSION 3.5)
project(rtabmap_slim_odom)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch
   DESTINATION share/${PROJECT_NAME}
)

ament_package()
