import yahoo_fin.stock_info as si

def high_gained_earnings():
    tickers = si.tickers_sp500()
    gainers= si.get_day_gainers()
    gainers_from_in_tickers = []
    for ticker in tickers:
        if ticker in gainers['Symbol'].values:
            gainers_from_in_tickers.append(gainers.loc[gainers['Symbol'] == ticker].to_dict('r')[0])
    return gainers_from_in_tickers
gainers = high_gained_earnings()


