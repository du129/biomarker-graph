# Deployment Guide (GitHub -> Render + Netlify)

## 1) Push project to GitHub

From repo root:

```bash
cd /Users/jonathandu/azure-practice/ai-practice/food-biomarker
git init
git add .
git commit -m "Prepare app for Render + Netlify deployment"
```

Create a GitHub repo, then connect and push:

```bash
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

If `origin` already exists, run:

```bash
git remote set-url origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## 2) Deploy backend on Render

1. In Render, choose **New +** -> **Blueprint**.
2. Select your GitHub repo (Render reads `/render.yaml`).
3. Render creates service `food-biomarker-api`.
4. After first deploy, open the service and copy URL:
   - Example: `https://food-biomarker-api.onrender.com`
5. Set env vars in Render service:
   - `CORS_ORIGINS=https://<your-netlify-site>.netlify.app,http://localhost:5173`
   - Optional for previews: `CORS_ORIGIN_REGEX=https://.*\.netlify\.app`
6. Redeploy after env var changes.

## 3) Deploy frontend on Netlify

1. In Netlify, choose **Add new site** -> **Import an existing project**.
2. Select your GitHub repo.
3. Build settings are auto-read from `/netlify.toml`:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`
4. Add environment variable before deploy:
   - `VITE_API_BASE_URL=https://<your-render-service>.onrender.com`
5. Deploy site.

## 4) Verify integration

1. Open Netlify site.
2. Confirm dashboard and graph load data.
3. If data fails to load, check:
   - Netlify env var `VITE_API_BASE_URL`
   - Render `CORS_ORIGINS`
   - Render logs for CORS errors
