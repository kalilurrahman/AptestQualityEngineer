from langchain_core.tools import tool
from src.tools.schemas import InteractWithUIInput, InteractWithUIOutput
from playwright.sync_api import sync_playwright, Page, Browser
import time
import os

class PlaywrightMCPServer:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser: Browser = None
        self.page: Page = None
        self.playwright = None

    def start(self):
        if not self.playwright:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.page = self.browser.new_page()

    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def resolve_element(self, description: str, dom_snapshot: str) -> str:
        """
        Uses an LLM/VLM to resolve the description to a selector.
        In a real implementation, this would call GPT-4o with the screenshot.
        Here we mock it or use heuristics.
        """
        # Mock implementation for demonstration
        print(f"[VLM] Resolving element: '{description}'")
        if "submit" in description.lower():
            return "button[type='submit']"
        if "login" in description.lower():
            return "#login-btn"
        return f"text={description}"

    def interact(self, action: str, description: str, value: str = None) -> dict:
        """
        Interacts with a UI element based on visual description.
        """
        if not self.page:
            try:
                self.start()
            except Exception as e:
                # Fallback for environments where Playwright cannot run (e.g. some CI/CD)
                return {
                    "success": False,
                    "message": f"Failed to start Playwright: {str(e)}. Running in simulation mode.",
                    "screenshot": None
                }

        try:
            if action == "navigate":
                self.page.goto(description)
                return {
                    "success": True,
                    "message": f"Navigated to {description}",
                    "screenshot": None
                }

            # Capture snapshot for VLM
            dom_snapshot = ""
            try:
                dom_snapshot = self.page.content()
            except:
                pass

            selector = self.resolve_element(description, dom_snapshot)

            if action == "click":
                self.page.click(selector, timeout=2000)
            elif action == "type":
                self.page.fill(selector, value, timeout=2000)
            elif action == "hover":
                self.page.hover(selector, timeout=2000)
            elif action == "wait":
                 time.sleep(float(value) if value else 1)

            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f"screenshot_{int(time.time())}.png")
            self.page.screenshot(path=screenshot_path)

            return {
                "success": True,
                "message": f"Successfully performed {action} on {description}",
                "screenshot": screenshot_path
            }
        except Exception as e:
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f"error_screenshot_{int(time.time())}.png")
            try:
                self.page.screenshot(path=screenshot_path)
            except:
                pass
            return {
                "success": False,
                "message": str(e),
                "screenshot": screenshot_path
            }

# Global instance
server = PlaywrightMCPServer()

@tool(args_schema=InteractWithUIInput)
def interact_with_ui(action: str, description: str, value: str = None) -> dict:
    """Interacts with a UI element based on visual description."""
    return server.interact(action, description, value)
