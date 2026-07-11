from app.ingest.refresh import diff_new, parse_rss
from app.schemas.updates import FeedItem

RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>RBI Notifications</title>
  <item>
    <title>Master Direction on Cards - Amendment 2026</title>
    <link>https://rbi.org.in/notifications/1</link>
    <guid>g1</guid>
    <pubDate>Fri, 10 Jul 2026 10:00:00 GMT</pubDate>
  </item>
  <item>
    <title>Circular on UPI limits</title>
    <link>https://rbi.org.in/notifications/2</link>
    <guid>g2</guid>
    <pubDate>Sat, 11 Jul 2026 10:00:00 GMT</pubDate>
  </item>
</channel></rss>"""


def test_parse_rss_extracts_items():
    items = parse_rss(RSS)
    assert len(items) == 2
    assert items[0].title == "Master Direction on Cards - Amendment 2026"
    assert items[0].link == "https://rbi.org.in/notifications/1"
    assert items[1].guid == "g2"


def test_parse_rss_bad_xml_is_empty():
    assert parse_rss("<not-xml") == []
    assert parse_rss("") == []


def test_diff_new_filters_known_links():
    items = parse_rss(RSS)
    new = diff_new(items, known_links={"https://rbi.org.in/notifications/1"})
    assert len(new) == 1
    assert new[0].link == "https://rbi.org.in/notifications/2"


def test_diff_new_dedupes_same_link():
    dup = [
        FeedItem(title="a", link="https://rbi.org.in/x", guid="g1"),
        FeedItem(title="b", link="https://rbi.org.in/x", guid="g2"),
    ]
    assert len(diff_new(dup, set())) == 1
