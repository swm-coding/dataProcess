import re
import math
from pymongo import MongoClient

def _getCompany(text):
    companyList = [
        ['삼성', 'SAMSUNG'],
        ['LG', '엘지', '엘쥐'],
        ['ASUS', '에이수스'],
        ['APPLE', '맥', '애플', '아이맥'],
        ['한성'],
        ['HP'],
        ['LENOVO', '레노버', '레노보'],
        ['롯데']
    ]

    for companyNames in companyList:
        for companyName in companyNames:
            if companyName in text:
                return companyNames[0]

    return ''


def _getCpu(text):
    if "I3" in text:
        return 'Intel i3'

    if "I5" in text:
        return 'Intel i5'

    if "I7" in text:
        return 'Intel i7'


def _getRam(text):
    text = "\n" + text + "\n"
    ramDeclares = ['램', 'RAM']
    candidate = []

    for Declare in ramDeclares:
        idx = text.find(Declare)

        if text[idx - 1] == "그":
            idx = text.find(Declare, idx + 1)

        if idx == -1:
            continue

        # leave only one line that includes declare
        line = text[text.rfind("\n", 0, idx) + 1:text.find("\n", idx)]
        idx = line.find(Declare)

        post = re.search(r'\d+', line[idx:])
        if post != None:
            candidate.append(int(post.group()))
        pre = re.search(r'\d+', line[idx::-1])
        if pre != None:
            candidate.append(int(pre.group()[::-1]))

    if len(candidate) == 0:
        return -1

    def ramSort(val):
        if val <= 0:
            return -1
        return -bin(val).count("1") * 10000 - abs(math.log2(val) - 2.5) * 100 + val

    return sorted(candidate, key=ramSort, reverse=True)[0]


def _getSsd(text):
    # TODO: discuss whether to seperate ssd hdd
    text = "\n" + text + "\n"
    ssdDeclares = ['스스디', 'SSD', '하드']
    candidate = []

    for Declare in ssdDeclares:
        idx = text.find(Declare)

        if idx == -1:
            continue

        # leave only one line that includes declare
        line = text[text.rfind("\n", 0, idx) + 1:text.find("\n", idx)]
        idx = line.find(Declare)

        post = re.search(r'\d+', line[idx:])
        if post != None:
            candidate.append(int(post.group()))
        pre = re.search(r'\d+', line[idx::-1])
        if pre != None:
            candidate.append(int(pre.group()[::-1]))

    if len(candidate) == 0:
        return -1

    def ssdSort(val):
        if val <= 0:
            return -1
        return -bin(val).count("1") * 10 - abs(math.log2(val) - 7.5)

    return sorted(candidate, key=ssdSort, reverse=True)[0]


def _getDisplay(text):
    def _get_first_nbr_from_str(input_str):
        '''
        :param input_str: strings that contains digit and words
        :return: the number extracted from the input_str
        demo:
        'ab324.23.123xyz': 324.23
        '.5abc44': 0.5
        '''
        try:
            if not input_str and not isinstance(input_str, str):
                return 0
            out_number = ''
            for ele in input_str:
                if (ele == '.' and '.' not in out_number) or ele.isdigit():
                    out_number += ele
                elif out_number:
                    break
            return float(out_number)
        except ValueError:
            return -1.0

    def _get_last_nbr_from_str(input_str):
        '''
        :param input_str: strings that contains digit and words
        :return: the number extracted from the input_str
        demo:
        'ab324.23.123xyz': 23.123
        '.5abc44': 44
        '''
        input_str = input_str[::-1]
        try:
            if not input_str and not isinstance(input_str, str):
                return 0
            out_number = ''
            for ele in input_str:
                if (ele == '.' and '.' not in out_number) or ele.isdigit():
                    out_number += ele
                elif out_number:
                    break
            # print(out_number,out_number[::-1])
            return float(out_number[::-1])
        except ValueError:
            return -1.0

    text = "\n" + text + "\n"
    displayDeclares = ['인치', '"', "''"]
    candidate = []

    for Declare in displayDeclares:
        idx = text.find(Declare)

        if idx == -1:
            continue

        # leave only one line that includes declare
        line = text[text.rfind("\n", 0, idx) + 1:text.find("\n", idx)]
        idx = line.find(Declare)

        post = _get_first_nbr_from_str(line[idx:])
        if post != -1:
            candidate.append(post)
        pre = _get_last_nbr_from_str(line[:idx])
        if pre != -1:
            candidate.append(pre)

    if len(candidate) == 0:
        return -1.0

    def displaySort(val):
        return -abs(val - 14)

    return sorted(candidate, key=displaySort, reverse=True)[0]

def _getDisplayTech(text):
    List = ["OLED", "QLED", "UHD", "FHD", "HD"]

    for i in List:
        if i in text:
            return i

def _getRefgrigeratorSize(text):
    # TODO: 냉장고 용량 데이터 처리 '리터' 'L' 구분,
    return ''


def _getf2f(text):
    if "직거래" in text:
        return 1

    return 0

def Laptop(title, price, URL, time, text):

    company = _getCompany(title)
    f2f = _getf2f(text)
    cpu = _getCpu(text)
    ram = _getRam(text)
    ssd = _getSsd(text)
    display = _getDisplay(text)

    data = {
        "title" : title,
        "price" : price,
        "company" : company,
        "cpu" : cpu,
        "ram" : ram,
        "ssd" : ssd,
        "display" : display,
        "time" : time,
        "url" : URL,
        "text" : text,
        "f2f": f2f
    }

    client = MongoClient("mongodb://dev:dev@13.125.4.46:27017/test")
    coll = client.test.laptop
    coll.insert(data)

def Refrigerator(title, price, URL, time, text):

    company = _getCompany(text)
    size = _getRefgrigeratorSize(text)
    f2f = _getf2f(text)

    data = {
        "title": title,
        "price": price,
        "company": company,
        "size": size,
        "time": time,
        "url": URL,
        "text": text,
        "f2f": f2f
    }

    client = MongoClient("mongodb://dev:dev@13.125.4.46:27017/test")
    coll = client.test.refrigerator
    coll.insert(data)

def SmartPhone(title, price, URL, time, text):

    company = _getCompany(text)
    f2f = _getf2f(text)

    data = {
        "title": title,
        "price": price,
        "company": company,
        "time": time,
        "url": URL,
        "text": text,
        "f2f": f2f
    }

    client = MongoClient("mongodb://dev:dev@13.125.4.46:27017/test")
    coll = client.test.smartphone
    coll.insert(data)

def TV(title, price, URL, time, text):

    company = _getCompany(text)
    display = _getDisplay(text)
    displayTech = _getDisplayTech(text)
    f2f = _getf2f(text)

    data = {
        "title": title,
        "price": price,
        "company": company,
        "display": display,
        "displayTech" : displayTech,
        "time": time,
        "url": URL,
        "text": text,
        "f2f": f2f
    }

    client = MongoClient("mongodb://dev:dev@13.125.4.46:27017/test")
    coll = client.test.tv
    coll.insert(data)

def Washer(title, price, URL, time, text):

    company = _getCompany(text)
    f2f = _getf2f(text)

    data = {
        "title": title,
        "price": price,
        "company": company,
        "time": time,
        "url": URL,
        "text": text,
        "f2f": f2f
    }

    client = MongoClient("mongodb://dev:dev@13.125.4.46:27017/test")
    coll = client.test.washer
    coll.insert(data)
