from rest_framework.routers import SimpleRouter
from player_app import views


router = SimpleRouter()

router.register(r'authenuser', views.AuthenUserViewSet, 'AuthenUser')
router.register(r'anonyvisitor', views.AnonyVisitorViewSet, 'AnonyVisitor')
router.register(r'message', views.MessageViewSet, 'Message')
router.register(r'censorword', views.CensorWordViewSet, 'CensorWord')
router.register(r'streamstatistic', views.StreamStatisticViewSet, 'StreamStatistic')

urlpatterns = router.urls
