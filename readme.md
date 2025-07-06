# 🧱 Byte of Legacy — Claim Your Pixel, Immortalize Your Story

**A Django-powered interactive legacy wall supporting TechStart TV through ₱69 community contributions.**

[Live Demo Coming Soon]

## 📌 Overview

**Byte of Legacy** is a community-driven fundraising microsite inspired by the Million Dollar Homepage — but modern, meaningful, and Filipino. For just ₱69, anyone can claim a slot on a digital mosaic wall and leave behind a message, an icon, and a link. It’s built to help fund and grow [TechStart TV](https://www.techstart.tv), a Cebu-based media platform for startups, tech, and innovation stories in the Philippines.

> 💡 Each slot claimed contributes to storytelling, operations, and building the first grassroots innovation media in the Visayas.

---

## ⚙️ Features

- 🎨 Claim and customize a legacy card (color, name, icon, and message)
- 📷 Upload proof of payment (manual verification)
- 💾 Secure file uploads to **Supabase Storage**
- 📧 Email confirmation for submissions
- 🔐 Confidential image storage for sensitive uploads
- 📡 PostgreSQL-powered deployment via Supabase
- 🌈 Real-time mosaic view of all claimed slots
- 🧱 Built with Django, Bootstrap 5, and Supabase REST API

---

## 🛠️ Tech Stack

- **Backend**: Django 4+
- **Frontend**: Bootstrap 5, HTML5, JavaScript
- **Database**: PostgreSQL (via Supabase)
- **File Storage**: Supabase Buckets (Public + Confidential)
- **Deployment**: Render.com (for now)
- **Email**: Gmail SMTP
- **Version Control**: Git + GitHub

---

## 📦 Environment Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/drewmtv/byteoflegacy.git
   cd byte-of-legacy

2. **Create a virtual environment**
    ```bash
    python -m venv env
    source evn/bin/activate # or env\Scripts\activate
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt

4. **Setup `.env` file**
    Create a `.env` file in the root with the following:
    ```bash
    DEBUG=True
    SECRET_KEY=your_django_secret
    SUPABASE_URL=https://your-supabase-url.supabase.co
    SUPABASE_SERVICE_KEY=your-supabase-service-key
    SUPABASE_STORAGE_BUCKET=your-public-bucket
    SUPABASE_STORAGE_BUCKET_CONFIDENTIAL=your-private-bucket
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=your-email@gmail.com
    EMAIL_HOST_PASSWORD=your-app-password
5. **Run migrations**

    ```
    python manage.py makemigrations
    python manage.py migrate
6. **Collect Static Files**

    ```
    python manage.py collecstatic
7. **Run the dev server**

    ```
    python manage.py runserver

# ✅ To Do / Roadmap
- Stripe or GCash integration for instant payment confirmation

- Public mosaic filtering and sorting

- Leaderboard or featured supporters

- Admin dashboard improvements

- Integration with TechStart TV main site

# 🧩 Folder Structure
    byte_of_legacy/
    │
    ├── legacy/              # Django app (models, views, forms, templates)
    ├── templates/           # HTML templates
    ├── static/              # CSS, JS, images
    ├── utils.py             # Supabase upload logic
    ├── validators.py        # File validators
    ├── .env.example         # Sample environment config
    ├── requirements.txt     # Python dependencies
    └── manage.py

# 🤝 Contributing
We welcome contributions! Feel free to fork the repo and submit pull requests. You can also help by:

- Filing issues and suggestions

- Sharing with your community

- Claiming your byte at Site To Be Announced.

# 📄 License
MIT License © 2025 TechStart TV & Contributors

# 🌐 Connect
- 🌍 [TechStart TV Website](https://linktr.ee/techstarttv)

- 🎥 BoostStrap Podcast - Coming soon

- 📧 matheu.andrew143@gmail.com