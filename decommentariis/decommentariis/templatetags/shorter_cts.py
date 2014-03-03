from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='prettyctsurn', is_safe=True)
@stringfilter
def pretty_cts_urn(value):
	"""Makes a cts urn look nicer"""
	cts_urn = str(value)
	print(cts_urn)
	if not cts_urn.startswith("urn:cts:"):
		return cts_urn
	s = cts_urn.split(":")[3:]
	s = " ".join(s).split(".")
	return " ".join(s)
