import requests


def set_customer_details(
        customername,
        parentid,
        zip_postalcode=None,
        street1=None,
        street2=None,
        city=None,
        state_province=None,
        telephone=None,
        country=None,
        externalid=None,
        firstname=None,
        lastname=None,
        title=None,
        department=None,
        contact_telephone=None,
        ext=None,
        email=None,
        licensetype="Professional"
):
    """
    From the N-central JavaDoc
    settings - A list of settings stored in a List of EiKeyValue objects. Below is a list of the acceptable keys and values.

    Mandatory (Key) customername - (Value) Desired name for the new customer or site. Maximum of 120 characters.
    Mandatory (Key) parentid - (Value) the (customer) id of the parent service organization or parent customer for the new customer/site.
    (Key) zip/postalcode - (Value) Customer's zip/ postal code.
    (Key) street1 - (Value) Address line 1 for the customer. Maximum of 100 characters.
    (Key) street2 - (Value) Address line 2 for the customer. Maximum of 100 characters.
    (Key) city - (Value) Customer's city.
    (Key) state/province - (Value) Customer's state/ province.
    (Key) telephone - (Value) Phone number of the customer.
    (Key) country - (Value) Customer's country. Two character country code, see http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 for a list of country codes.
    (Key) externalid - (Value) An external reference id.
    (Key) firstname - (Value) Customer contact's first name.
    (Key) lastname - (Value) Customer contact's last name.
    (Key) title - (Value) Customer contact's title.
    (Key) department - (Value) Customer contact's department.
    (Key) contact_telephone - (Value) Customer contact's telephone number.
    (Key) ext - (Value) Customer contact's telephone extension.
    (Key) email - (Value) Customer contact's email. Maximum of 100 characters.
    (Key) licensetype - (Value) The default license type of new devices for the customer. Must be "Professional" or "Essential". Default is "Essential".
    """

    settings = {
        'customername': customername,
        'parentid': parentid,
        'zip/postalcode': zip_postalcode,
        'street1': street1,
        'street2': street2,
        'city': city,
        'state/province': state_province,
        'telephone': telephone,
        'country': country,
        'externalid': externalid,
        'firstname': firstname,
        'lastname': lastname,
        'title': title,
        'department': department,
        'contact_telephone': contact_telephone,
        'ext': ext,
        'email': email,
        'licensetype': licensetype
    }
    settings_string = ''
    for setting, setting_value in settings.items():
        if setting_value:
            settings_string += f'<ei2:settings>\n<ei2:key>{setting}</ei2:key>\n<ei2:value>{setting_value}</ei2:value>\n</ei2:settings>\n'

    return settings_string


def create_body(user, password, settings_string):
    return f"""
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:ei2="http://ei2.nobj.nable.com/">
<soap:Header/>
<soap:Body>
<ei2:customerAdd>
<ei2:username>{user}</ei2:username>
<ei2:password>{password}</ei2:password>
{settings_string}
</ei2:customerAdd>
</soap:Body>
</soap:Envelope>
"""


if __name__ == '__main__':
    # add your username
    username = 'YOUR USERNAME'

    # add your JWT
    jwt = 'YOUR JWT'

    # add the uri for your N-central server
    nc_uri = 'YOUR SERVER FQDN'
    headers = {'content-type': 'text/xml'}

    customer_details = set_customer_details('New Customer', '50')
    body = create_body(username, jwt, customer_details)
    response = requests.post(url=f'{nc_uri}/dms2/services2/ServerEI2', headers=headers, data=body)
    xml_response = response.content
    print(xml_response)
