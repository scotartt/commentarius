from allauth.account.signals import email_confirmed, email_changed, email_added, email_removed, user_signed_up, user_logged_in
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from django.dispatch import receiver
#
# intercept signals from allauth
#

# user has confirmed the email manually
@receiver(email_confirmed)
def email_confirmed_(sender, email_address, **kwargs) :
	#print(email_address.email + " confirmed email.")
	query = {'email' : email_address.email}
	if email_address.primary :
		user = User.objects.get(**query)
		#print(str(user) + " confirmed primary email.")
		group = Group.objects.get(name='AllowedCommentary')
		user.groups.add(group)

# when a user signs up
@receiver(user_signed_up)
def user_signed_up_(sender, request, user, **kwargs) :
	# print("SIGN UP " + str(user) + " signed up and kwargs=" + str(kwargs))
	social_login = kwargs.get('sociallogin', None)
	if social_login :
		social_account = social_login.account
		if social_account :
			if 'verified_email' in social_account.extra_data :
				if social_account.extra_data['verified_email'] == True:
					group = Group.objects.get(name='AllowedCommentary')
					user.groups.add(group)


