import factory
import random
from datetime import date
from pinit_api.models import User, Account, Pin


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    class Params:
        # And optional random_sequence that can be passed by the AccountFactory below,
        # to create consistency between the account's username and its owner's email address
        random_sequence = None

    email = factory.LazyAttribute(
        lambda o: f"user_{o.random_sequence if o.random_sequence else '%06d' % random.randint(0, 999999)}@example.com"
    )
    birthdate = date(1990, 1, 1)
    is_admin = False


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    class Params:
        random_sequence = factory.LazyAttribute(
            lambda _: "%06d" % random.randint(0, 999999)
        )

    username = factory.LazyAttribute(lambda o: f"user_{o.random_sequence}")
    type = "personal"
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    initial = factory.LazyAttribute(lambda account: account.first_name[0].upper())
    owner = factory.SubFactory(
        UserFactory, random_sequence=factory.SelfAttribute("..random_sequence")
    )


class PinFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pin

    title = factory.Faker("sentence", nb_words=5)
    image_url = factory.Faker("image_url")
    author = factory.SubFactory(AccountFactory)
