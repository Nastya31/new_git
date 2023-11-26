import threading
import time
import psutil
import pandas as pd


def get_cpu_temp(date, time_list, queuee):
    while True:
        time.sleep(60)
        date.append(psutil.cpu_stats().ctx_switches)
        time_list.append(f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}")
        queuee.append("Число переключений контекста")


def memory(mem_date, time_list, queuee):
    while True:
        time.sleep(60)
        mem_date.append(psutil.virtual_memory().percent)
        time_list.append(f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}")
        queuee.append("Процент использования памяти, проценты")


def collecter(work_time: float):
    time_list = []

    date = []
    queuee = []
    t1 = threading.Thread(target=get_cpu_temp, args=(date, time_list, queuee,), daemon=True)
    t2 = threading.Thread(target=memory, args=(date, time_list, queuee,), daemon=True)

    t1.start()
    t2.start()

    delta = 0
    start_time = time.time()
    while (delta <= work_time):
        delta = time.time() - start_time

    t1.join(0.1)
    t2.join(0.1)

    print(time_list)
    print(queuee)
    print(date)

    table = pd.DataFrame({"Время": time_list, "Процесс": queuee, "Данные": date})
    table.to_csv("table.csv", sep=";")

if __name__ == '__main__':
    collecter(125)