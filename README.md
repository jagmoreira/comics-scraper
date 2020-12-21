# Comics Scraper

Scrapy crawler to get information about upcoming comic book releases using data from [Comic List](http://www.comiclist.com/index.php).

**Remember to scrape responsibly!**

## Using the scraper

1. Create a python 3.6+ using pyenv/virtualenv/anaconda/etc.
1. Install Scrapy from the `requirements.txt`:

        $ pip install -r requirements.txt

1. Rename the user settings template:

        $ cp comics/user_settings.template comics/user_settings.py

1. Edit the `user_settings.py` file according to your needs:

        # Crawl responsibly by identifying yourself (and your website) on the user-agent
        USER_AGENT = '<Your Name> comics scraper'

        # Titles to include from all companies.
        # Will include all comics with partial match except those matching the EXCLUDE
        # matches below
        INCLUDE = ('Iron Man', 'Avengers' , 'Batman')

        # Comics to exclude (words from included titles)
        # In this case comics like 'Uncanny Avengers' or 'Batman Beyond' will be excluded
        EXCLUDE = ('Uncanny', 'Beyond')

        # Comic book companies to include
        # You include the companies of ALL comics you want to parse, otherwise
        # the crawler won't be able to find them.
        COMPANIES = ('marvel-comics', 'dc-comics')

1. Run the crawler:

        $ scrapy crawl comics

1. Output is saved to a file called `final_data.txt`:

        ****************
        March:
            03/13/2019
            -Batman Who Laughs The Grim Knight #1 (3 covers)
            -Avengers No Road Home #1 (1 covers)
            -Avengers No Road Home #5 (2 covers)
            -Tony Stark Iron Man #9 (3 covers)

            03/20/2019
            -Batman #67 (2 covers)
            -Avengers #17 (2 covers)
            -Avengers No Road Home #6 (5 covers)
            -West Coast Avengers #9 (1 covers)

            03/27/2019
            -Avengers No Road Home #7 (2 covers)

        ****************
        April:
            04/03/2019
            -Batman #68 (2 covers)
            -Avengers No Road Home #2 (1 covers)
            -Avengers No Road Home #3 (1 covers)
            -Avengers No Road Home #8 (2 covers)
            -True Believers Avengers Nebula #1 (1 covers)
            -True Believers Avengers Thanos Vs The Marvel Universe#1 (1 covers)

        (...)
