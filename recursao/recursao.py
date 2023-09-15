def sum(n):
    if n == 1:
        return n
    else:
        return n + sum(n - 1)
    
print(sum(5))

# from bytecode import Bytecode, dump_bytecode
# fn_print_sequence = Bytecode.from_code(print_sequence.__code__)
# dump_bytecode(fn_print_sequence)