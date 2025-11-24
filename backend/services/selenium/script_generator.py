import re
from typing import Optional


class SeleniumScriptGenerator:

    @staticmethod
    def _extract_text_steps(steps: str) -> list:
        """
        Convert step text into structured actions.
        Example:
            "Enter SAVE15 in discount field, proceed to checkout"
        """
        raw_steps = re.split(r",|\n|->|•|- ", steps)
        cleaned = [s.strip() for s in raw_steps if s.strip()]
        return cleaned

    @staticmethod
    def _guess_selector_from_step(step: str) -> Optional[str]:
        """
        Very controlled selector inference based ONLY on explicit wording.
        No hallucination.
        """
        step_lower = step.lower()

        # Discount code input
        if "discount" in step_lower and ("enter" in step_lower or "type" in step_lower):
            return "#discount-code"

        # Apply button
        if ("apply" in step_lower and "discount" in step_lower) or "apply button" in step_lower:
            return "#apply-discount"

        # Checkout button
        if "checkout" in step_lower:
            return "#checkout-button"

        return None  # No assumptions allowed

    @staticmethod
    def generate_script(test_id: str, scenario: str, steps: str, expected_result: str) -> str:
        parsed_steps = SeleniumScriptGenerator._extract_text_steps(steps)

        action_blocks = []
        for s in parsed_steps:
            selector = SeleniumScriptGenerator._guess_selector_from_step(s)

            if selector:
                # Input field
                if "enter" in s.lower() or "type" in s.lower():
                    # Extract the text typed
                    match = re.search(r"enter\s+([A-Za-z0-9_-]+)", s, re.IGNORECASE)
                    value = match.group(1) if match else ""
                    action_blocks.append(
                        f'    element = wait_for_first_visible(driver, ["{selector}"])\n'
                        f'    element.send_keys("{value}")\n'
                    )
                else:
                    # Button click
                    action_blocks.append(
                        f'    element = wait_for_first_visible(driver, ["{selector}"])\n'
                        f'    element.click()\n'
                    )

        # Assertion block
        assertion_block = ""
        if expected_result:
            assertion_block = (
                "    result = wait_for_first_visible(driver, [\"#discount-result\"])\n"
                f"    assert \"{expected_result}\" in result.text, \\\n"
                f"        f\"Expected text not found. Got: {{result.text}}\"\n"
            )

        # Final script
        script = f"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def wait_for_first_visible(driver, selectors, timeout=10):
    for selector in selectors:
        try:
            return WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
            )
        except:
            pass
    raise Exception("No selectors matched any element on the page.")

def setup():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    return driver

def teardown(driver):
    driver.quit()

def test_case():
    driver = setup()
    try:
        driver.get("checkout.html")

        # Scenario: {scenario}
        # Steps:
"""
        script += "\n".join(action_blocks)

        script += "\n        # Validation\n"
        script += assertion_block

        script += """
    finally:
        teardown(driver)

if __name__ == "__main__":
    test_case()
"""

        return script.strip()
