from selenium import webdriver

def getBrowser(url):

    phantomJSPath = "C:/phantomjs-2.1.1-windows/bin/phantomjs.exe "

    browser = webdriver.PhantomJS(phantomJSPath)

    browser.get(url)
    browser.implicitly_wait(3)

    return browser

def quitBrowser(browser):
    browser.quit()