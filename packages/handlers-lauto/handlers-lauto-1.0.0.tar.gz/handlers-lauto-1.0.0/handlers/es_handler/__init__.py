from logging import StreamHandler
from requests_aws4auth import AWS4Auth
from handlers.es_handler.models import *
from elasticsearch import Elasticsearch,RequestsHttpConnection
import datetime
import ast
import pytz


class ElasticHandler(StreamHandler):
	def elasticConnection(self):
		self.es = Elasticsearch(hosts=[self.hosts],
					http_auth=AWS4Auth(self.aws_access_key,self.aws_secret_key, self.aws_region,'es'),
					use_ssl=True,
					verify_certs=True,
					connection_class=RequestsHttpConnection)
		self.es.indices.create(index=self.index, ignore=400)

	def __init__(self, hosts,aws_access_key,aws_secret_key,aws_region,index):
		StreamHandler.__init__(self)
		metadata.create_all(engine)
		connected = False
		self.hosts = hosts
		self.aws_access_key = aws_access_key
		self.aws_secret_key = aws_secret_key
		self.aws_region = aws_region
		self.index = index

		while not connected:
			try:
				self.elasticConnection()
				connected = True
			except:
				connected = False

	def sendToElastic(self,i):
		try:
			aux = ast.literal_eval(i.msg)
		except:
			aux = dict()
			aux['msg'] = i.msg
		aux['data_entrada'] = i.data_entrada
		aux['levelname'] = i.levelname
		aux['name'] = i.name
		aux['pathname'] = i.pathname
		aux['lineno'] = i.lineno
		aux['args'] = i.args
		aux['exc_info'] = i.exc_info
		self.es.index(index=self.index, body=aux)

	def sendObjects(self):
		try:
			for i in session.query(ElasticLogStructure).all():
				self.sendToElastic(i)
				session.delete(i)
				session.commit()
		except:
			self.elasticConnection()

	def emit(self, record):
		log = ElasticLogStructure()
		time = datetime.datetime.now()
		log.data_entrada = time
		log.levelname = record.levelname
		log.name = record.name
		log.pathname = record.pathname
		log.lineno = record.lineno
		log.msg = record.msg
		log.exc_text = record.exc_text
		log.stack_info = record.stack_info
		log.args = ''
		for i in record.args:
			log.args+=(i+',')
		log.exc_info = record.exc_info
		session.add(log)
		session.commit()
		self.sendObjects()