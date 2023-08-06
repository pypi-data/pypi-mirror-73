#can only calculate regular polygon
def calculate(dimension, n_o_e, types, typed, a=1, b=1, h=1, r=1, material=None):
    def two_dimension():
        import math
        if n_o_e == 3:
            h_sanjiaoxing = math.sqrt(n_o_e ** 2 - (n_o_e / 2) ** 2)
            s = a * h
            c = 3 * a
            if typed == 'c':
                return c
            elif typed == 's':
                return s
            else:
                return None
        elif n_o_e == 4:
            if types == 'square':
                s = a ** 2
                c = 4 * a
                if typed == 'c':
                    return c
                elif typed == 's':
                    return s
                else:
                    return None
            elif types == 'rectangle':
                s = a * b
                c = a * 2 + b * 2
                if typed == 'c':
                    return c
                elif typed== 's':
                    return s
                else:
                    return None
            elif types == 'parallelogram':
                s = a * h
                if typed == 's':
                    return s
                else:
                    return None
            elif types == 'trapezoid':
                s = (a + b) * h / 2
                if typed == 's':
                    return s
                else:
                    return None
            else:
                return None