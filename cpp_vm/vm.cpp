#include "vm.h"
#include <stdexcept>
#include <iostream>
#include <cstring>

namespace minipy {

VM::VM(const std::vector<Instruction>& code,
       const std::vector<Value>& consts,
       const std::vector<std::string>& names)
    : code_(code), consts_(consts), names_(names), ip_(0) {
}

void VM::push(Value value) {
    if (stack_.size() >= MAX_STACK_SIZE) {
        throw std::runtime_error("Stack overflow");
    }
    stack_.push_back(value);
}

Value VM::pop() {
    if (stack_.empty()) {
        throw std::runtime_error("Stack underflow");
    }
    Value value = stack_.back();
    stack_.pop_back();
    return value;
}

Value VM::peek() const {
    if (stack_.empty()) {
        throw std::runtime_error("Stack underflow");
    }
    return stack_.back();
}

void VM::run() {
    ip_ = 0;
    
    while (ip_ < code_.size()) {
        const Instruction& instr = code_[ip_];
        const std::string& opcode = instr.opcode;
        int64_t arg = instr.arg;
        
        if (opcode == "LOAD_CONST") {
            push(consts_[arg]);
            ip_++;
        }
        else if (opcode == "LOAD_NAME") {
            const std::string& name = names_[arg];
            if (globals_.find(name) == globals_.end()) {
                throw std::runtime_error("Undefined variable: " + name);
            }
            push(globals_[name]);
            ip_++;
        }
        else if (opcode == "STORE_NAME") {
            Value value = pop();
            const std::string& name = names_[arg];
            globals_[name] = value;
            ip_++;
        }
        else if (opcode == "ADD") {
            Value b = pop();
            Value a = pop();
            push(a + b);
            ip_++;
        }
        else if (opcode == "SUB") {
            Value b = pop();
            Value a = pop();
            push(a - b);
            ip_++;
        }
        else if (opcode == "MUL") {
            Value b = pop();
            Value a = pop();
            push(a * b);
            ip_++;
        }
        else if (opcode == "DIV") {
            Value b = pop();
            Value a = pop();
            if (b == 0) {
                throw std::runtime_error("Division by zero");
            }
            push(a / b);
            ip_++;
        }
        else if (opcode == "CMP_LT") {
            Value b = pop();
            Value a = pop();
            push(a < b ? 1 : 0);
            ip_++;
        }
        else if (opcode == "CMP_GT") {
            Value b = pop();
            Value a = pop();
            push(a > b ? 1 : 0);
            ip_++;
        }
        else if (opcode == "CMP_LE") {
            Value b = pop();
            Value a = pop();
            push(a <= b ? 1 : 0);
            ip_++;
        }
        else if (opcode == "CMP_GE") {
            Value b = pop();
            Value a = pop();
            push(a >= b ? 1 : 0);
            ip_++;
        }
        else if (opcode == "CMP_EQ") {
            Value b = pop();
            Value a = pop();
            push(a == b ? 1 : 0);
            ip_++;
        }
        else if (opcode == "CMP_NEQ") {
            Value b = pop();
            Value a = pop();
            push(a != b ? 1 : 0);
            ip_++;
        }
        else if (opcode == "JUMP") {
            if (arg < 0 || static_cast<size_t>(arg) >= code_.size()) {
                throw std::runtime_error("Invalid jump target");
            }
            ip_ = arg;
        }
        else if (opcode == "JUMP_IF_FALSE") {
            Value value = pop();
            if (value == 0) {
                if (arg < 0 || static_cast<size_t>(arg) >= code_.size()) {
                    throw std::runtime_error("Invalid jump target");
                }
                ip_ = arg;
            } else {
                ip_++;
            }
        }
        else if (opcode == "JUMP_IF_TRUE") {
            Value value = pop();
            if (value != 0) {
                if (arg < 0 || static_cast<size_t>(arg) >= code_.size()) {
                    throw std::runtime_error("Invalid jump target");
                }
                ip_ = arg;
            } else {
                ip_++;
            }
        }
        else if (opcode == "POP") {
            pop();
            ip_++;
        }
        else if (opcode == "PRINT") {
            Value value = pop();
            std::cout << value << std::endl;
            ip_++;
        }
        else if (opcode == "HALT") {
            break;
        }
        else {
            throw std::runtime_error("Unknown opcode: " + opcode);
        }
    }
}

} // namespace minipy

