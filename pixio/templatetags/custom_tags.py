from django import template
from django.urls import resolve
from django.urls.exceptions import Resolver404
from loguru import logger

register = template.Library()


# This the custom filter, name is getitems
def getdata(json_data, args):
	func_name = ""
	try:
		myfunc, myargs, mykwargs = resolve(args)
		if myfunc:
			logger.success("*" * 50)
			print()
			logger.debug("Function Name:> {} ", myfunc.__name__, feature="f-strings")
			logger.debug("Module Name:> {} ", myfunc.__module__, feature="f-strings")
			logger.debug("URL_Path:> {} ", args, feature="f-strings")
			func_name = myfunc.__name__
			print()
			logger.success("*" * 50)
	except Resolver404:
		logger.debug("something went wrong", feature="f-strings")
		pass

	return json_data.get(func_name)


register.filter("getdata", getdata)


# request.path	                  /home/
# request.get_full_path	         /home/?q=test
# request.build_absolute_uri	 http://127.0.0.1:8000/home/?q=test
