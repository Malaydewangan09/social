# Create Django Rest API in Docker

### 1. Create a directory <app> in the main project directory
##### tree -->
    django-project
        - app
        -.gitignore
        - docker-compose.yml
        - Dockerfile
        
        
### 2. Basic Setup
- Create your project on ßGithub
- Create a folder for the repo on local
- Clone the project
#
    git clone <project path>
- Open it in PyCharm
- Create a .gitignore file and exclude what you need to from git
#
    .idea
    __pycache__
    *.pyc
    .DS_Store


### 3. Create a directory scripts and a script
    ./scripts/run.sh


### 4.1 Create the requirements.yml file to update the environment of the container
    name: base
    dependencies:
    name: base
    dependencies:
      - python=3.6
      - psycopg2=2.7.4
      - pip:
          - django==2.2.2
          - flake8
  #####  Django Rest Framework packages 
          - djangorestframework
          - markdown       # Markdown support for the browsable API.
          - django-filter  # Filtering support
          - django-rest-auth
          - requests
          - django-allauth
          - pillow


### 4.2 Create Dockerfile
- Go to docker hub and find the miniconda3 image
- Create a Dockerfile
#
    FROM continuumio/miniconda3:4.5.12
    
    ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
    
    RUN apt-get update && apt-get install -y wget bzip2
    
    COPY ./app/requirements.yml /app/requirements.yml
    RUN conda env update -f /app/requirements.yml
    
    COPY ./app /app
    
    COPY ./scripts/* /scripts/
    RUN chmod +x /scripts/*
    
    WORKDIR /app


### 5. Create a docker-compose.yml
    version: '3'
    services:
      app:
        image: django-api:latest
        ports:
          - 8000:8000
        volumes:
          - ./app:/app
        depends_on:
          - postgres
    
      postgres:
        image: postgres:latest
        ports:
          - 5432:5432
        volumes:
          - django-project:/var/lib/postgresql/data
    
    volumes:
      django-project:


### 6. Build the image
    docker build -t <image name>:latest .

##### to remove an image
    docker rmi <image name>
##### or to force remove
    docker rmi -f <image name>


### 7. Run the image to spin-up a new container
    docker-compose run --service-ports app bash


### 8. If dependencies not in Dockerfile, Install django on container
    pip install django


### 9. Start django project
- Inside the app folder start the project
#####
    django-admin startproject project .
- Go to settings.py and change the database
#####
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'PORT': 5432,
            'HOST': 'postgres',
            'PASSWORD': 'postgres',
            'USER': 'postgres'
        }
    }

##### Initialise a new database
    python manage.py migrate
    python manage.py makemigrations
    python manage.py migrate

##### Create superuser to access admin
    python manage.py createsuperuser

##### Run the server
    python manage.py runserver 0.0.0.0:8000

##### Server
    http://localhost:8000
 
##### Admin's page
    http://localhost:8000/admin


### 10. Connect to Postgres from Pycharm
##### View - Tools window - Databases - Postgres
    localhost: postgres
    user: postgres
    password: postgres
    port: 5432


### 11. Create an app
    python manage.py startapp <app name>


### 12. Add the app to the settings.py
    INSTALLED_APPS = [
        .....
        '<app name>',
    ]


### 13. Create a model
##### example:
    class Post(models.Model):
        title = models.CharField(max_length=200)
        author = models.ForeignKey(
            'auth.User',
            on_delete=models.CASCADE,
        )
        body = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
    
        def __str__(self):
            return self.title


### 14. Save the changes to the database
    python manage.py makemigrations
    python manage.py migrate

##### List migrations
    python manage.py <app name> showmigrations


### 15. Check that the table has been created
    table name = <app name>_<model class name in lowercase>

### 16. If you want to give access to the admin,
##### Go to app directory / admin.py
    admin.site.register(<model class name>)


### 17. Create the views inside the app / views.py


### 18. Create a urls.py inside the app directory to include the app's views
    <app name> / urls.py
    urlpatterns = [
        path('', view_all), # name='get-all-posts'
    ]


### 19. Include in django's urls.py the path of the app's urls
    <django project > / urls.py
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('blog/', include('blog.urls')),
    ]
    
    

## Create Django REST API ##

### 1. Install packages if not already in the requirements.yml
##### Django Rest Framework (DRF)
    pip install djangorestframework

##### Markdown support for the browsable API
    pip install markdown  

##### Filtering support     
    pip install django-filter  


### 2. Add 'rest_framework' to your INSTALLED_APPS settings.py
    INSTALLED_APPS = (
        ...
        'rest_framework',
    )


### 3. If you're intending to use the browsable API you'll probably also want to add REST framework's login and logout views.
##### Add the following to your root urls.py file
    urlpatterns = [
        ...
        path('api-auth/', include('rest_framework.urls')),
    ]


### 4. Any global settings for a REST framework API are kept in a single configuration dictionary named REST_FRAMEWORK.
##### Add the following to the settings.py module
    REST_FRAMEWORK = {
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        ]
    }


### 5. Create a serializers.py in <app name> directory
##### blog/serializers.py -->
    from rest_framework import serializers
    from .models import <Model class>
    class <model class>Serializer(serializers.ModelSerializer):
        class Meta:
            model = <model class>
            fields = ['author', 'title', 'body', 'created_at']
    

### 6. Create the Api View in
    <app name>/views.py


### 7. Map the Api View in
    urls.py <app name>/urls.py


### 8. Check that the app's urls are mapped in projects urls
    app/project/urls.py

### Useful Docker commands
    docker-compose run --rm app sh -c "django-admin.py startproject app ."
    docker-compose run --service-ports --rm app sh -c "python manage.py runserver 0.0.0.0:8000"
    docker-compose run --rm app sh -c "python manage.py migrate"
    docker-compose run --service-ports app bash


### TIPS
##### How to change the data's timezone ??
use local time from python library

##### What is the difference between Views and Generics.Views ??
There are different classes, Generic has more packages

##### What is: from django.contrib.auth import get_user_model ?? 
You import Django's User Table (<auth_user> in postgres)
