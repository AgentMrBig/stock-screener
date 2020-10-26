from tda import auth, client
import json
import td_ameritrade_config as config
import datetime

try: 
  c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
  from selenium import webdriver
  with webdriver.Chrome(executable_path='/Users/Admin/Python/stock-screener/chromedriver') as driver:
    c = auth.client_from_login_flow(
      driver, config.api_key, config.redirect_uri, config.token_path
    )
    
# r = c.get_price_history('AAPL',
#                         period_type=client.Client.PriceHistory.PeriodType.YEAR,
#                         period=client.Client.PriceHistory.Period.TWENTY_YEARS,
#                         frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
#                         frequency=client.Client.PriceHistory.Frequency.DAILY)
# assert r.ok, r.raise_for_status()
# print(json.dumps(r.json(), indent=4))

# response = c.get_quote('BA')

# print(response.json())

# response = c.search_instruments(['AAPL'],c.Instrument.Projection.FUNDAMENTAL)

# response = c.get_option_chain('AAPL')

# print(json.dumps(response.json(), indent=4))

# call options for a specific strike and date range
# response = c.get_option_chain('AAPL', contract_type=c.Options.ContractType.CALL, strike=116)

# print(json.dumps(response.json(), indent=4))
start_date = datetime.datetime.strptime('2020-10-27', '%Y-%m-%d')
end_date = datetime.datetime.strptime('2020-11-03', '%Y-%m-%d')
response = c.get_option_chain('AAPL', contract_type=c.Options.ContractType.CALL, strike=116, strike_from_date=start_date, strike_to_date=end_date)

print(json.dumps(response.json(), indent=4))