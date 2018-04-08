from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .serializers import FoodCategorySerializer
from .models import FoodCategory


class Restaurant(APIView):
    pass


class FoodCategoryView(ListAPIView):
    model = FoodCategory
    serializer_class = FoodCategorySerializer

    def get_queryset(self):
        order_option = self.request.query_params.get('order', '')
        category_query = {
            '': FoodCategory.objects.all(),
            'cnt': FoodCategory.objects.annotate(restaurant_count=Count('restaurant')).order_by('-restaurant_count')
        }
        return category_query.get(order_option, FoodCategory.objects.all())

    def list(self, request, *args, **kwargs):
        # call the original 'list' to get the original response
        response = super(FoodCategoryView, self).list(request, *args, **kwargs)

        # customize the response data
        response.data = {"categories": response.data}

        # return response with this custom representation
        return response
