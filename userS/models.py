from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.
class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    raitingAuthor = models.SmallIntegerField(default=0)
    
    def update_rating(self):
        post_rating = self.post_set.aggregate(postRating=Sum('rating'))
        postRat = 0
        postRat += post_rating.get('postRating')

        comment_rating = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        comRat = 0
        comRat += comment_rating.get('commentRating')

        self.raitingAuthor = postRat * 3 + comRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    news = 'nw'
    article = 'ar'
    CHOICE_CATEGORY = (
        (news, 'Новости'),
        (article, 'Статья'),
    )

    categoryType = models.CharField(max_length=2, choices=CHOICE_CATEGORY, default=article)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:124]}...'


class PostCategory(models.Model):
    postTrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryTrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
