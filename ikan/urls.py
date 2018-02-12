from django.conf.urls import url

from ikan.service.denomination.denomination_view import DenominationView
from ikan.service.feed.feed_views import FeedView, HomeFeedView, TrendingFeedView, DiscoverFeedView, \
    RecommendFeedView, FeedLikeView, FeedSearchView, TrendingMoreFeedView, CommentView, SegmentView, FeedBuyView
from ikan.service.feedback.feedback_view import FeedbackView
from ikan.service.account.account_view import AccountView
from ikan.service.assets.assets_view import AssetsView
from ikan.service.notification.notification_views import NotificationView
from ikan.service.solution.help_document_views import HelpDocumentView
from ikan.service.token.token_view import TokenView
from ikan.service.upload.upload_view import UploadImageView
from ikan.service.version.version_update_view import VersionUpdateView

app_name = 'ikan'

urlpatterns = [
    url('^account/(?P<pk>[0-9]+)/$', AccountView.as_view()),
    url('^account/$', AccountView.as_view()),

    url('^account/balance/$', AssetsView.as_view()),

    url('^denomination/$', DenominationView.as_view()),

    url('^upload/$', UploadImageView.as_view()),

    url('^feed/(?P<pk>[0-9]+)/$', FeedView.as_view()),
    url('^feed/search/$', FeedSearchView.as_view()),
    url('^feed/home/$', HomeFeedView.as_view()),
    url('^feed/trending/$', TrendingFeedView.as_view()),
    url('^feed/trending/more/$', TrendingMoreFeedView.as_view()),
    url('^feed/discover/$', DiscoverFeedView.as_view()),
    url('^feed/recommend/$', RecommendFeedView.as_view()),
    url('^feed/(?P<pk>[0-9]+)/like/$', FeedLikeView.as_view()),
    url('^feed/(?P<pk>[0-9]+)/comment/$', CommentView.as_view()),
    url('^feed/(?P<pk>[0-9]+)/buy/$', FeedBuyView.as_view()),

    url('^token/refresh/$', TokenView.as_view()),

    url('^notification/(?P<pk>[0-9]+)/$', NotificationView.as_view()),
    url('^notification/$', NotificationView.as_view()),

    url('^segment/$', SegmentView.as_view()),

    url('^version/$', VersionUpdateView.as_view()),

    url('^solution/', HelpDocumentView.as_view()),
    url('^feedback/', FeedbackView.as_view()),
]
