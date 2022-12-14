import math

# Ratio uses for round functions
ROUNDING_RATIO = 4

# Selects
# 0 - mine
# 1 - example
# 2+ - optional
SELECT_VARIANT_31, SELECT_VARIANT_32, \
SELECT_VARIANT_33, SELECT_VARIANT_34, \
SELECT_VARIANT_35 = 0, 0, 0, 0, 0

def f_31(x):
    return x * math.cos(x)


def test_f1(x):
    return math.log(x)


def test_f2(x):
    return math.sin(math.pi / 6 * x)


def omega(x_list):
    result = []
    for i in range(len(x_list)):
        tmp = 1
        for j in range(len(x_list)):
            if i != j:
                tmp *= x_list[i] - x_list[j]
        result.append(round(tmp, 5))
    return result


def get_multiples(x, x_list: list[float]):
    result: list[float] = []
    for i in range(len(x_list)):
        tmp = 1
        for j in range(len(x_list)):
            if j != i:
                tmp *= x - x_list[j]
        result.append(round(tmp, 5))
    return result


def lagrang_get_table(x1, x2, x3, x4, first_part_letter: str):
    use_f = [
        f_31,
        test_f1
    ][SELECT_VARIANT_31]
    X = [
        math.pi / 4,    # My x point
        0.8,            # First example
    ][SELECT_VARIANT_31]# Choose x from list above

    x_list: list[float] = [round(x1, 5), round(x2, 5), round(x3, 5), round(x4, 5)]
    f_list: list[float] = []
    omega_list: list[float] = omega(x_list)
    fdo_list: list[float] = []
    xlast_list: list[float] = []

    for idx, x in enumerate(x_list):
        f_list.append(round(use_f(x), 5))
        fdo_list.append(round(f_list[idx] / omega_list[idx], 5))
        xlast_list.append(round(X - x, 1))

    multiples_list = get_multiples(X, x_list)
    print(multiples_list)
    L = fdo_list[0] * multiples_list[0] + \
        fdo_list[1] * multiples_list[1] + \
        fdo_list[2] * multiples_list[2] + \
        fdo_list[3] * multiples_list[3]
    yL = use_f(X)
    precision = abs(yL - L)

    return {
        f'l{first_part_letter}_x_list': x_list,
        f'l{first_part_letter}_f_list': f_list,
        f'l{first_part_letter}_omega_list': omega_list,
        f'l{first_part_letter}_fdo_list': fdo_list,
        f'l{first_part_letter}_xlast_list': xlast_list,
        f'l{first_part_letter}_precision': round(precision, 4),
    }


def newtone_get_table(x1, x2, x3, x4, first_part_letter: str):
    use_f = [
        f_31,
        test_f2,
    ][SELECT_VARIANT_31]
    X = [
        math.pi / 4,    # My x point
        1.5,            # Second example
    ][SELECT_VARIANT_31]# Choose x from list above

    x_list: list[float] = [round(x1, 5), round(x2, 5), round(x3, 5), round(x4, 5)]
    f_list: list[float] = [round(use_f(x), 5) for x in x_list]
    fx_list: list[float] = [round((f_list[i] - f_list[i + 1])/ \
                (x_list[i] - x_list[i + 1]), 5) for i in range(3)]
    fxx_list: list[float] = [round((fx_list[0] - fx_list[1])/ \
                                   (x_list[0] - x_list[2]), 5),
                             round((fx_list[1] - fx_list[2])/ \
                                   (x_list[1] - x_list[3]), 5)]
    fxxx_list: list[float] = [round((fxx_list[0] - fxx_list[1])/ \
                                    (x_list[0] - x_list[3]), 5)]

    P = lambda x: fx_list[0]*x + fxx_list[0] * x * (x - x_list[1]) + \
            fxxx_list[0] * x * (x - x_list[1]) * (x - x_list[2])

    px = P(X)
    fx = use_f(X)

    precision = abs(fx - px)

    return {
        f'n{first_part_letter}_x_list': x_list,
        f'n{first_part_letter}_f_list': f_list,
        f'n{first_part_letter}_fx_list': fx_list,
        f'n{first_part_letter}_fxx_list': fxx_list,
        f'n{first_part_letter}_fxxx_list': fxxx_list,
        f'n{first_part_letter}_precision': round(precision, 4),
    }


