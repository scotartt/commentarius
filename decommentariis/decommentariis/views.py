import datetime
from django.http import HttpResponse
from decommentariis.models import TEIEntry, TEISection

def list_texts(request):
	now = datetime.datetime.now()
	html = "<html><body>"
	text_list = TEIEntry.objects.all()
	html += "<p>The available texts at {0} are:<p>".format(now)
	html += "\n<ul>\n"
	for text in text_list:
		html += "<li><a href='./{0}/'>{1}</a></li>\n".format(text.cts_urn, text)
	html += "</ul>\n"
	html += "</body></html>"
	return HttpResponse(html)

def get_text_sections(request, urn):
	now = datetime.datetime.now()
	text = TEIEntry.objects.get(cts_urn=urn)
	html = "<html><body>"
	html += "<pre>You requested text '{0}' at {1}.".format(urn, now)
	html += "\n\nThe text you requested is as follows:\n\nBibliographic data: '"
	html += "{0}'\n".format(text.bibliographic_entry)
	html += "\n\n\tAvailable section list:\n "
	for section in text.sections() :
		html += "\t{0} = {1}\n ".format(section.section_ref, section.cts_urn)
	html += "</pre>\n</body></html>"
	return HttpResponse(html)
