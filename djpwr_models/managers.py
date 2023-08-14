from django.apps import apps as django_apps
from django.db.models.manager import BaseManager


def get_manager(manager_label):
    """
    Get a model's Manager instance by label ('app_label.ModelName').
    If manager_label consists of three parts (i.e. users.User.inactive),
    this attribute - which should be a Manager instance - will be returned.

    :param manager_label: Django model string: 'app_label.ModelClass[.manager_attribute]'
    :return: Manager instance
    """
    manager_identifier = manager_label.split('.')

    model_label = '.'.join(manager_identifier[:2])

    model_class = django_apps.get_model(model_label)

    if len(manager_identifier) == 3:
        return getattr(model_class, manager_identifier[2])

    return model_class._default_manager


def from_queryset(qs_class):
    return BaseManager.from_queryset(qs_class)


def attr_filter(attr_lookup, filter_value=None, *, allow_only_values=None):
    """
    Create a Manager filter method based on an ORM attribute lookup, either
    with or without a fixed value.

    :param attr_lookup: ORM attribute_lookup, can use dots instead of dunder
    :param filter_value: Value to use for filtering
    :param allow_only_values: Attributes allowed to return as flat list
    :return: Manager filter function

    Example:

    class BookQueryset(Queryset):
        author = attr_filter('author')
        without_publisher = attr_filter('publisher__isnull', True)

    some_author = Author.objects.get(id=1234)
    books_by_some_author = Book.objects.author(some_author)
    books_without_publisher = Book.objects.without_publisher()
    """
    if filter_value is None:
        return attr_filter_arg_value(attr_lookup, allow_only_values=allow_only_values)
    else:
        return attr_filter_fixed_value(
            attr_lookup, filter_value, allow_only_values=allow_only_values
        )


def attr_filter_arg_value(attr_lookup, *, allow_only_values=None):
    """
    Create a Manager filter method based on an ORM attribute lookup

    :param attr_lookup: ORM attribute_lookup, can use dots instead of dunder
    :param allow_only_values: Attributes allowed to return as flat list
    :return: Manager filter function

    Example:

    class BookQueryset(Queryset):
        author = attr_filter_arg_value('author')
        publisher_city = attr_filter_arg_value('publisher__city')

    books_by_some_author = Book.objects.author('Some Author')
    books_published_in_rome = Book.objects.publisher_city('Rome')
    """
    def filter_func(self, value):
        filter_kwargs = {attr_lookup: value}

        return self.filter(**filter_kwargs)

    if allow_only_values is None:
        return filter_func

    return allow_only_values(*allow_only_values)(filter_func)


def attr_filter_fixed_value(attr_lookup, value, allow_only_values=None):
    """
    Create a Manager filter method based on an ORM attribute lookup and a
    specific value

    :param attr_lookup: ORM attribute_lookup, can use dots instead of dunder
    :param value: Value to use for filtering
    :param allow_only_values: Attributes allowed to return as flat list
    :return: Manager filter function

    Example:

    class BookQueryset(Queryset):
        without_publisher = attr_filter_fixed_value('publisher__isnull', True)

    books_without_publisher = Book.objects.without_publisher()
    """

    def filter_func(self):
        filter_kwargs = {attr_lookup: value}

        return self.filter(**filter_kwargs)

    if allow_only_values is None:
        return filter_func

    return allow_only_values(*allow_only_values)(filter_func)


def allow_only_values(*attribute_names):
    """
    Decorator for manager methods to optionally return only a specific value.

    Its purpose is to clarify which individual values may be retrieved
    by the application from a manager method's, without resorting to
    .values_list(..., flat=True) just anywhere in the code.

    Example:

    class BookManager(Manager):
        @allow_only_values('id')
        def author_name(self, author):
            return self.filter(author__name=author_name)

    book_ids_by_some_author = Book.objects.author_name('Some Author', only_values='id')
    """

    def func_wrapper(manager_method):
        def only_values_wrapper(*args, **kwargs):
            only_values_attribute = kwargs.pop('only_values', None)

            qs = manager_method(*args, **kwargs)

            if only_values_attribute:
                if only_values_attribute not in attribute_names:
                    raise ValueError(f"only_values='{only_values_attribute}' not allowed")

                qs = qs.values_list(only_values_attribute, flat=True)

            return qs

        return only_values_wrapper

    return func_wrapper


__all__ = [
    'get_manager',
    'from_queryset',
    'attr_filter',
    'allow_only_values',
]
