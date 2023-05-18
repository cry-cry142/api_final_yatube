from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        'Group', on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True
    )

    def __str__(self):
        return self.text[:settings.COUNT_CHAR_POST_STR]


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.text


class Follow(models.Model):
    following = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
    )
    user = models.ForeignKey(
        User,
        verbose_name='Подписчики',
        on_delete=models.CASCADE,
        related_name='follower',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'user'],
                name='unique_author_user_following'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='author_cannot_subscribe'
            ),
        ]
