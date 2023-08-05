def Tn(a1, n, d):
    return a1+((n-1)*d)


def Sn(a1, n, d):
    return ((n/2)*(2*a1 + (n-1)*d))


def find_mean1(a1, n, d):
    return (n/2*(2*a1 + (n-1)*d))/n


def find_mean2(a1, an):
    return (a1 + an) / 2


def find_d(am, an, m, n):
    if m == n:
        raise ValueError("m == n")
    return (am-an)/(m-n)
