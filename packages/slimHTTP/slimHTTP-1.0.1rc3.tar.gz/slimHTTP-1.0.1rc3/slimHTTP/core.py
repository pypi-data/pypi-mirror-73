import ipaddress
import ssl, os, sys, random, json
from os.path import isfile, abspath
from mimetypes import guess_type # TODO: issue consern, doesn't handle bytes,
#								   requires us to decode the string before guessing type.
from json import dumps
from time import time, sleep
import importlib.util

from socket import *
try:
	from select import epoll, EPOLLIN
except:
	""" #!if windows
	Create a epoll() implementation that simulates the epoll() behavior.
	This so that the rest of the code doesn't need to worry weither or not epoll() exists.
	"""
	import select
	EPOLLIN = None
	class epoll():
		def __init__(self):
			self.sockets = {}
			self.monitoring = {}

		def unregister(self, fileno, *args, **kwargs):
			try:
				del(self.monitoring[fileno])
			except:
				pass

		def register(self, fileno, *args, **kwargs):
			self.monitoring[fileno] = True

		def poll(self, timeout=0.5, *args, **kwargs):
			try:
				return [[fileno, 1] for fileno in select.select(list(self.monitoring.keys()), [], [], timeout)[0]]
			except OSError:
				return []

HTTP = 0b0001
HTTPS = 0b0010
def host(mode=HTTPS, *args, **kwargs):
	"""
	host() is essentially just a router.
	It routes a selected mode and sets up an instance of either HTTP_SERVER or HTTPS_SERVER.
	"""
	if mode == HTTPS:
		return HTTPS_SERVER(*args, **kwargs)
	elif mode == HTTP:
		return HTTP_SERVER(*args, **kwargs)

def drop_privileges():
	return True

imported_paths = {}
def handle_py_request(request):
	"""
		Handles the import of a specific python file.
	"""
	path = abspath('{}/{}'.format(request.web_root, request.headers[b'URL']))
	old_version = False
	request.CLIENT_IDENTITY.server.log(f'Request to "{path}"', level=4, origin='slimHTTP', function='handle_py_request')
	if path not in imported_paths:
		## https://justus.science/blog/2015/04/19/sys.modules-is-dangerous.html
		try:
			request.CLIENT_IDENTITY.server.log(f'Loading : {path}', level=4, origin='slimHTTP')
			spec = importlib.util.spec_from_file_location(path, path)
			imported_paths[path] = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(imported_paths[path])
			sys.modules[path] = imported_paths[path]
		except (SyntaxError, ModuleNotFoundError) as e:
			request.CLIENT_IDENTITY.server.log(f'Failed to load file ({e}): {path}', level=2, origin='slimHTTP', function='handle_py_request')
			return None
	else:
		request.CLIENT_IDENTITY.server.log(f'Reloading: {path}', level=4, origin='slimHTTP', function='handle_py_request')
		try:
			raise SyntaxError('https://github.com/Torxed/ADderall/issues/11')
		except SyntaxError as e:
			old_version = True
			request.CLIENT_IDENTITY.server.log(f'Failed to reload requested file ({e}): {path}', level=2, origin='slimHTTP', function='handle_py_request')
	return old_version, imported_paths[f'{path}']

def get_file(request, ignore_read=False):
	"""
	Read a local file.
	"""
	real_path = abspath('{}/{}'.format(request.web_root, request.headers[b'URL']))
	request.CLIENT_IDENTITY.server.log(f'Trying to fetch "{real_path}"', level=5, source='get_file')
	if b'range' in request.headers:
		_, data_range = request.headers[b'range'].split(b'=',1)
		start, stop = [int(x) for x in data_range.split(b'-')]
		request.CLIENT_IDENTITY.server.log(f'Limiting to range: {start}-{stop}', level=5, source='get_file')
	else:
		start, stop = None, None

	extension = os.path.splitext(real_path)[1]

	if isfile(real_path) and extension != '.py':
		if ignore_read is False:
			with open(real_path, 'rb') as fh:
				if start:
					fh.seek(start)
				if stop:
					data = fh.read(stop-start)
				else:
					data = fh.read()
		else:
			data = b''
		
		filesize = os.stat(real_path).st_size
		request.CLIENT_IDENTITY.server.log(f'Returning file content: {len(data)} (actual size: {filesize})', level=5, source='get_file')
		return 200, real_path, filesize, data

	request.CLIENT_IDENTITY.server.log(f'404 - Could\'t locate file {real_path}', level=3, source='get_file')
	return 404, '404.html', -1, b'<html><head><title>404 - Not found</title></head><body>404 - Not found</body></html>'

