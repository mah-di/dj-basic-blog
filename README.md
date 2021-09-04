# Django BlogSite
A basic blogsite built with the popular Python web framework, Django.


## Introduction
This is a basic blog with the most primary features, like creating new blog posts, updating/deleting/viewing them, commenting on blog posts, liking/unliking blog posts and comments. This is my first project built with Django. I built it mainly for practicing purposes and also for trying out new technologies/features I learn by implementing them.

I used Django for the backend as you've probably already guessed and the Django template engine and the default SQLite for database. I also created REST API for this project with django-rest-framework or DRF.


## Getting Started
There is a step by step breakdown of how to get this project running on your local machine:
- If you wish to download the source files simply click on the **Code** button and select "Download ZIP". After download is complete unzip it in your desired location.
- If you want to clone the repo, navigate to the directory where you want to have the repo, open Git Bash and run `git clone https://github.com/mah-di/dj-basic-blog.git`.
- Create a virtual environment and activate the environment.
- Now on your Bash terminal `cd` into the root directory of the project and run `pip install -r requirements.txt`. This will download and install all the necessary dependencies for the project.
- Run `python manage.py runserver` to start the development server. You can now access the site by entering `localhost:8000` or `127.0.0.1:8000` on your browser.


## Technologies Used
1. Django *(The whole project is built on)*
2. Django REST Framework *(Used to create REST API for the project)*
3. Token Authentication *(Used for authenticating users over API calls)*


## REST API | Endpoints, Methods and Actions

<dl>
<dt>127.0.0.1:8000/api/accounts/registration</dt>
  <dd>

    method allowed: POST
    authorization: No
    response: Creates a new user
  </dd>
</dl>

<dl>
<dt>127.0.0.1:8000/api/accounts/login</dt>
  <dd>

    method allowed: POST
    authorization: No
    response: Authenticates user and returns authorization token for that user
  </dd>
</dl>

<dl>
<dt> 127.0.0.1:8000/api/accounts/{username}/ </dt>
  <dd>

    method allowed: GET
    authorization: No
    response: Returns details of a user
  </dd>
</dl>

<dl>
<dt>127.0.0.1:8000/api/accounts/update</dt>
  <dd>

    method allowed: GET, PUT
    authorization: Yes
    response: Updates user information
  </dd>
</dl>

<dl>
<dt>127.0.0.1:8000/api/blog/</dt>
  <dd>

    method allowed: GET
    authorization: No
    response: Returns list of blog posts
  </dd>
</dl>

<dl>
<dt>127.0.0.1:8000/api/blog/create</dt>
  <dd>

    method allowed: POST
    authorization: Yes
    response: Creates a new post
  </dd>
</dl>

<dl>
<dt>127.0.0.1:8000/api/blog/{slug}/</dt>
  <dd>

    method allowed: GET
    authorization: No
    response: Returns a single post
  </dd>
</dl>

<dl>
<dt>127.0.0.1:8000/api/blog/{slug}/update</dt>
  <dd>

    method allowed: PUT
    authorization: Yes
    response: Updates a post
  </dd>
</dl>

<dl>
<dt>127.0.0.1:8000/api/blog/{slug}/delete</dt>
  <dd>

    method allowed: DELETE
    authorization: Yes
    response: Deletes a post
  </dd>
</dl>

<dl>
<dt>127.0.0.1:8000/api/blog/{slug}/like-unlike</dt>
  <dd>

    method allowed: POST, DELETE
    authorization: Yes
    response: Likes or unlikes a post
  </dd>
</dl>

<dl>
<dt>127.0.0.1:8000/api/blog/comment</dt>
  <dd>

    method allowed: POST
    authorization: Yes
    response: Creates a comment
  </dd>
</dl>

<dl>
<dt>127.0.0.1:8000/api/blog/comment/update</dt>
  <dd>

    method allowed: PUT
    authorization: Yes
    response: Updates a comment
  </dd>
</dl>

<dl>
<dt>127.0.0.1:8000/api/blog/comment/{pk}/delete</dt>
  <dd>

    method allowed: DELETE
    authorization: Yes
    response: Deletes a comment
  </dd>
</dl>

<dl>
<dt>127.0.0.1:8000/api/blog/comment/{pk}/like-unlike</dt>
  <dd>

    method allowed: POST, DELETE
    authorization: Yes
    response: Likes or unlikes a comment
  </dd>
</dl>
