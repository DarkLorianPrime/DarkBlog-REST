from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from blogs.models import Blog


class BlogSerializer(ModelSerializer):
    method = serializers.CharField(max_length=250, required=False)

    class Meta:
        model = Blog
        fields = '__all__'
        extra_kwargs = {'owner': {"required": False}}

    def create(self, validated_data):
        owner = self.context['request'].user_data
        if Blog.objects.filter(owner__id=owner.id, title=validated_data.get('title')).exists():
            raise ValidationError({'error': 'this blog already exists'})
        validated_data.update({"owner": owner})
        validated_data.pop('authors')
        instance = Blog.objects.create(**validated_data)
        return instance
