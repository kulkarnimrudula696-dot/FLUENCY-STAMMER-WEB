import urllib.request
import json

redirect_urls = [
    ("AUZIYQF9NmJFjgd13NjWbrGqMfjWBNI9EwXGXfMJ8Yeb8eAXBZW3s4bgZFc2gimOvIoiKB8iwTMSAjjKUTBZ2ipKCo7OoHUFuQmd8xxG5Lab3cSwu_2mk_FzogGeBtSmpbR6l84=", "Constantino 1"),
    ("AUZIYQGpbatdkE6rAmDOZQtYONUKlouvGlTw44DuZWLYX_ZxKInU5M2DR8f9K5GWShmIMEudkwxw8B5MCKvYeKdZI90RoqNVO_HVD5imPtOgHb8_WkvUjNglPmbWQX0igY8fMI4=", "Constantino 2"),
    ("AUZIYQE4iv-ZUJl5omHyaC1-I0xOx6u6In81NfGrp5V7oIOkmFK35zBDYpJzrV7q9QUgJhS3VR29HhdcxAOt208eXASJ2sTZ0JvWGPwXP8tAgM1XdUCzs03V-iuBsEiY0f_Ksgo=", "Constantino 3"),
    ("AUZIYQGR-7rJtxubO6vcvrh0iOp9kyhY7dQTN7eN4DIC6n9XRku56lXtHLhBMD4lScUB9zWkIWyddkcgNShRrkBuHa4LrHK1kyTWpUCaJlLnMsQUJW-1ZPrw184xTRb3vgaefyY=", "Constantino AIS")
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
