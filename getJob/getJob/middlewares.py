# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json

from scrapy import signals
import time

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.common.by import By


class GetjobSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GetjobDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    list_cookies = None
    def process_request(self, request, spider):
        # print(request.url)
        # 无头模式
        opt = Options()
        opt.add_argument("--headless")
        opt.add_argument("--disable-gpu")
        opt.add_argument("log-level=3")
        # opt.add_argument("--proxy-server=162.14.98.117:16817")  # selenium中设置代理
        # 规避检测
        chrome_opt = ChromeOptions()
        chrome_opt.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(executable_path="F:/pycharm/test/3.动态加载数据处理/chromedriver.exe", options=chrome_opt,
                                  chrome_options=opt)

        # 登录请求，获取cookie并保存
        if "login" in request.url:
            print("检测到登录请求")
            driver.get(request.url)
            time.sleep(5)
            driver.find_element(By.ID, "mask_body_item_username").send_keys("16737310919")
            driver.find_element(By.ID, "mask_body_item_newpassword").send_keys("abc12345.")
            driver.find_element(By.ID, "mask_body_item_login").click()
            time.sleep(2)
            self.list_cookies = driver.get_cookies()
            with open("./cookie.json", 'w') as fp:
                fp.write(json.dumps(self.list_cookies))
                print("cookie存储成功")
            # # 加载 cookie
            # with open("./cookie.json", "r") as fp2:
            #     list_cookies = json.loads(fp2.read())
            #     print("cookie存储成功")
            return None

        driver.get(request.url)  # 预请求，未携带cookie
        # 加载 cookie
        for cookie in self.list_cookies:
            cookie_dict = {
                "domain": ".58.com",
                # "expiry": int(cookie.get('expiry')),
                "httpOnly": False,
                "name": cookie.get('name'),
                "path": "/",
                "secure": False,
                "value": cookie.get('value')
            }
            driver.add_cookie(cookie_dict)
        driver.get(request.url)
        driver.refresh()
        time.sleep(2)
        data = driver.page_source
        driver.close()
        response = HtmlResponse(url=request.url, body=data, encoding='utf-8', request=request)
        return response

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
