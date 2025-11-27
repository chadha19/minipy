#ifndef MINIPY_BYTECODE_LOADER_H
#define MINIPY_BYTECODE_LOADER_H

#include "vm.h"
#include <string>

namespace minipy {

struct BytecodeFile {
    std::vector<Instruction> code;
    std::vector<Value> consts;
    std::vector<std::string> names;
};

BytecodeFile load_bytecode(const std::string& filename);

} // namespace minipy

#endif // MINIPY_BYTECODE_LOADER_H

