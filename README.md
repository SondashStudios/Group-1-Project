# GradPath Discussion Board Extension

This project adds a full-featured discussion board to the existing GradPath Django system, supporting:
-  Post creation
-  Commenting
-  Upvote/downvote on comments
-  Like posts
-  REST API (DRF)
-  Full test coverage
-  Optional WebSocket chat (via Channels)

---

##  Project Structure
```
discussionboard/
├── models.py          # Post, Comment, CommentVote models
├── views.py           # Views for post, comment, vote, DRF APIs
├── urls.py            # URL routing incl. API
├── templates/
│   └── post_detail.html  # Voting UI + comment form
├── serializers.py     # DRF serializers
├── tests.py           # Unit tests
├── consumers.py       # Optional: Live chat
├── routing.py         # WebSocket route for chat
```

---

##  Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add to `INSTALLED_APPS`:
```python
'discussionboard',
```

3. Add to `urls.py`:
```python
path('discussion/', include('discussionboard.urls')),
```

4. Migrate:
```bash
python manage.py makemigrations discussionboard
python manage.py migrate
```

---

##  Tests
```bash
python manage.py test discussionboard
```

---

##  API Endpoints (DRF)
| Endpoint | Description |
|----------|-------------|
| `/discussion/api/posts/` | CRUD for posts |
| `/discussion/api/comments/` | CRUD for comments |

---

##  Comment Voting Logic
- Votes are stored in `CommentVote`
- Score is tracked in `Comment`
- Users can upvote or downvote once per comment

---

##  UI Sample (post_detail.html)
```html
<form action="/discussion/comment/{{comment.id}}/vote/" method="post">
  <button name="value" value="1">⬆️</button>
  <strong>{{ comment.score }}</strong>
  <button name="value" value="-1">⬇️</button>
</form>
```

---

##  Security Notes
- All views are login-protected
- CSRF protected forms
- Votes restricted to one per user

---

##  Contact
Maintained by Team 1 | Spring 2025




## GradPath Command Reference

This document includes every necessary command to setup, run, and test the Group 1 Project.

---

##  Setup
```bash
cd Group-1-Project/Group-1-Project/gradpath
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

##  Start Server
```bash
python manage.py runserver
```
Visit: `http://127.0.0.1:8000/`

---

##  Accounts Module
| Feature | Path |
|---------|------|
| Signup | `/signup/` |
| Login | `/login/` |
| Dashboard | `/welcome/` |
| Account Settings | `/account-settings/` |

---

##  Checklist Module
| Feature | Path |
|---------|------|
| Learning Checklist | `/checklist/` |
| Save/Load Progress | via checkboxes |

---

##  Resume Builder
| Feature | Path |
|---------|------|
| Create Resume | `/resumes/create/` |
| Resume List | `/resumes/` |
| Edit Resume | `/resumes/edit/<id>/` |
| Generate PDF | `/resumes/generate_pdf/<id>/` |

---

##  Discussion Board
| Feature | Path |
|---------|------|
| View Posts | `/discussion/` |
| New Post | `/discussion/new/` |
| View Post | `/discussion/<post_id>/` |
| Like Post | `/discussion/<post_id>/like/` |
| Vote Comment | `/discussion/comment/<comment_id>/vote/` |

---

##  REST APIs
| API | Path |
|-----|------|
| Posts | `/discussion/api/posts/` |
| Comments | `/discussion/api/comments/` |

---

##  Run Tests
```bash
python manage.py test
```

---

##  WebSocket (Optional Chat)
```bash
daphne gradpath.asgi:application
```
URL: `ws://127.0.0.1:8000/ws/discussion/`

---

