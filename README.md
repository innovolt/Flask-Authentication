It is the implementation of flask server authentication using bearer token

Steps to run the app
--------------------
1. Clone the git repo
2. docker build -t <imagename> .
3. docker run -p 5000:5000 <imagename>


APIs supported by the Flask Server
----------------------------------
1. User Sign Up
   POST /user/signup

   Body Parameters:
   - email_id
     - type: String
     - example: "abc@def.com"
   - name
     - type: String
   - password
     - type: String

   Response:
   - email_id
   - name
   - user_id
     - type: Uuid

2. User Login
   POST /user/login

   Request Header:
   - Basic Authentication in Authorization Header

   Response:
   - access_token

3. Fetch User Profile
   GET /user/profile

   Request Header:
   - Bearer Token in Authorization Header

   Response:
   - email_id
   - name
   - user_id

Behind the Scene
----------------
1. When User sign up then all the information is stored in the test.db:user table
2. When User logs in using basic authentication then backend validates the user, creates a session, and stores the session_id and email_id mapping in test.db:session table
3. When User tries to fetch its profile then user has to provide Bearer Token recieved from 2, backend validates the session corresponding to provided bearer token and returns back the User profile if all is good

SQLITE, a lightweight DB, is used for storing the User and session information

Sample cURL commands
--------------------

Sign Up
-------
curl -X POST -H 'Content-Type: application/json' -d '{"email_id": "<email_id>", "name": "<name>", "password": "<password>"}'  -k http://localhost:5000/user/signup


Login
-----
curl -X POST -k -u <email_id>:<password> http://localhost:5000/user/login


User Profile
------------
curl -k -H 'Authorization: Bearer <bearer_token>' http://localhost:5000/user/profile
