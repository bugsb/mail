from django.urls import path,include
from . import views

urlpatterns = [
 path('', views.home,name="Login"),
 path('inbox/<str:email>', views.inbox,name="inbox"),
 path('outbox/<str:email>', views.outbox,name="outbox"),
 path('compose/<str:mail>', views.compose,name="compose"),
 path('send_draft/<int:mid>', views.send_draft,name="send"),
 path('view/<int:mid>/<str:coming_from>', views.view,name="view"),
 path('drafts/<str:mail>', views.drafts,name="drafs"),
 path('replay/<int:mid>', views.replay,name="relpy"),
 path('forward/<int:mid>', views.forward,name="drafs"),
 path('delete/<int:mid>/<str:val>', views.delete,name="drafs"),
 path('save/<str:mail>', views.save,name="Save"),
 path('autosuggest', views.autosuggest,name="autosuggest"),
 ]
