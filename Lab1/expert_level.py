from random import randint
from typing import Tuple


class RingElement:
    def __init__(self, data: dict[str, float], order: int):
        self.data = data
        self.order = order

    def __add__(self, other: "RingElement"):
        result = self.data.copy()
        for i_key, i_value in other.data.items():
            if result.get(i_key):
                result[i_key] += i_value
            else:
                result[i_key] = i_value
        return RingElement(result, self.order)

    def __sub__(self, other: "RingElement"):
        result = self.data.copy()
        for i_key, i_value in other.data.items():
            if result.get(i_key):
                result[i_key] -= i_value
            else:
                result[i_key] = -i_value
        return RingElement(result, self.order)

    def __mul__(self, other: Tuple[str, float]):
        monom = other[0]
        coef = other[1]
        result = dict()
        variables = [monom[i] for i in range(0, len(monom), 3)]
        degrees = [int(monom[i]) for i in range(2, len(monom), 3)]
        for i_key, i_value in self.data.items():
            new_monom = i_key
            for i in range(len(variables)):
                old_deg = int(i_key[i_key.find(variables[i]) + 2])
                new_deg = old_deg + degrees[i]
                x = variables[i]
                new_monom = new_monom.replace(f"{x}^{old_deg}", f"{x}^{new_deg}")
            result[new_monom] = i_value * coef
        return RingElement(result, self.order)

    def __str__(self):
        result = ""
        for i_key, i_value in self.data.items():
            if abs(i_value) < 1e-6:
                continue
            if result or i_value < 0:
                if i_value > 0:
                    result += " + "
                if i_value < 0:
                    result += " - "
            result += f"{abs(i_value)}{i_key}"
        if not result:
            result = "0"
        return result


def leading_monomial(polynom: RingElement):
    all_monoms = [i for i in polynom.data]
    max_monom = None
    for i in all_monoms:
        if abs(polynom.data[i]) > 1e-6:
            if not max_monom:
                max_monom = i
            else:
                max_monom = greater_monom(max_monom, i, polynom.order)
    return max_monom


def greater_monom(x, y, order):
    degrees_x = [int(x[i]) for i in range(2, len(x), 3)]
    degrees_y = [int(y[i]) for i in range(2, len(y), 3)]
    if order == 1:
        if sum(degrees_x) > sum(degrees_y):
            return x
        else:
            return y
    for i in range(len(degrees_x)):
        if degrees_x[i] > degrees_y[i]:
            return x
        if degrees_x[i] < degrees_y[i]:
            return y
    return x


def leading_term(polynom: RingElement):
    lm = leading_monomial(polynom)
    return lm, polynom.data[lm]


def normal_form(polynom: RingElement, base_polynoms: list[RingElement]):
    new_polynom = RingElement(polynom.data.copy(), polynom.order)
    for i_pol in base_polynoms:
        while leading_monomial(new_polynom) and is_divided(new_polynom, i_pol):
            lt_x = leading_term(new_polynom)
            lt_y = leading_term(i_pol)
            need_mul = div_monoms(lt_x[0], lt_y[0])
            new_polynom = new_polynom - (i_pol * (need_mul, lt_x[1] / lt_y[1]))
    return new_polynom


def is_divided(x: RingElement, y: RingElement):
    lm_x = leading_monomial(x)
    lm_y = leading_monomial(y)
    degrees_x = [int(lm_x[i]) for i in range(2, len(lm_x), 3)]
    degrees_y = [int(lm_y[i]) for i in range(2, len(lm_y), 3)]
    for i in range(len(degrees_x)):
        if degrees_x[i] < degrees_y[i]:
            return False
    return True


def div_monoms(x: str, y: str) -> str:
    result = ""
    degrees_x = [int(x[i]) for i in range(2, len(x), 3)]
    degrees_y = [int(y[i]) for i in range(2, len(y), 3)]
    variables = [x[i] for i in range(0, len(x), 3)]
    for i in range(len(degrees_x)):
        need_deg = degrees_x[i] - degrees_y[i]
        result += f"{variables[i]}^{need_deg}"
    return result


def s_polynomial(polynom_x: RingElement, polynom_y: RingElement) -> RingElement:
    lt_x = leading_term(polynom_x)
    lt_y = leading_term(polynom_y)
    lcm = ""
    variables = [lt_x[0][i] for i in range(0, len(lt_x[0]), 3)]
    degrees_x = [int(lt_x[0][i]) for i in range(2, len(lt_x[0]), 3)]
    degrees_y = [int(lt_y[0][i]) for i in range(2, len(lt_y[0]), 3)]
    for i in range(len(variables)):
        lcm += f"{variables[i]}^{max(degrees_x[i], degrees_y[i])}"
    m_x = div_monoms(lcm, lt_x[0])
    m_y = div_monoms(lcm, lt_y[0])

    new_polynom = (polynom_x * (m_x, max(lt_x[1], lt_y[1]) / lt_x[1]) -
                   polynom_y * (m_y, max(lt_x[1], lt_y[1]) / lt_y[1]))
    return new_polynom


def buchberger(generic: list[RingElement]) -> list[RingElement]:
    for i in generic:
        for j in generic:
            new_polynom = normal_form(s_polynomial(i, j), generic)
            if leading_monomial(new_polynom):
                generic.append(new_polynom)
                return buchberger(generic)

    return generic


