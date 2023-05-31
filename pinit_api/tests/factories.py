import factory
from datetime import date
from pinit_api.models import User, Account, Pin


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    birthdate = date(1990, 1, 1)
    is_admin = False


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    username = factory.Sequence(lambda n: f"user{n}")
    type = "personal"
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    initial = factory.LazyAttribute(lambda account: account.first_name[0].upper())
    owner = factory.SubFactory(UserFactory)


class PinFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pin

    title = factory.Faker("sentence", nb_words=5)
    image_url = factory.Faker("image_url")
    author = factory.SubFactory(AccountFactory)
