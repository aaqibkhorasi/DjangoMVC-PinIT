# [PinIt](http://cmpt470.csil.sfu.ca:8003/PinIt)
PinIt is a virtual bulletin board for sharing text and image content.

This web application is used to create boards, of various topics, and then users will create posts which can be shared
with the rest of the users on the site.

Anonymous users can only view the boards and posts

Registered users can create posts and edit the posts they have created. They can up/down vote and leave comments on posts.

Admin users can create boards and posts and edit all boards and posts

#### Technologies


---
#### URL
http://cmpt470.csil.sfu.ca:8003/PinIt

- [Django](https://www.djangoproject.com/)
- [Django comments](https://github.com/django/django-contrib-comments)
- [Django tastypie](https://django-tastypie.readthedocs.org/en/latest/)
- [Django crispy forms](ttp://django-crispy-forms.readthedocs.org/en/latest/)
- [Pillow](https://python-pillow.github.io/)
- [Easy Maps](https://pypi.python.org/pypi/django-easy-maps/)
- [Bootstrap](http://getbootstrap.com/)

---
#### Credentials
|Username|Password|Type|
|--------|--------|----|
|Professor|GiveUsAnA|Regular user|
|SSJIV_Professor|Please|Admin user|
---
#### Feature rundown
SQLite
> Little to no initial configuration. Easily portable as a single database file.

Model-View-Controller
> Django uses the MVC architecture. Different views for managing different functionality: boards, posts, user, etc.

Responsive design
> Layout scales according to device size i.e. mobile vs. desktop.

Authentication
> 3 user levels: Anonymous, Regular, and Administrator.

Authorization
> Anonymous users are unable to post. Regular users are able to post and vote. Administrators are able to delete.

CSS
> Bootstrap for layout.


Markup Validation
> Django templates does a good job of throwing errors when tags do not line up properly. VIM editor also highlights unclosed tags. Developer tools works well as a debugging tool for why elements show up incorrectly.

Encryption
> Passwords are hashed and salted.

Security
> CSRF tokens on forms mitigating XSS attacks. Virtually immune to SQL injection attacks due to Django ORM. All user inputs are escaped.

HTTP Status codes
> Appropriate status codes are returned for REST API and bad pages i.e. 200, 404, 502, etc.

Redirects
> After the user submits forms we often redirect them to an appropriate page to view their content. This can be seen after creating a board and being redirected to the board listing.

Caching
> Since we expect a limited amount of traffic on the site we have used Django’s built in caching system to enable a site-wide cache

REST API
> Endpoints for GET on (readonly) Boards and User data. Endpoints for GET, POST, and PUT on Post data. API key is generated on user creation and displayed on user profile page.

> Sample request to view all posts (replace the username/api_key parameter): http://cmpt470.csil.sfu.ca:8003/PinIt/api/v1/post/?format=json&username=admin&api_key=60e76ad88c742b648ee213331daad1015af0f641

Object-Relational Mapper (ORM)
> Django provides an ORM that is used for handing all data in this project

RSS (Rich Site Summary)
> Feed generated for posts

Social network integration
> Facebook integration for sharing

Maps
> We have used easy_maps third party application which simply takes addresses and displays them on a google map.
