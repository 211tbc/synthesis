Requirements:
    Java JDK 1.6                                http://java.sun.com
    Grails 1.1.1 (or presumably more recent)    http://www.grails.org
    tomcat6                                     if you want to deploy under a web container (apt-get install tomcat6)

The grails distribution includes all libraries required to create and run the application.  Set GRAILS_HOME in
your login script and place {GRAILS_HOME}/bin in your PATH.

Before running the app, please edit grails-app/conf/DataSource.groovy to point to the appropriate URL for
the database to which you want to connect for "development" and "production" deployments.  

Running the app simple version/development mode:
    $ cd synthesis/webservices
    $ grails run-app

This will use grails to host the web application in "development" mode and start a web listener on port 8080.
Connect to port 8080 on localhost to see the grails welcome screen.  To access the application, visit

    http://localhost:8080/${application_name}

in this case, the application name is "synthesis" but can be changed in the 'application.properties' file if
so desired.  (There's no need to unless the name will conflict with another URL.)

For this application as of now, it shows a pre-built list of controllers which only contains the 'xml' controller
at the moment.  If you click this link, you will be shown the list of actions available for this controller.  If
you want to visit one of these actions directly, the URLs are of the form:

    http://localhost:8080/${application_name/${controller}/${action}

So for example to view the "person" action on the "xml" controller, you would visit:

    http://localhost:8080/synthesis/xml/person

Running the app, production deployment version:

    $ cd synthesis/webservices
    $ grails war

This will build a standard and complete war file that can be deployed into any container that supports deployment
of a war file.  (i.e. tomcat, jetty, jboss, etc...)  The war file will be in the root directory of the project
and will be named:

    ${application_name}-${application_version}.war

The name and version again can be found in application.properties and can be updated as appropriate with no
impact on the application functionality.  When the war container deploys and starts running the app, it will
be running in "production" mode, the main consideration being the URL defined under grails-app/conf/DataSource.groovy
for the production database versus the development database as referred to above.

*** <VERY IMPORTANT NOTE> ***

On Debian-based systems (including Ubuntu) you absolutely must disable the Java security manager in
the /etc/init.d/tomcat6 file:

    # Use the Java security manager? (yes/no)
    # TOMCAT6_SECURITY=yes
    TOMCAT6_SECURITY=no

Unless you want to spend a LOT of tedious and unnecessary time tweaking Java security profile cofigurations.

You should also make the following changes:

    if [ -z "$JAVA_OPTS" ]; then
            JAVA_OPTS="-Djava.awt.headless=true -Xms64M -Xmx256M -XX:MaxPermSize=128M"
    fi

to increase the amount of memory tomcat will use for the app.  -Xmx is the total amount of heap memory tomcat
will allocate for the application and can be increased even further if OutOfMemoryException are encountered.

Once you have made these changes, you may drop the war into /var/lib/tomcat6/webapps and it should deploy and
execute without any problems.

*** </VERY IMPORTANT NOTE> ***

Important parts of the directory structure

/
    /grails-app         Most of the actual grails application is held under this directory
        /conf           Config files such as homepage and datasource config
        /controllers    Home for all the controller objects
        /domain         Home for all the domain model objects
        /i18n           Internationalization files
        /services       Home for web service classes (SOAP.  REST are regular controllers)
        /taglib         Custom taglibs
        /utils          Utility classes for the grails application
        /views          View templates for controller actions
    /lib                Any other external libraries needed to run the app not included with base grails
    /scripts            Scripts I've created to test xml functionality/aka half-assed attempt at unit tests
    /src                External sources (there's no real distinction in my mind why this would be here
                        versus placing extra code under /services or /utils above.  There is probably some
                        convention in grails to distinguish of which I am still unaware.)
    /test               Unit and Integration tests (sadly empty at the moment)
    /web-app            Static files that are part of the web application

If you panic, there are several resources available:
    $ grails help
    http://www.grails.org/
    http://groovy.codehaus.org/
    me

There are a number of good groovy and grails books available as well.  "Groovy Recipes", "Programming Groovy"
and "Grails in Action" are highly recommended.

** ANOTHER IMPORTANT NOTE

One of the downsides of a grails application is that (unlike some ORM systems) the properties of the domain
objects need to be manually kept in sync with the database.  If the database schema changes, the domain objects
will need to be updated to reflect those changes.

