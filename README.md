# 🌿 LifeLog
## Personal Diary & Mood Tracker

**A Python-based journaling application with file-based persistent storage.**

LifeLog is a console-based digital diary that allows users to write daily journal entries, review past logs, edit/delete entries, and track mood patterns — all stored securely in local files.

---

## ✅ Features

### 🔐 **User Authentication**

* Sign up with username + password
* User accounts stored in a file (`.lifelog/user.dat`)

### ✍️ **Add New Journal Entries**

* Write detailed diary entries
* Auto-capture current date
* Choose mood (Happy, Calm, Sad, Stressed, Confident)
* Entries stored in a local file (bin)

### 📖 **View Past Entries**

* View all logs
* View entries by **date range**
* View entries by **mood**
* Nicely formatted CLI output

### 🧹 **Edit / Delete Entries**

* Update title, mood, or content
* Remove specific entries cleanly from the storage file

### 📊 **Mood Analytics**

* Mood frequency charts using `matplotlib`
* Summaries to help users reflect on emotional patterns

---

## 🛠️ Tech Stack

### **Core Technology**

* **Python 3**
* **File-based storage**

  * Typically stored in:

    * User Data and Stats in `.lifelog/user.dat` & `.lifelog/stats.dat`
    * Diary entries in `.lifelog/<username>/`

### **Python Libraries Used**

* `pickle` — File-based persistence
* `datetime` — Managing timestamps
* `matplotlib` — Mood visualizations
* `os`, `time` — UI/UX polishing

---

## 📁 File Storage Design

### **.lifelog/user.dat**

Stores all user accounts.

Example (data before serialization):

```json
[
  {
    "username": "nav343",
    "password": "password",
    "usePass": true
  }
]
```

### **.lifelog/stats.dat**

Stores stats for last session.

Example (data before serialization):

```json
  {
    "username": "navsnm",
    "lastLogged":"05 November 2025"
  }
```


### **.lifelog/(Username)/(Diary Title).dat**

Stores journal entries

Example (data before serialization):

```json
  {
      "content": "Hi there....This is my first diary entry...",
      "mood": 2,
      "date": "05 November 2025"
  }
```


---

## 🧱 Project Structure

```
LifeLog/
|
└── .lifelog/
|   └── <username>/
|   |   |── <diary_title_1>.dat
|   |   └── <diary_title_2>.dat
|   |── stats.dat
|   └── user.dat
|
└── utils/
|   └── window.py
|
|── main.py
|── plot.py
└── README.md
```

---

## 🚀 How to Run
1. Clone the repository:

   ```
   git clone https://github.com/nav343/LifeLog
   ```
2. Change Directory
    ```
    cd LifeLog
    ```
2. Install dependencies:

   ```
   pip install matplotlib
   ```
* (Using a virtual environment is recommended)
4. Run the app:

   ```
   python main.py
   ```

- (NOTE: It creates .lifelog folder)
---

## 🌈 Additional Highlights

* Clean CLI design with ASCII borders and emojis
* Motivational quotes after entries
* Recursive text formatter for clean display
* Lightweight and portable — no database needed
