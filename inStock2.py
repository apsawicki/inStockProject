from bs4 import BeautifulSoup
import requests
import os
import discord
from dotenv import load_dotenv
import asyncio

# 3070: https://www.newegg.com/p/pl?N=100007709%20601357250
# 1060: https://www.newegg.com/p/pl?d=gtx+1060

stockStatus = {"inStock": [], "outStock": [], "allStock": []}

productInfo = {"name": [], "price": [], "img": [], "shipping": []} # make the "name" array into another dictionary and have a timer next to the item when it was called "name": {"timer" : "product name"}



def Diff(li1, li2): # gets the difference of a list
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))



def newEggList(): # makes a list with items that are inStock
    print("newEggList")
    url = 'https://www.newegg.com/p/pl?d=gtx+1060'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    containerElement = soup.find_all(class_='item-img')
    print(containerElement)

    indexList = 0

    for link in containerElement:
        print("product url: " + link.get('href'))
        stockStatus['allStock'].append(link.get('href')) # adds every single product url to url list # ERROR

        print("after")
        if soup.find(class_='item-promo').text == 'OUT OF STOCK':
            stockStatus['outStock'].append(link.get('href')) # if it sees the out of stock class it adds the url of the product to outStock list


        indexList = indexList + 1


    stockStatus['inStock'] = Diff(stockStatus['allStock'], stockStatus['outStock']) # creates inStock list by subtracting the lists url by outStock

    print("end newEggList")




def newEggPage(): # checks each of the items in the inStock list
    print("newEggPage")
    index = 0

    for link in stockStatus['outStock']: # gets product information for each link in the list inStock
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')


        priceElement = soup.find(class_='price-current') # product price
        productInfo['price'].append(priceElement.text)

        nameElement = soup.find(class_='product-title') # product name
        productInfo['name'].append(nameElement.text)

        imgElement = soup.find(class_='swiper-zoom-container') # product image
        productInfo['img'].append(imgElement.find('img').get('src'))

        shippingElement = soup.find(class_='price-ship') # product shipping cost
        if shippingElement.text.rstrip(" Shipping ()") != "":
            productInfo['shipping'].append(shippingElement.text.rstrip(" Shipping ()"))
        else:
            productInfo['shipping'].append("null")

    print("end newEggPage")
            
        
        

def discordBot():
    client = discord.Client()

    print("inStockBot has started:")
    load_dotenv()
    TOKEN = 'NzgwMjM1ODA5MzUzMTA1NDI5.X7sJOQ.LKW0_EZr5qjJD3Kg7MQJo9JPCpc'


    async def printStock():
        await client.wait_until_ready()
        while not client.is_closed():
            try:
                
                newEggList()

                newEggPage()
                
                channel = client.get_channel(780551336810774558)
                for name, price, img, shipping, link in zip(productInfo["name"], productInfo["price"], productInfo["img"], productInfo["shipping"], stockStatus["inStock"]):
                    await channel.send(name)
                    await channel.send(img)
                    await channel.send(price)
                    await channel.send(shipping)
                    await channel.send(link)
                    print("WORKING")

                await asyncio.sleep(5)
            except Exception as e:
                print(e)
                print("EXCEPTION")
                await asyncio.sleep(5)
 

    client.loop.create_task(printStock())
    client.run(TOKEN)



    

discordBot()