# DNSTool-Middleware-API Documentation

#### Contents

- [Overview](#1-overview)
- [Authentication](#2-authentication)
- [Resources](#3-resources)
  - [Domain Zones](#31-domain-zones)
  - [GCP Zones](#32-gcp-zones)
  - [Check Emails](#33-check-emails)
  - [Register](#34-register)
  - [Get Scans](#35-get-scans)
  - [Create Scans](#36-create-scans)
  - [Update Scans](#37-update-scans)
  - [Delete Scans](#38-delete-scans)
  - [Download Service Account](#39-get-service-account)
  - [Get Scan Results Files List](#310-get-scan-results-files-list)
  - [Download Scan Results File](#311-download-scan-results-file)

## 1. Overview

DNSTool-Middleware-API is a JSON based API. All requests must be secured with `https`.

## 2. Authentication

To access resources in DNSTool-Middleware-API, the user needs to provide a JWT bearer token as the `Authorization`
header. Certain API endpoints require a specifically minted Firebase JWT token whereas certain API endpoints require a
specially minted JWT token using a specific service account JSON file.

```bash
Authorization: Bearer <token>
```

Authorization header should be provided as mentioned above.

## 3. Resources

DNSTool-Middleware-API is a RESTFul API, and it is arranged around resources. All requests must be made with an access
token unless noted otherwise. All requests should be made using `https`.

### 3.1. Domain Zones

#### Getting the domain zones

Returns the domain zones for the provided query.

```
GET /zones/{{query}}
```

Example request:

```
GET /zones/com HTTP/1.1
Host: DNSTool
Content-Type: application/json
Accept: application/json
Accept-Charset: utf-8
```

The response is a list of matching zones within a data envelope.

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "data": [
    ".com",
    ".company"
  ]
}
```

Possible errors:

| Error code                | Description                        |
| ------------------------- | ---------------------------------- |
| 500 Internal Server Error | Internal server error has occurred |

### 3.2. GCP Zones

#### Getting the GCP zones

Returns the domain zones for the provided query.

```
GET /gcp-zones/{{query}}
```

Example request:

```
GET /gcp-zones/us-east HTTP/1.1
Host: DNSTool
Content-Type: application/json
Accept: application/json
Accept-Charset: utf-8
```

The response is a list of matching zones within a data envelope.

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "data": [
    "us-east1-b",
    "us-east1-c",
    "us-east1-d"
  ]
}
```

Possible errors:

| Error code                | Description                        |
| ------------------------- | ---------------------------------- |
| 500 Internal Server Error | Internal server error has occurred |

### 3.3. Check Emails

#### Check emails for validity

Returns a success message if the provided email is not a valid organization email.

```
POST /check-email
```

Example request:

```
POST /check-email HTTP/1.1
Host: DNSTool
Content-Type: application/json
Accept: application/json
Accept-Charset: utf-8

{
  "email": "w.nipuna@gmail.com"
}
```

The response is a success message if the email is accepted otherwise it is an error message with an HTTP 400 Bad Request.

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "message": "[{email}] is valid and accepted."
}
```

Possible errors:

| Error code                | Description                                         |
| ------------------------- | --------------------------------------------------- |
| 400 Bad Request           | Email domain is not an accepted organization domain |
| 500 Internal Server Error | Internal server error has occurred                  |

### 3.4. Register

#### Register a user

Creates a user account based on the provided user account information.

```
POST /register
```

Example request:

```
POST /register HTTP/1.1
Host: DNSTool
Content-Type: application/json
Accept: application/json
Accept-Charset: utf-8

{
  "full_name": "Nipuna Weerasekara",
  "email": "w.nipuna@gmail.com",
  "organization": "Niweera.inc",
  "profession": "Web Developer",
  "reason": "For education purposes",
  "password": "Super-secret-password",
  "g_recaptcha_response": "<Google reCAPTCHA v3 token>"
}
```

| Parameter            | Type   | Required? | Description                                                                                                                                              |
| -------------------- | ------ | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| full_name            | string | required  | Full name of the user                                                                                                                                    |
| email                | string | required  | Email address of the user                                                                                                                                |
| organization         | string | required  | Organization the user                                                                                                                                    |
| profession           | string | required  | Profession the user                                                                                                                                      |
| reason               | string | required  | Reason for using DNSTool                                                                                                                                 |
| password             | string | required  | Password of the user                                                                                                                                     |
| g_recaptcha_response | string | required  | Google reCAPTCHA v3 token. This is used to protect the API endpoint from abuse. Users need to provide a valid reCAPTCHA token to verify as a human user. |

The response is a success message if the email is not already in use.

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "message": "User account registered successfully"
}
```

Possible errors:

| Error code                | Description                        |
| ------------------------- | ---------------------------------- |
| 400 Bad Request           | Email already exists error         |
| 500 Internal Server Error | Internal server error has occurred |

### 3.5. Get Scans

#### Getting the scans

Get all the scans for the authenticated user.

```
GET /scans
```

Example request:

```
GET /scans HTTP/1.1
Host: DNSTool
Authorization: Bearer <JWT-Token-Signed-By-Firebase>
Content-Type: application/json
Accept: application/json
Accept-Charset: utf-8
```

The response is an object with scan data encapsulated within a data envelope.

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "data": {
    "1624893385247991": {
      "regions": [
        "us-east1-b",
        "us-east1-c"
      ],
      "state": "active",
      "zones": [
        ".com",
        ".lk"
      ]
    },
    "1624893391046098": {
      "regions": [
        "us-east1-c",
        "us-east1-b"
      ],
      "state": "active",
      "zones": [
        ".lk",
        ".com"
      ]
    },
    "1624893397158731": {
      "regions": [
        "us-east1-c",
        "us-east1-b"
      ],
      "state": "active",
      "zones": [
        ".lk",
        ".com"
      ]
    },
    "1624980505513786": {
      "regions": [
        "us-east1-c",
        "us-east1-b"
      ],
      "state": "active",
      "zones": [
        ".com",
        ".org"
      ]
    }
  }
}
```

Possible errors:

| Error code                | Description                        |
| ------------------------- | ---------------------------------- |
| 500 Internal Server Error | Internal server error has occurred |

### 3.6. Create Scans

#### Create a scan

Create a scan record.

```
POST /scans
```

Example request:

```
POST /scans HTTP/1.1
Host: DNSTool
Authorization: Bearer <JWT-Token-Signed-By-Firebase>
Content-Type: application/json
Accept: application/json
Accept-Charset: utf-8

{
  "zones": [
    ".com",
    ".lk"
  ],
  "regions": [
    "us-east1-b",
    "us-east1-c"
  ]
}
```

| Parameter | Type  | Required? | Description                  |
| --------- | ----- | --------- | ---------------------------- |
| zones     | array | required  | Zones list                   |
| regions   | array | required  | GCP Regions (GCP Zones) list |

The response is a success message.

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "message": "Scan has successfully recorded"
}
```

Possible errors:

| Error code                | Description                        |
| ------------------------- | ---------------------------------- |
| 500 Internal Server Error | Internal server error has occurred |

### 3.7. Update Scans

#### Update a scan

Update a scan record.

```
PATCH /scans/{{id}}
```

Example request:

```
PATCH /scans/1234567890 HTTP/1.1
Host: DNSTool
Authorization: Bearer <JWT-Token-Signed-By-Firebase>
Content-Type: application/json
Accept: application/json
Accept-Charset: utf-8

{
  "state": "suspend"
}
```

| Parameter | Type   | Required? | Description                |
| --------- | ------ | --------- | -------------------------- |
| state     | string | required  | Enum of (suspend / active) |

The response is a success message.

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "message": "[1234567890] state updated successfully"
}
```

Possible errors:

| Error code                | Description                        |
| ------------------------- | ---------------------------------- |
| 500 Internal Server Error | Internal server error has occurred |

### 3.8. Delete Scans

#### Delete a scan

Delete a scan record.

```
DELETE /scans/{{id}}
```

Example request:

```
DELETE /scans/1234567890 HTTP/1.1
Host: DNSTool
Authorization: Bearer <JWT-Token-Signed-By-Firebase>
Content-Type: application/json
Accept: application/json
Accept-Charset: utf-8

```

The response is a success message.

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "message": "scan [1234567890] deleted successfully"
}
```

Possible errors:

| Error code                | Description                        |
| ------------------------- | ---------------------------------- |
| 500 Internal Server Error | Internal server error has occurred |

### 3.9. Get Service Account

#### Getting the service account JSON file

Get the service account for a specific scan.

```
GET /service-account/{{id}}
```

Example request:

```
GET /service-account/123456789 HTTP/1.1
Host: DNSTool
Authorization: Bearer <JWT-Token-Signed-By-Firebase>
Content-Type: application/json
Accept: application/json
Accept-Charset: utf-8
```

The response is a file blob in bytes format.

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

<bytes-blob>
```

Possible errors:

| Error code                | Description                        |
| ------------------------- | ---------------------------------- |
| 500 Internal Server Error | Internal server error has occurred |

### 3.10. Get Scan Results Files List

#### Getting the scan results files list

Get the list of all the scan result files.

```
GET /list-downloads?client_id={{client_id}}&scan_id={{scan_id}}
```

| Parameter | Type   | Required? | Description                                        |
| --------- | ------ | --------- | -------------------------------------------------- |
| client_id | string | required  | Client ID as provided in Service Account JSON file |
| scan_id   | string | required  | Scan ID as provided in Service Account JSON file   |

Example request:

```
GET /list-downloads?client_id=SFvxWF53DSXCGr43fdd&scan_id=123456789 HTTP/1.1
Host: DNSTool
Authorization: Bearer <JWT-Token-Signed-By-Service-Account>
Content-Type: application/json
Accept: application/json
Accept-Charset: utf-8
```

The response is a list of downloadable file names.

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "file_paths": [
    "us-east1-c/.com/20210729.txt",
    "us-east1-c/.com/20210730.txt"
  ]
}
```

Possible errors:

| Error code                | Description                        |
| ------------------------- | ---------------------------------- |
| 500 Internal Server Error | Internal server error has occurred |

### 3.11. Download Scan Results File

#### Getting the scan results file

Download a scans results file.

```
GET /download/{{file-path}}
```

Example request:

```
GET /download/us-east1-c/.com/20210729.txt HTTP/1.1
Host: DNSTool
Authorization: Bearer <JWT-Token-Signed-By-Service-Account>
Content-Type: application/json
Accept: application/json
Accept-Charset: utf-8
```

The response is a file blob in bytes format.

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

<bytes-blob>
```

Possible errors:

| Error code                | Description                        |
| ------------------------- | ---------------------------------- |
| 500 Internal Server Error | Internal server error has occurred |
