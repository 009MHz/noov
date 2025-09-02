from playwright.async_api import Page, expect
import re

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        
        # Loader element
        self.preloader = page.locator(".preloader")
        self.loader_container = page.locator(".loader-container")
        
        # Header elements
        self.language_toggle = page.locator("#languageToggle")
        self.logo = page.get_by_alt_text("noovoleum logo")
        self.hero_text = page.get_by_text("Making everybody a green energy champion")

        # Banner Processes
        self.step1_image = page.get_by_role('img', name='step 1')
        self.step2_image = page.get_by_role('img', name='step 2')
        self.step3_image = page.get_by_role('img', name='step 3')
        self.step4_image = page.get_by_role('img', name='step 4')

        self.step1_desc = page.get_by_text("Collect previously utilized")
        self.step2_desc = page.get_by_text("Find the nearest UCO")
        self.step3_desc = page.get_by_text("Deposit your Used Cooking Oil")
        self.step4_desc = page.get_by_text("Receive instant credit")

        # Banner Mobile
        self.banner_mobile = page.locator("#about")
        self.apple_btn = self.banner_mobile.get_by_role('link').first
        self.android_btn = self.banner_mobile.get_by_role('link').nth(1)

        # Form Submit
        self.header_submit = page.get_by_text(re.compile(r"get in touch"))
        self.btn_send = page.get_by_role('link', name="Send Message")
        self.err_name = page.locator("#userNameError")
        self.err_email = page.locator("#userEmailError")
        self.err_message = page.locator("#userMessageError")
        self.input_name = page.get_by_role('textbox', name='Your Name')
        self.input_email = page.get_by_role("textbox", name="Email Address")
        self.input_message = page.get_by_role('textbox', name="Write Your Message Here")

        # Company Info
        self.info_logo = page.get_by_role('img', name='noovoleum white logo')
        self.company_sg_address = page.get_by_text(re.compile(r"NOOVOLEUM PTE\. LTD\..*189352 Singapore", re.DOTALL))
        self.company_id_address = page.get_by_text(re.compile(r"PT PMA Noovoleum Indonesia.*Jawa Barat", re.DOTALL))
        self.linkedin_link = page.get_by_role("link", name=" noovoleum")
        self.instagram_link = page.get_by_role('link').filter(has_text='noovoleumid')
        self.email_link = page.get_by_role('link').filter(has_text='contact@noovoleum.com')
        
        # Footer elements
        self.footer = page.locator('.copyright')
        self.copyright_text = page.get_by_text('© 2024 noovoleum. All right reserved.')
        self.self_declaration_link = page.get_by_role('link', name='Self Declaration')
        self.privacy_policy_link = page.get_by_role('link', name='Privacy policy')
        self.terms_conditions_link = page.get_by_role('link', name='Terms and Conditions')
        

    # ---------- internals ----------

    async def _disable_animations_and_reveal(self):
        await self.page.add_style_tag(content="""
            * { animation: none !important; transition: none !important; }
            .wow { visibility: visible !important; }
        """)

    async def _wait_preloader_gone(self, timeout: int = 8000):
        try:
            await self.preloader.wait_for(state="hidden", timeout=timeout)
        except Exception:
            try:
                await self.loader_container.wait_for(state="hidden", timeout=timeout // 2)
            except Exception:
                pass

    async def open(self, base_url: str = "https://noovoleum.com"):
        await self.page.goto(base_url)
        await self.page.wait_for_load_state("load")
        await self._wait_preloader_gone()
        await self._disable_animations_and_reveal()

        return self

    async def fill_contact_form(self, name: str, email: str, message: str):
        await self.input_name.fill(name)
        await self.input_email.fill(email)
        await self.input_message.fill(message)

    async def click_send_message(self):
        await self.btn_send.click()
        
    async def click_language_toggle(self):
        await self.language_toggle.click()
        
    async def click_main_logo(self):
        await self.logo.click()

    async def click_banner_apple_btn(self):
        await self.apple_btn.click()

    async def click_banner_android_btn(self):
        await self.android_btn.click()
        
    # Footer Actions
    async def click_self_declaration(self):
        return await self.self_declaration_link.click()
        
    async def click_privacy_policy(self):
        return await self.privacy_policy_link.click()
        
    async def click_terms_conditions(self):
        return await self.terms_conditions_link.click()