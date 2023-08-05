def format_percentage_number(number: float) -> str:
    """ Puts a number as a percentage """
    if abs(number) < 0.1:
        return '{percent:.2%}'.format(percent=number)
    elif abs(number) >= 0.1 and abs(number) < 1:
        return '{percent:.1%}'.format(percent=number)
    else:
        return '{percent:,.0%}'.format(percent=number).replace(',', ' ')


def format_spaced_number(number: float) -> str:
    """Write a number grouped by baskets of 3 numbers"""
    return '{:,}'.format(number).replace(',', ' ')


def format_large_number(number: float) -> str:
    """Enables to write large numbers efficiently"""
    k = float(1000)
    M = float(k ** 2)
    B = float(k ** 3)
    T = float(k ** 4)

    if abs(number) < k:
        return '{0:.3g}'.format(number)
    elif k <= abs(number) < M:
        return '{0:.3g}k'.format(number / k)
    elif M <= abs(number) < B:
        return '{0:.3g}M'.format(number / M)
    elif B <= abs(number) < T:
        return '{0:.3g}B'.format(number / B)
    elif T <= abs(number):
        return '{0:.3g}T'.format(number / T)


def format_devise_number(number: float, devise: str) -> str:
    """It is expected that devise is '$', '€' or '£'"""
    return format_large_number(number)+devise
