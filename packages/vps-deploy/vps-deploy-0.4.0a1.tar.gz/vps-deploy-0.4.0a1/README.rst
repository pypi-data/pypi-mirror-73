==========
VPS Deploy
==========

This Python package contains a number of Fabric 1.* and 2.* deployment functions
that we use across several Python/Django projects.

Fabric is a very handy tool for automating deployment processes. Unlike Salt or
Ansible, you're writing code from the beginning than diving into the Turing
Tarpit of templated YAML. Also unlike Salt, Ansible or shell scripts, Fabric
neatly coordinates local and remote SSH tasks. It might not necessarily be your
best choice for provisioning, but as a general tool for automatic custom
workflows, it is exceptional.


Installation (recommended Fabric 2.*)
-------------------------------------

If Fabric 2 is available as an operating system package::

  $ sudo apt install fabric invoke
  $ pip install --user vps-deploy

Otherwise::

  $ pip install --user fabric invoke vps-deploy


Installation (legacy Fabric 1.*)
--------------------------------

Fabric 1.* is recommended only for supporting existing projects. For new
projects, use Fabric 2.*.

Since Fabric 1.* is Python 2-only and you're probably using a Python 3 virtual
env, you'll need to install Fabric and VPS Deploy as a `--user` package::

  # System package for Fabric, user package for vps-deploy:
  $ sudo apt install fabric
  $ pip install --user vps-deploy

  # All in user packages:
  $ pip install --user fabric~=1.14 vps-deploy

Alternately, while Fabric 1.* remains available for some operating systems, you
could also install it that way.


Getting started
---------------

To get started, create a `fabfile.py` in your top-level project directory. For a
standard Python/Django project based on Nginx, uWSGI Emperor, Memcached and
PostgreSQL, it might look something like this:

.. code:: python
   from fabric import task
   from invoke.collection import Collection

   from vps_deploy import django_fabric2 as df2

   hosts = ['user@examplehost.com']

   @task(hosts=hosts)
   def deploy(c):
       df2.transfer_files_git(c)
       df2.init(c)
       df2.grep_for_pdb(c)
       df2.lint(c)
       df2.prepare_virtualenv(c)
       df2.prepare_django(c)
       df2.fix_permissions(c,
           # Sentry needs access to Git repo.
           read=[
               '.git', 'deploy', 'env', 'project'],
           read_write=['project', 'project/collected_static/CACHE'],
       )
       df2.reload_uwsgi(c)
       df2.flush_memcached(c)
       df2.update_nginx(c)

   ns = Collection(
       deploy,
       task(df2.download_postgres_db),
       task(df2.mirror_postgres_db),
       task(df2.mirror_media),
   )
   ns.configure({
       # Built-in Fabric config.
       'run': {
           'echo': True,
           # Needed so local commands work. Can also use FABRIC_RUN_REPLACE_ENV.
           'replace_env': False,
           # Needed for Guix. Can also use FABRIC_RUN_SHELL.
           # 'shell': '/run/current-system/profile/bin/bash',
       },

       # Our custom project config.
       'env': {
           'branch': 'master',
           'app_user': 'www-data',
           'db_name': 'exampledb',
           'user': 'exampledeployuser',
           'project_dir': '/srv/exampleproject',
           'media_dir': 'project/media',
           'virtualenv': '/srv/venvs/exampleproject-django-py38',
           'site_name': 'examplesite',
           'requirements': 'requirements/production.txt',
           'settings': 'project.settings.live',
           'uwsgi_conf': 'deploy/uwsgi.ini',
           'nginx_conf': 'deploy/nginx.conf',
           'python': '/usr/bin/python3.8',
       },
   })


Deploying
---------

To make a deployment:

`fab --prompt-for-sudo-password deploy`

This depends on a few things being already set up, such as SSH access to the
server and having the server-site software and accounts set up. Those tend to to
be better handled with configuration management tools like Salt or Ansible (and
potentially triggered by Fabric!).
