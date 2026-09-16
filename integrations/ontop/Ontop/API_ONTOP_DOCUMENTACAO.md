# Ontop API Documentation - Source of Truth

**Creation Date:** 2025-02-02  
**API Version:** Demo  
**Base URL:** `https://api.demo.getontop.com`

---

## Table of Contents

1. [Authentication](#1-authentication)
2. [Worker](#2-worker)
3. [Client Wallet](#3-client-wallet)
4. [Paylist](#4-paylist)
5. [Webhooks](#5-webhooks)

---

## 1. Authentication

### 1.1 Login

**Endpoint:** `POST /login/login/v2`

**Description:** New login endpoint to ensure more security.

**Headers:**
- `Content-Type: application/json`

**Body (JSON):**
```json
{
    "email": "admin@yopmail.com",
    "password": "password",
    "rememberMe": false,
    "recaptchaToken": "",
    "user": "admin@yopmail.com",
    "ip": "190.236.144.113",
    "webDeviceInfo": "Backend"
}
```

**Fields:**
- `email` (string, required): User email
- `password` (string, required): User password
- `rememberMe` (boolean): Whether to remember the login
- `recaptchaToken` (string): reCAPTCHA token (can be empty)
- `user` (string): Username (usually the same as email)
- `ip` (string): IP address
- `webDeviceInfo` (string): Device information (e.g., "Backend")

**cURL Example:**
```bash
curl --location 'https://api.demo.getontop.com/login/login/v2' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "admin@yopmail.com",
    "password": "password",
    "rememberMe": false,
    "recaptchaToken": "",
    "user": "admin@yopmail.com",
    "ip": "190.236.144.113",
    "webDeviceInfo": "Backend"
}'
```

**Note:** This endpoint returns an authentication token that must be used in the `Authorization: Bearer <token>` header for subsequent requests.

---

## 2. Worker

### 2.1 Invite Workers (Bulk)

**Endpoint:** `POST /contract/workers/inviteWorkersBulkLocked`

**Description:** Sends bulk invitations to workers. The `client_id` is obtained through the authentication token and will be stored at the moment the invitation is sent.

**Headers:**
- `Content-Type: application/json`
- `Authorization: Bearer <token>`

**Body (JSON Array):**
```json
[
    {
        "workerName": "Jane",
        "workerSurname": "Doe",
        "typeOfWorker": "Worker",
        "jobTitle": "Developer",
        "workerEmail": "jane.doe@example.com",
        "workerEmailText": "Hi, we would like to invite you to work with us.",
        "externalId": "ABC123",
        "countryIso": "MX"
    },
    {
        "workerName": "John",
        "workerSurname": "Smith",
        "workerLegalName": "Business Corp.",
        "typeOfWorker": "Business",
        "jobTitle": "Manager",
        "workerEmail": "john.smith@example.com",
        "workerEmailText": "Hello, we invite your business to collaborate with us.",
        "externalId": "XYZ456",
        "countryIso": "US"
    }
]
```

**Required Fields:**
- `workerName` (string): Worker's first name
- `workerSurname` (string): Worker's last name
- `typeOfWorker` (string): Type of worker - can be `"Worker"` or `"Business"`
- `workerEmail` (string): Worker's email
- `countryIso` (string): ISO 3166-1 alpha-2 code (e.g., MX, AR, US, BR)

**Conditional Fields:**
- `workerLegalName` (string): **Required** if `typeOfWorker` is `"Business"`

**Optional Fields:**
- `jobTitle` (string): Worker's job title
- `workerEmailText` (string): Custom email invitation text
- `externalId` (string): External ID for reference

**cURL Example:**
```bash
curl --location 'https://api.demo.getontop.com/contract/workers/inviteWorkersBulkLocked' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data-raw '[
    {
        "workerName": "Jane",
        "workerSurname": "Doe",
        "typeOfWorker": "Worker",
        "jobTitle": "Developer",
        "workerEmail": "john.doe.demo.test.73@yopmail.com",
        "workerEmailText": "Hi, we would like to invite you to work with us.",
        "externalId": "ABC123",
        "countryIso": "MX"
    }
]'
```

---

### 2.2 Get Workers

**Endpoint:** `GET /contract/workers/list`

**Description:** Returns a paginated list of workers linked to the client. The `client_id` is obtained through the authentication token. Can be filtered by worker status.

**Headers:**
- `Authorization: Bearer <token>`
- `Cookie: JSESSIONID=<session_id>` (optional)

**Query Parameters:**
- `statusId` (integer, optional): Filter by worker status
  - `0` = ACTIVE
  - `1` = INVITATION_SENT
  - `2` = VERIFICATION_PENDING
  - `3` = ENDED
  - If not provided, returns all workers

**cURL Example (all workers):**
```bash
curl --location 'https://api.demo.getontop.com/contract/workers/list' \
--header 'Authorization: Bearer <token>' \
--header 'Cookie: JSESSIONID=<session_id>'
```

**cURL Example (filtered by ACTIVE status):**
```bash
curl --location 'https://api.demo.getontop.com/contract/workers/list?statusId=0' \
--header 'Authorization: Bearer <token>' \
--header 'Cookie: JSESSIONID=<session_id>'
```

**Response Example:**
```json
{
    "content": [
        {
            "agreementId": 15,
            "firstName": null,
            "lastName": null,
            "legalName": null,
            "email": "john.doe.ontop@yopmail.com",
            "jobTitle": "Software Engineer",
            "country": null,
            "externalId": null,
            "workerCreationDate": "2023-09-29T22:33:34.377+00:00",
            "status": "INVITATION_SENT"
        },
        {
            "agreementId": 16,
            "firstName": "Juan",
            "lastName": "Perez",
            "legalName": null,
            "email": "juan.perez.ontop@yopmail.com",
            "jobTitle": "Ingeniero de Software",
            "country": "Argentina",
            "externalId": "SFK005",
            "workerCreationDate": "2023-09-21T14:42:38.793+00:00",
            "status": "ACTIVE"
        }
    ],
    "pageable": {
        "sort": {
            "empty": true,
            "sorted": false,
            "unsorted": true
        },
        "offset": 0,
        "pageNumber": 0,
        "pageSize": 20,
        "paged": true,
        "unpaged": false
    },
    "last": true,
    "totalPages": 1,
    "totalElements": 2,
    "number": 0,
    "sort": {
        "empty": true,
        "sorted": false,
        "unsorted": true
    },
    "size": 20,
    "first": true,
    "numberOfElements": 2,
    "empty": false
}
```

**Response Fields:**
- `agreementId` (integer): Agreement/worker ID
- `firstName` (string|null): Worker's first name
- `lastName` (string|null): Worker's last name
- `legalName` (string|null): Legal name (for businesses)
- `email` (string): Worker's email
- `jobTitle` (string|null): Job title
- `country` (string|null): Country
- `externalId` (string|null): External ID
- `workerCreationDate` (string): Creation date (ISO 8601)
- `status` (string): Worker status (ACTIVE, INVITATION_SENT, VERIFICATION_PENDING, ENDED)

---

### 2.3 Get Worker Info

**Endpoint:** `GET /contract/workers`

**Description:** Searches for individual worker information by email.

**Headers:**
- `Authorization: Bearer <token>`
- `Cookie: JSESSIONID=<session_id>` (optional)

**Query Parameters:**
- `email` (string, required): Email of the worker to search for

**cURL Example:**
```bash
curl --location 'https://api.demo.getontop.com/contract/workers?email=john.doe.ontop%40yopmail.com' \
--header 'Authorization: Bearer <token>' \
--header 'Cookie: JSESSIONID=<session_id>'
```

**Response Example (Worker with completed onboarding):**
```json
{
    "agreementId": 11,
    "firstName": "John",
    "lastName": "Doe",
    "legalName": null,
    "email": "john.doe.ontop@yopmail.com",
    "jobTitle": "Software Engineer",
    "country": "United States",
    "externalId": null,
    "workerCreationDate": "2023-01-31T17:51:20.297+00:00",
    "status": "ACTIVE"
}
```

**Notes:**
- If the worker has completed the onboarding process and successfully created an account, the response will show the same information as the "Get Workers" endpoint
- If the worker has not started the onboarding process, the response will be an exception explaining the reason

---

## 3. Client Wallet

### 3.1 Wallet Info & Balance

**Endpoint:** `GET /client-wallet/clients/{client_id}/wallet`

**Description:** Exposes the Client wallet information, such as enabled status and balance available to perform transactions.

**Headers:**
- `Authorization: Bearer <token>`

**Path Parameters:**
- `client_id` (integer): Client ID

**cURL Example:**
```bash
curl 'https://api.demo.getontop.com/client-wallet/clients/100/wallet' \
--header 'Authorization: Bearer <token>'
```

**Response Example:**
```json
{
  "id": 4,
  "wallet_version": 112,
  "client_id": 100,
  "enabled": true,
  "balance": 889.00,
  "over_draft_limit": 0.000000,
  "created_at": "2023-09-28T19:33:32.862876Z"
}
```

**Response Fields:**
- `id` (integer): Wallet ID
- `wallet_version` (integer): Wallet version
- `client_id` (integer): Client ID
- `enabled` (boolean): Whether the wallet is enabled
- `balance` (decimal): Available balance
- `over_draft_limit` (decimal): Overdraft limit
- `created_at` (string): Creation date (ISO 8601)

**Status Code:** `200` - Successful response

---

### 3.2 Wallet Transactions

**Endpoint:** `GET /client-wallet/clients/transactions`

**Description:** Exposes all journal entries made into the Client ledger. It is a paginated list so it can be traversed using page and/or size query parameters.

**Headers:**
- `Authorization: Bearer <token>`

**Query Parameters:**
- `page` (integer, optional): Page number
- `size` (integer, optional): Page size

**cURL Example:**
```bash
curl 'https://api.demo.getontop.com/client-wallet/clients/transactions?page=1&size=200' \
--header 'Authorization: Bearer <token>'
```

**Response Example:**
```json
{
  "content": [
    {
      "journal_id": 223,
      "wallet_id": 4,
      "client_id": 305,
      "idempotence_key": "2234db48f5d4f87118759fb125789ea4",
      "amount": -1.000000,
      "reason": "PAYMENT",
      "operation": "WITHDRAWAL",
      "transaction_data": {
        "payment_order_id": "335",
        "payment_purpose": "Client payment to worker"
      },
      "created_at": "2023-09-29T18:11:32.131304Z"
    }
  ]
}
```

**Response Fields:**
- `journal_id` (integer): Journal entry ID
- `wallet_id` (integer): Wallet ID
- `client_id` (integer): Client ID
- `idempotence_key` (string): Idempotence key
- `amount` (decimal): Transaction amount (negative for withdrawals)
- `reason` (string): Transaction reason (e.g., "PAYMENT")
- `operation` (string): Operation type (e.g., "WITHDRAWAL")
- `transaction_data` (object): Additional transaction data
- `created_at` (string): Creation date (ISO 8601)

**Status Code:** `200` - Successful response

---

## 4. Paylist

### 4.1 Create Paylist

**Endpoint:** `POST /payment-agent/paylists`

**Description:** Allows clients to create a new paylist, providing a description and simultaneously adding multiple payments. Upon processing the request, the service will validate each payment item. If everything is in order, it will return a response indicating the paylist has been accepted and will be processed asynchronously. The paylist is just a container of payments and only exists as the collection representation, without status.

**⚠️ IMPORTANT #1:** Take into consideration the `idempotence_key`: this identifies unequivocally the paylist on the system and needs to be unique for each one. The idea behind this is to not allow repeated paylist creation on retries due to network issues of any kind. The field has to be 32 characters long; we recommend using the MD5 hashing algorithm since it produces the required string size.

**⚠️ IMPORTANT #2:** The payment process will generate an idempotency key internally for it. The fields taken into account for this are: `amount`, `email` and `description`. If you have repetitive payments for the same amount and purpose, consider adding an extra text into the description to indicate the motive in a more precise way (i.e., dates, goals, etc.).

**Headers:**
- `Content-Type: application/json`
- `Authorization: Bearer <token>`

**Body (JSON):**
```json
{
    "description": "Payments september",
    "idempotence_key": "anuniquekey123",
    "payments": [
        {
            "description": "Payment 1",
            "amount": 10,
            "worker_email": "worker_n1@example.com"
        },
        {
            "description": "Payment 2",
            "amount": 30,
            "worker_email": "worker_n2@example.com"
        }
    ],
    "client_id": 100
}
```

**Required Fields:**
- `description` (string): Paylist description
- `idempotence_key` (string): Unique idempotence key (32 characters, MD5 recommended)
- `payments` (array): Array of payment objects
  - `description` (string): Payment description
  - `amount` (decimal): Payment amount
  - `worker_email` (string): Worker email
- `client_id` (integer): Client ID

**cURL Example:**
```bash
curl -X POST 'https://api.demo.getontop.com/payment-agent/paylists' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data-raw '{
    "description":"Payments september",
    "idempotence_key":"anuniquekey123",
    "payments":[
        {
            "description":"Payment 1",
            "amount":10,
            "worker_email":"worker_n1@example.com"
        },
        {
            "description":"Payment 2",
            "amount":30,
            "worker_email":"worker_n2@example.com"
        }
    ],
    "client_id":100
}'
```

**Response Example:**
```json
{
    "id": 23,
    "description": "Payments september",
    "client_id": 100,
    "idempotence_key": "anuniquekey123",
    "creation_date": "2023-09-29T14:01:37.151862380Z"
}
```

**Status Code:** `200` - Successful response

---

### 4.2 Get Paylist by ID

**Endpoint:** `GET /payment-agent/paylists/{paylist_id}`

**Description:** (Information not detailed in the original document, but mentioned in the API structure)

**Note:** This endpoint likely returns the details of a specific paylist by its ID.

---

### 4.3 Get Payment List by Paylist ID

**Endpoint:** `GET /payment-agent/paylists/{paylist_id}/payments`

**Description:** This is a paginated endpoint that exposes the list of payments involved in a previously created paylist. It can be traversed using page and/or size query parameters.

**Headers:**
- `Authorization: Bearer <token>`

**Path Parameters:**
- `paylist_id` (integer): Paylist ID

**Query Parameters:**
- `page` (integer, optional): Page number
- `size` (integer, optional): Page size

**cURL Example:**
```bash
curl 'https://api.demo.getontop.com/payment-agent/paylists/23/payments?page=1&size=20' \
--header 'Authorization: Bearer <token>'
```

**Response Example:**
```json
{
    "content": [
        {
            "id": 231,
            "description": "Worker n1",
            "amount": 10.00,
            "worker_email": "worker_n1@example.com",
            "paylist_id": 23,
            "idempotence_key": "2ffa2c706ab068dce719b38d1a795544",
            "creation_date": "2023-09-28T14:48:46.771546Z",
            "update_date": "2023-09-28T14:48:48.212830Z",
            "status": "SUCCESS",
            "cause": null
        },
        {
            "id": 232,
            "description": "Worker n2",
            "amount": 30.00,
            "worker_email": "worker_n2@example.com",
            "paylist_id": 23,
            "idempotence_key": "2ffa2c706ab068dce719b38d1a795544",
            "creation_date": "2023-09-28T14:48:46.771546Z",
            "update_date": "2023-09-28T14:48:48.212830Z",
            "status": "SUCCESS",
            "cause": null
        }
    ],
    "pageable": {
        "sort": {
            "unsorted": false,
            "sorted": true,
            "empty": false
        },
        "pageNumber": 0,
        "pageSize": 20,
        "offset": 0,
        "paged": true,
        "unpaged": false
    },
    "totalPages": 1,
    "totalElements": 2,
    "last": true,
    "numberOfElements": 2,
    "size": 20,
    "number": 0,
    "sort": {
        "unsorted": false,
        "sorted": true,
        "empty": false
    },
    "first": true,
    "empty": false
}
```

**Response Fields (Payment):**
- `id` (integer): Payment ID
- `description` (string): Payment description
- `amount` (decimal): Payment amount
- `worker_email` (string): Worker email
- `paylist_id` (integer): Paylist ID
- `idempotence_key` (string): Idempotence key
- `creation_date` (string): Creation date (ISO 8601)
- `update_date` (string): Update date (ISO 8601)
- `status` (string): Payment status (e.g., "SUCCESS")
- `cause` (string|null): Error cause, if any

**Status Code:** `200` - Successful response

---

### 4.4 Get Payment by ID

**Endpoint:** `GET /payment-agent/payments/{payment_id}`

**Description:** This endpoint serves to retrieve the comprehensive details of a specific payment by its unique ID. By fetching these details, users can inspect the status, the creation and update dates, making it a critical tool for monitoring and verifying bulk payment progress.

**Headers:**
- `Authorization: Bearer <token>`

**Path Parameters:**
- `payment_id` (integer): Payment ID

**cURL Example:**
```bash
curl 'https://api.demo.getontop.com/payment-agent/payments/231' \
--header 'Authorization: Bearer <token>'
```

**Response Example:**
```json
{
  "id": 231,
  "description": "Worker n1",
  "amount": 10.00,
  "worker_email": "worker_n1@example.com",
  "paylist_id": 23,
  "idempotence_key": "2ffa2c706ab068dce719b38d1a795544",
  "creation_date": "2023-09-28T14:48:46.771546Z",
  "update_date": "2023-09-28T14:48:48.212830Z",
  "status": "SUCCESS",
  "cause": null
}
```

**Status Code:** `200` - Successful response

---

### 4.5 Get Paylists

**Endpoint:** `GET /payment-agent/paylists`

**Description:** This endpoint serves to retrieve a paginated list of paylists for a specific client within a date range. Users can specify the start date and end date to filter the paylists. If not provided, default values will be used. This endpoint is a critical tool for monitoring and tracking the progress of paylists over a specific period of time.

**Headers:**
- `Authorization: Bearer <token>`

**Query Parameters:**
- `startDate` (string, optional): Start date (ISO 8601 format, e.g., `2023-09-01T00:00:00Z`)
- `endDate` (string, optional): End date (ISO 8601 format, e.g., `2023-09-30T23:59:59Z`)
- `page` (integer, optional): Page number (default: 0)
- `size` (integer, optional): Page size (default: 20)

**cURL Example:**
```bash
curl 'https://api.demo.getontop.com/payment-agent/paylists?startDate=2023-09-01T00:00:00Z&endDate=2023-09-30T23:59:59Z&page=0&size=20' \
--header 'Authorization: Bearer <token>'
```

**Response Example:**
```json
{
  "content": [
    {
      "paylistId": 231,
      "flowStage": "COMPLETED",
      "description": "Paylist for September 2023",
      "total": 10000.00
    }
  ],
  "pageable": {
    "sort": {
      "sorted": true,
      "unsorted": false,
      "empty": false
    },
    "offset": 0,
    "pageNumber": 0,
    "pageSize": 20,
    "paged": true,
    "unpaged": false
  },
  "totalElements": 100
}
```

**Response Fields:**
- `paylistId` (integer): Paylist ID
- `flowStage` (string): Flow stage (e.g., "COMPLETED")
- `description` (string): Paylist description
- `total` (decimal): Paylist total amount

---

### 4.6 Get Payments

**Endpoint:** `GET /payment-agent/payments`

**Description:** This endpoint is used to retrieve a paginated list of payments for a specific customer within a date range. Users can specify the start date and end date to filter the payments. If not provided, default values will be used. This endpoint is a critical tool for monitoring and verifying the progress of payments over a specific time period.

**Headers:**
- `Authorization: Bearer <token>`

**Query Parameters:**
- `startDate` (string, optional): Start date (ISO 8601 format, e.g., `2023-09-01T00:00:00Z`)
- `endDate` (string, optional): End date (ISO 8601 format, e.g., `2023-09-30T23:59:59Z`)
- `page` (integer, optional): Page number (default: 0)
- `size` (integer, optional): Page size (default: 20)

**cURL Example:**
```bash
curl 'https://api.demo.getontop.com/payment-agent/payments?startDate=2023-09-01T00:00:00Z&endDate=2023-09-30T23:59:59Z&page=0&size=20' \
--header 'Authorization: Bearer <token>'
```

**Response Example:**
```json
{
  "content": [
    {
      "id": 231,
      "description": "Worker n1",
      "amount": 10.00,
      "worker_email": "worker_n1@example.com",
      "paylist_id": 23,
      "idempotence_key": "2ffa2c706ab068dce719b38d1a795544",
      "creation_date": "2023-09-28T14:48:46.771546Z",
      "update_date": "2023-09-28T14:48:48.212830Z",
      "status": "SUCCESS",
      "cause": null
    }
  ],
  "pageable": {
    "sort": {
      "sorted": true,
      "unsorted": false,
      "empty": false
    },
    "offset": 0,
    "pageNumber": 0,
    "pageSize": 20,
    "paged": true,
    "unpaged": false
  },
  "totalElements": 100
}
```

**Status Code:** `200` - Successful response

---

## 5. Webhooks

### 5.1 Overview

**Description:** Webhooks function as a callback mechanism, where OnTop sends HTTP POST requests to a predefined URL defined by the Client in response to particular events. This approach to communication allows for seamless integration and data sharing between us and Clients, eliminating the need for constant polling or manual data retrieval.

**Configuration Endpoints:**
- `POST /webhooks` - Create configuration
- `GET /webhooks` - Retrieve configuration
- `POST /webhooks/test` - Test event notification

---

### 5.2 Event Types

#### 5.2.1 KYC Verified and Active

**Event Type:** `KYC`

**Description:** Contains information about the KYC event, including the verification status, worker ID, client ID, external ID, and worker email. This state implies that the worker has successfully verified its identity through the KYC and a wallet has been created.

**Payload Example:**
```json
{
  "event_type": "KYC",
  "data": {
    "status": "ACTIVE",
    "worker_id": 888,
    "client_id": 999,
    "external_id": "abc123",
    "worker_email": "john.doe@example.com"
  }
}
```

**Fields:**
- `event_type` (string): Event type ("KYC")
- `data.status` (string): Verification status (e.g., "ACTIVE")
- `data.worker_id` (integer): Worker ID
- `data.client_id` (integer): Client ID
- `data.external_id` (string): External ID
- `data.worker_email` (string): Worker email

---

#### 5.2.2 Payment Status

**Event Type:** `PAYMENT`

**Description:** Notifies about the final status of each payment enqueued using the Paylist interface. The event body includes the payment ID, the paylist ID, the amount transferred and worker data.

**Payload Example:**
```json
{
  "event_type": "PAYMENT",
  "data": {
    "payment_id": 20,
    "client_id": 999,
    "worker_id": 111,
    "paylist_id": 24,
    "idempotency_key": "bea3502a2a5a1f776bce4d7c2ce6f267",
    "email": "john.doe@example.com",
    "transaction_status": "SUCCESS",
    "transaction_amount": 100.00,
    "transaction_date_time": 1698708987.544633693
  }
}
```

**Fields:**
- `event_type` (string): Event type ("PAYMENT")
- `data.payment_id` (integer): Payment ID
- `data.client_id` (integer): Client ID
- `data.worker_id` (integer): Worker ID
- `data.paylist_id` (integer): Paylist ID
- `data.idempotency_key` (string): Idempotency key
- `data.email` (string): Worker email
- `data.transaction_status` (string): Transaction status (e.g., "SUCCESS")
- `data.transaction_amount` (decimal): Transaction amount
- `data.transaction_date_time` (number): Transaction timestamp

---

#### 5.2.3 Client Wallet Top-up

**Event Type:** `CLIENT_WALLET_TOP_UP`

**Description:** Provides details about a Client's Wallet top-up event, including transaction ID, transaction type, amount, and a reference ID (idempotence key).

**Payload Example:**
```json
{
  "event_type": "CLIENT_WALLET_TOP_UP",
  "data": {
    "transaction_id": 7,
    "transaction_type": "TRANSFER",
    "amount": 1000,
    "reference_id": "aabvadasxxxxbxyyyzzz"
  }
}
```

**Fields:**
- `event_type` (string): Event type ("CLIENT_WALLET_TOP_UP")
- `data.transaction_id` (integer): Transaction ID
- `data.transaction_type` (string): Transaction type (e.g., "TRANSFER")
- `data.amount` (decimal): Top-up amount
- `data.reference_id` (string): Reference ID (idempotence key)

---

## 6. General Information

### 6.1 Authentication

Most endpoints require authentication through the header:
```
Authorization: Bearer <token>
```

The token is obtained through the Login endpoint (`POST /login/login/v2`).

### 6.2 Base URL

- **Demo/Test:** `https://api.demo.getontop.com`
- **Production:** (verify with Ontop)

### 6.3 Date Formats

- **ISO 8601:** `2023-09-29T14:01:37.151862380Z`
- **Unix Timestamp:** `1698708987.544633693` (for some webhook fields)

### 6.4 HTTP Status Codes

- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

### 6.5 Pagination

Many endpoints return paginated results with the following structure:
```json
{
  "content": [...],
  "pageable": {
    "pageNumber": 0,
    "pageSize": 20,
    ...
  },
  "totalElements": 100,
  "totalPages": 5,
  ...
}
```

### 6.6 Idempotence

- **Paylists:** Require unique `idempotence_key` of 32 characters (MD5 recommended)
- **Payments:** Generate idempotence key internally based on `amount`, `email` and `description`

---

## 7. Implementation Notes

### 7.1 Typical Integration Flow

1. **Authentication:** Login to obtain token
2. **Manage Workers:** 
   - Invite workers
   - List workers
   - Check worker status
3. **Manage Wallet:**
   - Check balance
   - Monitor transactions
4. **Process Payments:**
   - Create paylist with multiple payments
   - Monitor payment status
   - Query payment history
5. **Configure Webhooks:**
   - Configure callback URL
   - Process received events

### 7.2 Best Practices

1. **Idempotence:** Always use unique idempotence keys for paylists
2. **Error Handling:** Implement retry logic with exponential backoff
3. **Webhooks:** Validate and process events asynchronously
4. **Security:** Never expose tokens or credentials in logs
5. **Validation:** Validate all data before sending to the API

---

**Last Updated:** Based on documentation copied on 2025-02-02  
**Document Version:** 1.0
