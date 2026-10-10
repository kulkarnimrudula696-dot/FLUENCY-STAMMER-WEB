import urllib.request, json

yids = [
    '_nbVTUYVKxg', '07d2dXHYb94', '38y_1EWIE9I', '5L4DQfVIcdg', 'P5yunhX3FIE',
    '2REkk9SCRn0', '1QAI4B_2Mfc', 'WjqiU5FgsYc', 'kNw8V_Fkw28', 'vbuq7w3ZDUQ',
    'OuJ4BBQ0nhc', 'EUm-vAOmV1o', 'Hz_d-cikWmI', 'HtFxYfhxS2M', 'yWd4mzGqQYo',
    'kQjtK32mGJQ', 'k1vCrsZ80M4', '76Xxn1FSdQ4', 'Ad3CMri3hOs', 'WhWc3b3KhnY'
]

for yid in yids:
    url = f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={yid}&format=json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f'OK: {yid} -> "{data.get("title")}"')
    except Exception as e:
        print(f'FAIL: {yid} -> {e}')
