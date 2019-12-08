int_codes = []


def get_value(pos: int, mode: int) -> int:
    if mode == 1:
        return int(pos)
    else:
        return int(int_codes[pos])


def get_modes(opcode: int) -> tuple:
    code = str(opcode);
    first_mode = 0
    second_mode = 0
    third_mode = 0
    length = len(str(code))
    if length == 5:
        third_mode = code[0]
        second_mode = code[1]
        first_mode = code[2]
    elif length == 4:
        second_mode = code[0]
        first_mode = code[1]
    elif length == 3:
        first_mode = code[0]
    code = int(code) % 100

    return int(code), int(first_mode), int(second_mode), int(third_mode)


def compute(codes: list, inputs: list = []) -> list:
    global int_codes
    int_codes = codes
    input_values = inputs.copy()
    pointer = 0
    output = []

    while pointer < len(int_codes) - 1:
        code = int_codes[pointer]
        modes = get_modes(code)

        first_mode = modes[1]
        second_mode = modes[2]
        third_mode = modes[3]
        code = modes[0]

        if code == 1:
            operand1pos = int_codes[1 + pointer]
            operand2pos = int_codes[2 + pointer]
            target = int_codes[3 + pointer]
            int_codes[target] = get_value(operand1pos, first_mode) + get_value(operand2pos, second_mode)
            pointer += 4
        elif code == 2:
            operand1pos = int_codes[1 + pointer]
            operand2pos = int_codes[2 + pointer]
            target = int_codes[3 + pointer]
            int_codes[target] = get_value(operand1pos, first_mode) * get_value(operand2pos, second_mode)
            pointer += 4
        elif code == 3:
            target = int_codes[pointer + 1]
            if len(input_values) == 0:
                int_codes[target] = input("Enter value for opcode 3: ")
            else:
                int_codes[target] = input_values.pop(0)
            pointer += 2
        elif code == 4:
            target = int_codes[pointer + 1]
            print(get_value(target, first_mode))
            output.append(get_value(target, first_mode))
            pointer += 2
        elif code == 5:
            if get_value(int_codes[1 + pointer], first_mode) != 0:
                pointer = get_value(int_codes[pointer + 2], second_mode)
            else:
                pointer += 3
        elif code == 6:
            if get_value(int_codes[1 + pointer], first_mode) == 0:
                pointer = get_value(int_codes[pointer + 2], second_mode)
            else:
                pointer += 3
        elif code == 7:
            operand1pos = int_codes[1 + pointer]
            operand2pos = int_codes[2 + pointer]
            target = int_codes[3 + pointer]
            if get_value(operand1pos, first_mode) < get_value(operand2pos, second_mode):
                int_codes[target] = 1
            else:
                int_codes[target] = 0
            pointer += 4
        elif code == 8:
            operand1pos = int_codes[1 + pointer]
            operand2pos = int_codes[2 + pointer]
            target = int_codes[3 + pointer]
            if get_value(operand1pos, first_mode) == get_value(operand2pos, second_mode):
                int_codes[target] = 1
            else:
                int_codes[target] = 0
            pointer += 4

        elif code == 99:
            break

    return output
