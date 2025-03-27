import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from xero_auth.helper import get_xero_tenant



class FetchChartOfAccounts(APIView):
    def get(self, request):
        access_token, tenant_id = get_xero_tenant()
        if not access_token or not tenant_id:
            return Response({"error": "Failed to authenticate with Xero"}, status=401)

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Xero-Tenant-Id": tenant_id,
            "Accept": "application/json"
        }
        url = "https://api.xero.com/api.xro/2.0/Accounts"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return Response({"error": "Failed to fetch accounts", "details": response.json()}, status=response.status_code)

        accounts = response.json().get("Accounts", [])
        print(accounts)
        # for account in accounts:
        #     XeroAccount.objects.update_or_create(
        #         account_id=account["AccountID"],
        #         defaults={
        #             "name": account["Name"],
        #             "type": account["Type"],
        #             "status": account["Status"],
        #             "description": account.get("Description", ""),
        #             "tax_type": account.get("TaxType", ""),
        #         },
        #     )

        return Response({"message": "Chart of Accounts updated successfully", "total_accounts": len(accounts)})
