from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from django.db import models
from django.utils.translation import gettext as _
from django.core.mail import send_mail, get_connection
from django.conf import settings

@receiver(pre_save, sender=User)
def check_if_existed_set_inactive(sender,instance,**kwargs):
    #print('looking up username: ' + instance.username)

    try:
        # if user with this name can be found in database on saveing it allready exists.
        # we do not need to set him inactive
        existing = User.objects.get(username = instance.username)
        print('existing')
    except:
        print('not existing ... setting inactive')
        instance.is_active = False

        send_mail(
            _('Willkommen '+instance.first_name + ' ' + instance.last_name +' bei der Einkaufsgemeinschaft PhiFi'),
            _('Wir werden deine Account so bald als möglich manuel freischalten. Du bekommst eine E-Mail sobald es soweit ist.'
            'Bitte bestätige in der Zwischenzeit deine E-Mail Adresse.'),
            settings.EMAIL_FROM,
            [instance.email],
            fail_silently=False
        )
        send_mail(
            'NEUER BENUTZER ' + instance.first_name + ' ' + instance.last_name,
            'neuer Benutzen: ' + instance.username + ' <a href="http://127.0.0.1:8000/admin/auth/user/' + str(
                instance.id) + '/change/">give access</a>',
            settings.EMAIL_FROM,
            [settings.EMAIL_ADMIN],
            False,
        )
