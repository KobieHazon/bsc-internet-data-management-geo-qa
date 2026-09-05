import rdflib
from rdflib import XSD, Literal
import requests
import sys
import lxml.html
import re

infobox_prefix = "//table[contains(@class,'infobox')]/tbody"
wiki_dom = "https://en.wikipedia.org/"
population_relation = rdflib.URIRef(wiki_dom + "population")
area_relation = rdflib.URIRef(wiki_dom + "area")
capital_relation = rdflib.URIRef(wiki_dom + "capital")
government_relation = rdflib.URIRef(wiki_dom + "government")
president_relation = rdflib.URIRef(wiki_dom + "president")
pm_relation = rdflib.URIRef(wiki_dom + "prime_minister")
born_relation = rdflib.URIRef(wiki_dom + "born")
g = rdflib.Graph()

# ~~~~~~~~~~~~Ontology Creation Functions~~~~~~~~~~~~~~~


def ascii_text(value):
    """Return ASCII-safe text without changing the value to bytes."""
    return value.encode('ascii', 'ignore').decode('ascii')


def get_bday_entity(url):
    person_page = requests.get(url)
    person_html = lxml.html.fromstring(person_page.content)
    bday_xpath = person_html.xpath(
        infobox_prefix + "//*[@class = 'bday']/text()")
    if bday_xpath:
        bday_entity = Literal(bday_xpath[0], datatype=XSD.date)
        return bday_entity
    return None


def process_country(url):
    country_page = requests.get(wiki_dom + url)
    country_html = lxml.html.fromstring(country_page.content)

    # ~~~~~~~~~~~GET COUNTRY NAME~~~~~~~~~~~~~~~~
    name_xpath = country_html.xpath("//h1[./@id = 'firstHeading']//text()")
    if not name_xpath:
        return
    name = name_xpath[0]
    country_entity = rdflib.URIRef(
        wiki_dom + ascii_text(name).replace(" ", "_").lower())

    # ~~~~~~~~~~~GET COUNTRY POPULATION~~~~~~~~~~~~~~~~
    population_xpath = country_html.xpath(
        infobox_prefix + "//tr[./th[contains(.//text(), 'Population')]]/following-sibling::*[1]/td//text()")
    if population_xpath:
        population_xpath = [
            item for item in population_xpath if item.strip() != ""]
        country_population = population_xpath[0].strip().split(" ")[0]
        population_entity = Literal(country_population)
        g.add((country_entity, population_relation, population_entity))

    # ~~~~~~~~~~~GET COUNTRY AREA~~~~~~~~~~~~~~~~
    area_xpath = country_html.xpath(
        infobox_prefix + "//tr[./th[normalize-space(.//text()) = 'Area']]/td//text()")
    if not area_xpath:
        area_xpath = country_html.xpath(
            infobox_prefix + "//tr[./th[normalize-space(.//text()) = 'Area']]/following-sibling::*[1]/td//text()")
    if area_xpath:
        area_xpath = [item for item in area_xpath if item.strip() != ""]
        country_area = area_xpath[0].strip()
        if ("mi" in country_area):
            country_area = country_area[country_area.find("mi") + 4:]
        if ("km" not in country_area):
            country_area += "_km2"
        else:
            country_area = country_area.split()[0] + "_km2"
        area_entity = Literal(country_area)
        g.add((country_entity, area_relation, area_entity))

    # ~~~~~~~~~~~GET COUNTRY CAPITAL~~~~~~~~~~~~~~~~
    capital_xpath = country_html.xpath(
        "//table[contains(@class,'infobox')]/tbody//tr[./th[contains(.//text(), 'Capital')]]/td//text()")
    if capital_xpath:
        capital_xpath = [ascii_text(item.strip())
                         for item in capital_xpath if item.strip() != ""]
        country_capital = capital_xpath[0]
        if (country_capital == "None"):
            capital_xpath = [
                item for item in capital_xpath if re.match("^[a-zA-Z]*$", item)]
            if (len(capital_xpath) > 1):
                country_capital = capital_xpath[1]
    else:
        country_capital = "None"
    capital_entity = Literal(country_capital.replace(" ", "_").lower())
    g.add((country_entity, capital_relation, capital_entity))

    # ~~~~~~~~~~~GET COUNTRY GOVERNMENT~~~~~~~~~~~~~~~~
    government_xpath = country_html.xpath(
        "//table[contains(@class,'infobox')]/tbody//tr[./th[contains(.//text(), 'Government')]]/td//text()")
    if government_xpath:
        government_xpath = [ascii_text(item.strip()).replace(" ", "_")
                            for item in government_xpath if ("[" not in item) and item.strip() != ""]
        country_government = "_".join(government_xpath).lower()
        government_entity = Literal(country_government)
        g.add((country_entity, government_relation, government_entity))

    # ~~~~~~~~~~~GET COUNTRY PRESIDENT AND BDAY~~~~~~~~~~~~~~~~
    president_xpath = country_html.xpath(
        "//table[contains(@class,'infobox')]/tbody//tr[./th[.//text() = 'President']]/td//text()")
    if president_xpath:
        president_xpath = [ascii_text(item.strip())
                           for item in president_xpath if item.strip() != ""]
        country_president = president_xpath[0].replace(" ", "_").lower()
        president_url = wiki_dom + country_html.xpath(
            "//table[contains(@class,'infobox')]/tbody//tr[./th[.//text() = 'President']]/td//@href")[0]
        bday_entity = get_bday_entity(president_url)
        president_entity = rdflib.URIRef(wiki_dom + country_president)
        if (bday_entity != None):
            g.add((president_entity, born_relation, bday_entity))
        g.add((country_entity, president_relation, president_entity))

    # ~~~~~~~~~~~GET COUNTRY PM AND BDAY~~~~~~~~~~~~~~~~
    pm_xpath = country_html.xpath(
        "//table[contains(@class,'infobox')]/tbody//tr[./th[.//text() = 'Prime Minister']]/td//text()")
    if pm_xpath:
        pm_xpath = [ascii_text(item.strip())
                    for item in pm_xpath if item.strip() != ""]
        country_pm = pm_xpath[0].replace(" ", "_").lower()
        pm_url = wiki_dom + country_html.xpath(
            "//table[contains(@class,'infobox')]/tbody//tr[./th[.//text() = 'Prime Minister']]/td//@href")[0]
        pm_entity = rdflib.URIRef(wiki_dom + country_pm)
        bday_entity = get_bday_entity(pm_url)
        if (bday_entity != None):
            g.add((pm_entity, born_relation, bday_entity))
        g.add((country_entity, pm_relation, pm_entity))


