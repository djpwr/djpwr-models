from django.db import models


class ReusableForeignKey(models.ForeignKey):
    """
    Save one line of code for every ForeignKey you define!

    Example:
        apps.example.fields.py

        class ExampleForeignKey(ReusableForeignKey):
            model_label = 'example.Example'
            verbose_name = _("Example")

        apps.some_app.models.py

        class SomeModel(models.Model):
            class Meta:
                default_related_name = 'some_models'

            example = ExampleForeignKey(on_delete=models.CASCADE)
    """
    model_label = None
    verbose_name = None

    def __init__(self, *args, **kwargs):
        params = kwargs.copy()

        params['to'] = self.model_label
        params['verbose_name'] = params.get('verbose_name', self.verbose_name)

        super().__init__(*args, **params)

    def deconstruct(self):

        name, path, args, kwargs = super().deconstruct()

        del kwargs['verbose_name']

        return name, path, args, kwargs
