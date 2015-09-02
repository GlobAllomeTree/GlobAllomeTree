
from rest_framework import serializers

from django.db.models.signals import post_save, post_delete

class ValidRelatedField(object):
    def __init__(self, model, field_name):
        self.model = model
        self.field_name = field_name
        self.require_reload = True

        def require_reload(**kwargs):
          
            self.require_reload = True
            print "Requiring reload of %s" % self.model

        post_delete.connect(require_reload, sender=self.model, weak=False)
        post_save.connect(require_reload, sender=self.model, weak=False)
        
    def __call__(self, value):
        if self.require_reload:
            self.valid_options = self.model.objects.values_list(self.field_name, flat=True)
            self.require_reload = False

        if value not in self.valid_options: 
            message = 'The value "%s" is not a valid choice.' % value
            raise serializers.ValidationError(message)

    

