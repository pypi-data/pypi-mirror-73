class Calculator:
    def __init__(self):
        pass

    def sum(self, a, b):
        sum_result = a + b

        return sum_result

    def sub(self, a, b):
        sub_result = a - b

        return sub_result

    def mul(self, a, b):
        mul_result = a * b

        return mul_result

    def div(self, a, b):
        try:
            div_result = a // b

            return div_result

        except Exception as e:
            print(e)
            return False
