from .client import ZengaPayAPI
from .utils import validate_number, validate_phone_number, validate_string


class Accounts(ZengaPayAPI):
    def get_account_balance(self):
        url = f"{self.config.base_url}/account/balance"
        res = self.request("GET", url)

        return res.json()

    def get_account_statement(self, url=None, limit=0, **kwargs):
        designations = ["TRANSACTION", "CHARGES"]
        currency_codes = ["UGX-MTNMM", "UGX-WARIDMM"]
        status = ["FAILED", "PENDING", "INDETERMINATE", "SUCCEEDED"]
        if url is None:
            url = f"{self.config.base_url}/account/statement?limit={validate_number(limit)}"
        if (
            "designation" in kwargs
            and kwargs.get("designation").upper() in designations
        ):
            url += f"&designation={kwargs.get('designation')}"
        if (
            "currency_code" in kwargs
            and kwargs.get("currency_code").upper() in currency_codes
        ):
            url += f"&currency_code={kwargs.get('currency_code')}"
        if "status" in kwargs and kwargs.get("status").upper() in status:
            url += f"&status={kwargs.get('status')}"
        if "start" in kwargs:
            url += f"&start={kwargs.get('start')}"
        if "end" in kwargs:
            url += f"&end={kwargs.get('end')}"
        res = self.request("GET", url)

        return res.json()
