from django.db.models import QuerySet

from .pages import QueryPage


class PowerQuerySet(QuerySet):
    page_class = QueryPage
    related_prefetched = []
    related_selected = []

    def with_related(self):
        return (
            self.prefetch_related(*self.related_prefetched)
                .select_related(*self.related_selected)
        )

    def without_related(self):
        return self.prefetch_related(None).select_related(None)

    def page(self, page_number, page_size=None):
        return self.page_class(self, page_number, page_size)