def process_country_list(url):
    countries_page = requests.get(url)
    countries_html = lxml.html.fromstring(countries_page.content)
    countries_urls = countries_html.xpath(
        "//table[./caption[contains(./b/text(), \"Countries\")]]/tbody//table[./@id = \"main\"]//span[./@class = 'flagicon']/following-sibling::a[1]/@href")
    for url in countries_urls:
        process_country(url)

# ~~~~~~~~~~~~~Question Answering Functions~~~~~~~~~~~~~


def country_query(type, country):
    query = "select ?entity where { <" + wiki_dom + \
        country + "> <" + wiki_dom + type + "> ?entity}"
    ans = list(g.query(query))
    if not ans:
        return "None"
    if type != "prime_minister" and type != "president":
        if type == "capital" and ans[0]['entity'].toPython() == "none":
            return "None"  # Should it print None?
        return ans[0]['entity'].toPython()
    else:
        return ans[0]['entity'].toPython()[len(wiki_dom):]


def born_query(type, country):
    person = country_query(type, country)
    if person == "None":
        return "None"
    query = "select ?bday where { <" + wiki_dom + \
        person + "> <" + wiki_dom + "born> ?bday }"
    ans = list(g.query(query))
    return ans[0]['bday'].toPython()


def person_query(person, type):
    query = "select ?country where { ?country <" + \
        wiki_dom + type + "> <" + wiki_dom + person + "> }"
    ret_str = ""
    ans = list(g.query(query))
    if ans:
        ret_str += type.replace("_", " ").capitalize() + " of "
        for res in ans:
            ret_str += res['country'].toPython().replace("_",
                                                         " ")[len(wiki_dom):] + ", "
        ret_str = ret_str[:-2]
        return ret_str
    else:
        return "None"


def answer_question(ques):
    g.parse("ontology.nt", format="nt")
    ques_words = ques.split(" of ", 1)

    if len(ques_words) == 2:
        type_with_the = ques_words[0].split(" the ", 1)
        if len(type_with_the) < 2:
            print("None")
            return
        else:
            type = type_with_the[1].replace(" ", "_")
        if "born" not in ques_words[1]:
            country = ques_words[1][:-1].replace(" ", "_")
            print(country_query(type, country).replace("_", " "))
        else:
            country = ques_words[1][:-len(" born?")].replace(" ", "_")
            print(born_query(type, country))
    else:
        person_with_is = ques_words[0][:-1].split(" is ", 1)
        if len(person_with_is) < 2:
            print("None")
            return
        else:
            person = person_with_is[1].replace(" ", "_")
        pm_str = person_query(person, "prime_minister")
        president_str = person_query(person, "president")
        if pm_str != "None" and president_str != "None":
            print(pm_str + ". " + president_str)
        elif pm_str == "None":
            print(president_str)
        else:
            print(pm_str)

# ~~~~~~~~~~~~~~Main Function~~~~~~~~~~~~~~~


def main():
    if (len(sys.argv) != 3):
        print("Error: Incorrect parameters.")
        exit(1)

    if (sys.argv[1] == "create"):
        process_country_list(
            "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)")
        g.serialize(sys.argv[2], format=sys.argv[2].split(".")[1])

    elif (sys.argv[1] == "question"):
        answer_question(sys.argv[2].lower())


if __name__ == "__main__":
    main()
