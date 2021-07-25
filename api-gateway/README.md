# DNSTool-Middleware-API

## DNSTool-Middleware-API[API-Gateway]

API-Gateway of DNSTool-Middleware-API handles the communications between the front-end and the Ray-Core.

### Environment Variables

```dotenv
FLASK_ENV=development
FIREBASE_DATABASE_URL="https://<firebase-project-id>.firebaseio.com"
FIREBASE_JSON="<firebase>.json"
GCS_JSON="<gcs>.json"
GCS_BUCKET_NAME="<storage-name>"
FIREBASE_API_KEY="<firebase-api-key>"
MAIL_SERVER="smtp.gmail.com"
MAIL_PORT=465
MAIL_USERNAME="<username>@gmail.com"
MAIL_PASSWORD="<password>"
MAIL_DEFAULT_SENDER="<username>@gmail.com"
GOOGLE_RECAPTCHA_SITE_KEY="<site-key>"
GOOGLE_RECAPTCHA_SECRET_KEY="<secret-key>"
```

### Service Account JSON file

To download requested resources, the user needs to provide a service account to the CLI. The following is the structure
of the service account.

File name: `service_account_<scan_id>.json`

Example: `service_account_1625850846648708.json`

Service Account JSON file

```json
{
  "type": "Type of the service account, defaults to 'service_account'",
  "project_id": "Project name, defaults to 'DNS-Tool'",
  "private_key_id": "16 bytes key hashed using SHA256 (Used to uniquely identify the service account JSON file)",
  "private_key": "2048 bit RSA key in PEM encoded format",
  "client_email": "Email address of the user",
  "client_id": "Firebase UID of the user",
  "scan_id": "Scan ID",
  "scans": [
    {
      "region": "GCP Region",
      "zone": "Domain Zone"
    }
  ]
}
```

Example: (The private key mentioned here is for reference purposes only)

```json
{
  "type": "service_account",
  "project_id": "DNS-TOOL",
  "private_key_id": "7be3f442d97c6b63b291dce7e4103bdde97ae00c4b42c2ad6f6c45d9dcdf04bc",
  "private_key": "-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCs8Nyfb/MYGzz/\nxCI6hqd18r7f9bi+z5eOdRODmm7yKL7OJDLToXUTNaNJjQiGxkPFVgRVXXce3hDO\nHaMlz0FlAc2pVzEohnb6t+joYGIhogXtgQ21lW6smvBoQT5idJISL2YBIInpy4z2\nxaSioVvTuWuTQy6VT1UILr9ZnUcHGUrBFyx3e/i1EYmWXMgxFTGzJL3qnmGRuK4T\nsHXFCZ0RaciOVopOi9mL5kDJHiLL4Ncc9C+MJ4RzyHKwCcJMBRXBkMIGO2Salunq\nop/yYl6dhFfeDZLIU4qE5+ZL4Ce0y+SQKAeFyKkh581glI5XVxoh47pT+vvHsWzL\no7u+mujhAgMBAAECggEAA0NOHlH557AH4Bl+vdTxjuekE0yrDiqThPQPiLGeu0Hq\ni7AiJ10J/PFLoeUfzo8qEyySy1uGllYBQipL/DgjVzkH/NRw0H9s+kEDC3NaFqFc\ndEU1kYH+wxHvTEBC4Y+qe95aEdZf08Hr6HIFL65UsbNzZKVlWRrUk2FyacnuX6Ni\nFFhIPnt+jpgkNx78oq1p+sVph08pgKQkD4RfU4kLuX2Nl0hhnN2oYnBVd6qhNO8g\n/nkYoH7N/jYinxYzQDPKKm/7CAlJcbMJ/29z7fox1BQ6/1zfH8Lpz4NmyBoxQz+T\nhg73qDQmnuC8pFMnFT6UV1sR/AMcC217PrpMybEcYQKBgQDLMyeBE618uoCn7P0e\n7puW2vQFNqG8xqOSbS1haVzLsUBmmb5F/ezLUS8MtHXH81CYSG4/3y+cN5SvqUOw\nOjGKVLb37eCs8ujTwSjxatnDzPGVHHZ5ZgFszpQdgVBzevhkl2QMf2ty2ufMfta5\n46nEBJOQ9GB8VAztGfgTtdMD6QKBgQDZ4OH8mMIoUWBe97HnpaKQw9HWQ2xg7Rw1\nf0rm1EzNibfo+hZFF4biUVdC/LmQqX8uCgX3oKn15W10uI0Q2PyQqFfhfJjvjrxU\ny7K/hVWBz2wh+TTdAWuRC+SLggAnCiNBhcJHl74+qAaf32c0VLELmE+S11q4EYCK\n1KZ6LXJ6OQKBgQCSmxHBeyUMfLMedUoa6ySursKokEYZIWga2VKImbAt9nD0lbBG\nZ3JVLvm3POxNmytm87s3shtzplZMdt8zYokjuQNZ1fLoVUnOneqgY+tB7bfPUX3Z\nENOuYU1UDFyzNOHKEcBJlBU+BNqBHHJoI+30Uyj0yJxkl2/MEZR/BAx/IQKBgEuN\nhhAX0Mw2W9rSveh8MYFNxkgsnTqHPo72kzy0ReXIafPqNSrEW8vDNSVPifG2NRn7\n89HI7ucMJgahsJk1BXAMUF0q3cXEk148PMHZNKuNCAxH5KL2yRxFKX2PGQpwo4Un\nIxW8cwY7MgDicWFeNP62VHGxKA5IU3DRCOG5PMdRAoGAEk3CI7E8UC6swFQ4pdB7\nL28xAccUQSiuTWnG0ssmcS0S07pe0HOu9To9tosMMBqTpd2IsxJRHcVmLkeu5zdr\nkNA4Rk/BfOIxXmdbd/lBRkTnQF6fY73Pgpx7dQgR55QCvVoiWG5i/glVy9l053ZJ\n5wrrzEkTzoDvIScf2ppcnmo=\n-----END ENCRYPTED PRIVATE KEY-----",
  "client_email": "email@domain.tld",
  "client_id": "UchQlgJb9ibBoV991fqtQ5ykfHz2",
  "scan_id": "1625850846648708",
  "scans": [
    {
      "region": "us-east1-c",
      "zone": ".com"
    },
    {
      "region": "us-east1-b",
      "zone": ".com"
    }
  ]
}
```
