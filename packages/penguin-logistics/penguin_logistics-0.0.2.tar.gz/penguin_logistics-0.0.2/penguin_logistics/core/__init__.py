from infinite_request import infinite_request

def test(n):
	url = "https://ak.hypergryph.com/penguinlogistics/tracking/track?seriesNumber=" + str(n) # 1314752
	txtres = infinite_request(url)
	
	if txtres != '{"success":false,"data":""}':
		return txtres