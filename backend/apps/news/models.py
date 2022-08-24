from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}: {self.title}'
