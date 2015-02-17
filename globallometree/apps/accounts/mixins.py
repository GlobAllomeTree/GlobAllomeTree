from django.http import HttpResponseRedirect

class RestrictedPageMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return super(RestrictedPageMixin, self).dispatch(request, *args, **kwargs)