class CertManager():
	def generate_key_and_cert(key_file, **kwargs):
		# TODO: Fallback is to use subprocess.Popen('openssl ....')
		#       since installing additional libraries isn't always possible.
		#       But a return of None is fine for now.
		try:
			from OpenSSL.crypto import load_certificate, load_privatekey, PKey, FILETYPE_PEM, TYPE_RSA, X509, X509Req, dump_certificate, dump_privatekey
			from OpenSSL._util import ffi as _ffi, lib as _lib
		except:
			return None

		"""
		Will join key and cert in the same .pem file if no cert_file is given.
		"""
		# https://gist.github.com/kyledrake/d7457a46a03d7408da31
		# https://github.com/cea-hpc/pcocc/blob/master/lib/pcocc/Tbon.py
		# https://www.pyopenssl.org/en/stable/api/crypto.html
		a_day = 60*60*24
		if not 'cert_file' in kwargs: kwargs['cert_file'] = None
		if not 'country' in kwargs: kwargs['country'] = 'SE'
		if not 'sate' in kwargs: kwargs['state'] = 'Stockholm'
		if not 'city' in kwargs: kwargs['city'] = 'Stockholm'
		if not 'organization' in kwargs: kwargs['organization'] = 'Evil Scientist'
		if not 'unit' in kwargs: kwargs['unit'] = 'Security'
		if not 'cn' in kwargs: kwargs['cn'] = 'server'
		if not 'email' in kwargs: kwargs['email'] = 'evil@scientist.cloud'
		if not 'expires' in kwargs: kwargs['expires'] = a_day*365
		if not 'key_size' in kwargs: kwargs['key_size'] = 4096
		if not 'ca' in kwargs: kwargs['ca'] = None

		priv_key = PKey()
		priv_key.generate_key(TYPE_RSA, kwargs['key_size'])
		serialnumber=random.getrandbits(64)

		if not kwargs['ca']:
			# If no ca cert/key was given, assume that we're trying
			# to set up a CA cert and key pair.
			certificate = X509()
			certificate.get_subject().C = kwargs['country']
			certificate.get_subject().ST = kwargs['state']
			certificate.get_subject().L = kwargs['city']
			certificate.get_subject().O = kwargs['organization']
			certificate.get_subject().OU = kwargs['unit']
			certificate.get_subject().CN = kwargs['cn']
			certificate.set_serial_number(serialnumber)
			certificate.gmtime_adj_notBefore(0)
			certificate.gmtime_adj_notAfter(kwargs['expires'])
			certificate.set_issuer(certificate.get_subject())
			certificate.set_pubkey(priv_key)
			certificate.sign(priv_key, 'sha512')
		else:
			# If a CA cert and key was given, assume we're creating a client
			# certificate that will be signed by the CA.
			req = X509Req()
			req.get_subject().C = kwargs['country']
			req.get_subject().ST = kwargs['state']
			req.get_subject().L = kwargs['city']
			req.get_subject().O = kwargs['organization']
			req.get_subject().OU = kwargs['unit']
			req.get_subject().CN = kwargs['cn']
			req.get_subject().emailAddress = kwargs['email']
			req.set_pubkey(priv_key)
			req.sign(priv_key, 'sha512')

			certificate = X509()
			certificate.set_serial_number(serialnumber)
			certificate.gmtime_adj_notBefore(0)
			certificate.gmtime_adj_notAfter(kwargs['expires'])
			certificate.set_issuer(kwargs['ca'].cert.get_subject())
			certificate.set_subject(req.get_subject())
			certificate.set_pubkey(req.get_pubkey())
			certificate.sign(kwargs['ca'].key, 'sha512')

		cert_dump = dump_certificate(FILETYPE_PEM, certificate)
		key_dump = dump_privatekey(FILETYPE_PEM, priv_key)

		if not os.path.isdir(os.path.abspath(os.path.dirname(key_file))):
			os.makedirs(os.path.abspath(os.path.dirname(key_file)))

		if not kwargs['cert_file']:
			with open(key_file, 'wb') as fh:
				fh.write(cert_dump)
				fh.write(key_dump)
		else:
			with open(key_file, 'wb') as fh:
				fh.write(key_dump)
			with open(kwargs['cert_file'], 'wb') as fh:
				fh.write(cert_dump)

		return priv_key, certificate

class slimHTTP_Error(BaseException):
	pass

class ConfError(BaseException):
	def __init__(self, message):
		print(f'[Warn] {message}')

