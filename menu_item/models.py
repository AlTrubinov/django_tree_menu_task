from django.db import models


class MenuTitle(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return f'{self.title}'


class MenuItem(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    menu_title = models.ForeignKey(MenuTitle, null=True, blank=True, on_delete=models.CASCADE)
    parent_menu_item = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    menu_url = models.CharField(max_length=50, null=True, blank=True, unique=True)

    class Meta:
        verbose_name = 'Раздел меню'
        verbose_name_plural = 'Разделы меню'

    def __str__(self):
        return f'{self.title}'
