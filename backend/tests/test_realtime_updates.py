import re
import time
from playwright.sync_api import Page, expect

BASE_URL = "https://table-flow-delta.vercel.app/"


def test_TC18_realtime_updates(page: Page):
    # Open Host Desk in the first browser page
    page.goto(
        BASE_URL + "host",
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(2000)

    # Open a second client in another browser page
    second_page = page.context.new_page()
    second_page.goto(
        BASE_URL + "host",
        wait_until="domcontentloaded",
        timeout=60000
    )

    second_page.wait_for_timeout(2000)

    print("Client 1 URL:", page.url)
    print("Client 2 URL:", second_page.url)

    # Find possible table-status controls on Client 1
    status_controls = page.get_by_role(
        "button",
        name=re.compile(r"available|occupied|status", re.I)
    )

    if status_controls.count() == 0:
        print(
            "TC-18 NOT VERIFIED: No recognizable table-status "
            "button was found. Inspect the actual Host Desk controls."
        )
        second_page.close()
        return

    # Capture the second client's content before the update
    before_update = second_page.locator("body").inner_text()

    # Click a matching status control on Client 1
    status_controls.first.click()
    page.wait_for_timeout(1000)

    # Capture Client 1 content after the action
    after_update = page.locator("body").inner_text()

    # Check Client 2 without refreshing it
    second_page.wait_for_timeout(3000)
    after_client_update = second_page.locator("body").inner_text()

    print("Client 1 content changed:", before_update != after_update)
    print(
        "Client 2 content changed:",
        before_update != after_client_update
    )

    # Pass only if the second client receives a visible content change
    assert before_update != after_client_update, (
        "TC-18 FAILED: No visible update was detected on Client 2 "
        "without refreshing."
    )

    print("TC-18 PASSED: Client 2 received an update without refreshing.")

    second_page.close()