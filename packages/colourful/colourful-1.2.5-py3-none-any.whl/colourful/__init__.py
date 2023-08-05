import requests

class Colour:
	def __init__(self, key):
		self.input = None
		self.key = key
	def colourize(self, input):
		self.input = input
		headers = {"api-key": self.key}
		payload = {"image": self.input}
		
		resp = requests.post("https://api.deepai.org/api/colorizer", headers=headers, data=payload)
		
		data = resp.json()
		url = data["output_url"]
		
		return url