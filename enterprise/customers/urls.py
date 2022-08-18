from django.urls import path, include
from customers import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
    path('subscriptioninfo/',  views.SubscriptionList.as_view()),
    path('subscriptioninfo/<int:pk>/', views.SubscriptionDetail.as_view()),
    path('', include('rest_framework.urls')),

]

"""
A common pattern for Web APIs is to use filename extensions on URLs to 
provide an endpoint for a given media type. For example, ‘http://example.com/api/users.json’ 
to serve a JSON representation.
Adding format-suffix patterns provides a shortcut to adding these patterns to our URL.
"""
urlpatterns = format_suffix_patterns(urlpatterns)