from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from blogs.models import Blog


class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

    def validate(self, attrs):
        if Blog.objects.filter(owner__id=attrs.get('owner').id, title=attrs.get('title')).exists():
            raise ValidationError({'error': 'this blog already exists'})
        return attrs

