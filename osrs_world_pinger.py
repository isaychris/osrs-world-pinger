from bs4 import BeautifulSoup
import subprocess
import collections
import requests
import re

url = "http://oldschool.runescape.com/slu?order=WMLPA"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

result = requests.get(url=url, headers=headers)
soup = BeautifulSoup(result.content, "html.parser")
table = soup.findAll("tr", "server-list__row")

server_list = {}

def get_ping(world):
    address = "oldschool{}.runescape.com".format(world)
    command = "ping {} -n 1".format(address)
    output = subprocess.check_output(command, shell=True).decode('utf-8')
    matches = re.findall("time=([\d.]+)ms", output)
    return int(matches[0])

def init_server_list():
    for row in table:
        data = row.find_all("td", class_="server-list__row-cell")
        w = data[0].text.split()[-1]
        p = data[1].text.split()[0]
        c, t, a, ping = data[2].text, data[3].text, data[4].text, None
        server_list[w] = {"players": p, "country": c, "type": t, "activity": a, "ping": 0}

def get_server_info(w):
    server_list[w]['ping'] = get_ping(w)
    return server_list[w]

def get_best_servers():
    print("Top Five Worlds: \n")
    print("{:<7} {:<20} {:<15} {:15} {:<10} {}".format("World", "Country", "Players", "Type", "Ping(ms)",
                                                       "Activity"))
    print("---------------------------------------------------------------------------------------")

    d = collections.OrderedDict(sorted(server_list.items(), key=lambda t: t[1]['ping']))

    count = 0
    for key, value in d.items():
        if count < 5:
            print("{:<7} {:<20} {:<15} {:<15} {:<10} {}".format(key, value["country"], value["players"],
                                                                value["type"], value["ping"], value["activity"]))
            count += 1

def main():
    print("// OSRS World Pinger - https://github.com/isaychris")
    print("// Press [enter] to ping ALL worlds OR enter a specific number. \n")
    init_server_list()

    x = input("Ping World[?]: ")

    print("{:<7} {:<20} {:<15} {:15} {:<10} {}".format("World", "Country", "Players", "Type", "Ping(ms) ", "Activity"))
    print("---------------------------------------------------------------------------------------")

    if x == "":
        for key, value in server_list.items():
            server = get_server_info(key)
            print("{:<7} {:<20} {:<15} {:<15} {:<10} {}".format(key, server["country"], server["players"],
                                                                server["type"], server["ping"], server["activity"]))

        print("=======================================================================================")

        get_best_servers()

    else:
        if x in server_list:
            server = get_server_info(x)
            print("{:<7} {:<20} {:<15} {:<15} {:<10} {}".format(x, server["country"], server["players"],
                                                                server["type"], server["ping"], server["activity"]))

        else:
            print("Unable to retrieve info for world [{}] ...".format(x))
main()
