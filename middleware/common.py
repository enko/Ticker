import re

class BrowserDetectionMiddleware(object):
	"""
	Middleware to detect a wap, mobile html or full compatible browser
	"""
	
	def process_request(self, request):
		browser_type = None
			
		if (request.META.has_key('HTTP_ACCEPT')):
			http_accept = request.META['HTTP_ACCEPT']
			# normal browser doesn't accept wml to render, so we can split this case 
			if 'wml' in http_accept:
				browser_type = 'wap'
			else:
				user_agent = request.META['HTTP_USER_AGENT'].lower()
				pattern = "(mobile|iphone|android|symbian|blackberry|rim)"
				prog = re.compile(pattern, re.IGNORECASE)
				match = prog.search(user_agent)
				
				if match:
					browser_type = 'mobile'
				else: 
					browser_type = 'full'
		
		request.browser_type = browser_type