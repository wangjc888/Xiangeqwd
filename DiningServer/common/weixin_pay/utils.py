# -*- coding=utf-8 -*-

import hashlib
import re
from random import Random
import requests


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
	"""
	Returns a bytestring version of 's', encoded as specified in 'encoding'.

	If strings_only is True, don't convert (some) non-string-like objects.
	"""
	if strings_only and isinstance(s, (types.NoneType, int)):
		return s
	if not isinstance(s, str):
		try:
			return str(s)
		except UnicodeEncodeError:
			if isinstance(s, Exception):
				# An Exception subclass containing non-ASCII data that doesn't
				# know how to print itself properly. We shouldn't raise a
				# further exception.
				return ' '.join([smart_str(arg, encoding, strings_only,
						errors) for arg in s])
			return unicode(s).encode(encoding, errors)
	# elif isinstance(s, unicode):
	#     return s.encode(encoding, errors)
	elif s and encoding != 'utf-8':
		return s.decode('utf-8', errors).encode(encoding, errors)
	else:
		return s


def format_url(params, api_key=None):
	url = "&".join(['%s=%s'%(key, smart_str(params[key])) for key in sorted(params)])
	if api_key:
		url = '%s&key=%s' % (url, api_key)
	return url


def calculate_sign(params, api_key):
	#签名步骤一：按字典序排序参数, 在string后加入KEY
	url = format_url(params, api_key)
	#签名步骤二：MD5加密, 所有字符转为大写
	return hashlib.md5(url.encode('utf-8')).hexdigest().upper()


def dict_to_xml(params, sign):
	xml = ["<xml>",]
	for (k, v) in params.items():
		if (v.isdigit()):
			xml.append('<%s>%s</%s>' % (k, v, k))
		else:
			xml.append('<%s><![CDATA[%s]]></%s>' % (k, v, k))
	xml.append('<sign><![CDATA[%s]]></sign></xml>' % sign)
	return ''.join(xml)


def xml_to_dict(xml):
	if xml[0:5].upper() != "<XML>" and xml[-6].upper() != "</XML>":
		return None, None

	result = {}
	sign = None
	content = ''.join(xml[5:-6].strip().split('\n'))

	pattern = re.compile(r"<(?P<key>.+)>(?P<value>.+)</(?P=key)>")
	m = pattern.match(content)
	while(m):
		key = m.group("key").strip()
		value = m.group("value").strip()
		if value != "<![CDATA[]]>":
			pattern_inner = re.compile(r"<!\[CDATA\[(?P<inner_val>.+)\]\]>")
			inner_m = pattern_inner.match(value)
			if inner_m:
				value = inner_m.group("inner_val").strip()
			if key == "sign":
				sign = value
			else:
				result[key] = value

		next_index = m.end("value") + len(key) + 3
		if next_index >= len(content):
			break
		content = content[next_index:]
		m = pattern.match(content)

	return sign, result


def validate_post_xml(xml, appid, mch_id, api_key):
	sign, params = xml_to_dict(xml)
	if (not sign) or (not params):
		return None

	remote_sign = calculate_sign(params, api_key)
	if sign != remote_sign:
		return None

	if params["appid"] != appid or params["mch_id"] != mch_id:
		return None

	return params


def random_str(randomlength=8):
	chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
	random = Random()
	return "".join([chars[random.randint(0, len(chars) - 1)] for i in range(randomlength)])

'''不使用证书'''
def post_xml(url, xml):
	return requests.post(url, data=xml)


'''使用证书'''
from requests.auth import HTTPBasicAuth
def post_xml_ssl(url, data, headers, cert, key, cacert):
	return requests.post(url, data=data, headers=headers, cert=(cert,key), verify=cacert)

# 其中SSLCERT_PATH, SSLKEY_PATH 为你的crt key(pem)文件在你服务器上的相对路径.


# try:  
#     import pycurl  
#     from cStringIO import StringIO  
# except ImportError:  
#     from io import StringIO

# def post_xml_ssl(url, xml, second=30, cert=True, post=True): 
#     """使用证书"""  

#     curl = pycurl.Curl()  
#     curl.setopt(pycurl.SSL_VERIFYHOST, False)  
#     curl.setopt(pycurl.SSL_VERIFYPEER, False)  
#     #设置不输出header  
#     curl.setopt(pycurl.HEADER, False) 


#     curl.setopt(pycurl.URL, url)  
#     curl.setopt(pycurl.TIMEOUT, second)  
#     #设置证书  
#     #使用证书：cert 与 key 分别属于两个.pem文件  
#     #默认格式为PEM，可以注释  
#     if cert:  
#         curl.setopt(pycurl.SSLKEYTYPE, "PEM")  
#         curl.setopt(pycurl.SSLKEY, "/path/to/DiningServer/ssl/apiclient_key.pem")  
#         curl.setopt(pycurl.SSLCERTTYPE, "PEM")  
#         curl.setopt(pycurl.SSLCERT, "/path/to/DiningServer/ssl/apiclient_cert.pem")  
#     #post提交方式  
#     if post:  
#         curl.setopt(pycurl.POST, True)  
#         curl.setopt(pycurl.POSTFIELDS, xml)  
#     buff = StringIO()  
#     curl.setopt(pycurl.WRITEFUNCTION, buff.write)  

#     curl.perform()  
#     # curl.close()  
#     return buff.getvalue() 
