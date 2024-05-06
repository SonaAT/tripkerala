from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns=[
    path("signin",views.signin,name="signin"),
    path("signup",views.signup,name="signup"),
    path("signout",views.signout,name="signout"),
    path("routing",views.routing,name="routing"),
    path("places",views.places,name="places"),
    path("welcome",views.welcome,name="welcome"),
    path('journal',views.print_hello,name="print_hello"),
    path('savejournal',views.saveJournal,name="savejournal"),
    path('bucket', views.main_page, name='bucket'),  # URL for the main page
    path('add_trip', views.add_trip, name='add_trip'),  # URL for adding a trip
    path('delete_trip/<int:trip_id>', views.delete_trip, name='delete_trip')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)