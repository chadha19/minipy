"""Tests for the virtual machine."""

import unittest
from bytecode import Instruction, LOAD_CONST, LOAD_NAME, STORE_NAME, ADD, SUB, MUL, DIV
from bytecode import CMP_LT, CMP_GT, CMP_EQ, JUMP, JUMP_IF_FALSE, PRINT, HALT
from vm import VM


class TestVM(unittest.TestCase):
    """Test cases for virtual machine."""
    
    def test_load_const(self):
        """Test loading constants."""
        code = [
            Instruction(LOAD_CONST, 0),
            Instruction(HALT)
        ]
        consts = [42]
        names = []
        vm = VM(code, consts, names)
        vm.run()
        self.assertEqual(vm.stack, [42])
    
    def test_store_and_load_name(self):
        """Test storing and loading variables."""
        code = [
            Instruction(LOAD_CONST, 0),
            Instruction(STORE_NAME, 0),
            Instruction(LOAD_NAME, 0),
            Instruction(HALT)
        ]
        consts = [10]
        names = ["x"]
        vm = VM(code, consts, names)
        vm.run()
        self.assertEqual(vm.globals["x"], 10)
        self.assertEqual(vm.stack, [10])
    
    def test_arithmetic(self):
        """Test arithmetic operations."""
        code = [
            Instruction(LOAD_CONST, 0),  # 5
            Instruction(LOAD_CONST, 1),  # 3
            Instruction(ADD),
            Instruction(HALT)
        ]
        consts = [5, 3]
        names = []
        vm = VM(code, consts, names)
        vm.run()
        self.assertEqual(vm.stack, [8])
    
    def test_subtraction(self):
        """Test subtraction."""
        code = [
            Instruction(LOAD_CONST, 0),  # 10
            Instruction(LOAD_CONST, 1),  # 3
            Instruction(SUB),
            Instruction(HALT)
        ]
        consts = [10, 3]
        names = []
        vm = VM(code, consts, names)
        vm.run()
        self.assertEqual(vm.stack, [7])
    
    def test_multiplication(self):
        """Test multiplication."""
        code = [
            Instruction(LOAD_CONST, 0),  # 4
            Instruction(LOAD_CONST, 1),  # 5
            Instruction(MUL),
            Instruction(HALT)
        ]
        consts = [4, 5]
        names = []
        vm = VM(code, consts, names)
        vm.run()
        self.assertEqual(vm.stack, [20])
    
    def test_division(self):
        """Test division."""
        code = [
            Instruction(LOAD_CONST, 0),  # 15
            Instruction(LOAD_CONST, 1),  # 3
            Instruction(DIV),
            Instruction(HALT)
        ]
        consts = [15, 3]
        names = []
        vm = VM(code, consts, names)
        vm.run()
        self.assertEqual(vm.stack, [5])
    
    def test_comparison_lt(self):
        """Test less-than comparison."""
        code = [
            Instruction(LOAD_CONST, 0),  # 3
            Instruction(LOAD_CONST, 1),  # 5
            Instruction(CMP_LT),
            Instruction(HALT)
        ]
        consts = [3, 5]
        names = []
        vm = VM(code, consts, names)
        vm.run()
        self.assertEqual(vm.stack, [1])  # True
    
    def test_comparison_gt(self):
        """Test greater-than comparison."""
        code = [
            Instruction(LOAD_CONST, 0),  # 5
            Instruction(LOAD_CONST, 1),  # 3
            Instruction(CMP_GT),
            Instruction(HALT)
        ]
        consts = [5, 3]
        names = []
        vm = VM(code, consts, names)
        vm.run()
        self.assertEqual(vm.stack, [1])  # True
    
    def test_comparison_eq(self):
        """Test equality comparison."""
        code = [
            Instruction(LOAD_CONST, 0),  # 5
            Instruction(LOAD_CONST, 1),  # 5
            Instruction(CMP_EQ),
            Instruction(HALT)
        ]
        consts = [5, 5]
        names = []
        vm = VM(code, consts, names)
        vm.run()
        self.assertEqual(vm.stack, [1])  # True
    
    def test_jump(self):
        """Test unconditional jump."""
        code = [
            Instruction(LOAD_CONST, 0),
            Instruction(JUMP, 3),  # Skip next instruction
            Instruction(LOAD_CONST, 1),
            Instruction(HALT)
        ]
        consts = [10, 20]
        names = []
        vm = VM(code, consts, names)
        vm.run()
        self.assertEqual(vm.stack, [10])  # Should not have 20
    
    def test_jump_if_false(self):
        """Test conditional jump."""
        code = [
            Instruction(LOAD_CONST, 0),  # 0 (False)
            Instruction(JUMP_IF_FALSE, 4),  # Jump to HALT
            Instruction(LOAD_CONST, 1),  # Should be skipped
            Instruction(LOAD_CONST, 2),
            Instruction(HALT)
        ]
        consts = [0, 10, 20]
        names = []
        vm = VM(code, consts, names)
        vm.run()
        self.assertEqual(vm.stack, [])  # Should jump before loading anything else


if __name__ == "__main__":
    unittest.main()

