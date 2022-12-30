from django.urls import path

from menu_item.views import MainMenuView, MenuItemView

urlpatterns = [
    path('', MainMenuView.as_view(), name="main_menu"),
    path('<slug:menu_url>/', MenuItemView.as_view(), name="menu_item"),
]