def is_in_ideal(polynom: RingElement, generic: list[RingElement]):
    generic = buchberger(generic)
    if leading_monomial(normal_form(polynom, generic)):
        return False
    return True


def str_into_polynom(string: str) -> dict[str, float]:
    result = dict()
    c: float = 0.0
    from_dot = 0
    string = string.replace(" ", "")
    i = 0
    is_minus = 1
    while i < len(string):
        if string[i] == "-":
            is_minus = -1
        if string[i] == "+":
            is_minus = 1
        i_let = string[i]
        if i_let.isdigit():
            if from_dot != 0:
                c += int(i_let) / 10 ** from_dot
                from_dot += 1
            else:
                if c < 10e-6:
                    c = float(i_let)
                else:
                    c *= 10
                    c += float(i_let)
        elif i_let == "." or i_let == ",":
            from_dot = 1
        elif i_let != "+" and i_let != "-":
            monom = ""
            if abs(c) < 1e-6:
                c = 1.0
            while i < len(string) and not (string[i] == "+" or string[i] == "-"):
                monom += string[i]
                i += 1
            result[monom] = c * is_minus
            c = 0.0
            i -= 1
        i += 1

    return result


polynoms_ls = ["3x^1y^5 - 4x^2y^4 + 3x^0y^1",
               "-2x^2y^1 - 6x^1y^5 + 10x^4y^1",
               "4x^5y^2 - 6x^2y^5 + 10x^8y^0"]

ring_list = [RingElement(str_into_polynom(i), 0) for i in polynoms_ls]

for i in ring_list:
    print(i)

x = ring_list[randint(0, 2)]
y = ring_list[randint(0, 2)]
print()
print(x)
print("+")
print(y)
print("=")
print(x + y)
print()
print(x)
print("-")
print(y)
print("=")
print(x - y)
print()
print("(", x, ") * 3x^1y^2 =", x * ("x^1y^2", 3))
print("(", y, ") * 4x^3y^0 =", y * ("x^3y^0", 4))
print()
for i in ring_list:
    print(i, "\nLM =", leading_monomial(i), "\nLT =", leading_term(i))
print()
print(is_divided(x, y))
print()
gen_pol = ["x^2y^0 - x^0y^1", "x^1y^1 - x^0y^0", "x^3y^0 - x^2y^1 + x^1y^2 - x^0y^2"]
gen = [RingElement(str_into_polynom(i), 0) for i in gen_pol]
print("N(", gen[2], ", gen) - ", normal_form(gen[2], gen[:2]))
# Ожидаемый результат: -2y^2 + 1y + 1
gen_pol = ["x^2 - 1x^0", "x^3 + x^2 - x^1 - 1x^0"]
gen = [RingElement(str_into_polynom(i), 0) for i in gen_pol]
print("N(", gen[1], ", gen) =", normal_form(gen[1], gen[:1]))
# Ожидаемый результат: 0 (или просто 2x)

# Тест 3: Нет редукции
gen_pol = ["x^2y^0 - x^0y^1", "x^0y^2 - 1x^0y^0", "x^1y^1 + x^0y^0"]
gen = [RingElement(str_into_polynom(i), 0) for i in gen_pol]
print("N(", gen[2], ", gen) =", normal_form(gen[2], gen[:2]))
# Ожидаемый результат: xy + 1

print()
# S полином
f1 = RingElement(str_into_polynom("x^2y^1 - y^2x^0"), 0)
f2 = RingElement(str_into_polynom("x^1y^2 - x^1y^0"), 0)
s_poly = s_polynomial(f1, f2)
print("Test 1: S(", f1, ",", f2, ") =", s_poly)
# Ожидаемый: -1y^3 + 1x^2

f1 = RingElement(str_into_polynom("x^3y^0 - x^0y^1"), 0)
f2 = RingElement(str_into_polynom("x^2y^1 - 1x^0y^0"), 0)
s_poly = s_polynomial(f1, f2)
print("Test 2: S(", f1, ",", f2, ") =", s_poly)
# Ожидаемый: x - y^2

f1 = RingElement(str_into_polynom("x^2y^0 - 1x^0y^0"), 0)
f2 = RingElement(str_into_polynom("x^3y^0 - x^1y^0"), 0)
s_poly = s_polynomial(f1, f2)
print("Test 3: S(", f1, ",", f2, ") =", s_poly)
# Ожидаемый: 0

print()
# Алгоритм Бухбергера
initial_basis = [
    "x^3y^0 - 2x^1y^1",
    "x^2y^1 - 2x^0y^2 + x^1y^0"
]

print("Начальный базис:")
for i, poly in enumerate(initial_basis):
    print(f"  f{i + 1} = {poly}")

basis_polys = [RingElement(str_into_polynom(poly), 0) for poly in initial_basis]

groebner_basis = buchberger(basis_polys)

print("\nРезультат алгоритма Бухбергера:")
for i, poly in enumerate(groebner_basis):
    print(f"  g{i + 1} = {poly}")

print("\nРезультат алгоритма Бухбергера:")
for i, poly in enumerate(groebner_basis):
    print(f"  g{i + 1} = {poly}")