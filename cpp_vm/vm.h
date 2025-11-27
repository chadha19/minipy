#ifndef MINIPY_VM_H
#define MINIPY_VM_H

#include <vector>
#include <string>
#include <unordered_map>
#include <cstdint>

namespace minipy {

// Value type - using int for simplicity (can be extended with std::variant)
using Value = int64_t;

// Instruction structure
struct Instruction {
    std::string opcode;
    int64_t arg;
    
    Instruction(const std::string& op, int64_t a = 0) : opcode(op), arg(a) {}
};

// Virtual Machine
class VM {
public:
    VM(const std::vector<Instruction>& code,
       const std::vector<Value>& consts,
       const std::vector<std::string>& names);
    
    void run();
    const std::unordered_map<std::string, Value>& getGlobals() const { return globals_; }
    
private:
    void push(Value value);
    Value pop();
    Value peek() const;
    
    std::vector<Instruction> code_;
    std::vector<Value> consts_;
    std::vector<std::string> names_;
    std::vector<Value> stack_;
    std::unordered_map<std::string, Value> globals_;
    size_t ip_;
    
    static constexpr size_t MAX_STACK_SIZE = 10000;
};

} // namespace minipy

#endif // MINIPY_VM_H

