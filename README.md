# Django Blog Application

This is a Django-based blog application where users can create, update, delete, and share blog posts, as well as comment on and like comments on posts. It includes authentication, search functionality, tagging, and email sharing features.

## Features

- **Post CRUD**: Users can create, read, update, and delete posts.
- **Commenting**: Authenticated users can comment on posts.
- **Comment Liking**: Authenticated users can like and unlike comments.
- **Tagging**: Posts can be tagged, and users can view posts filtered by tags.
- **Search**: Full-text search on post titles and content using PostgreSQL search features.
- **User Authentication**: Users can sign up, log in, log out, and view their profile.
- **Post Sharing**: Users can share posts via email.
- **Pagination**: The post list view is paginated to show 5 posts per page.
- **Authorization**: Only post authors can update or delete their posts.
  
## Requirements

- Python 3.x
- Django 4.x

- PostgreSQL (for advanced search functionality)
- Django Extensions 

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sainrohit98/Blog-Post.git
   cd Blog-Post

2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install the dependencies:
   pip install -r requirements.txt

4. Apply migrations:
   python manage.py migrate

5. Run the development server:
   python manage.py runserver


## API Endpoints

/signup/ : User signup page.
/accounts/profile/ : User profile page.
/logout/ : Log out the user.
/ : Homepage listing posts.
/post/new/ : Create a new post.
/post/<int:pk>/ : View the details of a post.
/post/<int:pk>/edit/ : Update an existing post.
/post/<int:pk>/delete/ : Delete a post.
/post/<int:pk>/share/ : Share a post via email.
/post/<int:pk>/comment/ : Add a comment to a post.
/comment/<int:pk>/like/ : Like or unlike a comment.
/search/ : Search for posts.
