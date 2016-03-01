
from django.http import HttpResponseRedirect

class RequireActiveUser(object):

    def process_request(self, request):
        protected_cms_pages = ['download-fantallometrik',] 
        
        if not request.user.is_active:
        	
        	for page in protected_cms_pages:
	        	if request.path.find(page) != -1:
	        		return HttpResponseRedirect("/accounts/register/")
       