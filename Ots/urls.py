from django.urls import path
from Ots.views import *
app_name='Ots'
urlpatterns=[
    path('',welcome),
    path('new-candidate',candidateRegistrationForm,name='registrationForm'),
    path('store-candidate',candidateRegistration,name='storeCandidate'),
    path('login',loginView,name='login'),
    path('home',candidateHome,name='home'),
    path('test-paper',testPaper,name='testpaper'),
    path('calculate-result',calculateTestResult,name='calculateTest'),
    path('test-history',testResultHistory,name='testHistory'),
    path('result',showTestResult,name='results'),
    path('logout',logoutView,name='logout'),

]
