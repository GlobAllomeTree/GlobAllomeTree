

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
        if (not requested_format \
        or not requested_format.endswith('full'))\
        and hasattr(self, 'simple_serializer_class'):
            self.serializer_class = self.simple_serializer_class
       
        if requested_format and requested_format.startswith('csv'):
            self.paginate_by = None
        else:
            self.paginate_by = 50

        return request


class NameQueryMixin(object):
    """
        mixin that allows a simple query by name on the queryset
    """

    def get_queryset(self):
        """
        This view should return a list of
            if q, all tags that contain q
            else, all tags
        """
        queryset = self.queryset
        query = self.request.QUERY_PARAMS.get('q', None)
        unique_name = self.request.QUERY_PARAMS.get('unique_name', False)
        if query is not None:
            queryset = queryset.filter(Name__istartswith=query)
        if unique_name:
            queryset = queryset.distinct('Name')
        return queryset
