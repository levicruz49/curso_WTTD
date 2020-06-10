from django.urls import path
from eventex.subscriptions.views import new, DescriptionDetailView

app_name = 'subscriptions'

urlpatterns = [
    path('', new, name='new'),
    path('<str:hashid>/', DescriptionDetailView.as_view(), name='detail'),

]
