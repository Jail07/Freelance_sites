from django.db import models
from account.models import Profile
import uuid


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(upload_to='main', null=True, blank=True, default="main/default.jpg")
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except AttributeError:
            url = './media/main/default.jpg'
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    def update_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value='up').count()
        total_votes = reviews.count()

        if total_votes > 0:
            ratio = (up_votes / total_votes) * 100
        else:
            ratio = 0

        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()

    @property
    def getVoteCount(self):
        return {'total_votes': self.vote_total, 'vote_ratio': self.vote_ratio}


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return f'{self.owner} voted {self.value}'


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
