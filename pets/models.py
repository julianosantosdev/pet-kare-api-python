from django.db import models


class PetGenre(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    NOT_INFORMED = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20, choices=PetGenre.choices, default=PetGenre.NOT_INFORMED
    )
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.PROTECT,
        related_name="pets"
    )

    def __repr__(self) -> str:
        return f'<{self.name, self.age, self.weight, self.sex, self.group}>'
