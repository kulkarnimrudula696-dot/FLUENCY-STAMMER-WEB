import urllib.request, json, re

urls = [
    'https://images.unsplash.com/photo-1519331379826-f10be5486c6f',
    'https://images.unsplash.com/photo-1517256064527-09c73fc73e38',
    'https://images.unsplash.com/photo-1507525428034-b723cf961d3e',
    'https://images.unsplash.com/photo-1530103862676-de8c9debad1d',
    'https://images.unsplash.com/photo-1578916171728-46686eac8d58',
    'https://images.unsplash.com/photo-1521587760476-6c12a4b040da',
    'https://images.unsplash.com/photo-1534438327276-14e5300c3a48',
    'https://images.unsplash.com/photo-1556910103-1c02745aae4d',
    'https://images.unsplash.com/photo-1524178232363-1fb2b075b655',
    'https://images.unsplash.com/photo-1475721027785-f74eccf877e2',
    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5',
    'https://images.unsplash.com/photo-1474487548417-781cb71495f3',
    'https://images.unsplash.com/photo-1506015391300-4802dc74de2e',
    'https://images.unsplash.com/photo-1503899036084-c55cdd92da26',
    'https://images.unsplash.com/photo-1533900298318-6b8da08a523e',
    'https://images.unsplash.com/photo-1515694346937-94d85e41e6f0',
    'https://images.unsplash.com/photo-1511795409834-ef04bbd61622',
    'https://images.unsplash.com/photo-1522071820081-009f0129c71c',
    'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d',
    'https://images.unsplash.com/photo-1519501025264-65ba15a82390'
]

for idx, u in enumerate(urls):
    photo_id = u.split('photo-')[-1]
    page_url = f'https://unsplash.com/photos/{photo_id}'
    req = urllib.request.Request(page_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            m_title = re.search(r'<title>(.*?)</title>', html)
            m_desc = re.search(r'<meta name="description" content="(.*?)"', html)
            print(f"[{idx+1}] ID: photo-{photo_id}")
            if m_title:
                print("   Title:", m_title.group(1))
            if m_desc:
                print("   Desc:", m_desc.group(1)[:120])
    except Exception as e:
        print(f"[{idx+1}] ID: photo-{photo_id} -> Error: {e}")
