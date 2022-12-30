from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import MenuItem, MenuTitle


class MainMenuView(ListView):
    template_name = 'menu_items/main.html'
    model = MenuTitle
    context_object_name = 'menus'


class MenuItemView(DetailView):
    template_name = 'menu_items/sel_menu.html'
    model = MenuItem
    context_object_name = 'menu'

    def get_object(self):
        object = get_object_or_404(MenuItem, menu_url=self.kwargs['menu_url'])
        return object

