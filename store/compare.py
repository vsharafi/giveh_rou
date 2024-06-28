from django.contrib import messages
from django.utils.translation import gettext as _


class Compare:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        

        compare_list = self.session.get('compare_list')

        if not compare_list:
            compare_list = self.session['compare_list'] = []

        self.compare_list = compare_list

    
    def add(self, pk):
        # product_id = product.id
        if len(self.compare_list) < 3:
            if pk in self.compare_list:
                messages.warning(self.request, _("This product is already in the comparison list"))
            else:
                self.compare_list.append(pk)
                messages.success(self.request, _('Product successfully added to comparison list.'))
        else:
            messages.warning(self.request, _("Your comparison list is full. Please remove an item to add this one."))

        self.save()

    
    def remove(self, pk):
        # product_id = product.id
        if pk in self.compare_list:
            self.compare_list.remove(pk)
            messages.success(self.request, _('Product successfully removed from comparison list.'))
            self.save()


    def save(self):

        """
        Mark session as modified to save changes
        """
        self.session.modified = True