""" Custom Seance objects for recrut sites
"""
import time
import requests
import random
import io
import codecs

import pdfkit as pdf_kit


from selenium import webdriver
from xhtml2pdf import pisa



class BaseException(Exception):
    def __init__(self, message):
        self.message = message


class URLError(BaseException):
    pass


class SeanceError(BaseException):
    pass


class SeanceValueError(BaseException):
    pass
#class BypassBase(object):
#    pass


#class BypassBaseAuth(object):
#    auth_url = None
#    login_field_class = None
#    pass_field_class = None

#    def __init__(self):
#        self

class BrowserSeanceBase(object):

    def __init__(self):
        self.browser = webdriver.Chrome()

    def __del__(self):
        browser = getattr(self, 'browser', None)

        if browser:
            browser.close()

    def _set_url(self, url=None):
        if not url:
            raise URLError("URL it's bad: %s" %(url))

        browser = getattr(self, 'browser', None)

        if not browser:
            raise SeanceError("Not active connect")

        browser.get(url)
        time.sleep(1)

        status = self._status_code()

        #if status != 200:
        #    raise SeanceError("Respons status code: %s" %(status))

    def _get_html(self):
        browser = getattr(self, 'browser', None)

        if not browser:
            raise SeanceError("Not active connect")

        return browser.page_source

    def _screenshot(self):
        browser = getattr(self, 'browser', None)

        if not browser:
            raise SeanceError("Not active connect")

        return browser.screen()

    def _convert_to_pdf(self, base_name, save_path=None):
        """Take thees object
        Returned current page as bayts in format pdf
        """
        rnadom_sequnce = random.random() * 10 ** 5
        file_uid =  str(int(rnadom_sequnce))
        file_name = str().join([save_path, base_name, file_uid, '.html'])
        out_file = codecs.open(file_name, mode="w",encoding='utf-8')
        html_content = self._get_html()
        out_file.write(html_content)
        out_file.close()
        #try:
        #pisaStatus = pisa.CreatePDF(html_content, dest=out_file,
        #                            raise_exception=False)
        #except pisa.ParserError:
            
        #out_file.close()

        #if not pisaStatus:
        #    pdf_name = None
        #else:
        #pdf_config = pdf_kit.configuration(
        #    wkhtmltopdf=r'C:\Program Files\Python36\wkhtmltopdf\bin\wkhtmltopdf.exe'
        #)
        #html_bytes = bytes(html_content, encoding = 'utf-8')
        #pdf_kit.from_string(html_content, file_name,
        #                  configuration=pdf_config)
        pdf_name = str().join(['/files/', base_name, file_uid, '.html'])

        return pdf_name

    def _get_element(self, target_name):
        element_name = getattr(self, "target_" + target_name, None)

        if element_name:
            browser = getattr(self, 'browser', None)
            element = browser.find_element_by_name(element_name)
        else:
            element = None

        return element

    def _set_element_value(self, element, value):

        if not value:
            raise SeanceValueError("Velue is empty!")

        element.send_keys(value)

    def _send_form_element(self, element):
        element.submit()

    def _status_code(self):
        url = self.browser.current_url
        connect = requests.get(url)
        connect.close()
        return connect.status_code

    def request_get(self, url):
        return self._set_url(url)

    def html(self):
        return self._get_html()

    def screenshot(self):
        return self._screenshot()

    def pdf(self):
        return self._convert_to_pdf(
                          'candidate', 
                           r'C:\Users\FPavlov\recrutDjango\files\\'
        )

    def status_code(self):
        return self._status_code()


class BrowserSeanceHh(BrowserSeanceBase):

    target_login = "username"
    target_password = "password"

    def __init__(self, login=None, password=None):

        if not (login and password):
            raise SeanceError(
                "Login or password is None (%s, %s)" %(login, password)
            )

        super(BrowserSeanceHh, self).__init__()
        self.auth = self._auth(login, password)

    def _auth(self, login, password):
        browser = getattr(self, "browser", None)

        if not browser:
            raise SeanceError("Bad Seance")

        self.request_get("https://hh.ru/account/login?backurl=%2F")
        login_element = self._get_element("login")
        password_element = self._get_element("password")
        self._set_element_value(login_element, login)
        self._set_element_value(password_element, password)
        self._send_form_element(password_element)
        status = self.status_code()

        if status != 200:
            auth_flag = False
        else:
            auth_flag = True

        return auth_flag


if __name__ == '__main__':
    test = BrowserSeanceHh('1', '2')
    time.sleep(10)