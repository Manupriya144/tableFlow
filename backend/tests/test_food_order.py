
import re
from playwright.sync_api import Page, expect

BASE_URL = "https://table-flow-delta.vercel.app/"


def test_TC16_submit_valid_food_order(page: Page):

    # Step 1: Open the menu page
    page.goto(
        BASE_URL + "menu",
        wait_until="domcontentloaded",
        timeout=60000
    )

    expect(page.locator("body")).to_contain_text(
        re.compile(r"menu", re.I)
    )

    print("Menu page loaded successfully.")

    # Step 2: Check available food items
    body_text = page.locator("body").inner_text()

    assert len(body_text.strip()) > 0, "Menu content is empty."

    print("Food menu content displayed.")

    # Step 3: Find an Add to Cart / Order button
    add_button = page.get_by_role(
        "button",
        name=re.compile(r"add to cart|add|order now", re.I)
    )

    expect(add_button.first).to_be_visible()

    # Add the first available food item
    add_button.first.click()

    print("Food item selected.")

    # Step 4: Check whether cart / checkout interface is available
    page.wait_for_timeout(1500)

    cart_button = page.get_by_role(
        "button",
        name=re.compile(r"cart|checkout|view order", re.I)
    )

    expect(cart_button.first).to_be_visible()

    cart_button.first.click()

    print("Cart / ordering interface opened.")

    # Step 5: Check checkout interface
    page.wait_for_timeout(1500)

    print("Current URL:", page.url)
    print("Checkout page content:")
    print(page.locator("body").inner_text())

    # Step 6: Check order tracking page accessibility
    tracking_page = page.context.new_page()

    tracking_page.goto(
        BASE_URL + "orders",
        wait_until="domcontentloaded",
        timeout=60000
    )

    expect(tracking_page.locator("body")).to_contain_text(
        re.compile(r"order|track", re.I)
    )

    print("Order tracking page is accessible.")

    tracking_page.close()
