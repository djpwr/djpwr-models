DJPWR-Models - Model, Manager and Query related improvements for the Django web framework.



from djpwr_models import QuerySet, from_queryset, attr_filter, 


class BookQuerySet(QuerySet):
    author = attr_filter('author')
    published = attr_filter('published', True)


class BookManager(from_queryset(BookQuerySet))
    pass
