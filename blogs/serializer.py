from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from blogs.models import Blog
from utils.extra_editor import delete_extra


class BlogSerializer(ModelSerializer):
    method = serializers.CharField(max_length=250, required=False)

    class Meta:
        model = Blog
        fields = '__all__'

    def create(self, validated_data):
        if Blog.objects.filter(owner__id=validated_data.get('owner').id, title=validated_data.get('title')).exists():
            raise ValidationError({'error': 'this blog already exists'})
        instance = Blog.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        if instance.owner != validated_data.get('owner'):
            raise ValidationError({'error': 'You are not owner!'})
        if validated_data.get('authors') is not None and validated_data.get('method') == 'add_authors':
            [instance.authors.add(author) for author in validated_data.get('authors') if
             author not in instance.authors.values() and author != instance.owner]
        if validated_data.get('authors') is not None and validated_data.get('method') == 'remove_authors':
            [instance.authors.remove(author) for author in validated_data.get('authors')]
        if validated_data.get('method') == 'common':
            title = validated_data.get('title')
            if Blog.objects.filter(owner__id=validated_data.get('owner').id, title=title).exists():
                raise ValidationError({'error': 'this blog already exists'})
            new_dict = delete_extra(need_types=['title', 'description'], update_dict=validated_data)
            new_dict['updated_at'] = datetime.now()
            Blog.objects.filter(id=instance.id).update(**new_dict)
        return instance
