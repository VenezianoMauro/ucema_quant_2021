
from pyhomebroker import HomeBroker
import datetime

hb = HomeBroker(209)

# Authenticate with the homebroker platform
hb.auth.login(dni='30137750', user='manum1983', password='Morgan@06', raise_exception=True)

# Connect to the server
hb.online.connect()

hb.online.subscribe_options()

symbol = 'SUPV'
from_date= datetime.date(2020, 1, 1)
to_date = datetime.date(2020, 6, 1)

history = hb.history.get_daily_history(symbol, from_date,to_date)
    
# Get the market snapshot
snapshot = hb.online.get_market_snapshot()

panel_1 = snapshot['options']

hb.online.subscribe_personal_portfolio()

port = hb.online.

def optionsfn(online, quotes):
    print(quotes)

hb.online.subscribe_personal_portfolio()
panel_2 = hb.online.subscribe_options





# Save each board with its settlements to a CSV file
#date = '{}'.format(datetime.now().strftime('%Y%m%d'))
#for board in snapshot:
#    snapshot[board].to_csv('{}_{}.csv'.format(date, board))