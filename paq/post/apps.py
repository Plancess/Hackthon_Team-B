from django.apps import AppConfig


class PostConfig(AppConfig):
    name = 'post'
    verbose_name = "Post Management"

    def ready(self):
        super().ready()
