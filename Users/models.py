from django.contrib.auth.models import User
from django.db import models
from Ranks.models import Rank
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.html import mark_safe

class Badge(models.Model):
    index = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="Badge_img")


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    STATUS = (
        ('regular', 'Regular'),
        ('subscriber', 'Subscriber'),
        ('moderator', 'Moderator')
    )

    status = models.CharField(max_length=20, choices=STATUS, default='regular')
    tel = models.CharField(max_length=16, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    pfp = models.ImageField(upload_to='profile_pics/', default='default_avatar.png')  # Change here
    rank = models.ManyToManyField(Rank, blank=True)
    badges = models.ManyToManyField(Badge, related_name='customusers', blank=True)
    bio = models.TextField(max_length=150, null=True, blank=True)
    enrolled_courses = models.ManyToManyField('Courses.Course', related_name='enrolled_users', blank=True)
    liked_videos = models.ManyToManyField("Courses.Video", blank=True, null=True)
    liked_products = models.ManyToManyField("Products.Product", blank=True, null=True)
    last_added_points_time = models.DateTimeField(blank=True, null=True)
    # liked_videos = models.ManyToManyField('Courses.Video', blank=True)

    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    points = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def calculate_profits(self):
        return self.transactions.filter(type='profit', status=True).aggregate(models.Sum('amount'))['amount__sum'] or 0

    def calculate_losses(self):
        return self.transactions.filter(type='loss', status=True).aggregate(models.Sum('amount'))['amount__sum'] or 0

    def calculate_balance(self):
        profits = self.calculate_profits()
        losses = self.calculate_losses()
        return profits - losses

    def calculate_overall_progress(self):
        # enrolled_courses = self.enrolled_courses.all()
        overall_progress = 0
        total_courses = 0  # enrolled_courses.count()

        # for course in enrolled_courses:
        #     course_progression, created = CourseProgression.objects.get_or_create(user=self, course=course)
        #     course_progress = course_progression.calculate_progression()
        #     overall_progress += course_progress

        if total_courses > 0:
            overall_progress_percentage = (overall_progress / (total_courses * 100)) * 100
        else:
            overall_progress_percentage = 0

        return overall_progress_percentage

    def pfp_image(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.pfp.url))


class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, related_name='transactions', null=True, on_delete=models.CASCADE) 
    TYPE = (
        ('profit', 'Profit'),
        ('loss', 'Loss'),
    )

    type = models.CharField(max_length=20, choices=TYPE, blank=False,  null=True)
    pair = models.CharField(max_length=20, blank=False,  null=True)
    amount = models.FloatField()
    img = models.ImageField(upload_to='user_transactions', blank=False, null=True)
    status = models.BooleanField(default=False, null=False, blank=False)
    date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class Professor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='professor')
    description = models.CharField(max_length=255, blank=False, null=True)

    def __str__(self):
        return str(self.user)


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    line = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.line}, {self.city}, {self.country} {self.zip_code}"


@receiver(post_save, sender=User)
def create_custom_user(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'customuser'):
        CustomUser.objects.create(user=instance, email=instance.email)

@receiver(post_save, sender=User)
def save_custom_user(sender, instance, **kwargs):
    try:
        instance.customuser.save()
    except CustomUser.DoesNotExist:
        pass


@receiver(pre_save, sender=CustomUser)
def update_user_email(sender, instance, **kwargs):
    if instance.pk:
        try:
            original_instance = CustomUser.objects.get(pk=instance.pk)
            if original_instance.email != instance.email:
                User.objects.filter(pk=instance.user.pk).update(email=instance.email)
        except CustomUser.DoesNotExist:
            pass
