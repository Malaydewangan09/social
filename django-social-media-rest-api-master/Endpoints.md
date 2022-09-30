# RestAPI
RestAPI for a Social Media website using Django's Rest Framework, PostgreSQL and Docker

## The app has the following Endpoints

### 1. Registration
- POST: Register new user by asking for an email (send email validation code) 
```/api/registration/```
- POST: Validate a new registered user with validation code sent by email
```/api/registration/validation/ ```

### 2. Auth
- POST: Get a new JWT by passing username and password.
```/api/auth/token/  ```
- POST: Get a new JWT by passing an old still valid JWT. 
```/api/auth/token/refresh/ ```
- POST: Verify a token by passing the token in the body 
```/api/auth/token/verify/ ```
-  POST: Reset users password by sending a validation code in a email
```/api/auth/password-reset/ ```
- POST: Validate password reset token and set new password for the user.
```/api/auth/password-reset/validate/```

### 3. Feed
- GET: lists all the posts of all users in chronological order 
```/api/feed/```
- GET: lists all the posts of a specific user in chronological order 
```/api/feed/<int:user_id>/ ```
- GET: lists all the posts of followees users in chronological order 
```/api/feed/followees/ ```
- GET: lists all the posts of followers users in chronological order 
```/api/feed/followers/ ```
- GET: lists all the posts of the logged in user’s friends in chronological order 
```/api/feed/friends/ ```

### 4. Posts
- POST: user can make a new post by sending post data 
```/api/posts/new-post/ ```
- GET: get a specific post by ID and display all the information about that post 
```/api/posts/<int:post_id>/ ```
- PATCH: update a specific post (only allow owner of post or admin) 
```/api/posts/<int:post_id>/ ```
- PUT: update a specific post (only allow owner of post or admin) 
```/api/posts/<int:post_id>/ ```
- DELETE: delete a post by ID (only allow owner of post or admin) 
```/api/posts/<int:post_id>/```
- POST: like a post 
```/api/posts/like/<int:post_id>/```
- DELETE: remove like from a post 
```/api/posts/like/<int:post_id>/ ```
- GET: the list of the posts the user likes 
```/api/posts/likes/ ```

### 5. Users
- GET: Get all the users 
```/api/users/```
- GET: Get all the users  profiles
```/api/users/profiles/```
- GET: Get specific user profile 
```/api/users/<int:pk>/```
- POST: follow a user 
```/api/users/follow/<int:user_id>/``` 
- DELETE: unfollow a user 
```/api/users/follow/<int:user_id>/``` 
- GET: List of all the logged in user’s followers 
```/api/users/followers/``` 
- GET: List of all the people the user is following 
```/api/users/following/``` 
- POST: Send friend request to another user 
```/api/users/friendrequest/<int:user_id>/``` 
- GET: List all open friend requests from others 
```/api/users/friendrequests/``` 
- GET: List all the logged in user’s pending friend requests 
 ```/api/users/friendrequests/pending/``` 
- POST: Accept an open friend request 
```/api/users/friendrequests/accept/<int:request_id>/```
- POST: Reject an open friend request 
```/api/users/friendrequests/reject/<int:request_id>/``` 
- GET: List all accepted friends 
```/api/users/friends/``` 
- DELETE: Unfriend a user 
```/api/users/friends/unfriend/<int:user_id>/``` 

### 6. Me
- GET: Get logged in user’s profile (as well private information like email, etc.) 
 ```/api/me/``` 
 - POST: Update the logged in user’s profile public info) 
```/api/me/``` 

