# Data Rights Protocol v.0.3

**DRAFT FOR COMMENT**

[Data Rights Protocol](https://github.com/consumer-reports-digital-lab/data-rights-protocol)

Changes from v0.2
- donotsell -> sale:opt-in opt-out
- terminology changes
- Request status chart
- identity tiger team recommendations
- API Authentication details
- Moved non-essential sections out of protocol spec

## 1.0 Introduction

This specification defines a web protocol encoding a set of standardized request/response data flows such that End-Users can exercise Personal Data Rights provided under regulations like the California Consumer Privacy Act, General Data Protection Regulation, and other regulatory or voluntary bases, and receive affirmative responses in standardized formats.

We aim to make the data rights protocol integrable with an ecosystem of data rights middlewares, agent services, automation tool kits, and privacy-respecting businesses which empower and build trust with consumers while driving the cost of compliance towards zero.

### 1.01 Motivation
Data Rights are increasingly becoming universal, but the method of request and protocol for communicating those requests varies and there is no universal interchange format. Companies operating under these regulatory regimes face not only technical challenges in collecting and delivering responses to users’ data rights requests but also face significant process burdens as consumers increasingly make use of these rights. At the same time, consumers find it tough to execute their data rights under new privacy laws, partially due to a lack of standardization among companies.

By providing a shared protocol and vocabulary for expressing these data rights, we aim to minimize the administrative burdens on consumers and businesses while providing a basis of trust for verifiable identity attestation which can be used by (individual) consumers (or by an agent intermediating the relationship on behalf of consumers) and businesses.


### 1.02 Scope
In this initial phase of the Data Rights Protocol, we want to enable a group of peers to form a voluntary trust network while expanding the protocol to support wider trust models and additional data flows.

Version 0.3 encodes the provisions of the California Code bla bla section bla as specified in the California Consumer Privacy act of 2018, referred herein as the “CCPA” and intends to encode the following rights. This is further enumerated in the [Supported Rights Actions](#301-supported-rights-actions) section of this document below.

### 1.03 Terminology

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

[XXX: move to bottom]
distinguish actors from components

- User (/consumer/subject)
- User Agent
- Authorized Agent
- AAi

- PIP
- PIPi

- CB
- CBi

## 2.0 HTTP Endpoint Specification

[note about including schemas by-reference from below.]

DRP 0.3 implementors MUST support application/json request and response bodies.

[expand endpoints with their failure states]

### 2.01 `GET /.well-known/data-rights.json` ("Data Rights Discovery" endpoint)

This is the Data Rights Discovery endpoint, responding at a well-known endpoint on the Covered Business’s primary End-User focused domain. This [RFC8615] URI will return a JSON document conforming to this schema. This endpoint exists for End-Users and Authorized Agents to be able to take Data Rights Actions.

For instance, an End-User looking to exercise their data rights for Example, Inc. whose homepage is https://example.com/ MUST be able to GET https://example.com/.well-known/data-rights.json without knowledge of the Covered Business’s relationship to any Privacy Infrastructure Provider. 

[XXX] ^ is this a MUST?

[XXX] This `well-known` resource SHOULD be registered with IANA before 1.0 specification.

```
{
  "version": "0.3",
  "api_base": "https://example.com/data-rights",
  "actions": ["sale:opt-out", "sale:opt-in", "access", "deletion"],
}
```

- `version` field is a string carrying the version of the protocol implemented. Currently this MUST read "0.3"
- `api_base` field is a URI under which the rest of the Data Rights Protocol is accessible. 
- `actions` is a list of strings enumerating the rights which may be exercised, as outlined in [Supported Rights Actions](#301-supported-rights-actions)

[XXX] re api_base: something like "This endpoint MAY be run by a Privacy Infrastructure Provider but SHOULD be accessible under the Covered Business's domains for legibility's sake."

### 2.02 `POST /exercise` ("Data Rights Exercise" endpoint)

This is the Data Rights Exercise endpoint which End-Users and Authorized Agents can use to exercise enumerated data rights.

```
{
  "meta": {
    "version": "0.3"
  },
  "legal_basis": "ccpa",
  "exercise": [
    "sale:opt-out"
  ],
  "identity": <jwt>... ,
  "status_callback": "https://dsr-agent.example.com/update_status"
}
```

- `meta` MUST contain only a single key `version` which contains a string referencing the current protocol version “0.3”.
- `legal_basis` MUST contain a string referencing the legal basis under which the Data Request is being taken. See [3.01 Supported Rights Actions](#301-supported-rights-actions).
- `exercise` MUST contain a list of rights to exercise.
- `identity` MUST contain an [RFC7515 JWT](https://datatracker.ietf.org/doc/html/rfc7515) conforming to one of the following specifications:
  - a string containing a JWT serialized in the Compact Serialization format [RFC7515 Section 3.1]
  - a document object containing a JWT serialized in the JSON Serialization formation [RFC7515 Section 3.2]
- `status_callback` MAY be specified with a URL that the Status Callback can be sent to. See ["Data Rights Status Callback" endpoint](#2041-post-status_callback-response).

[XXX]: replace regulatory_authority with legal_basis -> support contract/voluntary bases?
[XXX]: is exercise a list? is making multiple "requests" in a single request valid?

See [section 3.04](#304-schema-identity-encapsulation) regarding identity encapsulation.

#### 2.02.1 `POST /exercise` Response

Responses to this request MUST adhere to the [Exercise Status Schema](#303-schema-status-of-a-data-subject-exercise-request).

### 2.03 `GET /status` ("Data Rights Status" endpoint)

This is the Data Rights Status endpoint which End-Users and Authorized Agents can use to query for the status of an existing data rights request. Requests to this endpoint MUST provide a single URL parameter request_id which is the Request ID for the Data Rights Request.

`GET /status?request_id=c789ff35-7644-4ceb-9981-4b35c264aac3`

#### 2.03.1 `GET /status` Response

Responses to this request MUST adhere to the [Exercise Status Schema](#303-schema-status-of-a-data-subject-exercise-request).


### 2.04 `POST $status_callback` ("Data Rights Status Callback" endpoint)

The Status Callback endpoint SHOULD be implemented by Authorized Agents which will be exercising data rights for multiple Users. This endpoint exists to remove the need for Authorized Agents to query the Data Rights Status endpoint and instead allow a “push model” where AAs are notified when a request's status changes. The destination for a Status Callback URL is specified in the initial [Data Rights Exercise](#202-post-exercise-data-rights-exercise-endpoint) request.

The request body MUST adhere to the [Exercise Status Schema](#303-schema-status-of-a-data-subject-exercise-request). 

#### 2.04.1 `POST $status_callback` Response

Covered Business SHOULD make a best effort to ensure that a 200 status is recorded for the most recent status update. The body of the callback's response SHOULD be discarded and not be considered for parsing by the Covered Business.

### 2.05 `POST /revoke` ("Data Rights Revoke" endpoint)

An Authorized Agent SHALL provide Users with a mechanism to request cancellation of an open or in progress request by sending a Data Rights Revoke request with the following body parameters:

```
{
  "request_id": "c789ff35-7644-4ceb-9981-4b35c264aac3",
  "reason": "i don't want my account deleted"
}
```

Requests to this endpoint contain a single field:
- `request_id` MUST contain the ID of the request to revoke
- `reason` MAY contain a user provided reason for the request to be not processed.

#### 2.05.1 `POST /revoke` response

Responses to this request MUST adhere to the [Exercise Status Schema](#303-schema-status-of-a-data-subject-exercise-request). Responses MUST contain the *new* state.

## 3.0 Data Schemas

These Schemas are referenced in Section 2 outlining the HTTP endpoints and their semantics.

### 3.01 Supported Rights Actions

Requests made under the `legal_basis` “ccpa” can take the following actions:

* `sale:opt_out` - [RIGHT TO OPT-OUT OF SALE](https://oag.ca.gov/privacy/ccpa#sectionb)
* `sale:opt_in` - RECONSENT OR OPT-IN TO DATA SALE
* `deletion` - [RIGHT TO DELETE](https://oag.ca.gov/privacy/ccpa#sectione)
* `access` -  [RIGHT TO KNOW](https://oag.ca.gov/privacy/ccpa#sectionc)
* `access:categories` -  [RIGHT TO KNOW](https://oag.ca.gov/privacy/ccpa#sectionc)
  * Implementers SHOULD define this action before v1.0
* `access:specific` -  [RIGHT TO KNOW](https://oag.ca.gov/privacy/ccpa#sectionc)
  * Implementers SHOULD define this action before v1.0

[XXX] access:categories, access:specific encoding, how tightly do the rights map to CCPA? talk about what these rights loo like with the larger group

**Covered Businesses** specify which rights they support in the [Data Rights Discovery](#201-get-well-knowndata-rightsjson-data-rights-discovery-endpoint) endpoint while consumers and their agents can specify the rights they are making use of in the [Data Rights Exercise](#202-post-exercise-data-rights-exercise-endpoint) endpoint.

### 3.02 Request Statuses

This table shows valid states for Data Rights Requests, along with the criteria for transition into each state. Further, this table shows at which states certain fields are allowed to be *added* to a data rights request.

"Final" states are marked in the final field of the table. Requests which enter final state MAY be disregared after the lesser of the `expires_at` flag or 60 days, but no less than 7 days from when expiration was first specified.

| state       | reason                 | entrance criteria                                                   | new fields                        | Final? |
|-------------|------------------------|---------------------------------------------------------------------|-----------------------------------|--------|
|             |                        | user has created request, but not submitted it                      | base fields                       |        |
| open        |                        | user has submitted request to Data Rights Endpoint[1]               | request_id                        |        |
| in_progress |                        | CB has acknowledge receipt of request OR User solves verification   | received_at                       |        |
| in_progress | need_user_verification | CB doesn't have sufficient ID verification                          | user_verification_url, expires_at |        |
| fulfilled   |                        | CB has finished data rights request process                         | results_url, expires_at           | x      |
| revoked     |                        | user has explicitly actioned to revoke the request                  |                                   | x      |
| denied      | suspected_fraud        | CB or PIP believes this request was made fraudulently               |                                   | x      |
| denied      | insuf_verification     | the [in_progress, need_user_verification] stage failed or timed out |                                   | x      |
| denied      | no_match               | CB could not match user identity to data subject                    |                                   | x      |
| denied      | claim_not_covered      | user requesting data not covered under legal bases[XXX]                  |                                   | x      |
| denied      | outside_jurisdiction   | user requesting data under bases they are not covered by[XXX]            |                                   | x      |
| denied      | other                  | some other unspecified failure state reached                        | details?                          | x      |
| expired     |                        | the time is currently after the `expires_at` in the request.         |                                   | x      |

[XXX]: in the case of claim_not_covered, this may be about asking for categories of data which Covered Businesses are not required to present to the User. in the case of outside_jurisdiction, this may be because the business is not honoring CCPA requests for non-California residents

### 3.03 Schema: Status of a Data Subject Exercise Request

A single JSON object is used to describe any existing Data Exercise Request and is referred to as the Exercise Status object:

```
{
  "request_id": "c789ff35-7644-4ceb-9981-4b35c264aac3",
  "received_at": "20210902T152725.403-0700",
  "status": "in_progress",
  "reason": "need_user_verification",
  "user_verification_url": "https://example.com/data-rights/verify/c789ff35-7644-4ceb-9981-4b35c264aac3"
}
```

* `request_id` MUST contain a string that is the globally unique ID returned in the initial [Data Rights Exercise request](#202-post-exercise-data-rights-exercise-endpoint).[1] 
* `status` MUST contain a string which is one of the request states as defined in [Request Statuses](#302-request-statuses).
* `reason` MAY contain a string containing additional information about the current state of the request according to the [Request Statuses](#302-request-statuses).
* `received_at` SHOULD contain a string which is the [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339)-encoded time which the initial request was registered by the Covered Business.
  * When a Covered Business receives a request, this field MUST be present.
* `user_verification_url` MAY contain a URI which can be presented in a User Agent for identity verification.
* `expires_at` MAY contain an [RFC 3339]-encoded time after which time the **Covered Business** will no longer oblige themselves to record-keep the request under consideration.

[1]: `request_id` SHOULD be an UUID generated by the Covered Business or Privacy Infrastructure Provider immediately. This `request_id` SHOULD NOT be taken as an assumption that the **Covered Business** has received and is acting on the request, simply that the "middle layer" between has. If the Data Rights endpoints are operated directly by the Covered Business, requests SHOULD pass immediately from `open` to `in_progress`.
    
### 3.04 Schema: Identity Encapsulation

In development of this protocol a simple question with complex answers is raised repeatedly: how do we securely encode a user's identity in a way that is trustworthy to all implementing parties? This has traditionally been done in an ad-hoc fashion. In the scope of a Data Rights Protocol, this can be seen as a barrier to exercise: if a consumer has 50 companies they would like to access their data from, they should not need to complete 50 identity verification processes to exercise those rights. To that end, the parties implementing the protocol have spent some time researching the state of the art and the wider identity ecosystem and come to the following set of conclusions:

- OpenID Connect solves much of the questions around federated identity and trust, and the biggest barriers to uptake are implementation complexity and relatively early rollout of the technology. This, however, is the broad direction that federated identity on the web appears to be headed and we intend to follow that current.
- for Version 1 of the protocol the focus of development is on developing endpoints, defining the data structure of requests, defining end to end state transitions of the requests, and development of non-technical processes around this protocol.
- Implementers will work with minimal technical trust mechanisms and instead rely on an operating agreement between implementers deploying this protocol in production. See [governance.md](./governance.md). [XXX: this is still being drafted]
- Working Group intends to explore best practices in federated identity and emerging technologies like [OpenID Identity Assurance (eKYC)](https://openid.net/specs/openid-connect-4-identity-assurance-1_0-ID2.html).

Given the long-term goal of supporting OpenID Connect, protocol implementers SHALL encapsulate identity using [RFC7515-encoded JSON Web Tokens](https://datatracker.ietf.org/doc/html/rfc7515). Tokens can either be represented in their Compact Serialization or JSON Serialization representations; for complex JWTs containing sub-tokens (consider an Authorized Agent with a set of self-attested claims alongside a Covered Business-provided identity token), the JSON Serialization should be considered preferred, but for simple tokens compact serialization should be accepted. (these are purposefully NOT RFC1191 SHOULDs...)

Subject to further refinement of trust mechanisms and authorization workflow, JWTs MAY contain custom claims, and contain the following reserved and public claims:

| name                                      | description                                                                                                                                                                                                 |
|-------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `aud`                                     | audience claim MUST contain to the legal entity which is responsible for processing rights action                                                                                                           |
| `sub`                                     | if known, subject claim SHALL contain the Covered Business's preferred public identifier for the user.                                                                                                      |
| `name`                                    | if known, claim SHALL contain the user's full name most likely known by the Covered Business                                                                                                                |
| `email` or `email_verified`               | if known, claim SHALL contain the user's email address, if known. `email_verified` MUST only contain a value if this address was verified by the agent                                                      |
| `phone_number` of `phone_number_verified` | if known, claim SHALL contain the user's phone number, if known. `phone_number_verified` MUST only contain a value if this address was verified by the agent through a phone call or SMS one-time password. |
| `address`                                 | if known, claim SHALL contain the user's preferred address, if known.                                                                                                                                       |
| `address_verified`                        | this custom claim SHALL contain the user's preferred address, if that was affirmatively verified by the issuing party                                                                                       |

Covered Businesses SHALL determine for themselves the level of reliance they will place on a given token. Agents SHALL make reasonable efforts to provide trustworthy tokens, by verifying user-attested claims as possible, by attaching user-attested claims as available, and by ensuring their JWTs are signed by a key which the Covered Businesses and PIPs can verify against.

[XXX] JWTs should probably not be encrypted? managing the encryption key exchange here is very strange and necessarily happening out-of-scope of the protocol. but we already have shared-secret API authentication in [section 3.07](#307-api-authentication); I am queasy about having user tokens identity floating in the open here....

### 3.06 Error States

XXX: Todo, error states in processing, error states in POST exercise, etc...

### 3.07 API Authentication

In short:
- for v.0.3 we specify that client shared secrets will be used for authentication to all endpoints except the Data rights Discovery endpoint.
- Participating parties will need to exchange shared secrets out of band for now
  - the intention is to eventually leverage OAuth2 to secure these resources, either in concert with OIDC or out of band
- Each party MUST include an HTTP `Authorization` header in each response containing the SHA-512 hash of their secret.
- Requests which do not have an `Authorization` header MUST receive an `401` HTTP response.

## Footnotes and Errata
