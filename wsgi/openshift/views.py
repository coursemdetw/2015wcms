#@+leo-ver=5-thin
#@+node:2014spring.20140628104046.1770: * @file views.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:2014spring.20140628104046.1771: ** views declarations
from django.shortcuts import render_to_response

#@+node:2014spring.20140628104046.1772: ** home
def home(request):
     return render_to_response('home/home.html')
#@-others
#@-leo
