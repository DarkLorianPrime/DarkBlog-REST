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
        extra_kwargs = {'owner': {"required": False}}

    def create(self, validated_data):
        owner = self.context['request'].user_data
        if Blog.objects.filter(owner__id=owner.id, title=validated_data.get('title')).exists():
            raise ValidationError({'error': 'this blog already exists'})
        validated_data.update({"owner": owner})
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        methods = {'add_authors': instance.authors.add, 'remove_authors': instance.authors.remove, 'common': self.common_update}
        authors = validated_data.get('authors')
        method = validated_data.get('method')
        methods[method](*authors)
        return instance

    def common_update(self, *args):
        owner = self.context['request'].user_data
        title = self.validated_data.get('title')
        if Blog.objects.filter(owner__id=owner.id, title=title).exists():
            raise ValidationError({'error': 'this blog already exists'})
        new_dict = delete_extra(need_types=['title', 'description'], update_dict=self.validated_data)
        new_dict['updated_at'] = datetime.now()
        Blog.objects.filter(id=self.instance.id).update(**new_dict)