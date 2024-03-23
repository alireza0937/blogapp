from django.db import models


class Posts(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Posts"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.title} -> {self.content}"


class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    text = models.TextField()
    email = models.EmailField()
    answer = models.ForeignKey(
        "Comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    def __str__(self):
        return f"{self.email} -> {self.text}"

    class Meta:
        db_table = "Comments"
        verbose_name_plural = "Comments"
        
        
