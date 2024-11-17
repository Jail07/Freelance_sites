from datetime import timezone

from django.db import models

from account.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='project')
    budget = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class CodeImage(models.Model):
    image = models.ImageField(upload_to='images')
    post = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')


class Bids(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='proposals')
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='proposals')
    amount = models.PositiveIntegerField()
    message = models.TextField()
    status = models.BooleanField(default=False)
    term = models.DateTimeField(null=False)


class Order(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='orders')
    payment_status = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=False)


class Feedback(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='replies')
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='feedback')
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:15] + '...'

    class Meta:
        ordering = ('-created',)


class Bid(models.Model):
    id = models.ForeignKey(Bids, primary_key=True, on_delete=models.CASCADE, related_name='bids')
    freelancer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bids')
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bids')
    amount = models.PositiveIntegerField()
    message = models.TextField()
    status = models.BooleanField(default=False)


class Category_Project(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='categories')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')







