# Clarivo Web

Next.js and TypeScript frontend for Clarivo.

## Setup

From the repository root:

```bash
npm install --prefix apps/web
copy apps\web\.env.local.example apps\web\.env.local
npm run dev --prefix apps/web
```

Open `http://localhost:3000`.

The API must be running at the URL configured by `NEXT_PUBLIC_API_URL`.

The browser recording flow supports preparation, microphone permission,
recording, local playback, retry, upload, and playback after reload.
