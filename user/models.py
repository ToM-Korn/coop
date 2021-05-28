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
    # print(dir(User))
    # ['DoesNotExist', 'EMAIL_FIELD', 'Meta', 'MultipleObjectsReturned', 'REQUIRED_FIELDS', 'USERNAME_FIELD', '__class__',
    #  '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
    #  '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__',
    #  '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__',
    #  '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_default_pk',
    #  '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes',
    #  '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers',
    #  '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering',
    #  '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable',
    #  '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references',
    #  '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks',
    #  '_legacy_get_session_auth_hash', '_meta', '_password', '_perform_date_checks', '_perform_unique_checks',
    #  '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', 'check', 'check_password',
    #  'clean', 'clean_fields', 'date_error_message', 'date_joined', 'delete', 'email', 'email_user', 'first_name',
    #  'from_db', 'full_clean', 'get_all_permissions', 'get_deferred_fields', 'get_email_field_name', 'get_full_name',
    #  'get_group_permissions', 'get_next_by_date_joined', 'get_previous_by_date_joined', 'get_session_auth_hash',
    #  'get_short_name', 'get_user_permissions', 'get_username', 'groups', 'has_module_perms', 'has_perm', 'has_perms',
    #  'has_usable_password', 'id', 'is_active', 'is_anonymous', 'is_authenticated', 'is_staff', 'is_superuser',
    #  'last_login', 'last_name', 'logentry_set', 'natural_key', 'normalize_username', 'objects', 'password', 'pk',
    #  'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'set_password',
    #  'set_unusable_password', 'unique_error_message', 'user_permissions', 'username', 'username_validator',
    #  'validate_unique']

    print('looking up username: ' + instance.username)

    try:
        # if user with this name can be found in database on saveing it allready exists.
        # we do not need to set him inactive
        existing = User.objects.get(username = instance.username)
        print('existing')
    except:
        print('not existing ... setting inactive')
        instance.is_active = False
        #todo send mail to staff... new user

        send_mail(
            'Willkommen '+instance.first_name + ' ' + instance.last_name +' bei der Einkaufsgemeinschaft PhiFi',
            'Wir werden deine Account so bald als möglich manuel freischalten. Du bekommst eine E-Mail sobald es soweit ist.'
            'Bitte bestätige in der Zwischenzeit deine E-Mail Adresse.',
            'tom@krickl.eu',
            [instance.email],
            fail_silently=False
        )


@receiver(post_save, sender=User)
def send_new_user_mail(sender,instance,**kwargs):
    # conn = get_connection(settings.EMAIL_BACKEND)
    # send_mail(
    #     'NEUER BENUTZER ' + instance.first_name + ' ' + instance.last_name,
    #     'neuer Benutzen: ' + instance.username + ' <a href="http://127.0.0.1:8000/admin/auth/user/' + str(
    #         instance.id) + '/change/">give access</a>',
    #     settings.EMAIL_FROM,
    #     ['tom@krickl.eu'],
    #     False,
    #     settings.EMAIL_HOST_USER,
    #     settings.EMAIL_HOST_PASSWORD,
    #     conn
    # )
    send_mail(
        'NEUER BENUTZER ' + instance.first_name + ' ' + instance.last_name,
        'neuer Benutzen: '+ instance.username + ' <a href="http://127.0.0.1:8000/admin/auth/user/' + str(instance.id) + '/change/">give access</a>',
        settings.EMAIL_FROM,
        ['tom@krickl.eu'],
        False,
    )
