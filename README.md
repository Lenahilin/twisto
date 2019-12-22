# URL shortener

Simple URL shortener where admin can set that for instance, foo.bar/example redirects to www.example.com (where foo.bar is the domain the shortener is deployed to).

By default users get redirected straight to a login page where admin users can log in to gain access to a database view. 
There is a single table containing a path users should be redirected from, and the destination URL for each of these paths.

Both the app and the database are containerized; containers are attached to the default bridge network to be able to communicate with each other.
