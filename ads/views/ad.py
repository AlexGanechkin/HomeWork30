import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Publication, User, Category


@method_decorator(csrf_exempt, name="dispatch")
class PublicationListView(ListView):
    model = Publication

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse([{
            "id": publication.id,
            "name": publication.name,
            "author": publication.author_id.username,
            "price": publication.price
        } for publication in self.object_list], safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class PublicationDetailView(DetailView):
    model = Publication

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id.id,
            "author": self.object.author_id.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id.id,
            #"image": self.object.logo.url
        }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class PublicationCreateView(CreateView):
    model = Publication
    fields = ['name', 'author_id', 'price', 'description', 'is_published', 'category_id']

    def post(self, request, *args, **kwargs):
        request_data = json.loads(request.body)

        new_publication = Publication.objects.create(
            name=request_data["name"],
            author_id=get_object_or_404(User, pk=request_data['author_id']),
            price=int(request_data["price"]),
            description=request_data["description"],
            is_published=request_data["is_published"],
            category_id=get_object_or_404(Category, pk=request_data['category_id'])
        )

        return JsonResponse({
            "id": new_publication.id,
            "name": new_publication.name,
            "author": new_publication.author_id.username,
            "price": new_publication.price,
            "description": new_publication.description,
            "is_published": new_publication.is_published
        }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class PublicationUpdateView(UpdateView):
    model = Publication
    fields = ['name', 'author_id', 'price', 'description', 'category_id']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        request_data = json.loads(request.body)
        self.object.name = request_data['name']
        self.object.author_id = get_object_or_404(User, pk=request_data['author_id'])
        self.object.price = int(request_data['price'])
        self.object.description = request_data['description']
        self.object.category_id = get_object_or_404(Category, pk=request_data['category_id'])
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id.id,
            "author": self.object.author_id.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id.id
            #"image": self.object.
        }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class PublicationDeleteView(DeleteView):
    model = Publication
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"})