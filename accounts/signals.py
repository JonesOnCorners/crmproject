from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Customer



@receiver(post_save, sender=User)
def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="customers")
        instance.groups.add(group)
        Customer.objects.create(user=instance, name=instance.username)
        print("Customer Created!!!")