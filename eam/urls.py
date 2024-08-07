from django.urls import path
from .views import (EamUserView,
                    EamChangeView,
                    EamCommitView,
                    EamRefuseView,
                    GetUsersView,
                    LogoutView
                    )


urlpatterns = [
    path('eamuser', EamUserView.as_view()),
    path('eamchange', EamChangeView.as_view()),
    path('eamcommit', EamCommitView.as_view()),
    path('eamrefuse', EamRefuseView.as_view()),
    path('getuser', GetUsersView.as_view()),
    path('logout', LogoutView.as_view())
]
