from django.contrib import admin
from django import forms

from .models import SuperUser, Status, Order, Feedback
class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderAdminForm, self).__init__(*args, **kwargs)
        self.fields['id_courier'].queryset = SuperUser.objects.filter(type_user='courier')
        self.fields['id_client'].queryset = SuperUser.objects.filter(type_user='client')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = ('order_number', 'id_status', 'id_client', 'id_courier', 'address')
    list_filter = ('id_status',)
    search_fields = ('order_number', 'address', 'id_client__username', 'id_courier__username')


admin.site.register(SuperUser)
admin.site.register(Status)
admin.site.register(Feedback)
admin.site.site_header = "MD_StoneTrack"
admin.site.site_title = "MD_StoneTrack"
admin.site.index_title = "Администрирование"