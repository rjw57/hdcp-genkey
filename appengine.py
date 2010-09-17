from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson as json

from generate_key import *

class KeysHandler(webapp.RequestHandler):
	def __init__(self):
		self._key_matrix = read_key_file(open('master-key.txt'))

	def _gen_json(self, ksv, key, is_sink):
		return json.dumps( {
			'ksv': ('%010x' % ksv), 
			'key': map(lambda x: '%014x' % x, key),
			'type': 'sink' if is_sink else 'source' },
			sort_keys=True, indent=False)


	def get(self, key_type, ksv_string = None):
		self.response.headers['Content-Type'] = 'application/json'

		if ksv_string is not None:
			ksv = int(ksv_string, 16)
		else:
			ksv = gen_ksv()

		if key_type == 'source':
			key = gen_source_key(ksv, self._key_matrix)
		elif key_type == 'sink':
			key = gen_sink_key(ksv, self._key_matrix)
		else:
			raise RuntimeError('Unknown key type: %s' % key_type)

		self.response.out.write(self._gen_json(ksv, key, True if key_type == 'sink' else False))

class KsvHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('%010x' % gen_ksv())

application = webapp.WSGIApplication([
	('/keys/(sink|source)/([0-9a-f]{10})', KeysHandler),
	('/keys/(sink|source)', KeysHandler),
	('/keys/random_ksv', KsvHandler),
	], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
