from django.db.models import Q
from rest_framework.views import APIView

from ikan.core import paginator
from ikan.core.const import const
from ikan.core.response import XResponse
from ikan.decorators.common_validate import account_personal
from ikan.decorators.common_validate import login_required
from ikan.models import Feed, Category, Like, Comment, Segment, BuyLog, Bill, Recommend
from ikan.serializers import FeedDetailSerializer, FeedListSerializer, \
    CategorySerializer, LikeSerializer, CommentListSerializer, SegmentSerializer, CommentDetailSerializer, \
    BuyLogSerializer, RecommendSerializer
from ikan.service.token.util import decode_token


class FeedView(APIView):

    @staticmethod
    def get(request, pk):
        try:
            feed = Feed.objects.get(pk=pk)
            feed.watch_count = feed.watch_count + 1
            feed.save()
            serializer = FeedDetailSerializer(feed)

            def is_like():
                token = request.META.get(const.META_TOKEN, const.UNKNOWN)

                if token.strip() != const.UNKNOWN:
                    payload = decode_token(token)
                    account_id = payload.get(const.ACCOUNT_ID)
                    likes = Like.objects.filter(account=account_id).filter(feed=pk)
                    return likes.exists()
                else:
                    return False

            def is_bought():
                token = request.META.get(const.META_TOKEN, const.UNKNOWN)

                if token.strip() != const.UNKNOWN:
                    payload = decode_token(token)
                    account_id = payload.get(const.ACCOUNT_ID)
                    buy_logs = BuyLog.objects.filter(account=account_id).filter(feed=pk)
                    return buy_logs.exists()
                else:
                    return False

            data = serializer.data
            data["is_like"] = is_like()
            data["is_bought"] = is_bought()
            return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=data)
        except Feed.DoesNotExist:
            return XResponse(status_code=const.CODE_10005, msg=const.MSG_FAIL)

    @staticmethod
    def post(request):
        serializer = FeedListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=serializer.data)
        return XResponse(status_code=const.CODE_10007, msg=const.MSG_FAIL)

    @account_personal
    def patch(self, request, pk):
        try:
            feed = Feed.objects.get(pk=pk)
            serializer = FeedDetailSerializer(feed, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=serializer.data)
            else:
                return XResponse(status_code=const.CODE_10007, msg=const.MSG_FAIL)
        except Feed.DoesNotExist:
            return XResponse(status_code=const.CODE_10005, msg=const.MSG_FAIL)

    @account_personal
    def delete(self, request, pk):
        try:
            feed = Feed.objects.get(pk=pk)
            serializer = FeedDetailSerializer(feed, data=request.data)
            feed.delete()
            return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=serializer.data)
        except Feed.DoesNotExist:
            return XResponse(status_code=const.CODE_10005, msg=const.MSG_FAIL)


class HomeFeedView(APIView):

    @staticmethod
    def get(request):
        segment = request.GET.get(const.SEGMENT)

        if segment is not None:
            feeds = Feed.objects.all().filter(segment__name=segment)
        else:
            feeds = Feed.objects.all()

        return paginator.api_paging(feeds, request, FeedListSerializer)


class DiscoverFeedView(APIView):

    @staticmethod
    def get(request):
        feeds = Feed.objects.order_by('?')[:const.PAGE_SIZE]
        serializer = FeedListSerializer(feeds, many=True)
        return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=serializer.data)


class RecommendFeedView(APIView):

    @staticmethod
    def get(request):
        recommends = Recommend.objects.all()
        serializer = RecommendSerializer(recommends, many=True)
        return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=serializer.data)


class TrendingFeedView(APIView):

    @staticmethod
    def get(request):
        categories = Category.objects.all()
        return paginator.api_paging(categories, request, CategorySerializer)


class TrendingMoreFeedView(APIView):

    @staticmethod
    def get(request):
        category = request.GET.get(const.CATEGORY)

        feeds = Feed.objects.all().filter(type=const.FEED_TYPE_TRENDING).filter(category__name=category)
        return paginator.api_paging(feeds, request, FeedListSerializer)


class FeedLikeView(APIView):

    @login_required
    def post(self, request, pk):
        feed = pk

        token = request.META.get(const.META_TOKEN, const.UNKNOWN)
        payload = decode_token(token)
        account_id = payload.get(const.ACCOUNT_ID)
        account = account_id

        data = {const.FEED: feed, const.ACCOUNT: account}
        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            feed = Feed.objects.get(pk=feed)
            feed.like_count = feed.like_count + 1
            feed.save()
            return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS)
        else:
            return XResponse(status_code=const.CODE_10012, msg=const.MSG_FAIL)

    @login_required
    def delete(self, request, pk):
        try:
            feed = pk

            token = request.META.get(const.META_TOKEN, const.UNKNOWN)
            payload = decode_token(token)
            account_id = payload.get(const.ACCOUNT_ID)
            account = account_id

            like = Like.objects.get(feed=feed, account=account)
            like.delete()

            feed = Feed.objects.get(pk=feed)
            feed.like_count = feed.like_count - 1
            feed.save()
            return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS)
        except Like.DoesNotExist:
            return XResponse(status_code=const.CODE_10007, msg=const.MSG_FAIL)


class FeedBuyView(APIView):

    @login_required
    def post(self, request, pk):
        feed_id = pk

        token = request.META.get(const.META_TOKEN, const.UNKNOWN)
        payload = decode_token(token)
        account_id = payload.get(const.ACCOUNT_ID)

        bill = Bill.objects.get(account=account_id)
        feed = Feed.objects.get(pk=pk)
        if bill.balance >= feed.diamond:
            data = {const.FEED: feed_id, const.ACCOUNT: account_id}
            serializer = BuyLogSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

                bill.balance = bill.balance - feed.diamond
                bill.save()
                return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=None)
            else:
                return XResponse(status_code=const.CODE_10013, msg=const.MSG_FAIL)
        else:
            return XResponse(status_code=const.CODE_10014, msg=const.MSG_FAIL)


class FeedSearchView(APIView):

    @staticmethod
    def get(request):
        keyword = request.GET.get(const.SEARCH_KEYWORD)

        if keyword is not None:
            feeds = Feed.objects.filter(Q(title__contains=keyword) | Q(segment__name__contains=keyword))
        else:
            feeds = Feed.objects.all()

        return paginator.api_paging(feeds, request, FeedListSerializer)


class CommentView(APIView):

    @staticmethod
    def get(request, pk):
        comments = Comment.objects.filter(feed=pk)
        return paginator.api_paging(comments, request, CommentListSerializer)

    @login_required
    def post(self, request, pk):
        feed = pk
        token = request.META.get(const.META_TOKEN, const.UNKNOWN)
        payload = decode_token(token)
        account = payload.get(const.ACCOUNT_ID)
        content = request.data[const.COMMENT_CONTENT]
        data = {const.FEED: feed, const.ACCOUNT: account, const.COMMENT_CONTENT: content}
        serializer = CommentDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            del (data['account'])
            del (data['feed'])
            return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=data)
        return XResponse(status_code=const.CODE_10007, msg=const.MSG_FAIL)


class SegmentView(APIView):

    @staticmethod
    def get(request):
        segments = Segment.objects.all()
        serializer = SegmentSerializer(segments, many=True)
        return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=serializer.data)
