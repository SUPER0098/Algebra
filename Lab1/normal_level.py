from itertools import product
from random import randint

from sympy import symbols, Poly, solve, factor, gcdex, invert, GF

from configs import ISU
from utils import *

N = ISU % 20


def subgroups_of_sm(N: int) -> dict:
    result = {"cnt_subgroups": int,
              "random_subgroup": list[tuple[int]],
              "left_classes": list[set[tuple[int]]],
              "right_classes": list[set[tuple[int]]],
              "index": int,
              "is_normal": bool
              }
    symmetric_group = list(create_permutations(N % 5 + 4, 1))
    all_subs = all_subgroups(symmetric_group)
    result["cnt_subgroups"] = len(all_subs)
    result["random_subgroup"] = all_subs[randint(0, len(all_subs) - 1)]
    my_subgroup = all_subs[N % len(all_subs)]
    result["left_classes"] = create_classes(symmetric_group, my_subgroup, "left")
    result["right_classes"] = create_classes(symmetric_group, my_subgroup, "right")
    result["index"] = len(result["left_classes"])
    result["is_normal"] = is_equal_classes(result["left_classes"], result["right_classes"])
    return result


def element_powers_in_Sm(N: int) -> dict:
    answer = {
        "order_g^n1": int,
        "order_g^n2": int,
        "order_g^n3": int,
        "order_subgroup": int
    }

    symmetric_group = list(create_permutations(N % 5 + 4, 1))

    n1 = N % 6
    n2 = 2 + N % 10
    n3 = (N + 2) % 6

    g = symmetric_group[N % len(symmetric_group)]

    g_n1 = degree_permutations(g, n1)
    g_n2 = degree_permutations(g, n2)
    g_n3 = degree_permutations(g, n3)

    answer["order_g^n1"] = order(g_n1)
    answer["order_g^n2"] = order(g_n2)
    answer["order_g^n3"] = order(g_n3)
    answer["order_subgroup"] = order(create_subgroup(g))
    return answer


def solve_sigma_power_eq(N: int) -> dict:
    answer = {
        "cnt_solution": int,
        "3_random_solution": list[tuple[int]]
    }

    n = 2 + N % 10

    symmetric_group = list(create_permutations(N % 5 + 4, 1))
    need = [i for i in range(2, len(symmetric_group[0]) + 1)]
    need.append(1)
    need = tuple(need)
    solutions = all_solutions(symmetric_group, n, need)
    answer["cnt_solution"] = len(solutions)
    random_solutions = [solutions[randint(0, len(solutions) - 1)] for _ in range(min(3, len(solutions)))]
    answer["3_random_solution"] = random_solutions
    return answer


def elements_of_order_k_in_cyclic_group(N: int) -> dict:
    answer = {
        "g^k = e": list[tuple[int]],
        "order_k": list[tuple[int]]
    }
    m = N % 5 + 4
    k = 1 + N % 7
    symmetric_group = list(create_permutations(m, 1))
    cycle_group = []
    for i in symmetric_group:
        if len(create_subgroup(i)) == m:
            cycle_group = list(create_subgroup(i))
            break
    answer["g^k = e"] = all_solutions(cycle_group, k, tuple(range(1, m + 1)))
    answer["order_k"] = [x for x in cycle_group if order(x) == k]
    return answer


def subgroups_of_Zm_star(N: int) -> list:
    m = 4 + N % 5
    s = create_group_z_m(m)
    return all_subs_z_m(s)


def order_of_sr(N: int) -> int:
    p: int = 0
    s: int = 0
    match N % 5:
        case 0:
            p = 29
            s = 5
        case 1:
            p = 31
            s = 4
        case 2:
            p = 37
            s = 3
        case 3:
            p = 23
            s = 17
        case 4:
            p = 19
            s = 15
    return order_z_m(p, s)


