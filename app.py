import urllib.request
import time

def snake_case(x: str):
    return x.replace(" ", "_").lower()

def new_request(url: str) -> urllib.request.Request:
    USER_AGENT = "Endorsement Lister by mrfylke https://github.com/mrfylke2001/endorsement_lister/"

    request = urllib.request.Request(
        url,
        data=None,
        headers={
            "User-Agent": USER_AGENT
        }
    )
    return request

def xml_tag_content(xml: str, tag: str) -> str:
    tag_contents = xml.split(f"<{tag}>")[1].split(f"</{tag}>")[0]
    return tag_contents

def xml_tag_content_list(xml: str, tag: str, delimiter=",") -> list:
    tag_contents = xml_tag_content(xml, tag)
    contents_list = tag_contents.split(delimiter)
    return contents_list

def ns_api_url(target_query: str, data_queries: list) -> str:
    BASE_URL = "https://www.nationstates.net/cgi-bin/api.cgi"

    data_query_str = "q=" + "+".join(data_queries)
    url = f"{BASE_URL}?{target_query}&{data_query_str}"
    return url

def ns_nation_api_url(nation: str, data_queries: list) -> str:
    target_query = f"nation={nation}"
    return ns_api_url(target_query, data_queries)

def ns_region_api_url(region: str, data_queries: list) -> str:
    target_query = f"region={region}"
    return ns_api_url(target_query, data_queries)

def is_wa_member(api_xml_data: str) -> bool:
    wa_status = xml_tag_content(api_xml_data, "UNSTATUS")
    wa_bool = wa_status != "Non-member"
    return wa_bool

if __name__ == "__main__":
    user_nation = snake_case(input("Enter your nation: "))

    n_request_url = ns_nation_api_url(user_nation, ["region", "endorsements"])
    n_request = new_request(n_request_url)
    n_xml_data = str(urllib.request.urlopen(n_request).read())
    n_endorsed_by = xml_tag_content_list(n_xml_data, "ENDORSEMENTS")

    region = snake_case(xml_tag_content(n_xml_data, "REGION"))
    print(f"Got region: {region}")

    r_request_url = ns_region_api_url(region, ["nations"])
    r_request = new_request(r_request_url)
    r_xml_data = str(urllib.request.urlopen(r_request).read())
    r_nations = xml_tag_content_list(r_xml_data, "NATIONS", delimiter=":")

    wa_members = []
    unendorsed = []

    for nation in r_nations:
        print(f"Examining: {nation}")
        request_url = ns_nation_api_url(nation, ["wa", "endorsements"])
        request = new_request(request_url)
        xml_data = str(urllib.request.urlopen(request).read())

        if is_wa_member(xml_data):
            print(f"  {nation} is a WA member.")
            wa_members.append(nation)

            endorsed_by = xml_tag_content_list(xml_data, "ENDORSEMENTS")
            if user_nation not in endorsed_by:
                print(f"  {user_nation} has not endorsed {nation}.")
                unendorsed.append(nation)

        time.sleep(0.7)

    results = "<!DOCTYPE html><html><body><p>You have not endorsed:</p><ol>"

    for x in unendorsed:
        results += f"<li><a href='https://nationstates.net/nation={x}' target='_blank'>{x}</a></li>"
    results += "</ol><p>You have not been endorsed by:</p><ol>"

    for x in wa_members:
        if x not in n_endorsed_by:
            results += f"<li><a href='https://nationstates.net/nation={x}' target='_blank'>{x}</a></li>"
    results += "</ol></body></html>"

    with open("results.html", "w") as file:
        file.write(results)

    print("================")
    print("Complete")