class NotYetImplemented(BaseException):
	def __init__(self, message):
		print(f'[Warn] {message}')

class UpgradeIssue(BaseException):
	def __init__(self, message):
		print(f'[Error] {message}')

class Events():
	"""
	Events.<CONST> is a helper class to indicate which event is triggered.
	Events are passed up through the event chain deep from within slimHTTP.

	These events can be caught in your main `.poll()` loop, and react to different events.
	"""
	SERVER_ACCEPT = 0b10000000
	SERVER_CLOSE = 0b10000001
	SERVER_RESTART = 0b00000010

	CLIENT_DATA = 0b01000000
	CLIENT_REQUEST = 0b01000001
	CLIENT_RESPONSE_DATA = 0b01000010
	CLIENT_UPGRADED = 0b01000011
	CLIENT_UPGRADE_ISSUE = 0b01000100
	CLIENT_URL_ROUTED = 0b01000101
	CLIENT_DATA_FRAGMENTED = 0b01000110

	WS_CLIENT_DATA = 0b11000000
	WS_CLIENT_REQUEST = 0b11000001
	WS_CLIENT_COMPLETE_FRAME = 0b11000010
	WS_CLIENT_INCOMPLETE_FRAME = 0b11000011
	WS_CLIENT_ROUTED = 0b11000100

	NOT_YET_IMPLEMENTED = 0b00000000

	def convert(_int):
		def_map = {v: k for k, v in Events.__dict__.items() if not k.startswith('__') and k != 'convert'}
		return def_map[_int] if _int in def_map else None

class ROUTE_HANDLER():
	"""
	Stub function that will act as a gateway between
	@http.<function> and the in-memory route that is stored.

	I might be using annotations wrong, but this will store
	a route (/url/something) and connect it with a given function
	by the programmer.
	"""
	def __init__(self, route):
		self.route = route
		self.parser = None

	def gateway(self, f):
		self.parser = f

class HTTP_RESPONSE():
	def __init__(self, headers={}, payload=b'', *args, **kwargs):
		self.headers = headers
		self.payload = payload
		self.args = args
		self.kwargs = kwargs
		if not 'ret_code' in self.kwargs: self.kwargs['ret_code'] = 200

		self.ret_code_mapper = {200 : b'HTTP/1.1 200 OK\r\n',
								206 : b'HTTP/1.1 206 Partial Content\r\n',
								301 : b'HTTP/1.0 301 Moved Permanently\r\n',
								307 : b'HTTP/1.1 307 Temporary Redirect\r\n',
								302 : b'HTTP/1.1 302 Found\r\n',
								404 : b'HTTP/1.1 404 Not Found\r\n',
								418 : b'HTTP/1.0 I\'m a teapot\r\n'}

	def build_headers(self):
		x = b''
		if 'ret_code' in self.kwargs and self.kwargs['ret_code'] in self.ret_code_mapper:
			x += self.ret_code_mapper[self.kwargs['ret_code']]
		else:
			return b'HTTP/1.1 500 Internal Server Error\r\n\r\n'

		if not 'content-length' in [key.lower() for key in self.headers.keys()]:
			self.headers['Content-Length'] = str(len(self.payload))

		for key, val in self.headers.items():
			if type(key) != bytes: key = bytes(key, 'UTF-8')
			if type(val) != bytes: val = bytes(val, 'UTF-8')
			x += key + b': ' + val + b'\r\n'
		
		return x + b'\r\n'

	def clean_payload(self):
		tmp = {k.lower(): v for k,v in self.headers.items()}
		if 'content-type' in tmp and tmp['content-type'] == 'application/json' and type(self.payload) not in (bytes, str):
			self.payload = json.dumps(self.payload)
		if type(self.payload) != bytes:
			self.payload = bytes(self.payload, 'UTF-8') # TODO: Swap UTF-8 for a configurable encoding..

	def build(self):
		self.clean_payload()
		ret = self.build_headers()
		ret += self.payload
		return ret

