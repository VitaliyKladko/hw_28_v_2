import json

from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ads, Users, Location
from hw_28_v_2 import settings


def index(request):
    return JsonResponse({'message': 'Index page'}, status=200)


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for cat in self.object_list:
            response.append(
                {
                    'id': cat.id,
                    'name': cat.name,
                }
            )
        return JsonResponse(response, safe=False, status=200)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except Http404:
            return JsonResponse({'error': 'Not Found'}, status=404)

        return JsonResponse({
            'id': category.id,
            'name': category.name,
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        test_data = json.loads(request.body)

        category = Category.objects.create(
            name=test_data['name']
        )

        return JsonResponse({
            'id': category.id,
            'name': category.name,

        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)

        self.object.name = cat_data['name']
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            'status': 'Ok'
        }, status=200)


class AdsListView(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        items = []
        for advertisement in page_obj:
            items.append(
                {
                    'id': advertisement.id,
                    'name': advertisement.name,
                    'author_id': advertisement.author_id.id,
                    'author': advertisement.author_id.first_name,
                    'price': advertisement.price,
                    'description': advertisement.description,
                    'is_published': advertisement.is_published,
                    'category_id': advertisement.category_id.id,
                    'image': advertisement.image.url if advertisement.image else None

                }
            )

        response = {
            'items': items,
            'total_pages': paginator.num_pages,
            'total_elements': paginator.count
        }

        return JsonResponse(response, safe=False, status=200)


class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        try:
            advertisement = self.get_object()
        except Http404:
            return JsonResponse({'error': 'Not Found'}, status=404)

        return JsonResponse({
                    'id': advertisement.id,
                    'name': advertisement.name,
                    'author_id': advertisement.author_id.id,
                    'author': advertisement.author_id.first_name,
                    'price': advertisement.price,
                    'description': advertisement.description,
                    'is_published': advertisement.is_published,
                    'category_id': advertisement.category_id.id,
                    'image': advertisement.image.url if advertisement.image else None
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = Ads
    fields = ['name', 'author_id', 'price', 'description', 'is_published', 'category_id']

    def post(self, request, *args, **kwargs):
        advertisement_data = json.loads(request.body)

        advertisement = Ads.objects.create(
            name=advertisement_data['name'],
            author_id=Users.objects.get(pk=advertisement_data['author_id']),
            price=advertisement_data['price'],
            description=advertisement_data['description'],
            is_published=advertisement_data['is_published'],
            category_id=Category.objects.get(pk=advertisement_data['author_id'])
        )

        return JsonResponse({
            'id': advertisement.id,
            'name': advertisement.name,
            'author_id': advertisement.author_id.id,
            'price': advertisement.price,
            'description': advertisement.description,
            'is_published': advertisement.is_published,
            'category_id': advertisement.category_id.id,
            'category_name': advertisement.category_id.name,

        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ['name', 'author_id', 'price', 'description', 'category_id']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        advertisement_data = json.loads(request.body)

        self.object.name = advertisement_data['name']
        self.object.author_id = Users.objects.get(pk=advertisement_data['author_id'])
        self.object.price = advertisement_data['price']
        self.object.description = advertisement_data['description']
        self.object.category_id = Category.objects.get(pk=advertisement_data['category_id'])

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author_id.id,
            'author': self.object.author_id.first_name,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'category_id': self.object.category_id.id,
            'image': self.object.image.url if self.object.image else None,
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsDeleteView(DeleteView):
    model = Ads
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            'status': 'Ok'
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsImageView(UpdateView):
    model = Ads
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author_id.id,
            'author': self.object.author_id.first_name,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'category_id': self.object.category_id.id,
            'image': self.object.image.url if self.object.image else None,
        }, status=200)


class UserListView(ListView):
    model = Users

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        items = []
        for user in page_obj:
            items.append({
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'age': user.age,
                'locations': list(user.location_id.all().values_list("name", flat=True))
            })

        response = {
            'items': items,
            'total_pages': paginator.num_pages,
            'total_elements': paginator.count
        }

        return JsonResponse(response, safe=False, status=200)


class UserDetailView(DetailView):
    model = Users

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except Http404:
            return JsonResponse({'error': 'Not Found'}, status=404)

        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'locations': list(user.location_id.all().values_list("name", flat=True))
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = Users
    fields = ['username', 'password', 'first_name', 'last_name', 'role', 'age', 'locations']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = Users.objects.create(
            username=user_data['username'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=user_data['role'],
            age=user_data['age']
        )

        # создание локации (нужно передать список из 3-х элементов: name, lat, lng)
        if len(user_data['locations']) == 3:
            loc_obj, created= Location.objects.get_or_create(
                name=user_data['locations'][0],
                lat=user_data['locations'][1],
                lng=user_data['locations'][2],
            )

            user.location_id.add(loc_obj)
            user.save()

        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'locations': list(user.location_id.all().values_list("name", flat=True))
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = Users
    fields = ['username', 'password', 'first_name', 'last_name', 'age', 'location_id']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.username = user_data['username']
        self.object.password = user_data['password']
        self.object.first_name = user_data['first_name']
        self.object.last_name = user_data['last_name']
        self.object.age = user_data['age']

        for item in user_data['locations']:
            loc_obj, created = Location.objects.get_or_create(name=item)
            self.object.location_id.add(loc_obj)

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'username': self.object.username,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'age': self.object.age,
            'password': self.object.password,
            'locations': list(self.object.location_id.all().values_list('name', flat=True)),
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = Users
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            'status': 'Ok'
        }, status=200)
