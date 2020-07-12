# -*- coding:utf-8 _*-


import requests
import csv
from lxml import etree


class UCSDPoliScien:
    def __init__(self):
        # fill in your url
        self.url = 'https://polisci.ucsd.edu/grad/current-students/index.html'

    def send_get_request(self, url):
        r = requests.get(url)
        if r.text:
            html_result = r.text
            print('get result success')
            return html_result
        else:
            print('get result fail')
            return ''


    # Todo #1: add a function called extract_information( ) to extract the information from HTML Response
    def extract_infromation(self, response):
        raw_tree = etree.HTML(response)
        name_list = raw_tree.xpath('//*[@id="main-content"]/div[2]/div/section[1]/article[2]/ul/li/span/h3/descendant-or-self::text()')
        name_list = [name for name in name_list if name.strip() != '']
        email_list = raw_tree.xpath(
            '//*[@id="main-content"]/div[2]/div/section[1]/article[2]/ul/li/span/descendant-or-self::a[not(@title)]/@href')
        email_list = [email for email in email_list if email != 'mailto:kdove@ucsd.edu']
        field_list = raw_tree.xpath('//*[@id="main-content"]/div[2]/div/section[1]/article[2]/ul/li/span/p/descendant-or-self::text()[last()]|//*[@id="main-content"]/div[2]/div/section[1]/article[2]/ul/li/span/descendant-or-self::text()[last()]')
        field_list = [field.strip() for field in field_list if field.strip() != '']
        photo_list = raw_tree.xpath(
            '//*[@id="main-content"]/div[2]/div/section[1]/article[2]/ul/li/descendant-or-self::*/img/@src')
        for i in range(0, len(name_list)):
            dict_result = {}
            dict_result['name'] = name_list[i]
            dict_result['email'] = email_list[i]
            dict_result['photo'] = photo_list[i]
            dict_result['field'] = field_list[i]
            # write the context into a file
            self.save_information(dict_result)

    # Todo #2: add a function save_information( ) to save the extracted information in csv format.
    def save_information(self, raw_json):
        with open('ucsd_result.csv', 'a+') as out_f:
            csv_writer = csv.DictWriter(out_f, raw_json.keys())
            # What's this? Why do we need it?
            if out_f.tell() == 0:
                csv_writer.writeheader()

            csv_writer.writerow(raw_json)

    # Put all the things together
    def run(self):
        html_result = self.send_get_request(self.url)
        self.extract_infromation(html_result)
        # write the context into a file
        # with open('ucsd_result.html', 'w') as output_f:
        #     output_f.write(html_result)
        # print('The result is written in file ucsd_result.html')


if __name__ == '__main__':
    runner = UCSDPoliScien()
    runner.run()
