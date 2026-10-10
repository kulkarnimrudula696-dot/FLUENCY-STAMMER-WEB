import urllib.request
import re

redirect_urls = [
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEyChO5yHPfYt9w9xtwFyY160JNomLVnWoYgSz9sjMBX9zK1PU1IpEGU7ECvotVomKr8vTgdITzlrVUG_0rK2yUcH4HhOicqio90esPHzbhIOz1jiMALZpaOCw32blJ63_1",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHwOp6dTlbVFNTQCKVmu6zA_3dZgWqmNPQ1huE1DgvLDzI2Kq2sMZkhpXOZHi0mCcSF7f-GP0LTETEsQ5Y-ktOEy4a5-c_CQQsqtjs8sSWJ2__rKjZaEmC4eNODKBRwf3B4",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGFc3U63Y4dOVJ_RMgKi1GKKRQJKVwmNU_8PIL2WGCvRFcMuw6Li98ze6JCPaOQv7XnEAR-tP9BWAI_Y_W1YAztoZ6fWNmmChdp9kZH7QAvu3FjtukJEX9dK0aUKTIlLpg9",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE1eTHdM7I_7YmdonOGzKFsQxgGW7s4r29TvtFQPQOUySFP0Tnlm1QG2U2yz3ZJUn2d6dQpmLn9GOjaitSpWTIfuAKnz2RA22E_i_20306NE-Hiiz6TkJ5sDUXKCwu7l6CB",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHfIDop74yyejGlrS2hRLjM1-7SJKY04prlDFh7yeXQrTLv6-Upjcukg6QncgWtDoAs0FyEBh7YYGbJvdOs0Fw7A8v0o36JVjXnyJ7lSYHarVmDqY2fYgox2pi1BbF1oE5d",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHYkTrwPVeE2bePJ-qqNBF-U1lD1vrmuWz2A4jZYRvil5a6Nd7-onsbaWk8a2_dP95MgCo3qLC8Jvcn8a6m-8QX6GOaRtgFcAg6ymSARDqm8w3helqZ5DodeWAVQAKvaIYc"
]

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirect)

for u in redirect_urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        res = opener.open(req)
        print("Final:", res.geturl())
    except urllib.error.HTTPError as e:
        if e.code in (301, 302, 303, 307, 308):
            loc = e.headers.get('Location')
            print("Redirect ->", loc)
        else:
            print("HTTPError:", e.code)
    except Exception as e:
        print("Error:", e)
