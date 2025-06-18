import os
import re

class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None


class NumberRing:
    def __init__(self, digits):
        self.n = len(digits)
        self.head = None
        self._create_ring(digits)

    def _create_ring(self, digits):
        prev = None
        for d in digits:
            node = Node(d)
            if not self.head:
                self.head = node
            else:
                prev.next = node
            prev = node
        if prev:
            prev.next = self.head  

    def get_sequence(self, start, length):
        if length <= 0 or length > self.n:
            return ''

        current = self.head
        for _ in range(start):
            current = current.next

        result = []
        for _ in range(length):
            result.append(current.value)
            current = current.next

        return ''.join(result)

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
        first_digit = self.head.value if self.head else None
        if all(self.get_sequence(i, 1) == first_digit for i in range(self.n)):
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
        main()
        return False

    if re.search(r'[<>:"/\\|?*]', filename):
        print("Имя файла содержит запрещённые символы.")
        main()
        return False

    if not os.path.isfile(filename):
        print("Файл не найден.")
        main()
        return False

    return True


def main():
    filename = input("Введите имя файла с цифрами кольца(если вы хотите завершить программу введите 'завершить'): ").strip()

    if filename == 'завершить':
        return

    if not is_valid_filename(filename):
        return

    with open(filename, 'r') as f:
        user_input = f.readline().strip()

    if not user_input.isdigit():
        print("Строка должна содержать только цифры.")
        main()
        return

    if len(user_input) > 1000 or len(user_input) < 3:
        with open('output.txt', 'w') as f:
            f.write("В строке должно быть не меньше 3 и не больше 1000 цифр!\n")
        main()
        return

    if all(d == '0' for d in user_input):
        with open('output.txt', 'w') as f:
            f.write("0+0=0\n")
        print("Данные записаны в output.txt")
        main()
        return

    ring = NumberRing(user_input)
    result = ring.find_equation()

    with open('output.txt', 'w') as f:
        f.write(result + '\n')

    print("Данные записаны в output.txt")
    main()


if __name__ == "__main__":
    main()
