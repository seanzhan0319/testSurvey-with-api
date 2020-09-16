# DEPRECATED REPO

We are no longer using Flask for frontend development. 

All frontend has been switched to React since late June.

---

This project is linked to heroku app testexpt-w-api.

### how to create a role and users ###

Use admin access to:
```
db.createCollection("sean-col")
db.createRole({ 
    role: "use-sean-col", 
    privileges: [{ 
        resource: { db: "heroku_5qkz777p", collection: "sean-col" }, actions: [ "find", "insert", "remove", "update" ]}], 
    roles: []
    })
db.createUser({
    user:"sean", 
    pwd:"password", 
    roles:[{
        role:"use-sean-col", 
        db:"heroku_5qkz777p"}]
    })
```
Then, login using "sean", "password". User "sean" will only have access to collection with name "sean-col".

Before creating a user in /signup/success, first create a restricted role through mongo shell that only has access to a dummy collection. Then, when the user actually creates a collection(s), admin_db will create a new role for the user to only have access to the collection(s) that they have created. Role name: "restricted"

Currently for the login authentication method: 

As soon as a researcher signs up, their information is stored into a collection in mongodb. Only admin and themselves know their password. !!! Need to change authentication method somehow ???

At /researcher/submit, I encountered error: (not authorized to execute command updateUser). I had to go back to the mongodb that's linked to heroku to update my contact information so that I as heroku_5qkz777p can grant __system access to 'user'. Update: that didn't work. I cant' grantRole or udpateUser. I don't think I have full access to the mlab database that's partnered with heroku. 

Go on to create a separate database on mlab. Got redirected to mongodb atlas. Created account and created cluster with name "demoCluster". 

```
pip install pymongo[srv]
```

FOR NOW, KEEP USING mLAB. Mongodb atlas has a lot more restrictions. Current workarounds: 1. user authentication 2. cannot updateUser (more privileg), thus we grantRolesToUser (less privilege).
