int_codes = []

relative_base = 0


def get_int_code(position: int) -> int:
    global int_codes
    if position >= len(int_codes):
        for num in range(len(int_codes), position + 2):
            int_codes.append(0)
    return int_codes[position]


def set_int_code(position: int, value: int):
    global int_codes
    if position >= len(int_codes):
        for num in range(len(int_codes), position + 2):
            int_codes.append(0)

    int_codes[position] = value


def get_value(pos: int, mode: int) -> int:
    if mode == 0:
        return int(get_int_code(pos))
    elif mode == 1:
        return int(pos)
    elif mode == 2:
        return int(get_int_code(pos + relative_base))


def get_modes(opcode: int) -> tuple:
    code = str(opcode)
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
    print(len(codes))
    global int_codes
    global relative_base
    int_codes = codes
    input_values = inputs.copy()
    pointer = 0
    output = []

    while pointer < len(int_codes):
        code = get_int_code(pointer)
        modes = get_modes(code)

        first_mode = modes[1]
        second_mode = modes[2]
        third_mode = modes[3]
        code = modes[0]

        # Code 1: Add
        if code == 1:
            operand1pos = get_int_code(1 + pointer)
            operand2pos = get_int_code(2 + pointer)
            target = get_int_code(3 + pointer)
            set_int_code(get_value(target, third_mode),
                         get_value(operand1pos, first_mode) + get_value(operand2pos, second_mode))
            pointer += 4
        # Code 2: Multiply
        elif code == 2:
            operand1pos = get_int_code(1 + pointer)
            operand2pos = get_int_code(2 + pointer)
            target = get_int_code(3 + pointer)
            set_int_code(get_value(target, third_mode),
                         get_value(operand1pos, first_mode) * get_value(operand2pos, second_mode))
            pointer += 4
        # Code 3: Input
        elif code == 3:
            target = get_int_code(pointer + 1)
            if len(input_values) == 0:
                set_int_code(get_value(target, first_mode), input("Enter value for opcode 3: "))
            else:
                set_int_code(get_value(target, first_mode), input_values.pop(0))
            pointer += 2
        # Code 4: Output
        elif code == 4:
            target = get_int_code(pointer + 1)
            print(get_value(target, first_mode))
            output.append(get_value(target, first_mode))
            pointer += 2
        # Code 5: Conditional Jump
        elif code == 5:
            if get_value(get_int_code(1 + pointer), first_mode) != 0:
                pointer = get_value(get_int_code(pointer + 2), second_mode)
            else:
                pointer += 3
        # Code 6: Conditional Jump
        elif code == 6:
            if get_value(get_int_code(1 + pointer), first_mode) == 0:
                pointer = get_value(get_int_code(pointer + 2), second_mode)
            else:
                pointer += 3
        # Code 7: Greater-Than
        elif code == 7:
            operand1pos = get_int_code(1 + pointer)
            operand2pos = get_int_code(2 + pointer)
            target = get_int_code(3 + pointer)
            if get_value(operand1pos, first_mode) < get_value(operand2pos, second_mode):
                set_int_code(get_value(target, third_mode), 1)
            else:
                set_int_code(get_value(target, third_mode), 0)
            pointer += 4
        # Code 8: Compare two positions for equality
        elif code == 8:
            operand1pos = get_int_code(1 + pointer)
            operand2pos = get_int_code(2 + pointer)
            target = get_int_code(3 + pointer)
            if get_value(operand1pos, first_mode) == get_value(operand2pos, second_mode):
                set_int_code(get_value(target, third_mode), 1)
            else:
                set_int_code(get_value(target, third_mode), 0)
            pointer += 4
        # Code 9: Modify relative base
        elif code == 9:
            parameter = get_value(pointer + 1, first_mode)
            relative_base += parameter
            pointer += 2
        # Code 99: Shut down
        elif code == 99:
            break
    return output
