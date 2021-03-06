"""
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from cromwellapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pphswitchon', views.pphSwitchOn, name='pphSwitchOn'),
    path('pphswitchoff', views.pphSwitchOff, name='pphSwitchOff'),
    path('new', views.new, name='pphSwitchOff'),
    path('startcrawler', views.startCrawler, name='startCrawler'),
    path('stopcrawler', views.stopCrawler, name='stopCrawler'),
]