class HTTP_SERVER():
	"""
	HTTP_SERVER is normally instanciated with :py:meth:`slimhttpd.host` which would
	safely spin up a HTTP / HTTPS server with all the correct arguments.

	In case of manual control, this class is the main server instance in charge
	of keeping the `"addr":port` open and accepting new connections. It contains a main
	event loop, which can be polled in order to accept new clients.

	It's also in charge of polling client identities for new events and lift them up
	to the caller of :py:func:`slimhttpd.HTTP_SERVER.poll`.
	"""
	def __init__(self, *args, **kwargs):
		"""
		`__init__` takes ambigious arguments through `**kwargs`.
		They are passed down to `HTTP_SERVER.config` transparently and used later.

		Some values are used upon `__init__` however, since they are part of the
		initiation process, those arguments are:

		:param addr: Address to listen on, default `0.0.0.0`.
		:type addr: str
		:param port: Port to listen on, default `80` unless HTTPS mode, in which case default is `443`.
		:type port: int
		"""
		if not 'port' in kwargs: kwargs['port'] = 80
		if not 'addr' in kwargs: kwargs['addr'] = ''

		self.config = {**self.default_config(), **kwargs}
		self.allow_list = None
		## If config doesn't pass inspection, raise the error message given by check_config()
		if (config_error := self.check_config(self.config)) is not True:
			raise config_error

		self.sockets = {}
		self.sock = socket()
		self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		try:
			self.sock.bind((self.config['addr'], self.config['port']))
		except:
			raise slimHTTP_Error(f'Address already in use: {":".join((self.config["addr"], str(self.config["port"])))}')
		self.main_sock_fileno = self.sock.fileno()
		
		self.pollobj = epoll()
		self.pollobj.register(self.main_sock_fileno, EPOLLIN)

		self.sock.listen(10)

		self.upgraders = {}
		self.on_upgrade_pre_func = None
		self.methods = {
			b'GET' : self.GET_func
		}
		self.routes = {}

		# while drop_privileges() is None:
		# 	log('Waiting for privileges to drop.', once=True, level=5, origin='slimHTTP', function='http_serve')

	def log(self, *args, **kwargs):
		"""
		A simple print wrapper, placeholder for more advanced logging in the future.
		Joins any `*args` together and safely calls :func:'str' on each argument.
		"""
		print('[LOG] '.join([str(x) for x in args]))

	def check_config(self, conf):
		"""
		Makes sure that the given configuration *(either upon startup via `**kwargs` or
		during annotation override of configuration (`@http.configuration`))* is correct.

		:param conf: Dictionary representing a valid configuration. #TODO: Add a doc on documentation :P
		:type conf: dict
		"""
		if not 'web_root' in conf: return ConfError('Missing "web_root" in configuration.')
		if not 'index' in conf: return ConfError('Missing "index" in configuration.')
		if not 'port' in conf: return ConfError('Missing "port" in configuration.')
		if not 'addr' in conf: return ConfError('Missing "addr" in configuration.')
		if 'vhosts' in conf:
			for host in conf['vhosts']:
				if not 'web_root' in conf['vhosts'][host]: return ConfError(f'Missing "web_root" in vhost {host}\'s configuration.')
				if not 'index' in conf['vhosts'][host]: return ConfError(f'Missing "index" in vhost {host}\'s configuration.')
		return True

	def unregister(self, identity):
		"""
		Unregisters a :py:class:`slimhttpd.HTTP_CLIENT_IDENTITY`  s socket by calling `self.pollobj.unregister`
		on the client identity socket fileno.

		:param identity: Any valid `*_CLIENT_IDENTITY` handler.
		:type identity: :py:class:`slimhttpd.HTTP_CLIENT_IDENTITY` or :py:class:`spiderWeb.WS_CLIENT_IDENTITY`
		"""
		self.pollobj.unregister(identity.fileno)

	def default_config(self):
		"""
		Returns a simple but sane default configuration in case no one is given.
		Defaults to hosting the `web_root` to the `/srv/http` folder.

		:return: {'web_root' : '/srv/http', 'index' : 'index.html', 'vhosts' : { }, 'port' : 80}
		:rtype: dict
		"""
		return {
			'web_root' : '/srv/http',
			'index' : 'index.html',
			'vhosts' : {
				
			},
			'port' : 80
		}

	def configuration(self, config=None, *args, **kwargs):
		"""
		A decorator which can be set with a `@http.configuration` annotation as well as directly called.
		Using the decorator leaves some room for processing configuration before being returned
		to this function, in cases where configuration-checks needs to be isolated to a function
		in order to make the code neat.::


			@app.configuration
			def config():
				return {
					"web_root" : "./web-root",
					"index" : "index.html"
				}

		.. warning::
			The following hook would be called after socket setup.
			There is there for no point in adding `addr` or `port` to this configuration as the socket
			layer has already been set up.

		:param config: Dictionary representing a valid configuration which will be checked with :py:func:`slimhttpd.HTTP_SERVER.check_config`.
		:type config: dict
		"""
		# TODO: Merge instead of replace config?
		if type(config) == dict:
			self.config = config
		elif config:
			staging_config = config(instance=self)
			if self.check_config(staging_config) is True:
				self.config = staging_config

	def GET(self, f, *args, **kwargs):
		self.methods[b'GET'] = f

	def GET_func(self, request):
		return self.local_file(request)

	def REQUESTED_METHOD(self, request):
		if request.headers[b'METHOD'] in self.methods:
			return self.methods[request.headers[b'METHOD']](request)

	def local_file(self, request):
		path = request.headers[b'URL']
		extension = os.path.splitext(path)[1]
		if extension == '.py':
			if isfile(f'{request.web_root}/{path}'):
				if (handle := handle_py_request(f'{request.web_root}/{path}')):

					response = handle.process(request)
					if response:
						if len(response) == 1: response = {}, response # Assume payload, and pad with headers
						respond_headers, response = response

						if respond_headers:
							if b'_code' in respond_headers:
								request.ret_code = respond_headers[b'_code']
								del(respond_headers[b'_code']) # Ugly hack.. Don't like.. TODO! Fix!
							for header in respond_headers:
								request.response_headers[header] = respond_headers[header]

							if not b'Content-Type' in respond_headers:
								request.response_headers[b'Content-Type'] = b'text/html'

						else:
							request.response_headers[b'Content-Type'] = b'text/html'
				else:
					response = b''
					request.response_headers[b'Content-Type'] = b'plain/text'

				if not b'Content-Length' in request.response_headers:
					request.response_headers[b'Content-Length'] = bytes(str(len(response)), 'UTF-8')
				return response
			else:
				print(404)
				request.ret_code = 404
				data = None
		else:
			data = get_file(request)
			if data:
				request.ret_code, path, length, data = data
				mime = guess_type(path)[0] #TODO: Deviates from bytes pattern. Replace guess_type()
				if not mime and path[-4:] == '.iso': mime = 'application/octet-stream'
				if b'range' in request.headers:
					_, data_range = request.headers[b'range'].split(b'=',1)
					start, stop = [int(x) for x in data_range.split(b'-')]
					request.response_headers[b'Content-Range'] = bytes(f'bytes {start}-{stop}/{length}', 'UTF-8')
					request.ret_code = 206
				else:
					if mime == 'application/octet-stream':
						request.response_headers[b'Accept-Ranges'] = b'bytes'

				request.response_headers[b'Content-Type'] = bytes(mime, 'UTF-8') if mime else b'plain/text'
				request.response_headers[b'Content-Length'] = bytes(str(len(data)), 'UTF-8')
			else:
				request.ret_code = 404
				data = None

		return data

	def allow(self, allow_list, *args, **kwargs):
		staging_list = []
		for item in allow_list:
			if '/' in item:
				staging_list.append(ipaddress.ip_network(item, strict=False))
			else:
				staging_list.append(ipaddress.ip_address(item))
		self.allow_list = set(staging_list)
		return self.on_accept_callback

	def on_accept_callback(self, f, *args, **kwargs):
		if f:
			self.on_accept = f

	def on_accept(self, f, *args, **kwargs):
		self.on_accept_func = f

	def on_accept_func(self, socket, ip, source_port, *args, **kwargs):
		return HTTP_CLIENT_IDENTITY(self, socket, ip, source_port, on_close=self.on_close_func)

	def on_close(self, f, *args, **kwargs):
		self.on_close_func = f

	def on_upgrade(self, f, *args, **kwargs):
		self.on_upgrade_func = f

	def on_upgrade_func(self, request, *args, **kwargs):
		return None

	# def on_upgrade(self, methods, *args, **kwargs):
	#	self.upgraders = {**self.upgraders, **methods}
	#	return self.on_upgrade_router

	# def on_upgrade_router(self, f, *args, **kwargs):
	#	self.on_upgrade_pre_func = f

	# def on_upgrade_func(self, request, *args, **kwargs):
	#	if self.on_upgrade_pre_func:
	#		if self.on_upgrade_pre_func(request):
	#			return None
	#
	#	if (upgrader := request.headers[b'upgrade'].lower().decode('UTF-8')) in self.upgraders:
	#		return self.upgraders[upgrader](request)

	def on_close_func(self, CLIENT_IDENTITY, *args, **kwargs):
		self.pollobj.unregister(CLIENT_IDENTITY.fileno)
		CLIENT_IDENTITY.socket.close()
		del(self.sockets[CLIENT_IDENTITY.fileno])

	def route(self, url, *args, **kwargs):
		"""
		A decorator for statically define HTTP request path's::

			@app.route('/auth/login')
			def route_handler(request):
				print(request.headers)

		.. note:: The above example will handle both GET and POST (any user-defined method actually)

		.. warning:: If routes end with a `/`, they will be appended by `/[index]` and treated as a normal folder.
				     This means that static routes ending on `/` should be defined as `@app.route('/example/index.html')` rather than `@app.route('/example/')`.

		:param timeout: is in seconds
		:type timeout: integer
		:param fileno: Limits the return events to a specific socket/client fileno.
		:type fileno: integer
		:return: `tuple(Events.<type>, EVENT_DATA)`
		:rtype: iterator
		"""
		self.routes[url] = ROUTE_HANDLER(url)
		return self.routes[url].gateway

	def poll(self, timeout=0.2, fileno=None):
		"""
		poll is to be called from the main event loop. poll will process any queues
		in need of processing, such as accepting new clients and check for data in
		any of the poll-objects (client sockets/identeties). A basic example of a main event loop would be::


			import slimhttpd

			http = slimhttpd.host(slimhttpd.HTTP)

			while 1:
				for event, *event_data in http.poll():
					pass

		:param timeout: is in seconds
		:type timeout: integer
		:param fileno: Limits the return events to a specific socket/client fileno.
		:type fileno: integer
		:return: `tuple(Events.<type>, EVENT_DATA)`
		:rtype: iterator
		"""
		for left_over in self.sockets:
			if self.sockets[left_over].has_data():
				yield self.do_the_dance(left_over)

		for socket_fileno, event_type in self.pollobj.poll(timeout):
			if fileno:
				if socket_fileno == fileno:
					yield (socket_fileno, event_type)
			else:
				if socket_fileno == self.main_sock_fileno:
					client_socket, client_address = self.sock.accept()
					client_fileno = client_socket.fileno()
					ip_address = ipaddress.ip_address(client_address[0])
					
					## Begin the allow/deny process
					allow = True
					if self.allow_list:
						allow = False
						for net in self.allow_list:
							if ip_address in net or ipaddress == net:
								allow = True
								break

					if not allow:
						print(client_address[0], 'not in allow_list')
						client_socket.close()
						continue

					identity = self.on_accept_func(socket=client_socket, ip=client_address[0], source_port=client_address[1])
					if not identity:
						identity = HTTP_CLIENT_IDENTITY(self, client_socket, client_address, on_close=self.on_close_func)

					self.sockets[client_fileno] = identity
					self.pollobj.register(client_fileno, EPOLLIN)
					yield (Events.SERVER_ACCEPT, identity)
				else:
					## Check for data
					for client_event, *client_event_data in self.sockets[socket_fileno].poll(timeout, force_recieve=True):
						yield (client_event, client_event_data) # Yield "we got data" event

						if client_event == Events.CLIENT_DATA:
							yield self.do_the_dance(socket_fileno) # Then yield whatever result came from that data

	def do_the_dance(self, fileno):
		for parse_event, *client_parsed_data in self.sockets[fileno].build_request():
			yield (parse_event, client_parsed_data)

			if parse_event == Events.CLIENT_REQUEST:
				for response_event, *client_response_data in client_parsed_data[0].parse():
					yield (response_event, client_response_data)

					if response_event in (Events.CLIENT_RESPONSE_DATA, Events.CLIENT_URL_ROUTED) and client_response_data:
						if type(client_response_data[0]) is bytes:
							self.sockets[fileno].send(client_response_data[0])
						elif type(client_response_data[0]) is HTTP_RESPONSE:
							self.sockets[fileno].send(client_response_data[0].build())

					if not self.sockets[fileno].keep_alive:
						self.sockets[fileno].close()

