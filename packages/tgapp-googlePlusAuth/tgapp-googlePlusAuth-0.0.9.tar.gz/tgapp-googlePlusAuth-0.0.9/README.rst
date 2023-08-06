About googleplusauth
--------------------

googleplusauth is a Pluggable application for TurboGears2.

It aims at making easy to implement authentication and registration with
Google in any TurboGears2 application.

Installing
-----------

googleplusauth can be installed both from pypi or from bitbucket::

    pip install tgapp-googleplusauth

should just work for most of the users

Plugging googleplusauth
-----------------------

In your application *config/app_cfg.py* import **plug**::

    from tgext.pluggable import plug

Then at the *end of the file* call plug with googleplusauth::

    plug(base_config, 'googleplusauth')

on a sql database, to create the table, you can run the migration(s) with::

  gearbox migrate-pluggable -c development.ini googleplusauth upgrade

or if you can still drop the database, `setup-app` should be just fine.

Googleplushaut Helpers
----------------------

googleplusauth provides a helpers which will automatically
generate the buttons and the javascript required to let
your users log into your application using Google:

    * **h.googleplusauth.login_button(client_id, scope=None, data_cookiepolicy=None, img_btn_login=None, remember=None)**
        Places a login/registration button, automatically creates a new user if he never logged with google, otherwise simply logs him in.

        The ``client_id`` parameter is YOUR_CLIENT_ID.apps.googleusercontent.com

        The ``scope`` parameter is the permissions that the application will ask to google.
        By default those are only https://www.googleapis.com/auth/userinfo.email.
        For more scope: https://developers.google.com/oauthplayground/

        The ``data_cookiepolicy`` parameter indicate the domains for which to create sign-in cookies.

        The ``img_btn_login`` parameter indicate the button image url.

        The ``remember`` parameter can be used to log the user with an expiration date instead
        of using a session cookie, so that the session can last longer than the browser tab life.

This is the html of the button, if you want customize the button style: ::

    <div id="button-container">
        <div id="google-login-button" style="cursor: pointer;" onclick="perform_google_login()">
            <img id="img-login" src='%(img_btn_login)s' alt='Google Login' />
        </div>
    </div>

Available Hooks
---------------

googleplusauth makes available a some hooks which will be
called during some actions to alter the default
behavior of the appplications:

    * **googleplusauth.on_registration(google_response, user)** -> Runs when it is registering a new user from google
        login, permits to add or modify additional data to the user.
    * **googleplusauth.on_login(google_response, user)** -> Runs when user perform google login,
        permits to update the user data.


Google Id and Profile Picture
------------------------------

Users will have a new related entity called ``googleplusauth``.
Accessing ``user.googleplusauth`` it is possible to access the user ``user.googleplusauth.google_id``
and ``user.googleplusauth.profile_picture`` and more.
