from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Validation:
    
    def phoneValidate(self,value):
        numbers ='0123456789'
        if value[0]=='1' and (value[1]=='0'or value[1]=='1' or value[1]=='2' or value[1]=='5'):
            for i in value:
                if i not in numbers:
                    raise ValidationError(
                        _('%(value)s is not a phone number'),
                        params={'value': value},
                    )
        else:
            raise ValidationError(
                        _('%(value)s is not a phone number'),
                        params={'value': value},
                    )
            
    def doctorValidate(self,value):
        pass