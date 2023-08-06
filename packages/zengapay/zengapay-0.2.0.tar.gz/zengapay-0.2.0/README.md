# ZengaPay API Python Client
### Power your apps with our ZengaPay API

This is the ZENGAPAY Python Client Library

# Usage
## Installation
Add the latest version of the library to your project by using pip:

```
$ pip install zengapay
```

This library supports Python 3.6+

# Sandbox and Production Environment
## Creating a sandbox environment user environment
Before using the library in your applications, please head over to the [API Documentation](https://developers.zengapay.com/#getting-started) to see how to set up your sandbox environment.

The following is the API Endpoint for our sandbox environment:

```
https://api.sandbox.zengapay.com/v1
```

Here is the API Endpoint for our production environment:

```
https://api.zengapay.com/v1
```

## Configuration
Before we can fully utilize the library, we need to specify the global configurations. The global configuration must contain the following.

- `ZENGAPAY_APP_SETTINGS`: Optional environment, either "sandbox" or "production". Default is "sandbox".
- `ZENGAPAY_BASE_URL`: An optional base url to ZengaPay API. By default the sandbox base url will be used.
- `ZENGAPAY_USER_API_TOKEN`: Your secret user API token. This is mandatory. See he [API Documentation](https://developers.zengapay.com/#getting-started) to obtain your API token.

Once you have specified the global config variables, the full configuration object to use in your project should look like this.

```python
config = {
    ZENGAPAY_ENVIRONMENT: os.environ.get("ZENGAPAY_APP_SETTINGS", "sandbox"),
    ZENGAPAY_BASE_URL: os.environ.get("ZENGAPAY_BASE_URL", "https://api.sandbox.zengapay.com/v1"),
    ZENGAPAY_USER_API_TOKEN: os.environ.get("ZENGAPAY_USER_API_TOKEN")
}
```

This will be need for each transaction you will be performing.

## Collections.
The collections client can be created with configuration parameters as indicated above.

```python
import os
from zengapay import Collections


config = {
    ZENGAPAY_ENVIRONMENT: os.environ.get("ZENGAPAY_APP_SETTINGS", "sandbox"),
    ZENGAPAY_BASE_URL: os.environ.get("ZENGAPAY_BASE_URL", "https://api.sandbox.zengapay.com/v1"),
    ZENGAPAY_USER_API_TOKEN: os.environ.get("ZENGAPAY_USER_API_TOKEN")
}

client = Collections(config)
```

### Methods
1. **collect**: This operation is used to request a payment from another consumer(Payer). The payer will be asked to authorize the payment. The transaction is executed once the payer has authorized the payment. The transaction will be in status PENDING until it is authorized or declined by the payer or it is timed out by the system. Status of the transaction can be validated by using `get_collection(transaction_ref)` or `get_transaction_status(transaction_ref)` using the `transaction reference`.

You can perform a collection using the payload as below. See he [API Documentation](https://developers.zengapay.com/#collections) to get what the parameters mean.

```python
payload = {
    "msisdn": "256703######",  # The phone number that the collection request is intended for.
    "amount": 20000,  #The collection request amount.
    "external_reference": "157899393020236",  # Internal description or reason for this collection request and must be unique for every request. 
    "narration":"Clearing Invoice - #157899393020236"  # Textual narrative describing the transaction. 
}

collection = client.collect(payload)
```

2. **get_collections**: Retrieve the collection transactions for a given account.

```python
collections = client.get_collections()
```

3. **get_collection**: Retrieve a certain collection transaction using the `transaction reference`

```python
collection = client.get_collection(transaction_ref)
```

4. **get_transaction_status**: The status of the transaction, this can be one of these; `PENDING`,`SUCCEEDED`,`FAILED`,`INDETERMINATE`

```python
trans_status = client.get_transaction_status(transaction_ref)
```

## Transfers.
The transfers client can be created with configuration parameters as indicated above.

```python
import os
from zengapay import Transfers


config = {
    ZENGAPAY_ENVIRONMENT: os.environ.get("ZENGAPAY_APP_SETTINGS", "sandbox"),
    ZENGAPAY_BASE_URL: os.environ.get("ZENGAPAY_BASE_URL", "https://api.sandbox.zengapay.com/v1"),
    ZENGAPAY_USER_API_TOKEN: os.environ.get("ZENGAPAY_USER_API_TOKEN")
}

client = Transfers(config)
```

### Methods
1. **transfer**: Used to transfer an amount from the owner’s account to a payee account. Status of the transaction can be validated by using `get_transfer(transaction_ref)` or `get_transaction_status(transaction_ref)` using the `transaction reference`.

You can perform a transfer using the payload as below. See he [API Documentation](https://developers.zengapay.com/#transfers) to get what the parameters mean.

```python
payload = {
    "msisdn": "256703######",  # The phone number that the transfer request is intended for.
    "amount": 20000,  #The transfer request amount.
    "external_reference": "157899393020236",  # Internal description or reason for this transfer request and must be unique for every request. 
    "narration":"Clearing Invoice - #157899393020236"  # Textual narrative describing the transaction. 
}

transfer = client.transfer(payload)
```

2. **get_transfers**: Retrieve the transfer transactions for a given account.

```python
transfers = client.get_transfers()
```

3. **get_transfer**: Retrieve a certain tranfer transaction using the `transaction reference`

```python
transfer = client.get_transfer(transaction_ref)
```

4. **get_transaction_status**: The status of the transaction, this can be one of these; `PENDING`,`SUCCEEDED`,`FAILED`,`INDETERMINATE`

```python
trans_status = client.get_transaction_status(transaction_ref)
```

## Account
The account client can be created with configuration parameters as indicated above.

```python
import os
from zengapay import Accounts


config = {
    ZENGAPAY_ENVIRONMENT: os.environ.get("ZENGAPAY_APP_SETTINGS", "sandbox"),
    ZENGAPAY_BASE_URL: os.environ.get("ZENGAPAY_BASE_URL", "https://api.sandbox.zengapay.com/v1"),
    ZENGAPAY_USER_API_TOKEN: os.environ.get("ZENGAPAY_USER_API_TOKEN")
}

client = Accounts(config)
```

See the [API Documentation](https://developers.zengapay.com/#account).

### Methods
1. **get_balance**: This API allows you to get the current merchant account balance.

```python
balance = client.get_balance()
```

2. **get_account_statement**: To retrieve a list of all transactions on your account (account statement). This will return a list of transactions. See [API Documentation](https://developers.zengapay.com/#account-statement) to see how to make filters.

```python
statement = client.get_account_statement()
```

Performing a limit and status filters. See link above for more filters

```python
statement = client.get_account_statement(limit=2, status='FAILED')
```
