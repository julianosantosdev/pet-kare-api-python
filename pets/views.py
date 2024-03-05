from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from pets.models import Pet
from groups.models import Group
from traits.models import Trait
from .serializers import PetSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


class PetViews(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:

        trait_name = request.query_params.get("trait", None)
        if trait_name:
            trait_content = Pet.objects.filter(traits__name=trait_name)
            result_page = self.paginate_queryset(trait_content, request)
            serializer = PetSerializer(instance=result_page, many=True)
            return self.get_paginated_response(data=serializer.data)

        pets = Pet.objects.get_queryset().order_by('id')
        result_page = self.paginate_queryset(pets, request)
        serializer = PetSerializer(instance=result_page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        traits = serializer.validated_data.pop("traits")
        traits_list = []

        for traits_dict in traits:
            trait_name = traits_dict["name"]
            trait_name_treated = ""
            numbers = "0123456789"

            for letter in trait_name:
                if letter not in numbers:
                    trait_name_treated += letter

            traits_dict["name"] = trait_name_treated.lower().strip()

            traits_content = Trait.objects.filter(
                name__iexact=traits_dict["name"].lower().strip()
            ).first()

            if not traits_content:
                new_trait = Trait.objects.create(**traits_dict)
                traits_list.append(new_trait)

            traits_list.append(traits_content)

        group = serializer.validated_data.pop("group")
        group_content = Group.objects.filter(
            scientific_name__iexact=group["scientific_name"].lower().strip()
            ).first()

        if not group_content:
            Group.objects.create(**group)

        pet = serializer.validated_data
        pet_group = Group.objects.get(scientific_name=group["scientific_name"])
        new_pet = Pet.objects.create(**pet, group=pet_group)
        new_pet.traits.set(traits_list)

        serializer = PetSerializer(instance=new_pet)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PetByIdView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(instance=pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, pet_id: int):
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        pet_new_group = serializer.validated_data.pop("group", None)
        if pet_new_group:
            group_existent = Group.objects.filter(
                scientific_name__iexact=pet_new_group["scientific_name"]
                .lower().strip()
            ).first()

            if group_existent:
                pet.group = group_existent
                pet.save()
            else:
                new_group = Group.objects.create(**pet_new_group)
                pet.group = new_group
                pet.save()

        pet_new_trait = serializer.validated_data.pop("traits", None)
        if pet_new_trait:
            traits_list = []

            for trait in pet_new_trait:
                trait_name = trait["name"]
                trait_name_treated = ""
                numbers = "0123456789"

                for letter in trait_name:
                    if letter not in numbers:
                        trait_name_treated += letter

                trait["name"] = trait_name_treated.lower().strip()

                traits_content = Trait.objects.filter(
                    name__iexact=trait["name"].lower().strip()
                ).first()

                if traits_content:
                    traits_list.append(traits_content)
                else:
                    new_trait = Trait.objects.create(**trait)
                    traits_list.append(new_trait)

            pet.traits.set(traits_list)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(instance=pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)

        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
