from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class UpdateUserObjectsOnlyAuthorization(DjangoAuthorization) :

	def update_list(self, object_list, bundle) :
		allowed = []

		# Since they may not all be saved, iterate over them.
		for obj in object_list :
			if obj.user == bundle.request.user:
				allowed.append(obj)

		return allowed

	def update_detail(self, object_list, bundle) :
		if super(UpdateUserObjectsOnlyAuthorization, self).update_detail(object_list, bundle) :
			return bundle.obj.user == bundle.request.user
		else :
			raise Unauthorized("You are not allowed to update that resource.")

