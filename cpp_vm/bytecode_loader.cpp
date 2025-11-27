#include "bytecode_loader.h"
#include <fstream>
#include <sstream>
#include <stdexcept>

namespace minipy {

BytecodeFile load_bytecode(const std::string& filename) {
    BytecodeFile bf;
    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open bytecode file: " + filename);
    }
    
    // Simple text-based format: opcode,arg per line
    // Format: CODE_SIZE
    // Then: opcode arg (one per line)
    // Then: CONSTS_SIZE
    // Then: value (one per line)
    // Then: NAMES_SIZE
    // Then: name (one per line)
    
    size_t code_size;
    file >> code_size;
    for (size_t i = 0; i < code_size; i++) {
        std::string opcode;
        int64_t arg = 0;
        file >> opcode;
        if (opcode != "HALT" && opcode != "ADD" && opcode != "SUB" && 
            opcode != "MUL" && opcode != "DIV" && opcode != "PRINT" &&
            opcode != "POP") {
            file >> arg;
        }
        bf.code.emplace_back(opcode, arg);
    }
    
    size_t consts_size;
    file >> consts_size;
    for (size_t i = 0; i < consts_size; i++) {
        Value value;
        file >> value;
        bf.consts.push_back(value);
    }
    
    size_t names_size;
    file >> names_size;
    file.ignore(); // Skip newline
    for (size_t i = 0; i < names_size; i++) {
        std::string name;
        std::getline(file, name);
        bf.names.push_back(name);
    }
    
    return bf;
}

} // namespace minipy

