from django import views
from django.urls import include, path
from finance.views import DashboardView, RegisterView,TranactionCreateView, TransactionListView, GoalCreateView
    

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),  #
    path('transaction/add/', TranactionCreateView.as_view(), name='transaction_add'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('goal/add/', GoalCreateView.as_view(), name='goal_add'),
]