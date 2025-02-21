from django.utils.functional import cached_property

from .. import settings


class QueryPage:
    """
    Container for a single 'page' of a queryset
    """
    def __init__(self, queryset, current_page: int, page_size: int = None,
                 merge_final_results: int = None):

        self.queryset = queryset
        self.current_page = int(current_page)

        if page_size is None:
            self.page_size = settings.PAGINATION['page_size']
        else:
            self.page_size = int(page_size)

        if merge_final_results is None:
            self.merge_final_results = settings.PAGINATION['merge_final_results']
        else:
            self.merge_final_results = int(merge_final_results)

    def __iter__(self):
        for row in self.rows:
            yield row

    @cached_property
    def rows(self) -> list:
        start_offset = (self.current_page - 1) * self.page_size
        end_offset = self.current_page * self.page_size

        return self.queryset[start_offset:end_offset]

    @cached_property
    def result_count(self) -> int:
        return self.queryset.count()

    @property
    def current_page_valid(self):
        return 1 <= self.current_page <= self.page_count

    @property
    def has_previous_page(self) -> bool:
        return self.current_page > 1

    @property
    def has_next_page(self) -> bool:
        return self.current_page < self.page_count

    @property
    def page_count(self) -> int:
        return self._full_page_count + self._partial_page_count

    @property
    def _final_page_merged(self) -> bool:
        return self.result_count % self.page_size <= self.merge_final_results

    @property
    def _full_page_count(self) -> int:
        return int(self.result_count / self.page_size)

    @property
    def _partial_page_count(self) -> int:
        if self.result_count == 0:
            return 0

        if self.result_count < self.page_size:
            return 1

        if not self._final_page_merged:
            return 1

        return 0