def order_and_primitivity_of_t(N: int) -> dict:
    answer = {
        "order": int,
        "is_primitivity": bool
    }
    p: int = 0
    t: int = 0
    match N % 5:
        case 0:
            p = 29
            t = 9
        case 1:
            p = 31
            t = 8
        case 2:
            p = 37
            t = 7
        case 3:
            p = 23
            t = 12
        case 4:
            p = 19
            t = 14

    answer["order"] = order_z_m(p, t)
    answer["is_primitivity"] = is_primitivity(p, t)

    return answer


def generators_of_Zm_star(N: int) -> list:
    m = 4 + N % 5
    return all_generators(m)


def cyclic_subgroup_in_Zm_additive(N: int) -> dict:
    answer = {
        "cyclic_subgroup": list,
        "order": int,
        "all_generators": list
    }
    m = 4 + N % 5
    t = 0
    match N % 5:
        case 0:
            t = 9
        case 1:
            t = 8
        case 2:
            t = 7
        case 3:
            t = 12
        case 4:
            t = 14

    t %= m
    cyclic_subgroup = create_cycle(m, t, "+")
    answer["cyclic_subgroup"] = cyclic_subgroup
    answer["order"] = len(cyclic_subgroup)
    answer["all_generators"] = all_generators_for_ad(cyclic_subgroup, m)
    return answer


def isomorphism_of_cyclic_subgroup_Zm_star(N: int) -> dict:
    answer = {
        "cyclic_subgroup": list,
        "isomorphism": list
    }
    m = 4 + N % 5
    t = 0
    match N % 5:
        case 0:
            t = 9
        case 1:
            t = 8
        case 2:
            t = 7
        case 3:
            t = 12
        case 4:
            t = 14

    t %= m

    answer["cyclic_subgroup"] = create_cycle(m, t, "*")
    answer["isomorphism"] = [(1, 2, 3, 4)]
    return answer


def find_all_roots(N: int) -> tuple:
    x = symbols('x')
    poly1 = x ** 9
    for i in range(9):
        poly1 += ((i + N) % 4) * (x ** i)
    poly2 = 0
    for i in range(7):
        poly2 += ((i + N) % 7) * (x ** i)
    return [x.evalf() for x in solve(poly1)], [x.evalf() for x in solve(poly2)]


def factor_polynom(N: int) -> tuple:
    x = symbols('x')
    poly1 = x ** 5
    poly2 = x ** 4
    for i in range(5):
        poly1 += x ** i * ((N + i) % 5)
    for i in range(4):
        poly2 += x ** i * ((N + i) % 9)

    factor1 = factor(poly1)
    factor2 = factor(poly2)
    return factor1, factor2


def gcd_polynoms(N: int) -> dict:
    answer = {
        "gcd": Poly,
        "u(x)": Poly,
        "v(x)": Poly
    }
    x = symbols('x')
    poly1 = 0
    poly2 = 0
    for i in range(8):
        poly1 += x ** i * ((N + i) % 11)
    for i in range(4):
        poly2 += x ** i * ((N + i) % 11)

    answer["gcd"], answer["u(x)"], answer["v(x)"] = gcdex(poly1, poly2, x)

    return answer


def find_inverse_poly(N: int):
    x = symbols('x')

    poly1 = 0
    for i in range(3):
        poly1 += x ** i * ((N + i) % 11)
    poly2 = x ** 8 + x ** 4 + x ** 3 + 6 * x + 2
    p = 13
    return invert(poly1, poly2, modulus=p)


def generate_irreducible_polynomials(q: int, d: int) -> list:
    x = symbols('x')
    polynomials = []

    for coeffs in product(range(q), repeat=d + 1):
        if coeffs[-1] != 0:
            poly_expr = sum(c * x ** i for i, c in enumerate(coeffs))
            if factor(poly_expr) == poly_expr:
                polynomials.append(Poly(poly_expr, x, domain=GF(q)))

    return [x.as_expr() for x in polynomials]
