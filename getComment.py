from bs4 import BeautifulSoup
import uuid

def getComments(delimiter, browser, articleId):

    # 댓글 추출

    form = browser.find_element_by_css_selector('a.u_cbox_btn_more')
    while True:
        btn_text = browser.find_element_by_css_selector("span.u_cbox_page_more").text
        if btn_text == '더보기':
            try:
                form.click()
            except:
                continue
        else:
            break

    # for i in range(0, 5):
    #     clickAllReplyBtns3(browser)
    #     print('a')
    # browser.save_screenshot("a.png")


    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

    # comments = soup.select("div.u_cbox_text_wrap > span.u_cbox_contents")

    comments = soup.find_all('div', class_='u_cbox_area')

    fileComment = open('comment.txt', 'a', encoding='UTF8')
    fileReply = open('reply.txt', 'a')

    # for comment in comments:
    #     fileComment.write(str(articleId) + delimiter) # 기사 ID
    #     commentId = uuid.uuid4()
    #     fileComment.write(str(commentId) + delimiter) # 댓글 ID
    #     #fileComment.write(str(commentId) + delimiter)  # 작성자 ID
    #     fileComment.write(comment.string + '\n')
    #     i = i + 1

    for item in comments:
        fileComment.write(str(articleId) + delimiter) # 기사 ID
        commentId = uuid.uuid4()
        fileComment.write(str(commentId) + delimiter) # 댓글 ID

        # 날짜
        cmtDate = item.select_one('span.u_cbox_date').next
        fileComment.write(str(cmtDate) + delimiter)

        # 작성자 ID
        userId = item.select_one('span.u_cbox_nick').next
        fileComment.write(str(userId) + delimiter)

        # 공감 수
        tmpLikeit = item.select_one('em.u_cbox_cnt_recomm')
        if tmpLikeit is None:
            fileComment.write("0" + delimiter)
        else:
            likeit = tmpLikeit.next
            fileComment.write(str(likeit) + delimiter)
        tmpLikeit = item.select_one('em.u_cbox_cnt_unrecomm')
        if tmpLikeit is None:
            fileComment.write("0" + delimiter)
        else:
            likeit = tmpLikeit.next
            fileComment.write(str(likeit) + delimiter)

        # 답글 수
        numReply = item.select_one('span.u_cbox_reply_cnt')
        if numReply is None:
            fileComment.write("0" + delimiter)
        else:
            fileComment.write(str(numReply.next) + delimiter)

        # 댓글
        comment = item.select_one('div.u_cbox_text_wrap > span.u_cbox_contents')
        if comment is None:
            fileComment.write("Deleted comment" + '\n')
        else:
            fileComment.write(comment.string + '\n')
            # try:
            #     fileComment.write(comment.string + '\n')
            # except UnicodeEncodeError:
            #     fileComment.write("Error: Invalid unicode character included" + '\n')

    fileComment.close()
    fileReply.close()

def clickAllReplyBtns(browser):
    j=0
    form = browser.find_element_by_css_selector('a.u_cbox_btn_reply')
    while True:
        btn_text = browser.find_element_by_css_selector("strong.u_cbox_reply_txt").text
        if btn_text == '답글':
            try:
                form.click()
                print(form.enabled())
            except:
                continue
        else:
            break

def clickAllReplyBtns2(browser):

    count=0
    btnsFold = []
    btns = []
    btns = browser.find_elements_by_class_name('u_cbox_btn_reply')
    for item in btns:
        while True:
            if count == len(btnsFold):
                item.click()
                del btnsFold[:]
                btnsFold = browser.find_elements_by_class_name('u_cbox_btn_fold')
            else:
                count=count+1
                print(count)

                break

def clickAllReplyBtns3(browser):
    btns = browser.find_elements_by_class_name('u_cbox_btn_reply')
    for btn in btns:
        try:
            btn.click()
        except:
            pass



#def getReplys():