def run_through_32():
    X = [
        1.5, # My variant and example
    ][0]

    x_list = [
        [0.0, 1.0, 2.0, 3.0, 5.0], # mine
        [0.0, 1.0, 2.0, 3.0, 4.0]
    ][SELECT_VARIANT_32]
    f_list = [
        [0.0, 0.45345, 0.52360, 0.0, -2.2672],
        [0.0, 1.8415, 2.9093, 3.1411, 3.2432]
    ][SELECT_VARIANT_32]

    h_list = [x_list[i] - x_list[i - 1] for i in range(1, len(x_list))]

    c_list = [
        [0.0, -0.20454, -0.33174, -0.24971],
        [0.0, -0.44949, -0.52299, 0.03344], # example
    ][SELECT_VARIANT_32]

    b_list = [round((f_list[i] - f_list[i - 1])/h_list[i] -
              1/3 * h_list[i] * (c_list[i] + 2 * c_list[i - 1]), 5)
              for i in range(1, len(f_list) - 1)]
    b_list.append(round((f_list[4] - f_list[3])/h_list[3] - 2/3*h_list[3]*c_list[3], 5))
    d_list = [round((c_list[i] - c_list[i - 1])/3*h_list[i], 5)
              for i in range(1, len(f_list) - 1)]
    d_list.append(round(-c_list[3]/3*h_list[3], 5))

    end_f_func = lambda x: round(f_list[1] + b_list[1] * (x - 1) + \
            c_list[1] * ((x - 1)**2) + d_list[1] * ((x - 1)**3), 5)

    return {
        'x_list': x_list,
        'f_list': f_list,
        'b_list': b_list,
        'c_list': c_list,
        'd_list': d_list,
        'X': X,
        'res': end_f_func(X),
    }


def run_through_33():
    x_list = [
        [-1, 0, 1, 2, 3, 5], # my variant
        [0, 1.7, 3.4, 5.1, 6.8, 8.5] # example
    ][SELECT_VARIANT_33]
    y_list = [
        [-0.86603, 0, 0.86603, 1, 0, -4.3301], # my variant
        [0, 1.3038, 1.8439, 2.2583, 2.6077, 2.9155] # example
    ][SELECT_VARIANT_33]

    # N + 1
    u1 = 6
    # parametr with a0 at the bottom line
    u2 = sum(x_list)
    # parametr with a1 at the upper line
    v1 = u2
    # parametr with a1 at the bottom line
    v2 = sum([round(x**2, ROUNDING_RATIO) for x in x_list])
    # parametr after equal operator at the upper line
    c1 = sum(y_list)
    # at the bottom line
    c2 = sum([round(x_list[i] * y_list[i], ROUNDING_RATIO) for i in range(len(x_list))])

    a1 = round((u1 * c2 - u2 * c1) / (u1 * v2 - u2 * v1), ROUNDING_RATIO)
    a0 = round((c1 - v1 * a1) / u1, ROUNDING_RATIO)

    F1_list = [round(a0 + a1 * x, ROUNDING_RATIO) for x in x_list]
    miss_sum1 = round(sum([(F1_list[i] - y_list[i])**2 for i in range(len(F1_list))]), ROUNDING_RATIO)

    a2: float = [
        0.3284, # my variant
        -0.0355,
    ][SELECT_VARIANT_33]
    a1: float = [
        1.0213, # my variant
        0.6193,
    ][SELECT_VARIANT_33]
    a0: float = [
        0.3284, # my variant
        0.1295,
    ][SELECT_VARIANT_33]

    F2_list = [round(a0 + a1 * x + a2 * x**2, ROUNDING_RATIO) for x in x_list]
    miss_sum2 = round(sum(
            [(F2_list[i] - y_list[i])**2 for i in range(len(F2_list))]), ROUNDING_RATIO
        )

    return {
        'x_list': x_list,
        'y_list': y_list,
        'f1_list': F1_list,
        'miss1': miss_sum1,
        'f2_list': F2_list,
        'miss2': miss_sum2,
    }


def run_through_34():
    X = [
        0.4,
        0.2,
    ][SELECT_VARIANT_34]
    x_list = [
        [0, 0.2, 0.4, 0.6, 0.8],
        [0.0, 0.1, 0.2, 0.3, 0.4],
    ][SELECT_VARIANT_34]
    y_list = [
        [0, 0.048856, 0.23869, 0.65596, 1.4243],
        [1, 1.1052, 1.2214, 1.3499, 1.4918], # example
    ][SELECT_VARIANT_34]

    x_index = 2
    yleft = (y_list[x_index] - y_list[x_index - 1]) / \
        (x_list[x_index] - x_list[x_index - 1])

    yright = (y_list[x_index + 1] - y_list[x_index]) / \
        (x_list[x_index + 1] - x_list[x_index])

    first_derivative = (y_list[x_index] - y_list[x_index - 1]) / \
            (x_list[x_index] - x_list[x_index - 1]) + \
            ( \
                (y_list[x_index + 1] - y_list[x_index]) / \
                (x_list[x_index + 1] - x_list[x_index]) - \
                (y_list[x_index] - y_list[x_index - 1]) / \
                (x_list[x_index] - x_list[x_index - 1])
            ) * (2 * X - x_list[x_index - 1] - x_list[x_index]) / \
            (x_list[x_index + 1] - x_list[x_index - 1])

    second_derivative = 2 * (
            (y_list[x_index + 1] - y_list[x_index]) / \
            (x_list[x_index + 1] - x_list[x_index]) - \
            (y_list[x_index] - y_list[x_index - 1]) / \
            (x_list[x_index] - x_list[x_index - 1])
        ) / (x_list[x_index + 1] - x_list[x_index - 1])

    return {
        'x_list': x_list,
        'y_list': y_list,
        'X': X,
        'y_left': round(yleft, ROUNDING_RATIO),
        'y_right': round(yright, ROUNDING_RATIO),
        'f_der': round(first_derivative, ROUNDING_RATIO),
        's_der': round(second_derivative, ROUNDING_RATIO),
    }


