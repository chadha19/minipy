#include "vm.h"
#include "bytecode_loader.h"
#include <iostream>
#include <stdexcept>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <bytecode_file>" << std::endl;
        return 1;
    }
    
    try {
        minipy::BytecodeFile bf = minipy::load_bytecode(argv[1]);
        minipy::VM vm(bf.code, bf.consts, bf.names);
        vm.run();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}

