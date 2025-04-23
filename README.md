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

In another terminal:
cd Group-1-Project/Group-1-Project/discussionboard
php -S localhost:8000 (ensure php is installed for your specific OS)
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

