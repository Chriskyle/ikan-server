from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ikan.models import Feed, Category, Segment, Account, Actor, Feedback, Notification, Solution, ThirdParty, \
    UploadedImageModel, Bill, Like, Comment, Version, Denomination, BuyLog, Recommend


class BillSerializer(ModelSerializer):
    class Meta:
        model = Bill
        exclude = ('account',)


class AccountSerializer(ModelSerializer):
    balance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        exclude = ('create_time', 'is_active')

    @staticmethod
    def get_balance(obj):
        return Bill.objects.get(account=obj).balance


class DenominationSerializer(ModelSerializer):
    class Meta:
        model = Denomination
        fields = "__all__"


class CreateAccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        exclude = ('create_time', 'is_active')


class ThirdPartySerializer(ModelSerializer):
    class Meta:
        model = ThirdParty
        fields = "__all__"


class FeedAccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'nickname', 'avatar')


class ActorSerializer(ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class CommentListSerializer(ModelSerializer):
    account = FeedAccountSerializer(read_only=True)
    create_time = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_create_time(obj):
        return timezone.localtime(obj.create_time).strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Comment
        exclude = ('feed',)


class CommentDetailSerializer(ModelSerializer):
    create_time = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_create_time(obj):
        return timezone.localtime(obj.create_time).strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Comment
        fields = "__all__"


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class BuyLogSerializer(ModelSerializer):
    class Meta:
        model = BuyLog
        fields = "__all__"


class SegmentSerializer(ModelSerializer):
    class Meta:
        model = Segment
        fields = "__all__"


class FeedListSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = ('id', 'title', 'thumbnail', 'synopsis', 'diamond')


class FeedDetailSerializer(ModelSerializer):
    account = FeedAccountSerializer()
    roles = RoleSerializer(many=True)
    create_time = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_create_time(obj):
        return timezone.localtime(obj.create_time).strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Feed
        fields = ('id', 'url', 'title', 'thumbnail', 'synopsis', 'like_count',
                  'watch_count', 'create_time', 'account', 'roles', 'diamond', 'earn_diamond', 'file_name')


class CategorySerializer(ModelSerializer):
    feeds = serializers.SerializerMethodField()

    @staticmethod
    def get_feeds(obj):
        feeds = Feed.objects.filter(category=obj).order_by('?')[:4]
        return FeedListSerializer(feeds, many=True, read_only=True).data

    class Meta:
        model = Category
        fields = ('id', 'name', "feeds")


class RecommendSerializer(ModelSerializer):
    feeds = serializers.SerializerMethodField()

    @staticmethod
    def get_feeds(obj):
        feeds = Feed.objects.filter(recommend=obj)
        return FeedListSerializer(feeds, many=True, read_only=True).data

    class Meta:
        model = Recommend
        fields = ('id', 'name', "feeds")


class NotificationSerializer(ModelSerializer):
    create_time = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_create_time(obj):
        return timezone.localtime(obj.create_time).strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Notification
        fields = "__all__"


class SolutionSerializer(ModelSerializer):
    class Meta:
        model = Solution
        fields = "__all__"


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"


class UploadImageSerializer(ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = UploadedImageModel
        fields = ('name', 'image', 'account', 'status')


class VersionSerializer(ModelSerializer):
    class Meta:
        model = Version
        exclude = ('create_date', 'id')
