import urllib.request
import json

redirect_urls = [
    ("AUZIYQHBB86wKNxTKfMWjExoV4yW2QJTV4grQ4cCtefBcKtvNSP4vwAbeyTkZLTiuKULe3KwQ8ecIE7R2AxfaikxCv5ws9lxGF43k55v8uVn7vCFk4dGgxz5oFC80Mt24SSNAdCF", "Stuttering: For Kids By Kids"),
    ("AUZIYQFzwERhdH2eUb3iHXI1NAqZYEiMs16PK1ySnbfi_4sXOId6jXzA0pGkUYUltq8yFyrhVhvsEJye5eGfzJG-qBcFpILlaS_ahBPOgZYpCb99FvCXlxO3b-a_py_xRyvsIbRM", "If You Stutter: Advice for Adults"),
    ("AUZIYQHf7KXIAE3H13_n4T9qGZnHxbePB9rDXu07ciYeZ2j5DI9lxqvgImHWeLEaI5VfH1vZynNfySb_5SGJO5WY9kDu2PVnshNxRTlFUfDWHtMJnYaxE276FrwgWdW1q146P9Bu", "Stuttering and Your Child: Help for Parents"),
    ("AUZIYQFD4BeAgItzcKDck1H-3-W0DdVUynBKIpmUcKgtRI8O2nczLIUFB3hTCY_4LlpNALA0jMzdBsdTEuOqZTXNdBUQvmP3fYlJ-7fHo-THpoXsp4YVjWu85S9TCnREEiVqx6mA", "The ABCs of Stuttering"),
    ("AUZIYQFK8IdIsKwnf_xBp78YlmLgkBJs8xSfP5xSDSZNwy3fFN3x3e6cQIWYniZS7wdNgkJMklfo3OSdNEnqWcLFuQOfREo_ZzCjWyTpqTCP14bW96MyzUYI3VSuXUarxMpzXO4E", "National Stuttering Association"),
    ("AUZIYQEhDVufqmN66Z-qu1sSBHg9byN--535aaD7LgBrtyQz-xQ92W6oKqKg3o3RuKVM3sBYh7xOCLYkeJ90f7OB0uheliOgtTzpDgZwEETrEEAgsreuLBkv8fZn_psp2MHVWNZW", "NSA Connects"),
    ("AUZIYQE9RLFuhzAk1XJvx9jBVb-EzdcKAd1qRVNAejnCXu5UZmc_rEuUj_9a0Ek1fhUSBfDdoIN5Wcop7VgrhupQD9u9bl83wwH0QiZ6R7_ykWzZk3Q_i2h_66DpaloqcM7YM9FU", "Empowering Voices"),
    ("AUZIYQHCwnZiCedC7Ci8v_AAoL5MRES4EUPWIS3t_euBq4_0PpSXT6T-oC4UwDQzmmuZt_gbvEN8FDJgru0de-SZtNLG15vgqI_xMdkskdpNzoB0oLLfyf4USydAa_0n8yBuAXc3", "SAY & BBDO PSA"),
    ("AUZIYQFHd71GwX0UfO9Y3TJ-vbVuJWJdRztPa_8oln_yQ9ySipWUvWFE_3GTB20HPtSvSbqxEXkvvnLstZu5TC5sq-4X2e6t5d8-jP96Ak_ZLUnmLn0GLlIGpXLRKFeonyReQrtN", "My Beautiful Stutter")
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
