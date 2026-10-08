# Binary Search Simulator

A Streamlit app that animates binary search step by step. Part of The Weekly Algorithm.

## Files

| File | What it does |
|---|---|
| `app.py` | The whole app |
| `requirements.txt` | Tells the host which libraries to install (Streamlit only) |
| `.streamlit/config.toml` | Colour theme (pink and sage) |

## Run it on your own computer

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Put it online (free, Streamlit Community Cloud)

You need a GitHub account (free) and no extra software.

1. Go to github.com and click **New repository**. Name it `binary-search-simulator`, choose **Public**, click **Create repository**.
2. On the new repository page click **uploading an existing file**.
3. Drag in `app.py` and `requirements.txt`. Click **Commit changes**.
4. Add the theme file: click **Add file > Create new file**, type `.streamlit/config.toml` as the name (typing the slash makes the folder), paste the contents of `config.toml`, and click **Commit changes**.
5. Go to share.streamlit.io and sign in with GitHub.
6. Click **Create app** (or **New app**), choose **Deploy a public app from GitHub**.
7. Pick your repository, branch `main`, and main file path `app.py`. Click **Deploy**.
8. Wait 1 to 3 minutes. You get a link like `https://your-name.streamlit.app`. Share that link.

Notes:
- Free apps go to sleep when nobody visits for a while. The first visitor sees a "Wake this app up" button; one click and it starts.
- If you change `app.py` on GitHub, the website updates by itself.
- Without `config.toml` the app still works, but the main button turns Streamlit's default red.
