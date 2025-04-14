"""den synkrona versionen av Playwright inte fungerar bra i asynkrona miljöer som Behave,
medan den asynkrona versionen gör det. Eftersom Behave också kan köra asynkront så fungerar
koden när jag använder async och await.
"""


"""

Genom att använda den asynkrona versionen av Playwright (async_playwright) och
 se till att alla mina funktioner och teststeg är asynkrona, kan jag säkerställa 
att min kod körs effektivt och korrekt.
"""





from behave import given, when, then
from playwright.async_api import async_playwright
import asyncio

# ------------------ Webbläsarfunktioner ------------------

async def start_browser(context, url):
    context.playwright = await async_playwright().start()
    context.browser = await context.playwright.chromium.launch(headless=False)
    context.page = await context.browser.new_page()
    await context.page.goto(url)

async def close_browser(context):
    await context.browser.close()
    await context.playwright.stop()

# ------------------ Gemensamma steg ------------------

@given("att användaren öppnar startsidan")
async def step_open_start_page(context):
    await start_browser(context, "https://forverkliga.se/JavaScript/my-contacts/")

@given("att användaren öppnar kontaktsidan")
async def step_open_contact_page(context):
    await start_browser(context, "https://forverkliga.se/JavaScript/my-contacts/#/")

@then('ska webbadressen vara "{url}"')
async def step_check_url(context, url):
    current_url = context.page.url
    assert current_url == url, f"Expected URL to be {url}, but got {current_url}"

# ------------------ Vänlista ------------------

@when('användaren klickar på knappen "Vänlista"')
async def step_click_friends_list_button(context):
    await context.page.click("text=Vänlista")

@then("ska användaren se vänlistan")
async def step_see_friends_list(context):
    await context.page.wait_for_selector("text=Jean-Luc Picard", timeout=60000)

    assert await context.page.locator("text=Jean-Luc Picard").is_visible()
    assert await context.page.locator("text=captain.picard@starfleet.com").is_visible()
    assert await context.page.locator(".friend:has-text('Spock')").is_visible()
    assert await context.page.locator(".friend:has-text('science.officer.spock@starfleet.com')").is_visible()
    assert await context.page.locator(".friend:has-text('James T. Kirk')").is_visible()
    assert await context.page.locator(".friend:has-text('captain.kirk@starfleet.com')").is_visible()
    assert await context.page.locator(".friend:has-text('Data')").is_visible()
    assert await context.page.locator(".friend:has-text('android.data@starfleet.com')").is_visible()
    assert await context.page.locator(".friend:has-text('William Riker')").is_visible()
    assert await context.page.locator(".friend:has-text('commander.riker@starfleet.com')").is_visible()

    await close_browser(context)

# ------------------ Ny vän ------------------

@when('användaren klickar på knappen "Ny vän"')
async def step_click_new_friend_button(context):
    await context.page.click("text=Ny vän")

@when('användaren fyller i namn med "{namn}"')
async def step_fill_name(context, namn):
    await context.page.fill('input[placeholder="Namn"]', namn)

@when('användaren fyller i e-post med "{epost}"')
async def step_fill_email(context, epost):
    await context.page.fill('input[placeholder="E-post"]', epost)

@when('användaren klickar på knappen "Spara"')
async def step_click_save(context):
    await context.page.click("text=Spara")
    await context.page.wait_for_timeout(1000)

@then('ska användaren se meddelandet "Fyll i båda fälten för att lägga till din vän." visas inte')
async def step_no_error_message(context):
    error_locator = context.page.locator("text=Fyll i båda fälten för att lägga till din vän.")
    assert not await error_locator.is_visible(), "Felmeddelande visas trots att båda fält är ifyllda"

@then('den nya vännen "{namn}" ska synas i listan')
async def step_new_friend_visible(context, namn):
    await context.page.wait_for_selector(f"text={namn}", timeout=5000)
    assert await context.page.locator(f"text={namn}").is_visible(), f"{namn} syns inte i listan"
    await close_browser(context)
