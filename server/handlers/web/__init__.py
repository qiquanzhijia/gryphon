from server.handlers.web import download

web_handers = [
    (r'/', download.DownloadHandler),
]
