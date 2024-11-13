from rest_framework import serializers

from main.models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ('image', )


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'author', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = ImageSerializer(instance.images.all(),
                                                   many=True).data
        # representation['stars'] = StarSerializer(instance.star.all()).data

        action = self.context.get('action')
        if action == 'list':
            representation['replies'] = instance.replies.count()
        elif action == 'retrieve':
            representation['replies'] = ReplySerializer(instance.replies.all(),
                                                        many=True).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        print(request.user)
        post = Post.objects.create(author=request.user, **validated_data)
        for image in images_data.getlist('images'):
            CodeImage.objects.create(image=image, post=post)
        return post

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, val in validated_data.items():
            setattr(instance, key, val)

        images_data = request.FILES
        instance.images.all().delete()
        for image in images_data.getlist('images'):
            CodeImage.objects.create(
                image=image,
                problem=instance
            )
        return instance


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Reply
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ReplySerializer, self).to_representation(instance)

        action = self.context.get('action')

    def create(self, validated_data):
        request = self.context.get('request')
        reply = Reply.objects.create(
            author=request.user,
            **validated_data
        )
        return reply


class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ['star', ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        star = Post.objects.get('star')
        action = self.context.get('action')

        if star == False:
            representation['star'] = True
        elif star == True:
            representation['star'] = False

        return representation






