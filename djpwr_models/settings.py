from django.conf import settings

MODEL_SETTINGS = getattr(settings, 'DJPWR_MODELS', {})

PAGINATION = {
    'page_size': MODEL_SETTINGS.get('query_page_size', 100),
    'merge_final_results': MODEL_SETTINGS.get('query_merge_final_results', 0),
}
