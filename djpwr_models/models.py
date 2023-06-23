from django.apps import apps as django_apps


def get_model(model_label):
    return django_apps.get_model(model_label)
