import requests
from bs4 import BeautifulSoup

def kokleri_getir(text):    
    cookies = {
        'JSESSIONID': '1BA812941F613165A3EE475440B24FF4',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,tr;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'JSESSIONID=1BA812941F613165A3EE475440B24FF4',
        'Origin': 'http://tools.nlp.itu.edu.tr',
        'Referer': 'http://tools.nlp.itu.edu.tr/MorphAnalyzer',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    data = {
        'input': text,
        'output': '',
    }

    response = requests.post('http://tools.nlp.itu.edu.tr/MorphAnalyzer', cookies=cookies, headers=headers, data=data, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    lines = soup.find('textarea', {'name': 'output'}).text.split('\n')
    kokler = set()
    for line in lines:
        if line.strip() == '' or len(line.split()) < 2:
            continue
        kok = line.split()[1].split('+')[0]
        kokler.add(kok)
    
    return kokler

def get_is_pure(text):
    token_list = text.split()
    is_pure_map = {}

    text = ''

    with open('veri/turkish_ekler_kokler.txt', 'r') as f: 
      kelimeler = f.readlines()

    kelimeler = set(kelimeler)

    for token in token_list:
      if token + "\n" in kelimeler:
        is_pure_map[token] = True
        continue

      text += token + ' '

    if len(text.strip()) == 0:
        return is_pure_map

    kokler = kokleri_getir(text)
   
    token_list = text.split()

    for token in token_list:
        is_pure_map[token] = (token in kokler)

    return is_pure_map