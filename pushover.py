def pushover(title, message):
    import settings as s
    import httplib, urllib
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.urlencode({
        "token": s.pushoverAPP_TOKEN,
        "user": s.pushoverUSER_KEY,
        "title": title,
        "message": message,
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