class HTTPS_SERVER(HTTP_SERVER):
	def __init__(self, *args, **kwargs):
		HTTP_SERVER.__init__(self, *args, **kwargs)

	def default_config(self):
		"""
		Returns a simple but sane default configuration in case no one is given.
		Defaults to hosting the `web_root` to the `/srv/http` folder.

		:return: {'web_root' : '/srv/http', 'index' : 'index.html', 'vhosts' : { }, 'port' : 443}
		:rtype: dict
		"""
		## TODO: generate cert if not existing.
		return {
			'web_root' : '/srv/http',
			'index' : 'index.html',
			'vhosts' : {
				
			},
			'port' : 443,
			'ssl' : {
				'cert' : 'cert.pem',
				'key' : 'key.pem'
			}
		}

class HTTP_CLIENT_IDENTITY():
	"""
	client identity passed as a reference.
	"""
	def __init__(self, server, socket, address, source_port, on_close=None):
		self.server = server
		self.socket = socket
		self.fileno = socket.fileno()
		self.buffer_size = 8192
		self.address = address
		self.source_port = source_port
		self.closing = False
		self.keep_alive = False

		self.buffer = b''

		if on_close: self.on_close = on_close

	def close(self):
		if not self.closing:
			self.on_close(self)
			self.closing = True

	def on_close(self, *args, **kwargs):
		self.closing = True
		self.server.on_close_func(self)

	def poll(self, timeout=0.2, force_recieve=False):
		"""
		@force_recieve: If the caller knows there's data, we can override
		the polling event and skip straight to data recieving.
		"""
		if force_recieve or list(self.server.poll(timeout, fileno=self.fileno)):
			try:
				d = self.socket.recv(self.buffer_size)
			except: # There's to many errors that can be thrown here for differnet reasons, SSL, OSError, Connection errors etc.
					# They all mean the same thing, things broke and the client couldn't deliver data accordingly so eject.
				d = ''

			if len(d) == 0:
				self.on_close(self)
				return None

			self.buffer += d
			yield (Events.CLIENT_DATA, len(self.buffer))

	def send(self, data):
		return self.socket.send(data)

	def build_request(self):
		yield (Events.CLIENT_REQUEST, HTTP_REQUEST(self))

	def has_data(self):
		if self.closing: return False
		return True if len(self.buffer) else False

	def __repr__(self):
		return f'<slimhttpd.HTTP_CLIENT_IDENTITY @ {self.address}:{self.source_port}>'

