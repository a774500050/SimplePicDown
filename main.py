import requests
from bs4 import BeautifulSoup
import os
import re


def get_html_text(url, code="utf-8", timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        r.encoding = code
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
    except Exception as e:
        print('Error while getting html text: ', e)
        return ""


def quesq(url, prefix, path):
    os.chdir(path)
    site_name = "http://www.quesq.net/"
    html = get_html_text(url, code="shiftjis")
    top_pic = html.select("body > div:nth-child(1) > table > tr:nth-child(3)  tr > td > table > tr:nth-child(1) > td "
                          "> div table > tr:nth-child(3) td > table >tr:nth-child(5) > td > img")[0]
    # print(top_pic["src"])
    top_src = auto_completion(top_pic["src"], site_name, url)
    save_pic(path, title=prefix + "1", img_src=top_src)
    ul_list = html.find_all("ul", class_="clearfix")[0]
    li_list = ul_list.find_all("li")
    for li in li_list:
        index = li_list.index(li)
        suffix = str(index + 2)
        img_src = auto_completion("./" + li.select("img")[0]["src"], site_name, url)
        save_pic(path, title=prefix + suffix, img_src=img_src)
    return


def aquamarine(url, prefix, path):
    os.chdir(path)
    site_name = "http://aq-marine.jp/"
    html = get_html_text(url)
    top_pic = html.select("#syohin_img > a > img")[0]
    top_src = auto_completion(top_pic["src"], site_name, url)
    save_pic(path, title=prefix + "1", img_src=top_src)
    div_list = html.select("#main_col > div.post.clearfix > div.syohinsubimg")[0]
    href_list = div_list.find_all("a")
    for a in href_list:
        index = href_list.index(a)
        suffix = str(index + 2)
        img_src = auto_completion(a["href"], site_name, url)
        save_pic(path, title=prefix + suffix, img_src=img_src)
    return


def auto_completion(url, site_name, site_url):
    # if url is open with http:// or https:// , return
    if re.match('http://|https://', url):
        return url
    elif re.match('//', url):
        if 'https://' in site_name:
            return 'https:' + url
        elif 'http://' in site_name:
            return 'http:' + url
    elif re.match('/', url):
        return site_name + url
    elif re.match('./', url):
        return site_url + url[1::]


def img_type(header):
    # get file type
    image_attr = header['Content-Type']
    pattern = 'image/([a-zA-Z]+)'
    suffix = re.findall(pattern, image_attr, re.IGNORECASE)
    if not suffix:
        suffix = 'png'
    else:
        suffix = suffix[0]
    # get suffix
    if re.search('jpeg', suffix, re.IGNORECASE):
        suffix = 'jpg'
    return suffix


def save_pic(path, title=None, img_src=None, timeout=30):
    if img_src:
        # src = auto_completion(img_src)
        src = img_src
        # print(title)
        try:
            img = requests.get(src, timeout=timeout)
            img_content = img.content
            img_header = img.headers
            filename = f'{title}.{img_type(img_header)}'
            # print(filename)
            if img_content:
                with open(os.path.join(path, filename), 'wb') as imgFile:
                    imgFile.write(img_content)
                    print(f'Download {filename} Success ')
        except Exception as e:
            print('Error while saving pic: ', e)


def select_mode(url, prefix):
    mode_dict = {
        "1": quesq,
        "2": aquamarine
    }
    mode = input("Please select website to down: \n"
                 "1. Ques Q 2.Aqua Marine \n")
    save_loc = input("Please input directory, leave blank to save at current directory: ")
    # save_loc = "D:\THBWiki\PicTest"
    if save_loc == "":
        save_loc = os.getcwd()
    mode_dict[mode](url, prefix, save_loc)
    '''
    if mode == 1:
        quesq(url, prefix, save_loc)
    '''
    return


# website_name = "http://www.quesq.net/"
# website_url = "http://www.quesq.net/products/touhou_remilia_the_childish_moon_red_forever"
# filename_prefix = "Ques Q永远鲜红的幼月蕾米莉亚·斯卡蕾特-"

# website_url = "http://aq-marine.jp/archives/product/toho_reimu"
# filename_prefix = "AQUAMARINE哑采弦二Ver.博丽灵梦-"

website_url = input("Please input url: ")
filename_prefix = input("Please input prefix: ")

select_mode(website_url, filename_prefix)
