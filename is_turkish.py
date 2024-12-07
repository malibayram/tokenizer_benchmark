import requests
from bs4 import BeautifulSoup

def get_is_turkish(token_list, special_bow = None):
  # special_bow is special beginning of word. like ĠRisk, _Risk
  is_turkish_map = {}

  text = ''

  with open('veri/turkish_ekler_kokler.txt', 'r') as f: 
     kelimeler = f.readlines()

  kelimeler = set(kelimeler)

  for token in token_list:
    if special_bow is not None:
      token = token.replace(special_bow, '')

    if token + "\n" in kelimeler:
      is_turkish_map[token] = True
      continue

    text += token + ' '

  if len(text.strip()) == 0:
      return is_turkish_map
  
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
      'Referer': 'http://tools.nlp.itu.edu.tr/IsTurkish',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  }

  data = {
      'input': text.strip(),
      'output': '',
  }

  response = requests.post('http://tools.nlp.itu.edu.tr/IsTurkish', cookies=cookies, headers=headers, data=data, verify=False)

  soup = BeautifulSoup(response.text, 'html.parser')

  lines = soup.find('textarea', {'name': 'output'}).text.split('\n')

  for line in lines:
      if line.strip() == '' or len(line.split()) < 2:
          continue
      parts = line.split(':')
      word = parts[0].strip()

      is_turkish_map[word] = parts[1].startswith(' t')

  return is_turkish_map