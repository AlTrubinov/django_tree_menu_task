from django import template
from ..models import MenuItem

register = template.Library()


def serializer(menuItems):
    result = []
    for item in menuItems:
        result.append({
            'id': item.id,
            'title': item.title,
            'parent_item': item.parent_menu_item,
            'menu_url': item.menu_url,
            'first_level': False,
            'lower_level_children': [],
            'open': False,
            'active': False,
            'active_child': None,
        })
    return result


def recursive_open_parents(current_item, list_of_item):
    parent = current_item['parent_item']
    for item in list_of_item:
        if parent and item['id'] == parent.id:
            item['open'] = True
            item['active_child'] = current_item
            if item['parent_item']:
                return recursive_open_parents(item, list_of_item)


@register.inclusion_tag('menu_items/menu.html', takes_context=True)
def draw_menu(context, menu_title):
    try:

        # To render the menu, we use only 1 query to the database
        menuItems = MenuItem.objects.filter(menu_title__title=menu_title)

        serialized_menuItems = serializer(menuItems)

        # The rendered menu has a structure: first-level / children / active / children active
        #
        # For example 'tree':
        # ------------------------------------------------------------------------------------
        #
        # first-level_menu_1
        # first-level_menu_2                 <--- open
        #   - children_menu_1                  <--- open
        #       - children_menu_1.1              <--- open
        #           - active_menu                  <--- we are here (active)
        #               * children_active_menu_1
        #               * children_active_menu_1
        #               * children_active_menu_1
        # first-level_menu_3
        #
        # ------------------------------------------------------------------------------------

        tree = []
        for item in serialized_menuItems:
            if item['parent_item'] is None:
                item['first_level'] = True

            # Work with active item

            item['active'] = item['menu_url'] == context.request.path[1:-1]
            if item['active']:

                # Open children for active item
                for item2 in serialized_menuItems:
                    if item2['parent_item'] and item2['parent_item'].id == item['id']:
                        item['lower_level_children'].append(item2)
                        item2['open'] = True

                # Open parents for active item
                if item['parent_item']:
                    recursive_open_parents(item, serialized_menuItems)

        # Add item to render (in the 'tree' dict)
        for item in serialized_menuItems:
            if item['first_level']:
                tree.append(item)

                while item['active_child']:
                    tree.append(item['active_child'])
                    item = item['active_child']

                for i in item['lower_level_children']:
                    tree.append(i)
        return {'tree_menu': tree}

    except Exception as exc:
        print('draw_menu.py | ', exc)
