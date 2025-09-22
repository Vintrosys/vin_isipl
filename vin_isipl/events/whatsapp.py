import requests
import frappe
import json

def send_whynoo_template(to_number, template_name, parameters, language="en_US"):
    """
    Send WhatsApp template message via WhyNoo
    Reads credentials from WhyNoo Settings DocType
    """

    settings = frappe.get_single("Whynoo Settings")

    api_url = f"{settings.url}/{settings.vendoruid}/contact/send-template-message"
    token = settings.get_password("token")

    headers = {
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    payload = {
        "phone_number": str(to_number),
        "template_name": template_name,
        "template_language": language,
    }
    
    for idx, value in enumerate(parameters, start=1):
        payload[f"field_{idx}"] = value

    response = requests.post(f"{api_url}?token={token}", json=payload, headers=headers)
    if not response.ok:
        frappe.log_error(
            title="WhyNoo API Error",
            message=f"Payload: {json.dumps(payload, indent=2)}\n\nResponse: {response.text}"
        )

    response.raise_for_status()
    return response.json()
