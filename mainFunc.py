import getArticle
import BrowserManager
from selenium.webdriver.support.ui import WebDriverWait
import getComment
import shutil
import os
import time

if __name__ == "__main__":

    # 텍스트 파일 백업
    now = time.localtime()
    timeFormat = "%04d-%02d-%02d_%02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    backupDir = os.path.expanduser('backup/' + timeFormat)
    os.mkdir(backupDir)
    shutil.copy('article.txt', backupDir + '/article.txt')
    shutil.copy('comment.txt', backupDir + '/comment.txt')
    shutil.copy('reply.txt', backupDir + '/reply.txt')
    print('Backup to ' + 'directory of "' + timeFormat + '" is completed\n')

    delimiter = '!$?'
    baseUrl = "http://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId=000&date="
    startDate = 20170901

    currentDate = startDate
    month = str(startDate)[4:6]

    if month == '01' or month == '03' or month == '05' or month == '07' or month == '08' or month == '10' or month == '12':
        endDate = startDate + 30
    elif month == '02':
        endDate = startDate + 27
    elif month == '04' or month == '06' or month == '09' or month == '11':
        endDate = startDate + 29
    else:
        print('Invalid month')
        exit(0)

    cssElements = open('cssElements.txt', 'r')
    elements = cssElements.readlines()
    cssElements.close()

    while currentDate <= endDate:
        i = 0
        url = baseUrl
        url = url + str(currentDate)
        browser = BrowserManager.getBrowser(url)

        print(currentDate, 'starts')

        for element in elements:
            btn = browser.find_element_by_css_selector(element)
            btn.click()
            WebDriverWait(browser, timeout=5000).until(lambda x: x.find_elements_by_class_name('u_cbox_list'))
            articleId = getArticle.getArticleBody(delimiter, browser)

            # print(currentDate, 'the aricle', i, ': body is completed')
            print('         the aricle ' + str(i) + ': body is completed')

            WebDriverWait(browser, timeout=5000).until(lambda x: x.find_elements_by_class_name('u_cbox_list'))

            getComment.getComments(delimiter, browser, articleId)
            # print(currentDate, 'the aricle', i, ': comment is completed')
            print('                       comment is completed')

            browser.back()
            browser.back()

            i = i + 1

        currentDate = currentDate + 1
        BrowserManager.quitBrowser(browser)

        # print(currentDate, 'is completed\n')
        print('         is completed\n')

    print(month, 'is completed')





