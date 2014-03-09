from allauth.account.signals import email_confirmed, email_changed, email_added, email_removed, user_signed_up, user_logged_in
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from django.dispatch import receiver
#
# intercept signals from allauth
#

@receiver(email_confirmed)
def email_confirmed_(sender, email_address, **kwargs):
	print(email_address.email + " confirmed email.")
	query = {'email': email_address.email}
	if email_address.primary:
		user = User.objects.get(**query)
		print(str(user) + " confirmed primary email.")
		group = Group.objects.get(name='AllowedCommentary')
		user.groups.add(group)


@receiver(user_signed_up)
def user_signed_up_(sender, request, user, **kwargs):
	print(str(user) + " signed up")


@receiver(user_logged_in)
def user_logged_in_(sender, request, user, **kwargs):
	print("'{0}' logged in".format(user.username))
	groups = user.groups.all()
	for g in groups:
		print("group name=" + g.name)
		for p in g.permissions.all():
			print(str(p) + " codename=" + p.codename)

@receiver(email_changed)
def email_changed_(sender, request, user, from_email_address, to_email_address, **kwargs):
	print("'{0}' changed the email address from {1} to {2}".format(user.username, from_email_address, to_email_address))

@receiver(email_removed)
def email_changed_(sender, request, user, email_address, **kwargs):
	print("'{0}' removed the email address {1}".format(user.username, email_address))

