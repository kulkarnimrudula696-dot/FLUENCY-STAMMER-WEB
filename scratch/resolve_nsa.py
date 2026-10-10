import urllib.request
import json

redirect_urls = [
    ("AUZIYQFq3OfQAjd8dZ6EfhonEbN4exzYdAwY3__Fz13weY2oLGQIdtjHgpvFcu3Bp5eerjFYv7Hu3UztWrqzh__b8OaPOJmsT6lWxpDWth7XTgIuVyTV9Qx_a1HGIZQt3YnxkjWG", "Confident Presentations"),
    ("AUZIYQENTI1Z34FYwMVUsNB-p7yBvkdfzriKI9bYLtD8tBzi4dT5vxw84hIT7S6-BqxDOPoA61a_5UBJIySNoghuxzjGA7tzSsUlzb2WzDdQD_GKh63yJD2uJ3d27pbNGNBD-FQn", "Navigating Remote Work"),
    ("AUZIYQFvxm5YJAGw9ijfoNLepaMBzNZzb7xBJiqA7Pv0UZFUDJrdvouGYAC5JEvhsFt__G1fJOnDisM-T9lE7vbzhZRZmYrFrfGUUTaAEHC3npkxNsI92xa5cAUfV4LdmQmwFlVv", "Moving from Pressure to Presence"),
    ("AUZIYQHLwNvrZny2XWuTk_CIVWwUWeJnrwQbLqmU3leeoU1M-ZmTU6isVt1s35eW_vQcCxtAia35sD67Abdf4Fw37B-3VAqyEtI3uGHlJyQoIk6F7YkwMd02_T9ADJOdrepn5bk8", "Empowering Authenticity at Work")
]

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirect)

for tok, label in redirect_urls:
    u = f"https://vertexaisearch.cloud.google.com/grounding-api-redirect/{tok}"
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        res = opener.open(req)
        print(f"{label} -> {res.geturl()}")
    except urllib.error.HTTPError as e:
        if e.code in (301, 302, 303, 307, 308):
            loc = e.headers.get('Location')
            print(f"{label} -> {loc}")
        else:
            print(f"{label} -> HTTPError {e.code}")
    except Exception as e:
        print(f"{label} -> Error {e}")
