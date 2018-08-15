from bs4 import BeautifulSoup
import collections
import requests
import os

url = "http://oldschool.runescape.com/slu?order=WMLPA"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

result = requests.get(url=url, headers=headers)
soup = BeautifulSoup(result.content, "html.parser")
table = soup.findAll("tr", "server-list__row")

server_list = {}

def get_ping(world):
    address = "oldschool{}.runescape.com".format(world)
    result = os.popen('ping {} -n 1'.format(address)).readlines()
    first, *middle, last = result[-1].split()
    ms = int(''.join(list(filter(str.isdigit, last))))

    return ms

def get_server_list():
    for row in table:
        data = row.find_all("td", class_="server-list__row-cell")
        w = int(data[0].text.split()[-1])
        p = int(data[1].text.split()[0])
        c, t, a, ping = data[2].text, data[3].text, data[4].text, None
        server_list[w] = {"players": p, "country": c, "type": t, "activity": a, "ping": ping}

    for key, value in server_list.items():
        server_list[key]["ping"] = get_ping(key)
        print("{:<7} {:<20} {:<15} {:<15} {:<10} {}".format(key, value["country"], value["players"],
                                                            value["type"], value["ping"], value["activity"]))

def get_best_servers():
    d = collections.OrderedDict(sorted(server_list.items(), key=lambda t: t[1]['ping']))

    count = 0
    for key, value in d.items():
        if count < 5:
            print("{:<7} {:<20} {:<15} {:<15} {:<10} {}".format(key, value["country"], value["players"],
                                                                value["type"], value["ping"], value["activity"]))
            count += 1

def main():
    print("OSRS World Pinger - https://github.com/isaychris \n")
    print("{:<7} {:<20} {:<15} {:15} {:<10} {}".format("World", "Country", "Players", "Type", "Ping(ms) ", "Activity"))
    print("---------------------------------------------------------------------------------------")
    get_server_list()

    print("=======================================================================================")

    print("Top Five Worlds: \n")
    print("{:<7} {:<20} {:<15} {:15} {:<10} {}".format("World", "Country", "Players", "Type", "Ping(ms)", "Activity"))
    print("---------------------------------------------------------------------------------------")
    get_best_servers()

main()