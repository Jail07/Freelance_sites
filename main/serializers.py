from rest_framework import serializers
from main.models import Project, Tag, Review, Bids
from account.serializers import ProfileSerializer


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()  # Показывает имя владельца

    class Meta:
        model = Review
        fields = '__all__'


class BidSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()  # Показывает имя отправителя

    class Meta:
        model = Bids
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    team_members = serializers.StringRelatedField(many=True)
    # bids = BidSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


