from twitchio.ext import commands
from twitchio.client import Client
import random
import requests
import bs4
from keep_alive import keep_alive

clientid = 'xxx'
client_secret = 'xxx'
oauth = 'xxx'

bot = commands.Bot(
    irc_token= oauth,
    client_id= clientid,
    nick='2toesbot',
    prefix= '!',
    initial_channels= ['tommy_2_toes']
)

client = Client(
    client_id= clientid,
    client_secret= client_secret,
)

@bot.event
async def event_message(ctx):
    print(ctx.author.name, ctx.content)
    await bot.handle_commands(ctx)

@bot.command(name= 'odds')
async def odds(ctx):
    if ctx.content.strip() == '!odds':
        await ctx.send('How am I supposed to give you the odds of nothing? Nimwad!')
        return None
    sentence = ctx.content.split('!odds')[1]
    odds = random.randint(0, 100)
    await ctx.send(f'There is a {odds}% chance that{sentence}')

@bot.command(name= 'trump')
async def trump(ctx):
    quote = requests.get('https://www.tronalddump.io/random/quote').json()['value']
    await ctx.send(quote)

@bot.command(name= 'price')
async def price(ctx):
    if ctx.content.strip() == '!price':
        await ctx.send('Gimmie a ticker ya nimwad!')
        return None
    try:
        ticker = ctx.content.split('!price')[1].lstrip().upper()
        yahoo_res = requests.get(f'https://finance.yahoo.com/quote/{ticker}/')
        yahoo_html = bs4.BeautifulSoup(yahoo_res.content, 'html5lib')
        price = yahoo_html.find_all('span', class_ = 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')[0].text
        await ctx.send(f'The price of {ticker} is currently ${price}')
    except:
        await ctx.send(f'Enter a valid ticker ya nimwad!')
        return None

@bot.command(name= 'bot')
async def bot_response(ctx):
    await ctx.send(f'I was created with Python and the Twitchio API wrapper by the illustrious streamer, tommy_2_toes')

@bot.command(name= 'who')
async def get_chatters(ctx):
    chatters = await client.get_chatters('tommy_2_toes')
    all_chatters = ', '.join(chatters.all)
    await ctx.send(f"In chat: {all_chatters}")

if __name__ == '__main__':
    keep_alive()
    bot.run()
