from mitmproxy import http


def request(flow: http.HTTPFlow) -> None:
	if flow.request.pretty_url == "http://example.com/":
		flow.response = http.Response.make(
				200,
				'<html><body><center><h1>TailsNet</h1></center><audio autoplay><source src="http://192.168.0.107/tailsnet/assets/splash.mp3" type="audio/mpeg"></audio></body></html>'.encode(),
				{"Content-Type": "text/html"},
		)

