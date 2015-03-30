

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
