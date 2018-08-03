# # from django.db import models
#
# # Create your models here.
#
# from django.db import models
# from django.utils import timezone
# from django.contrib.auth.models import User
#
# # Create your models here.
#
# # Blogpost to be indexed into ElasticSearch
# class BlogPost(models.Model):
#    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogpost');
#    posted_date = models.DateField(default=timezone.now);
#    title = models.CharField(max_length=200);
#    text = models.TextField(max_length=1000);
#    //////////////////////////
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .search import BlogPostIndex
from django.db.models.signals import post_save
from django.dispatch import receiver


# Blogpost to be indexed into ElasticSearch
class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogpost')
    posted_date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=1000)

    # Add indexing method to BlogPost
    def indexing(self):
        obj = BlogPostIndex(
            meta={'id': self.id},
            author=self.author.username,
            posted_date=self.posted_date,
            title=self.title,
            text=self.text
        )
        obj.save(index='blogpost-index')
        return obj.to_dict(include_meta=True)


@receiver(post_save, sender=BlogPost)
def index_post(sender, instance, **kwargs):
    instance.indexing()