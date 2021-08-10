# DNSTool-Middleware-API Documentation

#### Contents

- [Overview](#1-overview)
- [Authentication](#2-authentication)
- [Resources](#3-resources)
  - [Domain Zones](#31-domain-zones)
  - [GCP Zones](#32-gcp-zones)
  - [Check Emails](#33-check-emails)
  - [Register](#34-register)

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
