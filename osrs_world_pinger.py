from bs4 import BeautifulSoup
from threading import Thread
import subprocess
import collections
import requests
import queue
import re

num_threads = 16
ping_queue = queue.Queue()

url = "http://oldschool.runescape.com/slu?order=WMLPA"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

result = requests.get(url=url, headers=headers)
soup = BeautifulSoup(result.content, "html.parser")
table = soup.findAll("tr", "server-list__row")

server_list = {}

# thread code : wraps system ping command
def thread_pinger(i, q):
    while True:
        world = q.get()
        address = "oldschool{}.runescape.com".format(world)

        command = "ping {} -n 1".format(address)
        output = subprocess.check_output(command, shell=True).decode('utf-8')
        matches = re.findall("time=([\d.]+)ms", output)
        server_list[world]['ping'] = int(matches[0])
        q.task_done()

def init_server_list():
    for row in table:
        data = row.find_all("td", class_="server-list__row-cell")
        w = data[0].text.split()[-1]
        p = data[1].text.split()[0]
        c, t, a, ping = data[2].text, data[3].text, data[4].text, None
        server_list[w] = {"players": p, "country": c, "type": t, "activity": a, "ping": 0}

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
        for key in sorted(server_list.keys()):
            ping_queue.put(key)

        # start the thread pool
        for i in range(num_threads):
            worker = Thread(target=thread_pinger, args=(i, ping_queue))
            worker.setDaemon(True)
            worker.start()

        # wait until worker threads are done to exit
        ping_queue.join()

        for key, value in server_list.items():
            print("{:<7} {:<20} {:<15} {:<15} {:<10} {}".format(key, value["country"], value["players"],
                                                                value["type"], value["ping"], value["activity"]))

        print("=======================================================================================")
        get_best_servers()

    else:
        if x in server_list:
            ping_queue.put(x)

            # start the thread pool
            for i in range(num_threads):
                worker = Thread(target=thread_pinger, args=(i, ping_queue))
                worker.setDaemon(True)
                worker.start()

            # wait until worker threads are done to exit
            ping_queue.join()
            print("{:<7} {:<20} {:<15} {:<15} {:<10} {}".format(x, server_list[x]["country"],server_list[x]["players"],
                                                                server_list[x]["type"], server_list[x]["ping"],
                                                                server_list[x]["activity"]))

        else:
            print("Unable to retrieve info for world [{}] ...".format(x))
			
if __name__ == "__main__":
    main()