Here is your cleaned, professional **README.md** without emojis and without the file structure section:

---

# Epidora — AI Dermatologist

Epidora is an AI-powered dermatology web application that analyzes skin images and provides insights, possible conditions, and skincare recommendations.

## Features

* Skin image upload and analysis
* AI-based dermatological insights
* Possible skin condition detection
* Skincare recommendations
* User authentication using Supabase
* Dashboard interface

---

## Tech Stack

**Frontend**

* HTML
* CSS
* JavaScript

**Backend**

* Node.js
* Express (if used)

**AI / ML**

* Skin analysis model (local or external API)

**Database & Authentication**

* Supabase

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/your-username/epidora.git
cd epidora/ai-dermatologist
```

### Install dependencies

```bash
npm install
```

### Set up environment variables

Create a `.env` file in the `ai-dermatologist` folder:

```
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_key
PORT=5001
```

### Run the server

```bash
node index.js
```

Server will start at:

```
http://127.0.0.1:5001
```

---

## Image Analysis API

Endpoint used for analyzing skin images:

```
POST /analyze-image
```

Example frontend call:

```js
const res = await fetch("http://127.0.0.1:5001/analyze-image", {
  method: "POST",
  body: formData
});
```

---

## Pages

* `index.html` — Landing page
* `login.html` — User login
* `dashboard.html` — User dashboard
* `image-consult.html` — Upload and analysis
* `about.html` — About the project

---

## Disclaimer

Epidora is intended for informational purposes only and does not replace professional medical advice. Always consult a qualified dermatologist for diagnosis and treatment.

---

## Author

Diya Singh
B.Tech Student

---

## Future Improvements

* Real-time skin tracking
* Personalized treatment plans
* Mobile application version
* Multi-language support

---



