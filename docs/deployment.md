# Deploy WiseLanka: Vercel frontend and Render API

The repository contains both services. Keep the repository root as the root
directory in both hosting projects. Commit and push the deployment changes
before importing the repository.

## 1. Deploy the backend on Render

1. In Render, create a **Blueprint** from this GitHub repository. The root
   `render.yaml` defines the Python service, dependency installation, start
   command, and `/health` endpoint.
2. Set `WISELANKA_CORS_ORIGINS` to your planned frontend origin, for example
   `https://wiselanka.vercel.app`. Replace it with the actual assigned domain
   after Vercel creates the project. Multiple trusted origins are comma-separated.
3. Deploy and copy the assigned `https://….onrender.com` address.
4. Open `https://….onrender.com/health`; the expected response is
   `{"status":"ok"}`.

For manual service creation, use:

| Setting | Value |
| --- | --- |
| Runtime | Python |
| Build command | `pip install -r requirements-render.txt` |
| Start command | `python -m uvicorn backend.app.api.main:app --host 0.0.0.0 --port $PORT` |
| Health check | `/health` |
| Python version | Set `PYTHON_VERSION` to the version in `render.yaml` |

The CSV knowledge base is deployed with the backend. Research collection and
optional Gemini exploration retain their existing disabled-by-default behaviour.
Enabling research collection later requires a separate persistent-storage plan;
this deployment does not enable or configure research storage.

## 2. Deploy the frontend on Vercel

1. Import the same repository into Vercel.
2. Keep **Root Directory** at the repository root and choose **Other** as the
   framework. `vercel.json` supplies `npm run build` and output directory `dist`.
   The project pins the build runtime to Node.js 24.x in `package.json`.
3. In the Vercel project's environment variables, add:
   `WISELANKA_API_BASE=https://your-api.onrender.com`.
   Use the actual Render URL and enable it for the deployment environments you use.
4. Deploy. The build generates the public runtime configuration. It fails if a
   Vercel build has no configured API URL, uses localhost, or uses plain HTTP.
5. Copy the assigned frontend origin into Render's `WISELANKA_CORS_ORIGINS`
   setting and redeploy/restart the API if needed.

`WISELANKA_API_BASE` is public configuration embedded into JavaScript. Do not put
an API key, password or token there. API secrets belong only in Render settings.
Changing the API URL requires a new Vercel build. CORS changes require the API
process to restart.

Only `dist` is published. It includes the seven public pages, frontend code,
public images/fonts/video icons, and UI translations. Backend source, research
pages, tests, documentation, and reference CSV records are excluded. Each page's
CSS is bundled with content-hashed filenames while retaining stylesheet order.

## Preview deployments and custom domains

Add each trusted frontend origin to `WISELANKA_CORS_ORIGINS`. A Vercel preview
has a different origin from production; use a stable preview alias or add its
exact origin explicitly. Do not allow all `vercel.app` projects or `*`.
When adding a custom domain, allow both the desired production origin and any
Vercel alias that will remain in use. Use HTTPS URLs for both services.

Render's free service can take time to wake up after inactivity. Requests have
a 45-second timeout with a retry message. This does not remove platform cold
starts; use an always-on service if the required response time demands it.

## Local development and verification

```powershell
python -m uvicorn backend.app.api.main:app --host 127.0.0.1 --port 8000
```

In another terminal, either serve the source tree for development:

```powershell
python -m http.server 5500 --bind 127.0.0.1
```

Or build and serve the same static output deployed to Vercel:

```powershell
npm run build
python -m http.server 5501 --bind 127.0.0.1 --directory dist
```

Local builds default to the API on port 8000. Set `$env:WISELANKA_API_BASE` before
building to exercise a different API. `.env.example` documents the settings;
the scripts do not automatically load `.env` files.

```powershell
npm run test:frontend
python -m pytest tests/integration/test_deployment.py tests/integration/test_guided_assistant.py -q
npm run build
python frontend/browser_tests/deployment_smoke.py
python frontend/browser_tests/workflow_smoke.py
```

The browser check requires Playwright and Chromium (`python -m playwright install
chromium`), the built site on port 5501, and the API on port 8000. It exercises
real HTTP requests for chat and recommendations, request failure/retry, profile
recovery and clearing, reuse of results, and public navigation. Node build tests
use a test API origin; rebuild before starting the browser check.

## Frontend maintenance

- Edit shared navigation in `frontend/navigation.json`; run `npm run sync` to
  update the checked-in static pages. Production builds generate it automatically.
- Edit shared colours, typography variables and spacing in
  `frontend/styles/tokens.css`. Page layouts keep their responsive overrides.
- Use `WiseAPI` from `frontend/components/api.js` for every API request. It owns
  timeouts, cancellation and connection/validation errors. POST requests are
  retried only by an explicit user action.
- Profile drafts are versioned and kept in this browser's local storage. The
  profile page exposes a clear action. They are not an account or server backup.
- The chat uses the deterministic `/assistant` API. It requires a programme and
  optional learner evidence for the selected topic; it is not a general LLM chat.

Official references: [Vercel project configuration](https://vercel.com/docs/project-configuration),
[Render Blueprint reference](https://render.com/docs/blueprint-spec).
