import os

class __Mysql(object):

    def __init__(self, params=None, *args, **kwargs):
        
        if params['mysql']  == 'initialize':
            os.system('python ~/.jump2/bin/mysql_init.py')
        elif params['mysql'] == 'start':
            os.system('mysqld_safe --defaults-file=~/mysql/my.cnf &')
        elif params['mysql'] == 'shutdown':
            os.system('mysqladmin -uroot -p shutdown')

class __Django(object):

    def __init__(self, params=None, *args, **kwargs):
        
        if params['django']  == 'initialize':
            self.set_mysql_default()
        else:
            self.django_manage(params['django'])

    def set_mysql_default(self):
        import json
        print('SET DJANGO DATABASE DEFAULT')
        print("Do you use a Mysql database and complete the installation based on Jump2?")
        if input('Enter (Y/N): ').lower() == 'y':
            sock = os.environ['HOME']+'/mysql/mysql.sock'
        else:
            print("Please manually modify the configuration file in '~/.jump2/env/django.json'")
            os.sys.exit()
        default = {'ENGINE': 'django.db.backends.mysql',
                   'HOSTNAME': os.environ['HOSTNAME'],
                   'OPTIONS': {'unix_socket':sock}
                   } 
        default['NAME'] = input('Database name: ')
        default['USER'] = input('Mysql username: ')
        default['PASSWORD'] = input('Mysql password: ')
        default['HOST'] = input('Cluater IP: ')
        default['PORT'] = input('Mysql port: ')
        with open(os.environ['HOME']+'/.jump2/env/django.json','w') as f:
            f.write(json.dumps(default,indent=3))

    def django_manage(self,argv):
        if argv == "makemigrations":
            root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            dir = root+'/db/materials/migrations'
            for file in os.listdir(dir):
                if file.startswith('00'):
                    os.remove(os.path.join(dir,file))

        argvs = ['manage.py',argv]
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jump2.db.db.settings")
        try:
            from django.core.management import execute_from_command_line
        except ImportError:
            # The above import may fail for some other reason. Ensure that the
            # issue is really that Django is missing to avoid masking other
            # exceptions on Python 2.
            try:
                import django
            except ImportError:
                raise ImportError(
                    "Couldn't import Django. Are you sure it's installed and "
                    "available on your PYTHONPATH environment variable? Did you "
                    "forget to activate a virtual environment?"
                )
            raise
        execute_from_command_line(argvs)

