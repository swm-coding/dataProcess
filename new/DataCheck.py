import DataProcess

def DataCheck(title, price, URL, time, text):

    LaptopDeclares = ["노트북","맥북","MACBOOK","넷북","탭북","그램"]
    SmartPhoneDeclares = ["아이폰", "갤럭시", "갤럭시 노트", "갤럭시노트",
                  "LG V50", "LG V40", "LG V35", "LG V30",
                  "LG G8", "LG G7"]
    RefrigeratorDeclares = ["냉장고"]
    TVDeclares = ["TV", "텔레비젼", "텔레비전"]
    WasherDeclares = ["세탁기", "통돌이"]


    title = title.upper()
    text = text.upper()

    for Declare in LaptopDeclares:
        if Declare in title:
            DataProcess.Laptop(title, price, URL, time, text)
            return

    for Declare in SmartPhoneDeclares:
        if Declare in title:
            DataProcess.SmartPhone(title, price, URL, time, text)
            return

    for Declare in RefrigeratorDeclares:
        if Declare in title:
            DataProcess.Refrigerator(title, price, URL, time, text)
            return

    for Declare in TVDeclares:
        if Declare in title:
            DataProcess.TV(title, price, URL, time, text)
            return

    for Declare in WasherDeclares:
        if Declare in title:
            DataProcess.Washer(title, price, URL, time, text)
            return

    return False
