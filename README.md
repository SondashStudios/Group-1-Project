## GradPath Command Reference
## Overview
GradPath is a career preparation web application designed to help students build resumes, track learning, and engage in discussions.

This document includes every necessary command to setup, run, and test the Group 1 Project.

---

##  Setup
```bash
cd Group-1-Project/Group-1-Project-main/gradpath
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

In another terminal:
cd Group-1-Project/Group-1-Project-main/discussionboard
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
| Feature            | Path                                 |
|--------------------|--------------------------------------|
| View All Questions | `/discussionboard/index.html`        |
| View Thread        | `/discussionboard/discussion.html?id=<question_id>` |
| Post Reply         | Handled via frontend JS + PHP        |
| Upvote/Downvote    | LocalStorage-based (client-side)     |

---

##  Run Tests
```bash
cd Group-1-Project/Group-1-Project-main/gradpath
python manage.py test accounts
python manage.py test resumes
cd Group-1-Project-main/Group-1-Project-main/discussionboard_tests
npm install
npx jest (provides test results of discussionboard and checklist)

```
## views resumes

go to URL: 'http://127.0.0.1:8000/api/v1/resumes/' to veiw submitted resumes. 

---

##  WebSocket (Optional Chat)
```bash
daphne gradpath.asgi:application
```
URL: `ws://127.0.0.1:8000/ws/discussion/`

---

