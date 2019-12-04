passwords = range(240920, 789858)


def check_password(password_input: int) -> bool:
    value = str(password_input)
    for pos in range(len(value) - 1):
        if int(value[pos]) > int(value[pos + 1]):
            return False

    for pos in range(len(value)):
        if value.count(value[pos]) == 2:
            return True


valid_passwords = 0
for password in passwords:
    if check_password(password):
        valid_passwords += 1

print(valid_passwords)
