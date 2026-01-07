import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup as bs

from util.nowtime import TaiwanTime

def news_summary(keyword: str, page: int=1) -> pd.DataFrame:
    """
    爬取 udn新聞網 新聞摘要。
    Returns:
        DataFrame: 時間戳、新聞標題、摘要、網址、來源。
    """
    df = get_udn_news_summary(keyword, page=page)

    df.sort_values(by='TimeStamp', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def get_udn_news_summary(keyword, page=1) -> pd.DataFrame:
    """
    爬取 udn新聞網 指定股票的新聞資料「摘要」。
    Returns:
        DataFrame: 時間戳、新聞標題、摘要、網址、來源。
    """
    data = []
    col = ["TimeStamp", "Title", "Summary", "Url", "Source"]

    udn_url = f"https://udn.com/api/more?page={page}&id=search:{keyword}&channelId=2&type=searchword&last_page=100"
    udn_json_news = requests.get(udn_url).json()['lists']
    for item in udn_json_news:
        url = item['titleLink']
        # if not url.startswith('https://udn.com/news'): continue  # 跳過專欄文章
        title = item['title']
        summary = item['paragraph']
        time_str = item['time']['dateTime']
        if len(time_str) == 16:  time_str += ":00"  # 補足秒數
        timestamp = int(datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=TaiwanTime.TIMEZONE).timestamp())   # 轉成時間戳（單位：秒）
        data.append([timestamp, title, summary, url, 'udn'])
    return pd.DataFrame(data, columns=col)


def parse_article(url: str, source: str='udn') -> str:
    """
    爬取指定新聞網址的完整內容。
    Args:
        url (str): 新聞網址
        source (str): 新聞來源，預設為 'udn'。可選擇 'udn' 或 'cnyes'。
    Returns:
        str: 新聞內容文字
    """
    
    try:
        if source == 'udn':
            news = requests.get(url).text
            news_find = bs(news,'html.parser').find("section",class_="article-content__editor").find_all("p")[:-1]
            news_data = "\n".join(x.text.strip() for x in news_find)
            news_data = news_data.replace("\n\n","\n").strip()
            return news_data
        elif source == 'cnyes':
            news = requests.get(url).text
            news_bs = bs(news,'html.parser')
            news_find = news_bs.find("main",class_="c1tt5pk2")
            news_data = "\n".join(x.text.strip() for x in news_find)
            news_data = news_data.replace("　　　","").replace("\n\n","")
            delete_strings = ["歡迎免費訂閱", "精彩影片","粉絲團", "Line ID","Line@","來源："]
            for delete_str in delete_strings:
                index = news_data.find(delete_str)
                if index != -1:
                    news_data = news_data[:index]  # 只保留不包含該字串的部分
                    break
            return news_data
    except Exception as e:
        print(f"Error fetching article from {url}: {e}")
    return ""
