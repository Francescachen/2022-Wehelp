import urllib.request as req
from bs4 import BeautifulSoup


# ---------------main program-------------------
# searchURL = baseURL + specialURL
# 透過每次更新specialURL來實現連續抓取頁面
baseURL = "https://www.ptt.cc/"
specialURL = "bbs/movie/index.html"

page = 1
# 個別存放: 好雷, 普雷, 無雷
set1 = []
set2 = []
set3 = []
while page<=10:
    searchURL = baseURL + specialURL
    
    # 設定網頁請求的參數, 包括網址(url), 請求的身分(headers)
    request = req.Request(
        searchURL,
        headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }
    )
    # 取得資料, 並用BeautifulSoup()包成一個物件, 使他可以像存取字典一樣的方式去存取html text.
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    document = BeautifulSoup(data,'html.parser')
    links = document.find_all("div", class_="title")
    for link in links:
        if link.a != None:
            title = link.a.text
            if "[好雷]" in title:
                set1.append(title)
            elif "[普雷]" in title:
                set2.append(title)
            elif "[無雷]" in title:
                set3.append(title)
            else:
                continue
    specialURL = document.find("a", string="‹ 上頁").get("href")
    page = page+1

# 將剛剛已分類好的標題資料, 一次寫入達成排序的結果
with open("movie.txt", mode="w") as file:
    for data in (set1+set2+set3):
        file.write(data + "\n")
    
    