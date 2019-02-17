from django import template

register = template.Library()

@register.filter
def addstr(str1):
	"""concantenate str1 & str2"""
	return '../media/ED/Experimental_design_' + str(str1) + '.xlsx'
