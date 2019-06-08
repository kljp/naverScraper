from bs4 import BeautifulSoup
import re
import uuid

def getArticleBody(delimiter, browser):

    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

    # 기사 추출

    fileArticle = open('article.txt', 'a', encoding='UTF8')

    # 기사 날짜
    articleDate = soup.select_one("div.sponsor > span.t11")
    fileArticle.write(articleDate.string)
    fileArticle.write(delimiter)

    # 기사 ID
    articleId = uuid.uuid4()
    fileArticle.write(str(articleId))
    fileArticle.write(delimiter)

    # 공감 수 (좋아요, 훈훈해요, 슬퍼요, 화나요, 후속기사 원해요)
    likeit = soup.select_one('a[data-type="like"] > span.u_likeit_list_count._count')
    fileArticle.write(likeit.string + delimiter)
    likeit = soup.select_one('a[data-type="warm"] > span.u_likeit_list_count._count')
    fileArticle.write(likeit.string + delimiter)
    likeit = soup.select_one('a[data-type="sad"] > span.u_likeit_list_count._count')
    fileArticle.write(likeit.string + delimiter)
    likeit = soup.select_one('a[data-type="angry"] > span.u_likeit_list_count._count')
    fileArticle.write(likeit.string + delimiter)
    likeit = soup.select_one('a[data-type="want"] > span.u_likeit_list_count._count')
    fileArticle.write(likeit.string + delimiter)

    # 성별
    gender = soup.select_one('div.u_cbox_chart_progress.u_cbox_chart_male > span.u_cbox_chart_per').next
    fileArticle.write(str(gender) + delimiter)
    gender = soup.select_one('div.u_cbox_chart_progress.u_cbox_chart_female > span.u_cbox_chart_per').next
    fileArticle.write(str(gender) + delimiter)

    # 연령 (10대, 20대, 30대, 40대, 50+대)
    ages = soup.find('div', class_='u_cbox_chart_age')
    for item in ages:
        age = item.find('span', class_='u_cbox_chart_per').next
        fileArticle.write(str(age) + delimiter)

    # 기사 본문
    articleContent = ''
    articleContents = soup.find_all('div', id='articleBodyContents')
    for item in articleContents:
        articleContent = articleContent + str(item.find_all(text=True))

    articleContent = re.sub('[a-zA-Z]', '', articleContent)
    articleContent = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                            '', articleContent)

    fileArticle.write(articleContent + '\n')

    fileArticle.close()

    form = browser.find_element_by_css_selector('a.u_cbox_btn_view_comment')
    form.click()

    return articleId


