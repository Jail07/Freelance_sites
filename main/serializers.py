from rest_framework import serializers
from main.models import Project, Tag, Review
from account.serializers import ProfileSerializer


class ReviewSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)  # Добавим информацию о владельце отзыва

    class Meta:
        model = Review
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)  # Получаем владельца проекта
    tags = TagSerializer(many=True)  # Получаем теги проекта
    reviews = serializers.SerializerMethodField()  # Сериализуем отзывы через метод

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):
        # Получаем все отзывы, связанных с проектом, и сериализуем их
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
