# Backend
## Setup
The aplication requieres some python libs to be installed first that usually aren't installed by default.
 - flask
 - flask_sqlalchemy
 - flask_cros

# Run the App
To execute the App in a non-production environment you simply need to run the main.py.
The Application will be serving on port 5000 on the local ip address. If for whatever reason the local ip sholdn't be working due to networksettings, remove the host='0.0.0.0' parameter at the bottom of the main.py file.

# Testing the API
In case you want to get the raw responses you need to comment the @login_required decorator for each function you want to test. You can use a browser to perform GET request or a tool like Postman to perform PUT/POST or DELETE requests.

# Default Database
The defaults.py provides a dataset for testing pourposes. The accounts and passwords can be found at the bottom of the file.<br>
Teacher-Accounts:
 - [username:password]
 - jurgen@plg:password
 - rainer@plg:schule
 - simon@plg:simon
 - peter@plg:schule

Student-Accounts:
 - [username:password]
 - hugh@plg:login
 - big@plg:test
 - bob@plg:seees
 - heinrich@plg:saaas

# Troubleshooting and Notes
in case something should screw up, just delete the database file and restart the app. The db gets recreated.
<br>
When accessing a Users Courses you may have to reload the page if where logged in as another user befor due to some caching bugs. Otherwise there might be the old users Courses displayed.
<br>
The Permission-Management is technicaly working BUT SQLite is overcomplicating things. Read the Note in auth.py to the courseAllowed() method