import os
import re

class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None


class NumberRing:
    def __init__(self, digits):
        self.digits = digits
        self.n = len(digits)

    def get_sequence(self, start, length):
        """Получает последовательность цифр заданной длины с учётом кольца"""
        if length <= 0 or length > self.n:
            return ''

        if start + length <= self.n:
            return self.digits[start:start + length]
        else:
            wrap = length - (self.n - start)
            return self.digits[start:] + self.digits[:wrap]

    def find_specific_equation(self, a_len, b_len, c_len):
        """Ищет конкретное уравнение с заданными длинами чисел"""
        for start in range(self.n):
            a = self.get_sequence(start, a_len)
            b = self.get_sequence((start + a_len) % self.n, b_len)
            c = self.get_sequence((start + a_len + b_len) % self.n, c_len)

            if len(a) > 1 and a[0] == '0':
                continue

            try:
                a_num = int(a)
                b_num = int(b)
                c_num = int(c)
            except:
                continue

            if a_num + b_num == c_num:
                return f"{a_num}+{b_num}={c_num}"
        return None

    def find_equation(self):
        """Ищет любое подходящее уравнение a + b = c"""
        if self.n >= 8:
            result = self.find_specific_equation(3, 2, 3)
            if result:
                return result

        # Если все цифры одинаковые
        if all(d == self.digits[0] for d in self.digits):
            return "No"

        # Ищем другие варианты
        for a_len in range(1, self.n - 1):
            for b_len in range(1, self.n - a_len):
                c_len = self.n - a_len - b_len
                if c_len < 1:
                    continue

                for start in range(self.n):
                    a = self.get_sequence(start, a_len)
                    b = self.get_sequence((start + a_len) % self.n, b_len)
                    c = self.get_sequence((start + a_len + b_len) % self.n, c_len)

                    if len(a) > 1 and a[0] == '0':
                        continue

                    try:
                        a_num = int(a)
                        b_num = int(b)
                        c_num = int(c)
                    except:
                        continue

                    if a_num + b_num == c_num:
                        return f"{a_num}+{b_num}={c_num}"
        return "No"


def is_valid_filename(filename):
    """Проверяет, что имя файла корректное и файл существует"""
    if not filename:
        print("Имя файла не может быть пустым.")
        return False

    # Проверка на запрещённые символы (зависит от ОС, здесь пример для Windows)
    if re.search(r'[<>:"/\|?*]', filename):
        print("Имя файла содержит запрещённые символы.")
        return False

    if not os.path.isfile(filename):
        print("Файл не найден.")
        return False

    return True


def main():
    filename = input("Введите имя файла с цифрами кольца: ").strip()

    if not is_valid_filename(filename):
        return

    with open(filename, 'r') as f:
        user_input = f.readline().strip()

    with open('output.txt', 'w') as f:

        if not user_input.isdigit():
            print("Строка должна содержать только цифры.")
            return

        if len(user_input) > 1000 or len(user_input) < 3:
            f.write("В строке должно быть не меньше 3 и не больше 1000 цифр!n")
            print("Данные записаны в output.txt")
            return

        # Особый случай для "000..."
        if all(d == '0' for d in user_input):
            f.write("0+0=0n")
            print("Данные записаны в output.txt")
            return

        ring = NumberRing(user_input)
        result = ring.find_equation()
        f.write(result + 'n')

    print("Данные записаны в output.txt")


if __name__ == "__main__":
    main()
