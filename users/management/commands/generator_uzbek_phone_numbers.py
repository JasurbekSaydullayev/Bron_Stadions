import random


def generate_uzbek_phone_number():
    uzbek_operators = [
        '20', '33', '55', '90', '91', '93', '94', '95', '97', '99'
    ]

    operator_code = random.choice(uzbek_operators)

    phone_number = ''.join([str(random.randint(0, 9)) for _ in range(7)])

    full_phone_number = f'+998{operator_code}{phone_number}'

    return full_phone_number
