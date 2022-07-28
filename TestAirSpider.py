from urllib import response
import feapder
from feapder.network.selector import Selector


class AirSpiderTest(feapder.AirSpider):
    def start_requests(self):
        yield feapder.Request("http://quotes.toscrape.com/")

    def parse(self, request, response :response):
        # selector = Selector(response.text)
        title =response.css(".quote .text::attr(textContent)").extract_first()
        author = response.css(".quote  small").extract_first()
       
        print(title,author)


if __name__ == "__main__":
    AirSpiderTest().start()
