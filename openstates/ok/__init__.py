from pupa.scrape import Jurisdiction, Organization
from .people import OKPersonScraper
from .committees import OKCommitteeScraper
# from .events import OKEventScraper
from .bills import OKBillScraper


class Oklahoma(Jurisdiction):
    division_id = "ocd-division/country:us/state:ok"
    classification = "government"
    name = "Oklahoma"
    url = "http://www.oklegislature.gov/"
    scrapers = {
        'people': OKPersonScraper,
        'committees': OKCommitteeScraper,
        # 'events': OKEventScraper,
        'bills': OKBillScraper,
    }
    # Sessions are named on OK's website as "{odd year} regular session" until the even year,
    # when all data rolls over. For example, even year sessions include all odd-year-session bills.
    # We have opted to name sessions {odd-even} Regular Session and treat them as such.
    # - If adding a new odd-year session, add a new entry and copy the biennium pattern as above
    # - If adding an even-year session, all you'll need to do is:
    #   - update the `_scraped_name`
    #   - update the session slug in the Bill scraper
    #   - ignore the odd-year session
    legislative_sessions = [
        {
            "_scraped_name": "2012 Regular Session",
            "identifier": "2011-2012",
            "name": "2011-2012 Regular Session"
        },
        {
            "_scraped_name": "2012 Special Session",
            "identifier": "2012SS1",
            "name": "2012 Special Session"
        },
        {
            "_scraped_name": "2014 Regular Session",
            "identifier": "2013-2014",
            "name": "2013-2014 Regular Session"
        },
        {
            "_scraped_name": "2013 Special Session",
            "identifier": "2013SS1",
            "name": "2013 Special Session"
        },
        {
            "_scraped_name": "2016 Regular Session",
            "identifier": "2015-2016",
            "name": "2015-2016 Regular Session"
        },
        {
            "_scraped_name": "2017 First Special Session",
            "identifier": "2017SS1",
            "name": "2017 First Special Session"
        },
        {
            "_scraped_name": "2017 Second Special Session",
            "identifier": "2017SS2",
            "name": "2017 Second Special Session"
        },
        {
            "_scraped_name": "2018 Regular Session",
            "identifier": "2017-2018",
            "name": "2017-2018 Regular Session",
            "start_date": "2017-02-06",
            "end_date": "2018-05-25",
        },
    ]
    ignored_scraped_sessions = [
        "2017 Regular Session",
        "2015 Regular Session",
        "2013 Regular Session",
        "2011 Regular Session",
        "2010 Regular Session",
        "2009 Regular Session",
        "2008 Regular Session",
        "2007 Regular Session",
        "2006 Second Special Session",
        "2006 Regular Session",
        "2005 Special Session",
        "2005 Regular Session",
        "2004 Special Session",
        "2004 Regular Session",
        "2003 Regular Session",
        "2002 Regular Session",
        "2001 Special Session",
        "2001 Regular Session",
        "2000 Regular Session",
        "1999 Special Session",
        "1999 Regular Session",
        "1998 Regular Session",
        "1997 Regular Session",
        "1996 Regular Session",
        "1995 Regular Session",
        "1994 Second Special Session",
        "1994 First Special Session",
        "1994 Regular Session",
        "1993 Regular Session"
    ]

    def get_organizations(self):
        legislature_name = "Oklahoma Legislature"
        lower_chamber_name = "House"
        lower_seats = 101
        lower_title = "Senator"
        upper_chamber_name = "Senate"
        upper_seats = 48
        upper_title = "Senator"

        legislature = Organization(name=legislature_name,
                                   classification="legislature")
        upper = Organization(upper_chamber_name, classification='upper',
                             parent_id=legislature._id)
        lower = Organization(lower_chamber_name, classification='lower',
                             parent_id=legislature._id)

        for n in range(1, upper_seats + 1):
            upper.add_post(
                label=str(n), role=upper_title,
                division_id='{}/sldu:{}'.format(self.division_id, n))
        for n in range(1, lower_seats + 1):
            lower.add_post(
                label=str(n), role=lower_title,
                division_id='{}/sldl:{}'.format(self.division_id, n))

        yield legislature
        yield upper
        yield lower

    def get_session_list(self):
        from openstates.utils import url_xpath
        sessions = url_xpath('http://webserver1.lsb.state.ok.us/WebApplication2/WebForm1.aspx',
                             "//select[@name='cbxSession']/option/text()")
        # OK Sometimes appends (Mainsys) to their session listings
        sessions = [s.replace('(Mainsys)', '').strip() for s in sessions]
        return sessions
