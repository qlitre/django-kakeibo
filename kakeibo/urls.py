from django.urls import path
from . import views

app_name = 'kakeibo'

urlpatterns = [
    path('', views.PaymentList.as_view(), name='payment_list'),
    path('income_list/', views.IncomeList.as_view(), name='income_list'),
    path('payment_create/', views.PaymentCreate.as_view(), name='payment_create'),
    path('income_create/', views.IncomeCreate.as_view(), name='income_create'),
    path('payment_update/<int:pk>/', views.PaymentUpdate.as_view(), name='payment_update'),
    path('payment_delete/<int:pk>/', views.PaymentDelete.as_view(), name='payment_delete'),
    path('income_update/<int:pk>/', views.IncomeUpdate.as_view(), name='income_update'),
    path('income_delete/<int:pk>/', views.IncomeDelete.as_view(), name='income_delete'),
    path('month/<int:year>/<int:month>/', views.MonthDashboard.as_view(), name='month_dashboard'),
    path('transition/', views.TransitionView.as_view(), name='transition'),
]
