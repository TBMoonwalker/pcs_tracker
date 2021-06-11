from web3 import Web3
from bscscan import BscScan
import asyncio 
import requests, json
import datetime, time, os, curses
import sqlite3

# Initialize screen
curses.initscr()
curses.start_color()

# Color scheme
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

# PancakeSwap information
pancakeswap_factory_abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

# Open JSON file
try:
    f = open('config.json')
    config = json.load(f)
except:
    print("No or missconfigured configuration file")

# Configuration parameter
for conf in config['config']:
    blockchain_url = conf['blockchain_url']
    bsc_api_key = conf['bsc_api_key']
    currency_api_key = conf['currency_api_key']
    currency = conf['currency']
    pancakeswap_factory = conf['pancakeswap_factory']
    bnb_busd_pair_address = conf['bnb_busd_pair_address']
    refresh_interval = conf['refresh_interval']

# Initialize database
con = sqlite3.connect('pcs_tracker.db')
c = con.cursor()

# Connect to blockchain node
try:
    blockchain = Web3(Web3.HTTPProvider(blockchain_url))
except:
    print("Node not connected")

def init_database():
    with con:
        c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='price'")
        if c.fetchone()[0] != 1:
            c.execute("CREATE TABLE price (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date DATE, price FLOAT, tokenamount FLOAT, balance INT, profit INT, token_id INT)")

def set_history(token_id, price, tokenamount, balance, profit):
    with con:
        c.execute(f"SELECT date FROM price WHERE token_id='{token_id}'")
        if not c.fetchone():
            c.execute(f"INSERT INTO PRICE(date, price, tokenamount, balance, profit, token_id) VALUES ('{datetime.datetime.now()}', '{price}', '{tokenamount}', '{balance}', '{profit}', '{token_id}')")
        else:
            c.execute(f"SELECT * FROM price WHERE token_id='{token_id}'")
            column = [d[0] for d in c.description]
            data = [dict(zip(column, row)) for row in c.fetchall()]
            return data

def calc_diff(value, history, percent=False):
    if percent:
        diff = ((value - history) / history) * 100
    else:
        diff = value - history
    return round(diff, 2)

def exchange_rate(currency):
    url = "https://free.currconv.com/api/v7/convert?q=USD_{0}&compact=ultra&apiKey={1}".format(currency, currency_api_key)
    return (float)(requests.get(url).json()["USD_{0}".format(currency)])

def token_price(pair_address, decimal_token0, decimal_token1):
    contract = blockchain.eth.contract(address=pair_address, abi=pancakeswap_factory_abi);
    reserve = contract.functions.getReserves().call()
    reserve_token0 = reserve[0]
    reserve_token1 = reserve[1]
    token_price = (reserve_token1 / 10 ** decimal_token1) / (reserve_token0 / 10 ** decimal_token0)
    return token_price

async def token_amount(token_address, wallet):
    async with BscScan(bsc_api_key) as client:
        return (
            await client.get_acc_balance_by_token_contract_address(contract_address=token_address, address=wallet)
        )

def create_table(description, price, tokencount, balance, profit, coord, token_history, price_history, balance_history, profit_history):
    wname = curses.newwin(5, 15, (1+coord), 10)
    wname.border(0)
    wname.addstr(1, 2, "Token", curses.color_pair(1))
    wname.addstr(3, 2, description['token_name'], curses.A_BOLD)
    wname.refresh()

    if (price_history < 0):
        colorpair = curses.color_pair(2)
    else:
        colorpair = curses.color_pair(1)

    wvalue = curses.newwin(5, 42, (1+coord), 25)
    wvalue.border(0)
    wvalue.addstr(1, 2, "Value", curses.color_pair(1))
    wvalue.addstr(1, 30, "Change %", curses.color_pair(1))
    wvalue.addstr(3, 2, str(price))
    wvalue.addstr(3, 30, str(price_history), colorpair)
    wvalue.refresh()

    wamount = curses.newwin(5, 42, (1+coord), 67)
    wamount.border(0)
    wamount.addstr(1, 2, "Token amount", curses.color_pair(1))
    wamount.addstr(1, 22, "Additional tokens", curses.color_pair(1))
    wamount.addstr(3, 2, str('{:,.0f}'.format(tokencount)))
    wamount.addstr(3, 22, str('{:,.0f}'.format(token_history)))
    wamount.refresh()

    if (balance_history < 0):
        colorpair = curses.color_pair(2)
    else:
        colorpair = curses.color_pair(1)
    
    wbalance = curses.newwin(5, 25, (1+coord), 109)
    wbalance.border(0)
    wbalance.addstr(1, 2, "Balance", curses.color_pair(1))
    wbalance.addstr(1, 15, "Change %", curses.color_pair(1))
    wbalance.addstr(3, 2, str(balance))
    wbalance.addstr(3, 15, str(balance_history), colorpair)
    wbalance.refresh()

    if (profit_history < 0):
        colorpair = curses.color_pair(2)
    else:
        colorpair = curses.color_pair(1)

    wprofit = curses.newwin(5, 25, (1+coord), 134)
    wprofit.border(0)
    wprofit.addstr(1, 2, "Profit", curses.color_pair(1))
    wprofit.addstr(1, 15, "Change %", curses.color_pair(1))
    wprofit.addstr(3, 2, str(profit))
    wprofit.addstr(3, 15, str(profit_history), colorpair)
    wprofit.refresh()
        
def main():
    token_history = 0
    price_history = 0
    balance_history = 0
    profit_history = 0

    init_database()

    while True:
        coord = 0
        rate = exchange_rate(currency)

        for i in config['tokens']:
            coord = coord + 5
            tokencount = round(int(asyncio.run(token_amount(i['token_address'], i['wallet']))) / 1000000000)
            
            if (i['token_currency'] == "BUSD"):
                tprice = token_price(i["token_pair"], i["decimal_token0"], i["decimal_token1"])
                price = '%.18f' % tprice
            # convert WBNB to BUSD
            else:
                bprice = token_price(bnb_busd_pair_address, 18, 18)
                tprice = token_price(i["token_pair"], i["decimal_token0"], i["decimal_token1"])
                price = '%.18f' % (bprice * tprice)
                   
            balance = int( (float(price) * tokencount) * rate)
            profit = int(balance - int(i['investment']))
            
            # Write initial values to history database
            history = set_history(i['id'], price, tokencount, balance, profit)
            # Calculate differences since start
            if history:  
                token_history = calc_diff(tokencount, history[0]['tokenamount'])
                price_history = calc_diff(float(price), history[0]['price'], percent=True)
                balance_history = calc_diff(balance, history[0]['balance'], percent=True)
                profit_history = calc_diff(profit, history[0]['profit'], percent=True)

            create_table(i, price, tokencount, balance, profit, coord, token_history, price_history, balance_history, profit_history)
            

        time.sleep(refresh_interval)

if __name__ == "__main__":
    main()