def f_35(x):
    if SELECT_VARIANT_35 == 1: # example
        return x/(3*x + 4)**2
    return 4*x**3 + x**2


def F_letter(x):
    if SELECT_VARIANT_35 == 1: # example
        return math.log(abs(3*x + 4))/9 + 4/(9*(3*x + 4))
    return x**4 + (x**3)/3


def integ_f_35(a, b):
    return F_letter(b) - F_letter(a)


def generate_x(x0, xn, h):
    result_list = [x0]
    while result_list[-1] < xn:
        result_list.append(result_list[-1] + h)
    return result_list


def square(h, y_list, x_list):
    parts = []
    for i in range(len(y_list) - 1):
        parts.append(f_35((x_list[i] + x_list[i + 1]) / 2))
    result = [0]
    memory_sum = 0
    for part in parts:
        memory_sum += part
        result.append(round(h * memory_sum, ROUNDING_RATIO + 1))
    return result


def trapezoid(h, y_list):
    parts = [y_list[0] / 2]
    for i in range(1, len(y_list) - 1):
        parts.append(y_list[i])
    parts.append(y_list[-1] / 2)
    result = [0]
    memory_sum = 0
    for part in parts:
        memory_sum += part
        result.append(round(h * memory_sum, ROUNDING_RATIO + 1))
    return result


def simpson(h, y_list):
    parts = []
    is_required_four = True
    for i in range(len(y_list)):
        if i == 0 or i == len(y_list) - 1:
            parts.append(y_list[i])
        elif is_required_four:
            parts.append(4 * y_list[i])
            is_required_four = False
        else:
            parts.append(2 * y_list[i])
            is_required_four = True
    result = [0]
    memory_sum = y_list[0]
    for i in range(1, len(parts), 2):
        memory_sum += parts[i] + parts[i + 1]
        result.append(round(h/3 * memory_sum, ROUNDING_RATIO + 1))
    return result


def runge_romberg_rich_method(h1, F1, h2, F2, p):
    if h1 < h2:
        return F1 + (F1 - F2) / ((h2 / h1)**p - 1)
    return F2 + (F2 - F1) / ((h1 / h2)**p - 1)


def rectangle_method(a, b, h, y):
    integ = 0.0
    x = a
    while x < b:
        integ += y(x + h / 2)
        x += h
    return h*integ


def run_through_35():
    x0, xn = [
        (1, 5),
        (-1, 1),
    ][SELECT_VARIANT_35]
    h1, h2 = [
        (1, 0.5),
        (0.5, 0.25),
    ][SELECT_VARIANT_35]

    x_list1, x_list2 = generate_x(x0, xn, h1), generate_x(x0, xn, h2)
    y_list1, y_list2 = [round(f_35(x), ROUNDING_RATIO + 1) for x in x_list1], \
        [round(f_35(x), ROUNDING_RATIO + 1) for x in x_list2]

    square_list1, square_list2 = square(h1, y_list1, x_list1), \
        square(h2, y_list2, x_list2)

    trapez_list1, trapez_list2 = trapezoid(h1, y_list1), \
                        trapezoid(h2, y_list2)

    simpson_list1, simpson_list2 = simpson(h1, y_list1), simpson(h2, y_list2)

    real_solution = [
        665.33333,
        -0.16474,
    ][SELECT_VARIANT_35]

    p = 2
    rung_square = runge_romberg_rich_method(h1, square_list1[-1], h2, square_list2[-1], p)
    g_integ = integ_f_35(x_list1[0], x_list1[-1])

    p = 2
    rung_trapez = runge_romberg_rich_method(h1, trapez_list1[-1], h2, trapez_list2[-1], p)

    p = 2
    rung_simpson = runge_romberg_rich_method(h1, simpson_list1[-1], h2, simpson_list2[-1], p)

    return {
        'x_list_1': x_list1,
        'x_list_2': x_list2,
        'y_list_1': y_list1,
        'y_list_2': y_list2,
        'square_list1': square_list1,
        'square_list2': square_list2,
        'trap_list1': trapez_list1,
        'trap_list2': trapez_list2,
        'simp_list1': simpson_list1,
        'simp_list2': simpson_list2,
        'real_solution': real_solution,
        'h1': h1,
        'h2': h2,
        'rung_square': round(rung_square, 5),
        'square_ratio': abs(g_integ - rung_square),
        'rung_trapez': round(rung_trapez, 5),
        'trapez_ratio': abs(g_integ - rung_trapez),
        'rung_simpson': round(rung_simpson, 5),
        'simpson_ratio': abs(g_integ - rung_simpson),
    }
