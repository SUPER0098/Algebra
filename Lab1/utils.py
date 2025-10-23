from math import sqrt, ceil
from typing import List, Dict


def is_prime(x: int) -> bool:
    """
    Проверяет, является ли число простым.
    Возвращает True для простых чисел, False для составных и специальных случаев.
    """
    if x == 2:
        return True
    if x <= 0:
        return False
    if x % 2 == 0:
        return False
    if x == 1:
        return False

    sq: int = ceil(sqrt(x))
    for div in range(3, sq + 1, 2):
        if x % div == 0:
            return False

    return True


def is_palindromic(x: int) -> bool:
    """
    Проверяет, является ли число палиндромом (читается одинаково слева направо и справа налево).
    Возвращает True для палиндромов, False в противном случае.
    """
    reversed_x: str = ""

    if x == 0:
        return True

    while x:
        reversed_x += str(x % 10)
        if reversed_x == str(x) or str(x // 10) == reversed_x:
            return True
        x //= 10

    return False


def create_permutations(n: int, permutations: List = None) -> set[tuple[int]]:
    """
    Рекурсивно генерирует все возможные перестановки для n элементов.
    Возвращает множество кортежей, представляющих перестановки.
    """
    result: set = set()

    if len(permutations) == n:
        result.add(tuple(permutations))
        return result

    for i in range(n):
        if i not in permutations:
            new = permutations.copy()
            new.append(i)
            result.update(create_permutations(n, new))

    return result


def apply_permutation(x: int, permutations: tuple) -> int:
    """
    Применяет перестановку к цифрам числа.
    Возвращает новое число, полученное перестановкой цифр согласно заданной перестановке.
    """
    new_num = 0

    for i in reversed(permutations):
        dig = x % 10
        new_num += dig * 10 ** (len(permutations) - i - 1)
        x //= 10
    return new_num


def create_all_options(x: int) -> List[int]:
    """
    Создает все возможные числа путем перестановки цифр исходного числа.
    Возвращает список всех возможных перестановок цифр числа.
    """
    result = []

    len_x = len(str(x))

    for i in create_permutations(len_x, []):
        result.append(apply_permutation(x, i))

    return result


def check_circular_primes(x: int) -> bool:
    """
    Проверяет, является ли число круговым простым (все циклические перестановки цифр числа являются простыми).
    Возвращает True, если число круговое простое, False в противном случае.
    """
    str_num = str(x)
    if x == 2 or x == 5:
        return True
    if "0" in str_num or "2" in str_num or "4" in str_num or "5" in str_num or "6" in str_num or "8" in str_num:
        return False
    for i_opt in create_all_options(x):
        if not is_prime(i_opt):
            return False

    return True


def all_nums_with_digits(n: int, dig: List[int], num: int) -> set[int]:
    """
    Рекурсивно генерирует все числа длины n, состоящие только из заданных цифр.
    Возвращает множество всех возможных чисел.
    """
    if len(str(num)) == n:
        return {num}

    result = set()
    for i_dig in dig:
        result.update(all_nums_with_digits(n, dig, num * 10 + i_dig))

    return result


def all_prime_nums(n: int, dig: List[int]) -> List[int]:
    """
    Генерирует все простые числа длины n, состоящие только из заданных цифр.
    Возвращает список простых чисел.
    """
    result = []

    for i_num in all_nums_with_digits(n, dig, 0):
        if is_prime(i_num):
            result.append(i_num)

    return result


def primes_with_digits(dig: str) -> List[int]:
    """
    Находит первые 100 простых чисел, содержащих заданную последовательность цифр.
    Поиск начинается с чисел длины 1 и увеличивает длину, пока не найдется 100 простых чисел.
    Возвращает отсортированный список из 100 простых чисел.
    """
    dig_cnt = 1
    result = []
    while len(result) < 100:
        result.extend(all_prime_nums(dig_cnt, [int(x) for x in dig]))
        dig_cnt += 1

    result = sorted(result)
    new_result = []
    for i in result:
        new_result.append(i)
        if len(new_result) == 100:
            break

    return new_result


def dig_div(n: int, div: int) -> int:
    """
    Рекурсивно вычисляет степень, с которой простой делитель входит в число.
    Возвращает количество раз, которое число можно разделить на делитель без остатка.
    """
    if n % div != 0:
        return 0
    return dig_div(n // div, div) + 1


def num_factors(num: int) -> Dict[int, int]:
    """
    Вычисляет факторизацию числа num! (факториала).
    Возвращает словарь, где ключи - простые делители, значения - их степени в разложении.
    """
    result = dict()
    for i_factor in range(2, num + 1):
        for i in range(2, i_factor + 1):
            if i_factor % i == 0 and is_prime(i):
                if result.get(i):
                    result[i] += dig_div(i_factor, i)
                else:
                    result[i] = dig_div(i_factor, i)
    return result


def gcd(a: int, b: int):
    """
    Вычисляет наибольший общий делитель (НОД) двух чисел с помощью алгоритма Евклида.
    Возвращает НОД чисел a и b.
    """
    if a < b:
        a, b = b, a
    if a % b == 0:
        return b
    return gcd(b, a % b)


def prime_divs(x: int) -> List[tuple[int, int]]:
    """
    Выполняет факторизацию числа на простые множители.
    Возвращает список кортежей (простой_делитель, степень).
    """
    result = []

    if x % 2 == 0:
        result.append((2, dig_div(x, 2)))

    x //= 2 ** dig_div(x, 2)
    sq = ceil(sqrt(x))

    for i_div in range(3, sq + 1, 2):
        if x == 1:
            break
        if x % i_div == 0:
            result.append((i_div, dig_div(x, i_div)))
            x //= i_div ** dig_div(x, i_div)

    if x != 1:
        result.append((x, 1))

    return result
