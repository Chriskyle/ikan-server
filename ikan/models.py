from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(models.Model):
    nickname = models.CharField(max_length=10)
    gender = models.CharField(max_length=2, default=u"男")
    avatar = models.CharField(max_length=100)
    create_time = models.DateTimeField(u'create time', auto_now_add=True)
    is_active = models.BooleanField(default=True)


class ThirdParty(models.Model):
    openid = models.CharField(max_length=50)
    bind_type = models.IntegerField(default=0)

    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class Bill(models.Model):
    total = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)

    account = models.OneToOneField(Account, on_delete=models.CASCADE)


class BillLog(models.Model):
    amount = models.IntegerField(default=0)
    create_time = models.DateTimeField(u'create time', auto_now_add=True)
    Bill = models.ForeignKey(Bill, related_name='bill_logs', on_delete=models.CASCADE)


class Denomination(models.Model):
    amount = models.IntegerField(default=0)
    qr_code = models.CharField(max_length=50)
    payment_code = models.CharField(max_length=20)


class Segment(models.Model):
    name = models.CharField(max_length=10)


class Category(models.Model):
    name = models.CharField(max_length=10)


class Recommend(models.Model):
    name = models.CharField(max_length=20)


class Feed(models.Model):
    title = models.CharField(max_length=20)
    url = models.CharField(max_length=5000)
    thumbnail = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100, default='')
    synopsis = models.CharField(max_length=100)
    duration = models.DurationField(default=0)
    type = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    watch_count = models.IntegerField(default=0)
    diamond = models.IntegerField(default=0)
    earn_diamond = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    create_time = models.DateTimeField(u'create time', auto_now_add=True)

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    recommend = models.ForeignKey(Recommend, on_delete=models.CASCADE, blank=True, null=True)


class Actor(models.Model):
    name = models.CharField(max_length=10)
    avatar = models.CharField(max_length=100)


class Role(models.Model):
    playing = models.CharField(max_length=10)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, related_name='roles', on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    create_time = models.DateTimeField(u'create time', auto_now_add=True)


class Like(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("account", "feed"),)


class BuyLog(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("account", "feed"),)


class Notification(models.Model):
    type_choices = (
        (0, 'system'),
        (1, 'activity'),
        (2, 'personal')
    )
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    type = models.IntegerField(choices=type_choices, default=0)
    create_time = models.DateTimeField(u'create_time', auto_now_add=True)


class Feedback(models.Model):
    content = models.TextField()
    create_time = models.DateTimeField(u'create time', auto_now_add=True)


class Solution(models.Model):
    title = models.CharField(max_length=20)
    url = models.CharField(max_length=100)


class UploadedImageModel(models.Model):
    STATUS_SIZES = (
        (0, '进行中'),
        (1, '已完成'),
    )
    name = models.CharField('名称', max_length=10)
    image = models.ImageField('图片', upload_to='static/images/%Y/%m/%d', blank=False)
    create_date = models.DateTimeField("时间", auto_now_add=True)
    status = models.IntegerField('状态', default=0, choices=STATUS_SIZES)

    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        db_table = "ikan_image"


class Version(models.Model):
    code = models.IntegerField(default=0)
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=200)
    size = models.CharField(max_length=10)
    update_log = models.TextField()
    md5 = models.CharField(max_length=50)
    is_constraint = models.BooleanField(default=False)
    create_date = models.DateTimeField("更新日期", auto_now_add=True)
