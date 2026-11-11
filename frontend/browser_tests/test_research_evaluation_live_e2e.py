"""Local synthetic browser-to-FastAPI flow. No real participant data is used."""
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"
sys.path.insert(0, str(ROOT))
from backend.app.research import responses  # noqa: E402
from backend.app.research.reporting import calculate_summary  # noqa: E402


def free_port():
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]


class ResearchCollectionLiveE2ETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="wiselanka-synthetic-e2e-")
        cls.temp_path = Path(cls.temp.name)
        cls.database = cls.temp_path / "synthetic-research.sqlite3"
        responses.initialize_database(cls.database)
        cls.invitation = responses.create_invitation(cls.database, consent_verified=True, expires_in_minutes=30)
        responses.insert_session_observation(cls.database, cls.invitation["session_id"],
            "Task 1 — A/L learner profile", "UNASSISTED", 39)
        cls.api_port = free_port()
        cls.static_port = next((port for port in (5500, 5501) if cls._serves_questionnaire(port)), None)
        cls.owns_static = False
        if cls.static_port is None:
            cls.static_port = next((port for port in (5500, 5501) if cls._port_available(port)), None)
            if cls.static_port is None:
                raise RuntimeError("Both approved local frontend ports 5500 and 5501 are occupied by other services")
            cls.owns_static = True
        env = os.environ.copy()
        env.update({"RESEARCH_COLLECTION_ENABLED": "true", "RESEARCH_DATABASE_PATH": str(cls.database),
                    "PYTHONPATH": str(ROOT)})
        cls.api_log = (cls.temp_path / "api-synthetic.log").open("w")
        cls.static_log = (cls.temp_path / "static-synthetic.log").open("w")
        cls.api = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.app.api.main:app",
                                    "--host", "127.0.0.1", "--port", str(cls.api_port), "--no-access-log"],
                                   cwd=ROOT, env=env, stdout=cls.api_log, stderr=subprocess.STDOUT)
        cls.static = None
        if cls.owns_static:
            cls.static = subprocess.Popen([sys.executable, "-m", "http.server", str(cls.static_port),
                                           "--bind", "127.0.0.1", "--directory", str(FRONTEND)],
                                          cwd=ROOT, env=env, stdout=cls.static_log, stderr=subprocess.STDOUT)
        cls._wait_for(f"http://127.0.0.1:{cls.api_port}/openapi.json")
        cls._wait_for(f"http://127.0.0.1:{cls.static_port}/pages/research-evaluation.html")

    @staticmethod
    def _port_available(port):
        with socket.socket() as probe:
            return probe.connect_ex(("127.0.0.1", port)) != 0

    @staticmethod
    def _serves_questionnaire(port):
        try:
            with urlopen(f"http://127.0.0.1:{port}/pages/research-evaluation.html", timeout=1) as response:
                body = response.read().decode("utf-8", "replace")
                return response.status == 200 and "WISELANKA · INDEPENDENT STUDY" in body
        except Exception:
            return False

    @classmethod
    def _wait_for(cls, url):
        deadline = time.time() + 15
        while time.time() < deadline:
            try:
                with urlopen(url, timeout=1) as response:
                    if response.status == 200:
                        return
            except Exception:
                exited = [(name, process.poll()) for name, process in
                          (("API", cls.api), ("frontend", cls.static)) if process is not None]
                stopped = [(name, code) for name, code in exited if code is not None]
                if stopped:
                    detail = ""
                    for name, stream_name in (("API", "api_log"), ("frontend", "static_log")):
                        stream = getattr(cls, stream_name, None)
                        if stream and name in {item[0] for item in stopped}:
                            stream.flush()
                            detail += "\n" + stream.name + ": " + Path(stream.name).read_text(errors="replace")[-2000:]
                    raise RuntimeError(f"A local synthetic E2E service exited during startup: {stopped}{detail}")
                time.sleep(0.1)
        raise RuntimeError(f"Timed out starting local synthetic test service: {url}")

    @classmethod
    def tearDownClass(cls):
        for process in (getattr(cls, "static", None), getattr(cls, "api", None)):
            if process and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
        for stream_name in ("api_log", "static_log"):
            stream = getattr(cls, stream_name, None)
            if stream:
                stream.close()
        cls.temp.cleanup()

    def test_desktop_and_mobile_invitation_submission_round_trip(self):
        errors = []
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel="chrome", headless=True)
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.add_init_script(f"window.WISELANKA_API_BASE_URL='http://127.0.0.1:{self.api_port}'")
            page.on("pageerror", lambda error: errors.append(str(error)))
            url = f"http://127.0.0.1:{self.static_port}/pages/research-evaluation.html#invite={self.invitation['invitation_token']}"
            page.goto(url, wait_until="domcontentloaded")
            page.get_by_text("Research invitation active").wait_for()
            self.assertNotIn("invite=", page.url)
            page.locator("#age-yes").check()
            page.get_by_role("button", name="Continue →").click()
            page.locator("#device-1").check()
            page.locator("#tasks-0").check()
            page.locator("#route-0").check()
            page.get_by_role("button", name="Continue →").click()
            page.locator("#Q5-rating-3").check()
            page.get_by_role("button", name="Continue →").click()
            page.get_by_role("button", name="Continue →").click()
            page.get_by_role("button", name="Continue →").click()
            page.locator("#Q25").fill("SYNTHETIC: local E2E comment, not participant feedback.")
            page.get_by_role("button", name="Review and submit →").click()
            page.get_by_text("The server confirmed that your questionnaire response was stored.").wait_for(timeout=10000)
            self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 390)
            page.set_viewport_size({"width": 1280, "height": 900})
            self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 1280)
            self.assertEqual(errors, [])
            browser.close()

        with __import__("sqlite3").connect(self.database) as connection:
            rows = connection.execute("SELECT session_id,adult_confirmed,consent_confirmed,answers_json FROM research_responses").fetchall()
            self.assertEqual(len(rows), 1)
            session_id, adult, consent, answers_json = rows[0]
            self.assertEqual(session_id, self.invitation["session_id"])
            self.assertEqual((adult, consent), (1, 1))
            self.assertIn("SYNTHETIC: local E2E comment", answers_json)
            self.assertEqual(connection.execute("SELECT count(*) FROM research_invitations WHERE used_at_utc IS NOT NULL").fetchone()[0], 1)
        summary = calculate_summary(self.database)
        self.assertEqual(summary["submitted_responses"], 1)
        self.assertEqual(summary["observations_by_task"]["Task 1 — A/L learner profile"]["observations"], 1)
        self.assertEqual(summary["item_counts"]["Q5"]["rating_mean"], 4)


if __name__ == "__main__":
    unittest.main()
