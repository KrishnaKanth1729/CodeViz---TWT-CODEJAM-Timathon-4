import os
import time

from selenium.webdriver.common.keys import Keys

from .models import *
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.conf import settings
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from .forms import *


def getdata(text):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

    driver.get('http://flowchart.js.org/')
    time.sleep(2)
    elements = driver.find_elements_by_class_name('ace_text-input')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "ace_text-input"))).send_keys(text)
    k = elements[1]
    k.clear()
    k.send_keys(text)
    time.sleep(2)

    el = driver.find_element_by_class_name('diagram2')
    code = el.get_attribute('innerHTML')

    '''element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Beginner Python Tutorials"))
        )
        element.click()
        print(driver.current_url)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sow-button-19310003"))
        )
        element.click()
        driver.back()
        driver.back()
        driver.back()'''
    return code


def index(request):
    return render(request, 'index.html', {})


def get_flowchart(request):
    k = ''
    l = ''
    error = ''
    color = ''
    if request.method != 'POST':
        form = FiForm()
    else:
        fs = FileSystemStorage()
        fs.delete('file.py')
        form = FiForm(request.POST, request.FILES)
        k = request.POST.get('name')
        color = request.POST.get('color')
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        if not uploaded_file.name.endswith('.py'):
            error = 'Pls upload a python file'
            print(error)
        else:
            fs.save('file.py', uploaded_file)
        print(k)

        from pyflowchart import Flowchart
        try:
            with open(f'{settings.BASE_DIR}/{settings.MEDIA_URL}/file.py') as f:
                code = f.read()
            code.replace('async', '')
            if 'async' in code:
                print('no')
                code.replace('async', '')
            else:
                print('yes')
            fc = Flowchart.from_code(code, inner=True)
            print(fc)
            k = fc.flowchart()

            l = getdata(k)
            print(l)
        except FileNotFoundError:
            error = 'Pls upload a python file'
        fs = FileSystemStorage()

        # delete_file()
    return render(request, 'flow.html', {'form': form, 'code': l, 'error': error, 'color': color})


def delete_file():
    books = PyFile.objects.all()
    for book in books:
        book.delete()


def yt(request):
    json = {}
    res = ''
    label =''
    y= ''
    labels = []
    values = []
    type = ''
    title = ''
    if request.method != 'POST':
        form = GraphForm()
    else:
        form = GraphForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            type = form.cleaned_data['type']
            if type == ['1']:
                type = 'doughnut'
            elif type == ['2']:
                type = 'line'
            elif type == ['3']:
                type = 'area'
            elif type == ['4']:
                type = 'column'
            elif type == ['5']:
                type = 'pie'
            print(type)
            type.replace('[', '')
            type.replace(']', '')
            json = form.cleaned_data['json']
            json = eval(json)


            for key, value in json.items():
                labels.append(key)
                values.append(value)

            '''res = []
            for i in range(len(labels)):
                k = f'label: "{labels[i]}", y: {values[i]}'
                k = '{' + k + '}'
                res.append(k)

            res = str(res)
            res = res.replace('[', '')
            res = res.replace(']', '')
            res = res.replace("'", '')
            try:
                res = dict(res)
            except:
                pass
            print(res, type(res))'''

    return render(request, 'yt.html', {'keys': labels, 'values': values, "form": form, "type": type, 'title': title})


def removeChar(s, c):
    # find total no. of
    # occurrence of character
    counts = s.count(c)

    # convert into list
    # of characters
    s = list(s)

    # keeep looping untill
    # counts become 0
    while counts:
        # remove character
        # from the list
        s.remove(c)

        # decremented by one
        counts -= 1

    # join all remaining characters
    # of the list with empty string
    s = ''.join(s)

    return s



