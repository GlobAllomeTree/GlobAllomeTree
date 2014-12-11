

class SimpleSerializerMixin(object):
    """
        mixin that looks for the formats simplejson, simplexml
        and switches to the simple_serializer_class set on the ViewSet or View
    """


    def initialize_request(self, request, *args, **kwargs):
        """
        Allow for switching out the serializer based on the request 
        """
        request = super(SimpleSerializerMixin, self).initialize_request(request, *args, **kwargs)

        requested_format = request.GET.get('format', False)
        if(requested_format) \
        and requested_format.startswith('simple') \
        and hasattr(self, 'simple_serializer_class'):
            self.serializer_class = self.simple_serializer_class
        else:
            # The hyperlinked views are paginated since they are slower to render
            # and cannot use the elasticsearch database
            self.paginate_by = 10
        return request
