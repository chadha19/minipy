cmake_minimum_required(VERSION 3.10)
project(minipy_vm)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(minipy_vm
    main.cpp
    vm.cpp
    bytecode_loader.cpp
)

target_include_directories(minipy_vm PRIVATE .)

