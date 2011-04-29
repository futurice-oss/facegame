from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from fumapi import read, read_list
from django import forms
import random

class NameForm(forms.Form):
	name = forms.ChoiceField(widget = forms.RadioSelect)

def index(request):	
	#names = request.session.setdefault('names', [user['uid'] for user in read_list('user')])
	names = request.session.setdefault('names', filternames())

	if 'used_names' not in request.session:
		used_names = []
		request.session['used_names'] = used_names
		used_names.append(correct_user)
	else:
		used_names = request.session.setdefault('used_names', [])

	if 'namesession' not in request.session:
		random_users, correct_user = random_user(used_names, names)
		request.session['namesession'] = random_users, correct_user
	else:
		random_users, correct_user = request.session['namesession']

	formchoices = [(user, read('user', user)['cn']) for user in random_users]
	if request.method == 'POST':
		#print "Sessions:"
		#print dict(request.session)
		#random_users, correct_user = request.session['namesession']
		form = NameForm(request.POST, initial={'name': random_users})
		print "here its kinda"
		#form.fields['name'].choices = [(user, read('user', user)['cn']) for user in random_users]
		form.fields['name'].choices = formchoices
		print "slow"
		if correct_user == request.POST['name']:
			if form.is_valid():
				form = NameForm()
				request.session.pop('namesession', None)
				#used_names = request.session.setdefault('used_names', [])
				print used_names
				random_users, correct_user = random_user(used_names, names)
				used_names.append(correct_user)
				print "takes a little"
				form.fields['name'].choices = [(user, read('user', user)['cn']) for user in random_users]
				print "while"
				request.session['namesession'] = random_users, correct_user
				request.session['used_names'] = used_names
				{'rnCorrect': correct_user}
				return render_to_response('form.html', {'form': form, 'rncorrect': correct_user}, context_instance=RequestContext(request))
		else:
			print "WRONG ANSWER"
			print "I don't even know how you got here"
			print "probably because you posted TWICE! check your codez"
	else:
		form = NameForm()
		#used_names = []
		#request.session['used_names'] = used_names

	#random_users, correct_user = random_user(used_names, names)
	#used_names.append(correct_user)
	print "this is kinda"
	form.fields['name'].choices = formchoices
	print "slow"
	#request.session['namesession'] = random_users, correct_user
	#request.session['used_names'] = used_names
	return render_to_response('template.html', {'form': form, 'rncorrect': correct_user}, context_instance=RequestContext(request, {}))

def filternames():
	names = [user['uid'] for user in read_list('user')]
	filterednames = []
	for name in names:
		if len(name) < 5:
			filterednames.append(name)
	return filterednames

def random_user(used_names, names):
	names_set = set(names)
	used_names_set = set(used_names)
	not_used = list(names_set - used_names_set)
	
	rncorrect = not_used[random.randrange(0, len(not_used))]
	random_names = [rncorrect]
	for ind in range(0, 4):
		rn = names[random.randrange(0, len(names))]
		while rn in random_names:
			rn = names[random.randrange(0, len(names))]
		random_names.append(rn)
	random.shuffle(random_names)
	return random_names, rncorrect