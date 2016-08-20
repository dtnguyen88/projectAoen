import finsymbols


def get_constitutes(index):
    return {
        'amex': finsymbols.get_amex_symbols,
        'nyse': finsymbols.get_nyse_symbols,
        'nasdaq': finsymbols.get_nasdaq_symbols,
        'sp500': finsymbols.get_sp500_symbols
    }.get(index, [])()
