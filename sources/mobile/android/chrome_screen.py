from selenium.webdriver.common.by import By
from sources.mobile.__base import BaseMobileScreen

class ChromeScreen(BaseMobileScreen):
    __home_search = (By.ID, "com.android.chrome:id/search_box_text")
    __omnibox = (By.ID, "com.android.chrome:id/url_bar")
    __search_results = (By.XPATH, '//android.view.View[@resource-id="center_col"]')


    async def search_keyword(self, keyword: str):
        await self._tap(self.__home_search)
        await self._type(self.__omnibox, keyword)
        self.driver.press_keycode(66)

        
    async def url_redirection(self, param: str) -> bool:
        address_bar = await self._find(self.__omnibox)
        return param in address_bar.text

    async def verify_results_not_empty(self) -> bool:
        return await self._wait_visible(self.__search_results)
        

