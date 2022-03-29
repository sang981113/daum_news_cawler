from bs4 import BeautifulSoup as bs
import requests

i = 1
current_page = ""
while True:
    url = "https://news.daum.net/breakingnews/politics?page={}&regDate=20211101".format(i)

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    
    #마지막 페이지에 도달하면 종료
    if(current_page == soup.select_one('em.num_page')):
        break

    current_page = soup.select_one('em.num_page')
    i+=1

    #추천연재 제거를 위해 2번 검색
    news = soup.find(attrs={"class":"box_etc"}).find_all(attrs={"class":"tit_thumb"})

    for n in news:
        url = n.a["href"]#하이퍼 링크만 가져오기
        print(url)
        res = requests.get(url)
        soup = bs(res.text, 'html.parser')

        title = soup.select_one('h3.tit_view')
        re = soup.select_one('span.txt_info')
        num = soup.select_one('span.num_date')
        content = soup.select_one('div#harmonyContainer')

        news_crawling = "뉴스제목:"+title.text+" /기자:"+re.text+" /날짜:"+num.text+" /내용:"+content.text.strip()+"\n\n"

        with open("news_crawling.txt", "a", encoding="utf8") as f:
            f.write(news_crawling)
