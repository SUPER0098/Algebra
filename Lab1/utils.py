from math import sqrt, ceil
from typing import List, Dict, Any


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


def create_permutations(n: int, plus: int = 0, permutations: List = []) -> set[tuple[int]]:
    """
    Рекурсивно генерирует все возможные перестановки для n элементов.
    Возвращает множество кортежей, представляющих перестановки.
    """
    result: set = set()

    if len(permutations) == n:
        result.add(tuple(permutations))
        return result

    for i in range(plus, n + plus):
        if i not in permutations:
            new = permutations.copy()
            new.append(i)
            result.update(create_permutations(n, plus, new))

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

    for i in create_permutations(len_x, 0, []):
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


def compozition_permutation(x: tuple[int], y: tuple[int]) -> tuple[int]:
    result: List[int] = []
    for i in range(len(x)):
        result.append(y[x[i] - 1])
    return tuple(result)


def is_group(group: list[tuple[int]]) -> bool:
    if not tuple(range(1, len(group[0]))) in group:
        return False

    for x in group:
        for y in group:
            if not compozition_permutation(x, y) in group:
                return False

    return True


def permutation_1(group: list[tuple[int]], permutation: tuple[int]) -> tuple[int]:
    for i in group:
        if compozition_permutation(i, permutation) == (1, 2, 3, 4):
            return i


def rec(ls, cur, n):
    if n == len(ls):
        if is_group(cur):
            return [tuple(cur)]
        return []
    subgroups = []
    subgroups.extend(rec(ls, cur.copy(), n + 1))
    cur.append(ls[n][0])
    if ls[n][0] != ls[n][1]:
        cur.append(ls[n][1])
    subgroups.extend(rec(ls, cur.copy(), n + 1))
    return subgroups


def all_subgroups(group: list[tuple[int]]) -> list[list[tuple[int]]]:
    first_list = []
    second_list = []
    for i in group:
        if i not in second_list:
            first_list.append(i)
            second_list.append(permutation_1(group, i))

    new_list = [(first_list[i], second_list[i]) for i in range(len(first_list))]

    return rec(new_list, [], 0)


def create_classes(group: list[tuple[int]], subgroup: list[tuple[int]], t: str) -> list[set[tuple[int]]]:
    result = []

    for g in group:
        t_class = set()
        for s in subgroup:
            if t == "left":
                t_class.add(compozition_permutation(g, s))
            else:
                t_class.add(compozition_permutation(s, g))
        if t_class not in result:
            result.append(t_class)

    return result


def is_equal_classes(class_1: list[set[tuple[int]]], class_2: list[set[tuple[int]]]) -> bool:
    for i in class_1:
        if i not in class_2:
            return False
    return True


def degree_permutations(permutation: tuple[int], d: int) -> tuple[int]:
    result = permutation
    for _ in range(d - 1):
        result = compozition_permutation(result, permutation)
    return result


def create_subgroup(permutation: tuple[int]) -> set[tuple[int]]:
    cur = permutation
    subgroup = set()
    while cur not in subgroup:
        subgroup.add(cur)
        cur = compozition_permutation(cur, permutation)
    return subgroup


def order(x: Any) -> int:
    if isinstance(x, tuple):
        for i in range(1, 100):
            if degree_permutations(x, i) == tuple(range(1, len(x) + 1)):
                return i
    else:
        return len(x)


def all_solutions(group: list[tuple[int]], d: int, need: tuple[int]) -> list[tuple[int]]:
    result = []
    for i in group:
        if degree_permutations(i, d) == need:
            result.append(i)

    return result


def create_group_z_m(m: int) -> list[int]:
    result = []
    for i in range(1, m):
        if gcd(i, m) == 1:
            result.append(i)

    return result


def all_subs_z_m(group: list[int]) -> list[set[int]]:
    return [{group[0]}, {group[0], group[1]}]


def order_z_m(m: int, x: int) -> int:
    dig = 1
    t = x
    while t != 1:
        t = t * x % m
        dig += 1
    return dig


def is_primitivity(m: int, x: int) -> bool:
    return len(create_group_z_m(m)) == order_z_m(m, x)


def all_generators(m: int) -> List[int]:
    z_m = create_group_z_m(m)
    return [i for i in z_m if is_primitivity(m, i)]


def create_cycle(m: int, t: int, v: str):
    result = []
    temp = t
    while temp not in result:
        result.append(temp)
        if v == "+":
            temp = (temp + t) % m
        else:
            temp = temp * t % m
    return result


def all_generators_for_ad(group: List[int], m: int) -> List[int]:
    result = []
    for i in group:
        if set(create_cycle(m, i, "+")) == set(group):
            result.append(i)

    return result
