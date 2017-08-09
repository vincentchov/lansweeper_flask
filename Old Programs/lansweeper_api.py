import requests, json

api_key = "5844fcc1-4e0d-4565-af6c-e43e733d00bf"

get_ticket_base_url = "http://psi-sql:81/api.aspx?Action=GetTicket&Key={}&TicketID={}"

ticket_id = str(input("What ticket id do you want to search for? "))

url = get_ticket_base_url.format(api_key, ticket_id)

r = requests.get(url)

json_response = json.loads(r.text)

print(json.dumps(json_response, indent=4, sort_keys=True))
