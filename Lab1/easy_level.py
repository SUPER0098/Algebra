import time
from math import prod
from typing import List, Dict, Tuple

from utils import is_palindromic, check_circular_primes, is_prime, primes_with_digits, num_factors, gcd, prime_divs


def palindromic_squares_and_circular_primes() -> tuple[List[int], List[int]]:
    """
    Находит числа, которые являются палиндромами и в квадрате дают палиндром (до 10^5),
    а также круговые простые числа (до 10^6).
    Возвращает кортеж из двух списков.
    """
    palindromic_squares_nums = []
    circular_primes_nums = []

    for i_num in range(10 ** 5):
        if is_palindromic(i_num) and is_palindromic(i_num ** 2):
            palindromic_squares_nums.append(i_num)

    for i_num in range(10 ** 6):
        if check_circular_primes(i_num):
            circular_primes_nums.append(i_num)

    return palindromic_squares_nums, circular_primes_nums


def palindromic_cubes_and_palindromic_primes() -> tuple[List[int], List[int]]:
    """
    Находит числа, которые являются палиндромами и в кубе дают палиндром (до 10^5),
    а также палиндромные простые числа (до 10^6).
    Возвращает кортеж из двух списков.
    """
    palindromic_cubes_nums = []
    palindromic_primes_nums = []

    for i_num in range(10 ** 5):
        if is_palindromic(i_num) and is_palindromic(i_num ** 3):
            palindromic_cubes_nums.append(i_num)

    for i_num in range(10 ** 6):
        if is_palindromic(i_num) and is_prime(i_num):
            palindromic_primes_nums.append(i_num)

    return palindromic_cubes_nums, palindromic_primes_nums


def primes_with_two_digits() -> Dict[str, List[int]]:
    """
    Находит простые числа, содержащие определенные двузначные последовательности.
    Возвращает словарь, где ключи - двузначные строки, значения - списки простых чисел.
    """
    nums_dict = {
        "13": [],
        "15": [],
        "17": [],
        "19": []
    }

    for i_key in nums_dict.keys():
        nums_dict[i_key] = primes_with_digits(i_key)

    return nums_dict


def twin_primes_analysis(limit_pairs: int = 1000) -> Tuple[List[Tuple[int, int]], List[float]]:
    """
    Анализирует пары простых чисел-близнецов (простые числа, отличающиеся на 2).
    Возвращает кортеж: список пар близнецов и список отношений количества пар к количеству проверенных чисел.
    """
    twin_pairs = []
    relationship_list = []
    cnt_pairs = 0
    num = 2
    p_cnt = 0
    while cnt_pairs < limit_pairs:
        if is_prime(num):
            p_cnt += 1
            if is_prime(num + 2):
                twin_pairs.append((num, num + 2))
                cnt_pairs += 1
                relationship_list.append(cnt_pairs / (p_cnt + 1))
        num += 1

    return twin_pairs, relationship_list


def factorial_plus_one_factors() -> Dict[int, Dict[int, int]]:
    """
    Вычисляет факторизацию чисел вида n! + 1 для n от 2 до 50.
    Возвращает словарь, где ключи - числа n, значения - словари с факторизацией.
    """
    result = dict()

    for i in range(2, 51):
        result[i] = num_factors(i)

    return result


def euler_phi_direct(n: int) -> int:
    """
    Вычисляет функцию Эйлера φ(n) прямым методом - подсчетом чисел, взаимно простых с n.
    """
    cnt = 0
    for k in range(1, n):
        if gcd(n, k) == 1:
            cnt += 1

    return cnt


def euler_phi_factor(n: int) -> int:
    """
    Вычисляет функцию Эйлера φ(n) через факторизацию числа.
    Использует формулу Эйлера: φ(n) = n * ∏(1 - 1/p) для всех простых делителей p числа n.
    """
    primes = prime_divs(n)
    return int(n * prod([1 - 1 / primes[i][0] for i in range(len(primes))]))


def compare_euler_phi_methods(test_values: List[int]) -> dict:
    """
    Сравнивает производительность двух методов вычисления функции Эйлера.
    Измеряет время выполнения для каждого метода на заданных тестовых значениях.
    Возвращает словарь с временами выполнения для каждого метода.
    """
    result = {
        "euler_phi_direct": [],
        "euler_phi_factor": [],
        "totient": []
    }
    for i_test in test_values:
        start = time.time()
        euler_phi_direct(i_test)
        end = time.time()
        result["euler_phi_direct"].append(end - start)
        start = time.time()
        euler_phi_factor(i_test)
        end = time.time()
        result["euler_phi_factor"].append(end - start)
        start = time.time()
        end = time.time()
        result["totient"].append(end - start)

    return result
