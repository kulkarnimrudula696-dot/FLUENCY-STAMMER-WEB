import urllib.request
import json

redirect_urls = [
    ("AUZIYQHC4hjyAaOaQdjCDvdNPiWNHBDVjXE0ZWeCCMHAns5ng0JMiAYQksvmDvsSfoOHT5Mw4kf-Zv2AmFvbmtaXpFgQTPPhalReAWF3RQCsd5f2OPFo60frWDsmvCNxueTAuNLu", "Role of Acceptance Commitment Mindfulness"),
    ("AUZIYQHFK6yoomRx8V8i0UNRN-dgl6HuLhIqDmOuanqRZLym6MOfWrK7QsJwifP4ey22OpV5r2QqwE-fK0b5Lyjjgpjr4_2WdLQtUNLWKlo-beuxKkuKUWe0xipI_TRbuu4QmsHy", "What Is ACT for Disfluency"),
    ("AUZIYQGXYrRv090CZjOvjgpNIrUb2TIEOaOsVgJkDBKit5xMzrwP_qpLWA3HxNvYUhY3AJwBKro3w3U-uWzs5sKmpcaIJ2QVqDF1Yc6dMxmlh6V_duMaw2py3pmSycQQHWHWtZfZ", "ACT Taster Stuttering Foundation"),
    ("AUZIYQGGGERmzOvewvhPqQUlv8u15Uunv6hmQnRrlsh2-ZrH2MYSROT_Ov74nH3FlytGyYW0EMYgXaeiaEdgIcb4G9lMm_pct5K00ZeIgU1-mc2ZpMfys4HA79Zo3pjm5lweYnBE", "Voluntary Stuttering"),
    ("AUZIYQFCv997Q-aksCb81qhdQ8JzCt_yqC3kLacqoSPRaZefowzlFoZxdi4qs9rt4sPbgFBQNNSzTMuFppvxXkBZ4-QGNcXVTyOyvyoqPekR6A3q_pB09WI3VGJwxv4iKohOyei8Dbu0iU2PuqH6a87r2j9Jc0q0x-xWa7UW85j2-YAYPH8=", "Clinical Review Evidence")
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
