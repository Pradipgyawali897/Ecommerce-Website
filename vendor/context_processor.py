from category.models import Vendor_Pannel_Category

def vendor_category():
    obj=Vendor_Pannel_Category.objects.all()
    return (dict(list=obj))        