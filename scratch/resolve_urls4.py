import urllib.request
import json

redirect_urls = [
    ("AUZIYQFcqvne8c0ro9Mmy1Df9HfW6J9T7lOo_KqgEQcc17_1Di5FVstdlw8KhakYyz8Xi5NoGWqhrLPN9RoOQCy7ZF3a7Oh6iZJ8_dLzsTkC62sgKy90j0GKKUq4SGNgTouYAOc=", "Vivian Sisskin"),
    ("AUZIYQHu-nvk_AvK5BOyjEF5FShXc-b7Xg3SIaXqZh-YqoGVNAKBNVpn934t3jUWLkWgPLfLXZBTjfmM7XR9DgtCwpkZO6wmbpWbWN83YLcB9D4UiTtGrOiHpPkxXaLRu4WDjUU=", "Kristin Chmela"),
    ("AUZIYQG-6zjj0GHl_ncL-tF5pYub2t16kzZdklp9CNiZSvOU42quzLpIYUntSziaoP8Gt2AyU3CFiKQt9WhLLxsP7PhDYmyvWsjFpQViqeFZNzbxSQMxqujWcsqNoWQLvWA4SsU=", "Vivian Sisskin 2")
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