class HTTP_REQUEST():
	"""
	General request formatter passed as an object throughout the event stack.
	"""
	def __init__(self, CLIENT_IDENTITY):
		""" A dummy parser that will return 200 OK on everything. """
		self.CLIENT_IDENTITY = CLIENT_IDENTITY
		self.headers = {}
		self.payload = b''
		self.ret_code = 200 # Default return code.
		self.ret_code_mapper = {200 : b'HTTP/1.1 200 OK\r\n',
								206 : b'HTTP/1.1 206 Partial Content\r\n',
								302 : b'HTTP/1.1 302 Found\r\n',
								404 : b'HTTP/1.1 404 Not Found\r\n',
								418 : b'HTTP/1.0 I\'m a teapot\r\n'}
		self.response_headers = {}
		self.CLIENT_IDENTITY.server.log(f'Building request/reponse for client: {CLIENT_IDENTITY}', level=5, source='HTTP_REQUEST')
		self.web_root = self.CLIENT_IDENTITY.server.config['web_root']

		#print(self.CLIENT_IDENTITY.buffer)

	def build_request_headers(self, data):
		## Parse the headers
		METHOD, header = data.split(b'\r\n',1)
		for item in header.split(b'\r\n'):
			if b':' in item:
				key, val = item.split(b':',1)
				self.headers[key.strip().lower()] = val.strip()

		METHOD, URL, proto = METHOD.split(b' ', 2)
		URI_QUERY = {}
		if b'?' in URL:
			URL, QUERIES = URL.split(b'?', 1)
			for item in QUERIES.split(b'&'):
				if b'=' in item:
					k, v = item.split(b'=',1)
					URI_QUERY[k.lower()] = v

		self.headers[b'URL'] = URL.decode('UTF-8')
		self.headers[b'METHOD'] = METHOD
		self.headers[b'URI_QUERY'] = URI_QUERY

		self.vhost = None

	def locate_index_file(self, index_files, return_any=True):
		if type(index_files) == str:
			if isfile(self.web_root + self.headers[b'URL'] + index_files):
				return index_files
			if return_any:
				return index_files
		elif type(index_files) in (list, tuple):
			for file in index_files:
				if isfile(self.web_root + self.headers[b'URL'] + file):
					if not return_any:
						return file
					break
			if return_any:
				return file

	def build_headers(self):
		x = b''
		if self.ret_code in self.ret_code_mapper:
			x += self.ret_code_mapper[self.ret_code]# + self.build_headers() + (response if response else b'')
		else:
			return b'HTTP/1.1 500 Internal Server Error\r\n\r\n'

		for key, val in self.response_headers.items():
			if type(key) != bytes: key = bytes(key, 'UTF-8')
			if type(val) != bytes: val = bytes(val, 'UTF-8')
			x += key + b': ' + val + b'\r\n'
		
		return x + b'\r\n'

	def parse(self):
		"""
		Split the HTTP data into headers and body.
		"""
		if b'\r\n\r\n' in self.CLIENT_IDENTITY.buffer:
			header, remainder = self.CLIENT_IDENTITY.buffer.split(b'\r\n\r\n', 1) # Copy and split the data so we're not working on live data.
			self.payload = b''

			self.build_request_headers(header)
			if self.headers[b'METHOD'] == b'POST':
				if b'content-length' in self.headers:
					content_length = int(self.headers[b'content-length'].decode('UTF-8'))
					self.payload = remainder[:content_length]

					if len(self.payload) < content_length:
						return (Events.CLIENT_DATA_FRAGMENTED, self)

					self.CLIENT_IDENTITY.buffer = remainder[content_length:] # Add any extended data outside of Content-Length back to the buffer
				else:
					return (Events.NOT_YET_IMPLEMENTED, NotYetImplemented('POST without Content-Length isn\'t supported yet.'))


			_config = self.CLIENT_IDENTITY.server.config
			if b'host' in self.headers and 'vhosts' in _config and self.headers[b'host'].decode('UTF-8') in _config['vhosts']:
				self.vhost = self.headers[b'host'].decode('UTF-8')
				if 'web_root' in _config['vhosts'][self.vhost]:
					self.web_root = _config['vhosts'][self.vhost]['web_root']

			# If the request *ends* on a /
			# replace it with the index file from either vhosts or default to anything if vhosts non existing.
			if self.headers[b'URL'][-1] == '/':
				vhost_specific_index = False
				if self.vhost and 'index' in _config['vhosts'][self.vhost]:
					index_files = _config['vhosts'][self.vhost]['index']
					if (_ := self.locate_index_file(index_files, return_any=False)):
						self.headers[b'URL'] += _
			if self.headers[b'URL'][-1] == '/':
				self.headers[b'URL'] += self.locate_index_file(_config['index'], return_any=True)

			# Find suitable upgrades if any
			if {b'upgrade', b'connection'}.issubset(set(self.headers)) and b'upgrade' in self.headers[b'connection'].lower():
				requested_upgrade_method = self.headers[b'upgrade'].lower()
				new_identity = self.CLIENT_IDENTITY.server.on_upgrade_func(self)
				if new_identity:
					self.CLIENT_IDENTITY.server.log(f'{self.CLIENT_IDENTITY} has been upgraded to {new_identity}', level=5, source='HTTP_REQUEST.parse()')
					self.CLIENT_IDENTITY.server.sockets[self.CLIENT_IDENTITY.fileno] = new_identity
					yield (Events.CLIENT_UPGRADED, new_identity)
				else:
					yield (Events.CLIENT_UPGRADE_ISSUE, UpgradeIssue(f'Could not upgrade client {self.CLIENT_IDENTITY} with desired upgrader: {requested_upgrade_method}'))
					return

				#self.client.server.log('{} wants to upgrade with {}'.format(self.client, self.headers[b'upgrade']), level=5, origin='slimHTTP', function='parse')
				#upgraded = self.client.server.upgrades[self.headers[b'upgrade'].lower()].upgrade(self.client, self.headers, self.payload, self.on_close)
				#if upgraded:
				#	self.client.server.log('Client has been upgraded!', level=5, origin='slimHTTP', function='parse')
				#	self.client.server.sockets[self.client.socket.fileno()] = upgraded

			elif self.headers[b'URL'] in self.CLIENT_IDENTITY.server.routes:
				yield (Events.CLIENT_URL_ROUTED, self.CLIENT_IDENTITY.server.routes[self.headers[b'URL']].parser(self))

			elif (response := self.CLIENT_IDENTITY.server.REQUESTED_METHOD(self)):
				self.CLIENT_IDENTITY.server.log(f'{self.CLIENT_IDENTITY} sent a "{self.headers[b"METHOD"].decode("UTF-8")}" request to path "[{self.web_root}/]{self.headers[b"URL"]} @ {self.vhost}"', level=5, source='HTTP_REQUEST.parse()')
				if type(response) == dict: response = json.dumps(response)
				if type(response) == str: response = bytes(response, 'UTF-8')
				yield (Events.CLIENT_RESPONSE_DATA, self.build_headers() + response if response else self.build_headers())
			else:
				self.CLIENT_IDENTITY.server.log(f'Can\'t handle {self.headers[b"METHOD"]} method.', level=2, source='HTTP_REQUEST.parse()')