def viz(request):
    fs = FileSystemStorage()
    inc = 0
    while inc < 5:
        try:
            inc += 1
            fs.delete(f'image{inc}.png')
        except:
            pass


    context = {}
    text = ''
    if request.method != 'POST':
        form = VizForm()
    else:
        form = VizForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            print(f'text -- {text}')
    nums = []
    l = ''
    if text != '':
        k = get_words(text)
        print(k)
        l = get_images(k)
        print(l)

        for i in range(l):
            nums.append(i)
    else:
        error = 'You should enter some text'

    return render(request, 'viz.html', {'media_url': settings.MEDIA_URL, 'media-root': settings.MEDIA_ROOT, 'form': form, 'i': nums})


def get_words(sentence):
    from nltk.tag import pos_tag


    tagged_sent = pos_tag(sentence.split())
    # [('Michael', 'NNP'), ('Jackson', 'NNP'), ('likes', 'VBZ'), ('to', 'TO'), ('eat', 'VB'), ('at', 'IN'), ('McDonalds', 'NNP')]

    propernouns = [word for word, pos in tagged_sent if pos == 'NNP']
    # ['Michael','Jackson', 'McDonalds']

    return propernouns

def get_images(search_list):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time
    from django.conf import settings

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    i = 0
    for item in search_list[:5]:
        i += 1
        driver.get('https://www.google.com/imghp?hl=en')

        box = driver.find_element_by_class_name('gLFyf')
        if item == 'Python.' or item == 'python' or item == 'PYTHON':
            box.send_keys('Python Logo')
        elif item == 'Tim.' or item == 'tim' or item == 'Tim':
            box.send_keys('Tech With Tim')
        elif item == 'JavaScript' or item == 'javascript':
            box.send_keys('JavaScript logo')
        else:
            box.send_keys(item)

        box.send_keys(Keys.ENTER)

        k = driver.find_element_by_class_name('hide-focus-ring')
        k.click()

        try:
            l = driver.find_elements_by_class_name('rg_i')
            element = l[0]
            element.screenshot(f'{settings.BASE_DIR}/{settings.MEDIA_URL}/image{i}.png')
        except Exception as e:
            print(e)

    return i


def stock(request):

    import pandas as pd
    import pandas_datareader as web
    import datetime as dt
    context = {}
    if request.method != 'POST':
        form = CandleForm()
    else:
        form = CandleForm(data=request.POST)
        context['form'] = form
        if form.is_valid():

            ticker = form.cleaned_data['ticker']
            print(ticker)
            context['ticker'] = ticker
            from datetime import datetime
            start = datetime(2021, 1, 1)
            end = datetime(2021, 3, 24)

            data = web.DataReader(ticker, 'yahoo', start, end)
            context['high'] = process_data_high(data)
            context['low'] = process_data_low(data)
            context['open'] = process_data_open(data)
            context['close'] = process_data_close(data)
            dates = list(dates_bwn_twodates(start, end))
            context['dates'] = dates

    context['form'] = form
    return render(request, 'stock.html', context)


def process_data_high(data):
    high = []
    for item in data['High']:
        item = str(item)
        k = item.split('.')
        k[1] = k[1][:3]
        k = k[0] + '.' + k[1]
        item = float(k)
        high.append(item)
    print(high)

    return high


def process_data_low(data):
    high = []
    for item in data['Low']:
        item = str(item)
        k = item.split('.')
        k[1] = k[1][:3]
        k = k[0] + '.' + k[1]
        item = float(k)
        high.append(item)
    print(high)

    return high


def process_data_close(data):
    high = []
    for item in data['Close']:
        item = str(item)
        k = item.split('.')
        k[1] = k[1][:3]
        k = k[0] + '.' + k[1]
        item = float(k)
        high.append(item)
    print(high)

    return high


def process_data_open(data):
    high = []
    for item in data['Open']:
        item = str(item)
        k = item.split('.')
        k[1] = k[1][:3]
        k = k[0] + '.' + k[1]
        item = float(k)
        high.append(item)
    return high

import moment
def dates_bwn_twodates(start_date, end_date):
    start_date = moment.date(str(start_date))
    end_date = moment.date(str(end_date))
    diff = abs(start_date.diff(end_date).days)

    for n in range(0, diff + 1):
        yield start_date.strftime("%Y-%m-%d")
        start_date = (start_date).add(days=1)

