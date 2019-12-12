inputs = [1, 2, 3]

pointer = 0
while pointer <= len(inputs):
    inputs.append(0)
    print(inputs[pointer])
    pointer = pointer + 1