from bs4 import BeautifulSoup
from loguru import logger

from llm_engineering.domain.documents import ArticleDocument

from .base import BaseSeleniumCrawler


class MediumCrawler(BaseSeleniumCrawler):
    model = ArticleDocument

    def set_extra_driver_options(self, options) -> None:
        options.add_argument(r"--profile-directory=Profile 2")

    def extract(self, link: str, **kwargs) -> None:
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Article already exists in the database: {link}")

            return

        logger.info(f"Starting scrapping Medium article: {link}")

        self.driver.get(link) # navigate to the article page
        self.scroll_page() # scroll through the article to load all the content

        soup = BeautifulSoup(self.driver.page_source, "html.parser") # parse the HTML content of the article
        title = soup.find_all("h1", class_="pw-post-title") # find the title of the article
        subtitle = soup.find_all("h2", class_="pw-subtitle-paragraph") # find the subtitle of the article

        data = {
            "Title": title[0].string if title else None, # get the text of the title
            "Subtitle": subtitle[0].string if subtitle else None, # get the text of the subtitle
            "Content": soup.get_text(), # get the text of the content of the article
        }

        self.driver.close() # close the browser

        user = kwargs["user"]
        instance = self.model( # create a new instance of the article document model and save it to the database
            platform="medium",
            content=data,
            link=link,
            author_id=user.id,
            author_full_name=user.full_name,
        )
        instance.save()

        logger.info(f"Successfully scraped and saved article: {link}")
