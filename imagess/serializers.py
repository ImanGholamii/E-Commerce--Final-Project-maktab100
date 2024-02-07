from rest_framework import serializers
from .models import ProductImages, ProductImageAlbum

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductImageAlbumSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImageAlbum
        fields = '__all__'