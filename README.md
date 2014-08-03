### aircooledrescue.com
This is the source for that site. I made the site a while ago in a weekend and recently someone asked for the code, don't judge. 

### setup
should be standard python stuff. I run it in a virtual environment, so put this dir in the virtuelnv and activate it. then you can do ```pip install -r requirements.txt```. this is setup to work with mysql, but you'll need to set the credentials in the settings.py file. then you can do ```python manage.py syncdb``` and then use south to setup the managed tables. any questions just open an issue or email me. 

