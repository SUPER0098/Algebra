from typing import Union, List


class RingElement:
    """Базовый класс для элементов колец: целых чисел и полиномов."""


    def __init__(self, data: Union[int, List[float]]):
        """
        data:
            - если это целое число → элемент кольца Z;
            - если это список коэффициентов [a0, a1, ..., an] → полином a0 + a1*x + ... + → an*x^n.
        """
        self.data = data
        self.is_polynomial = isinstance(data, list)


    def __repr__(self) -> str:
        terms = []
        if self.is_polynomial:
            terms = [f"{c}*x^{i}" if i > 0 else str(c) for i, c in enumerate(self.data) if
                     c != 0]
        return " + ".join(terms) if terms else str(self.data)



def gcd_ring_elements(elements: List[RingElement]) -> RingElement:
    """
    Возвращает порождающий главного идеала, порождённого заданными элементами.- Для Z: НОД целых чисел.- Для K[x]: НОД полиномов (с коэффициентами в поле K).
    """
    if elements[0].is_polynomial:
        data = [list(reversed(elements[i].data)) for i in range(len(elements))]
        gcd = data[0]
        for i_num in data:
            gcd = gcd_for_polynoms(gcd, i_num)
        return RingElement(list(reversed(gcd)))
    else:
        gcd = elements[0].data
        data = [elements[i].data for i in range(len(elements))]
        for i_num in data:
            gcd = gcd_for_int(gcd, i_num)
        return RingElement(gcd)


def gcd_for_int(a: int, b: int) -> int:
    a = abs(a)
    b = abs(b)
    if b > a:
        a, b = b, a
    while b:
        a, b = b, a % b
    return a


def gcd_for_polynoms(a: List[float], b: List[float]) -> List[float]:
    if len(b) > len(a):
        a, b = b, a
    while b:
        b, a = div_polynoms(a, b)[1], b
    return a


def div_polynoms(a: List[float], b: List[float]) -> (List[float], List[float]):
    result = []
    for i in range(len(a) - len(b) + 1):
        result.append(a[i])
        for j in range(1, len(b)):
            a[i + j] -= b[j] * a[i] / b[0]
        a[i] = 0

    ost = []
    for c_i in a:
        if abs(c_i) > 1e-6:
            ost.append(c_i)
    return result, ost
