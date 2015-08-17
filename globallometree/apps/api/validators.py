

class ValidRelatedField(object):
    def __init__(self, model, field_name):
        self.model = model
        self.field_name = field_name

    def __call__(self, value):
        if 1:
            message = 'The value %d is not a valid choice.' % value
            raise serializers.ValidationError(message)