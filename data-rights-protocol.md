# [Data Rights Protocol](https://github.com/consumer-reports-digital-lab/data-rights-protocol) v.0.5

**DRAFT FOR COMMENT**: Visit the [Data Rights Protocol](https://datarightsprotocol.org/) home page for details on our Data Rights Roundtable on October 19th, 2021.  To provide feedback on this draft protocol, make a [new issue](https://github.com/consumer-reports-digital-lab/data-rights-protocol/issues/new) or [pull request](https://github.com/consumer-reports-digital-lab/data-rights-protocol/pulls) in this repository or you may provide feedback through this form: [https://forms.gle/YC7nKRs3ZQMWLvw27](https://forms.gle/YC7nKRs3ZQMWLvw27).

Protocol Changes from 0.4 to 0.5:

- [new request state "denied/`too_many_requests`"](https://github.com/consumer-reports-digital-lab/data-rights-protocol/commit/14fea83a1b7856da55a2075a6233039f8a7c9c81)
- [openapi.yaml](https://github.com/consumer-reports-digital-lab/data-rights-protocol/blob/0.5/openapi.yaml) specification for PIP server interface
- [encode time-extensions in to the request status, along with a `processing_details` field](https://github.com/consumer-reports-digital-lab/data-rights-protocol/commit/f758f164e33b862e990526b8a2aafba49d777862)
- [draft minimal implementation guide](https://github.com/consumer-reports-digital-lab/data-rights-protocol/blob/0.5/implementation-guide.org)
- [draft PIP certification/conformance suite](https://github.com/consumer-reports-digital-lab/data-rights-protocol-cert/)
- [respecification of identity tokens to match OIDC Core 1.0](https://github.com/consumer-reports-digital-lab/data-rights-protocol/pull/44)

## 1.0 Introduction

This specification defines a web protocol encoding a set of standardized request/response data flows such that Users can exercise Personal Data Rights provided under regulations like the California Consumer Privacy Act, General Data Protection Regulation, and other regulatory or voluntary bases, and receive affirmative responses in standardized formats.

We aim to make the data rights protocol integrable with an ecosystem of data rights middlewares, agent services, automation tool kits, and privacy-respecting businesses which empower and build trust with consumers while driving the cost of compliance towards zero.

### 1.01 Motivation
Data Rights are increasingly becoming universal, but the method of request and protocol for communicating those requests varies and there is no universal interchange format. Companies operating under these regulatory regimes face not only technical challenges in collecting and delivering responses to users’ data rights requests but also face significant process burdens as consumers increasingly make use of these rights. At the same time, consumers find it tough to execute their data rights under new privacy laws, partially due to a lack of standardization among companies.

By providing a shared protocol and vocabulary for expressing these data rights, we aim to minimize the administrative burdens on consumers and businesses while providing a basis of trust for verifiable identity attestation which can be used by (individual) consumers (or by an agent intermediating the relationship on behalf of consumers) and businesses.


### 1.02 Scope
In this initial phase of the Data Rights Protocol, we want to enable a group of peers to form a voluntary trust network while expanding the protocol to support wider trust models and additional data flows.

Version 0.5 encodes the rights as specified in the California Consumer Privacy act of 2018, referred herein as the “CCPA”. This is further enumerated in the [Supported Rights Actions](#301-supported-rights-actions) section of this document below.

### 1.03 Terminology

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

- *User* is the individual who is exercising their rights. This User may or may not have a direct business relationship or login credentials with the Covered Business.
- *User Agent* (**UA**) is the application, software, or browser which is used by the User to mediate their interaction with the *Data Rights Protocol*. 

- *Authorized Agent* (**AA**) is a natural person or business entity that a User has authorized to act on their behalf to exercise the rights encoded in this protocol
- *Authorized Agent Interface* (**AAi**) is the software component managed by an Authorized Agent to accept ["Data Rights Status Callback" endpoint](#2041-post-status_callback-response) calls.

- *Privacy Infrastructure Provider* (**PIP**) is a business entity which provides software and process automation to enabled Covered Businesses to receive and process Data Rights Requests.
- *PIP Interface* (**PIPi**) is the software component managed by a PIP which is responsible for providing the endpoints specified in sections [2.02](#202-post-exercise-data-rights-exercise-endpoint), [2.03](#203-get-status-data-rights-status-endpoint), and [2.05](#205-post-revoke-data-rights-revoke-endpoint). In cases where the Covered Business is operating without a PIP, these components will be operated by the *Covered Business*

- *Covered Business* (**CB**) is the business entity which the *User* is exercising their rights with.
- *Covered Business Interface* (**CBi**) is the software component managed by a Covered Business to provide the [Data Rights Discovery endpoint](#201-get-well-knowndata-rightsjson-data-rights-discovery-endpoint) and MAY also provide services for user identity verification.


## 2.0 HTTP Endpoint Specification

[note about including schemas by-reference from below.]

DRP 0.5 implementors MUST support application/json request and response bodies.

[expand endpoints with their failure states]

### 2.01 `GET /.well-known/data-rights.json` ("Data Rights Discovery" endpoint)

This is the Data Rights Discovery endpoint, responding at a well-known endpoint on the Covered Business’s primary User focused domain. This [RFC8615] URI will return a JSON document conforming to this schema. This endpoint exists for Users and Authorized Agents to be able to take Data Rights Actions.

For instance, an User looking to exercise their data rights for Example, Inc. whose homepage is https://example.com/ MUST be able to GET https://example.com/.well-known/data-rights.json without knowledge of the Covered Business’s relationship to any Privacy Infrastructure Provider. 

```
{
  "version": "0.5",
  "api_base": "https://example.com/data-rights",
  "actions": ["sale:opt-out", "sale:opt-in", "access", "deletion"],
  "user_relationships": [ ... ]
}
```

- `version` field is a string carrying the version of the protocol implemented. Currently this MUST read "0.5"
- `api_base` field is a URI under which the rest of the Data Rights Protocol is accessible. This endpoint MAY be run by a Privacy Infrastructure Provider but SHOULD be accessible under the Covered Business's domains for legibility's sake.
- `actions` is a list of strings enumerating the rights which may be exercised, as outlined in [Supported Rights Actions](#301-supported-rights-actions)
- `user_relationships` is a list of strings enumerating the contexts by which a User may have a relationship with the Covered Business. The enumeration of possible relationships is left unspecified and future versions of the protocol may have more to say about them.


### 2.02 `POST /exercise` ("Data Rights Exercise" endpoint)

This is the Data Rights Exercise endpoint which Users and Authorized Agents can use to exercise enumerated data rights.

```
{
  "meta": {
    "version": "0.5"
  },
  "regime": "ccpa",
  "exercise": [
    "sale:opt-out"
  ],
  "relationships": ["customer", "marketing"],
  "identity": <jwt>... ,
  "status_callback": "https://dsr-agent.example.com/update_status"
}
```

- `meta` MUST contain only a single key `version` which contains a string referencing the current protocol version “0.5”.
- `regime` MAY contain a string specifying the legal regime under which the Data Request is being taken.  Requests which do not supply a `regime` MAY be considered for voluntary processing.
  - The legal regime is a system of applicable rules, whether enforceable by statute, regulations, voluntary contract, or other legal frameworks which prescribe data rights to the User. See [3.01 Supported Rights Actions](#301-supported-rights-actions) for more discussion.
- `exercise` MUST contain a list of rights to exercise.
- `relationships` MAY contain a list of string 'hints' for the Covered Business signaling that the Covered Business may have data of the User's outside of the expected Customer/Business relationship, and which the User would like to be considered as part of this Data Rights Exercise.
- `identity` MUST contain an [RFC7515 JWT](https://datatracker.ietf.org/doc/html/rfc7515) conforming to one of the following specifications:
  - a string containing a JWT serialized in the Compact Serialization format [RFC7515 Section 3.1]
  - a document object containing a JWT serialized in the JSON Serialization formation [RFC7515 Section 3.2]
  - See [section 3.04](#304-schema-identity-encapsulation) regarding identity encapsulation.
- `status_callback` MAY be specified with a URL that the Status Callback can be sent to. See ["Data Rights Status Callback" endpoint](#204-post-status_callback-data-rights-status-callback-endpoint).

[XXX] is exercise a list? is making multiple "requests" in a single request valid?

#### 2.02.1 `POST /exercise` Response

Responses to this request MUST adhere to the [Exercise Status Schema](#303-schema-status-of-a-data-subject-exercise-request).

### 2.03 `GET /status` ("Data Rights Status" endpoint)

This is the Data Rights Status endpoint which Users and Authorized Agents can use to query for the status of an existing data rights request. Requests to this endpoint MUST provide a single URL parameter request_id which is the Request ID for the Data Rights Request.

`GET /status?request_id=c789ff35-7644-4ceb-9981-4b35c264aac3`

#### 2.03.1 `GET /status` Response

Responses to this request MUST adhere to the [Exercise Status Schema](#303-schema-status-of-a-data-subject-exercise-request).


### 2.04 `POST $status_callback` ("Data Rights Status Callback" endpoint)

The Status Callback endpoint SHOULD be implemented by Authorized Agents which will be exercising data rights for multiple Users. This endpoint exists to remove the need for Authorized Agents to query the Data Rights Status endpoint and instead allow a “push model” where AAs are notified when a request's status changes. The destination for a Status Callback URL is specified in the initial [Data Rights Exercise](#202-post-exercise-data-rights-exercise-endpoint) request. If a Data Rights Request specifies a `status_callback` field, the Privacy Infrastructure Provider SHALL use that mechanism to notify Authorized Agents of status updates.

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

These are the CCPA rights which are encoded in v0.5 of the protocol:

| Regime | Right               | Details                                                              |
|--------|---------------------|----------------------------------------------------------------------|
| ccpa   | `sale:opt_out`      | [RIGHT TO OPT-OUT OF SALE](https://oag.ca.gov/privacy/ccpa#sectionb) |
| ccpa   | `sale:opt_in`       | RECONSENT OR OPT-IN TO DATA SALE                                     |
| ccpa   | `deletion`          | [RIGHT TO DELETE](https://oag.ca.gov/privacy/ccpa#sectione)          |
| ccpa   | `access`            | [RIGHT TO KNOW](https://oag.ca.gov/privacy/ccpa#sectionc)            |
| ccpa   | `access:categories` | [RIGHT TO KNOW](https://oag.ca.gov/privacy/ccpa#sectionc)[☆]         |
| ccpa   | `access:specific`   | [RIGHT TO KNOW](https://oag.ca.gov/privacy/ccpa#sectionc)[☆]         |

**Covered Businesses** specify which rights they support in the [Data Rights Discovery](#201-get-well-knowndata-rightsjson-data-rights-discovery-endpoint) endpoint while consumers and their agents can specify the rights they are making use of in the [Data Rights Exercise](#202-post-exercise-data-rights-exercise-endpoint) endpoint.

Requests to exercise these rights SHALL be made under either a processing `regime` of "ccpa", or on a voluntary basis by leaving the regime unspecified. The encoding of CCPA rights in this section is not to be interpreted to exclude requests made under GDPR statutes or other regional privacy or accessibility legislation; other legal regimes shall be encoded in to the protocol in future iterations.

[☆] The schema and semantics of the `access:categories` and `access:specific` rights shall be declared at a later date. Discussion in [GitHub issue #9](https://github.com/consumer-reports-digital-lab/data-rights-protocol/issues/9).

### 3.02 Request Statuses

This table shows valid states for Data Rights Requests, along with the criteria for transition into each state. Further, this table shows at which states certain fields are allowed to be *added* to a data rights request.

"Final" states are marked in the final field of the table. Requests which enter final state MAY be disregared after the lesser of the `expires_at` flag or 60 days, but no less than 7 days from when expiration was first specified.

| state       | reason                 | entrance criteria                                                   | new fields                                   | Final? |
|-------------|------------------------|---------------------------------------------------------------------|----------------------------------------------|--------|
|             |                        | user has created request, but not submitted it                      | base fields                                  |        |
| open        |                        | user has submitted request to Data Rights Endpoint[1]               | request_id                                   |        |
| in_progress |                        | CB has acknowledge receipt of request OR User solves verification   | received_at, expected_by, processing_details |        |
| in_progress | need_user_verification | CB doesn't have sufficient ID verification                          | user_verification_url, expires_at            |        |
| fulfilled   |                        | CB has finished data rights request process                         | results_url, expires_at                      | x      |
| revoked     |                        | user has explicitly actioned to revoke the request                  |                                              | x      |
| denied      | suspected_fraud        | CB or PIP believes this request was made fraudulently               | processing_details                           | x      |
| denied      | insuf_verification     | the [in_progress, need_user_verification] stage failed or timed out | processing_details                           | x      |
| denied      | no_match               | CB could not match user identity to data subject                    | processing_details                           | x      |
| denied      | claim_not_covered      | user requesting data not covered under legal bases[XXX]             | processing_details                           | x      |
| denied      | outside_jurisdiction   | user requesting data under bases they are not covered by[XXX]       | processing_details                           | x      |
| denied      | too_many_requests      | user has submitted more requests than the CB is legally obliged to process | details?
| denied      | other                  | some other unspecified failure state reached                        | processing_details                           | x      |
| expired     |                        | the time is currently after the `expires_at` in the request.        |                                              | x      |

[XXX] in the case of claim_not_covered, this may be about asking for categories of data which Covered Businesses are not required to present to the User. in the case of outside_jurisdiction, this may be because the business is not honoring CCPA requests for non-California residents and there is no other basis on which to honor the request. [#28](https://github.com/consumer-reports-digital-lab/data-rights-protocol/issues/28) for discussion on `too_many_requests`

#### 3.02.1: `need_user_verification` State Flow Semantics

When a Data Rights Request enters the `in_progress`/`need_user_verification` state, the PIPi SHALL inform the Agent through either the [Data Rights Status Callback](#2041-post-status_callback-response) or the [Data Rights Status endpoint](#203-get-status-data-rights-status-endpoint). A Data Rights Request can enter this state if the identity tokens are not already sufficiently verifiable by the Covered Business, or they could not unambiguously match the User to an account based on those tokens.

These request statuses MUST contain a `user_verification_url` string which is an HTTPS or otherwise secure URL; the user's identity token will be included in requests to that URL. The Authorized Agent is responsible for presenting the URL in the Status's `user_verification_url` with some URL parameters attached to it:

- `identity` MUST contain the same identity token presented in the original Data Rights Request, or a JWT containing the same claims
- `redirect_to` MUST contain a URL-safe encoded URL which the PIPi will redirect to upon successful identity verification.
- `request_id` MUST contain the `request_id` of the Data Rights Request under consideration.

The PIPi SHOULD provide a `user_verification_url` which refers to a unique Data Rights Request and then SHALL verify that the `request_id` specified by the Authorized Agent refers to the same Data Rights Request before presenting a verification.

The PIPi SHOULD NOT redirect the user back to the Authorized Agent's `redirect_to` URL when the user verification fails or is canceled, but the Authorized Agent SHOULD NOT assume that loading that URL is enough to assume the verification is complete and request is ready to proceed; they should query the [Data Rights Status endpoint](#203-get-status-data-rights-status-endpoint) or wait for a Status callback.

### 3.03 Schema: Status of a Data Subject Exercise Request

A single JSON object is used to describe any existing Data Exercise Request and is referred to as the Exercise Status object:

```
{
  "request_id": "c789ff35-7644-4ceb-9981-4b35c264aac3",
  "received_at": "20210902T152725.403-0700",
  "expected_by": "20211015T152725.403-0700",
  "processing_details": "this user has many records",
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
* `expected_by` SHOULD contain a date before which the Authorized Agent can expect to see an update on the status of the Data Rights Request. This field should conform to the legal regime's deadline guidances, and may be amended by the PIP or Covered Business according to those same regulations. `processing_details` MUST be updated to reflect the reason for this extension. 
* `processing_details` MAY contain a string reflecting the state of the Data Rights Request so that the Agent may communicate this state to the End User.
* `user_verification_url` MAY contain a URI which can be presented in a User Agent for identity verification.
* `expires_at` MAY contain an [RFC 3339]-encoded time after which time the **Covered Business** will no longer oblige themselves to record-keep the request under consideration.

[1]: `request_id` SHOULD be an UUID generated by the Covered Business or Privacy Infrastructure Provider immediately. This `request_id` SHOULD NOT be taken as an assumption that the **Covered Business** has received and is acting on the request, simply that the "middle layer" between has. If the Data Rights endpoints are operated directly by the Covered Business, requests SHOULD pass immediately from `open` to `in_progress`.

    
### 3.04 Schema: Identity Encapsulation

In development of this protocol a simple question with complex answers is raised repeatedly: how do we securely encode a user's identity in a way that is trustworthy to all implementing parties? This has traditionally been done in an ad-hoc fashion. In the scope of a Data Rights Protocol, this can be seen as a barrier to exercise: if a consumer has 50 companies they would like to access their data from, they should not need to complete 50 identity verification processes to exercise those rights. To that end, the parties implementing the protocol have spent some time researching the state of the art and the wider identity ecosystem and come to the following set of conclusions:

- OpenID Connect solves much of the questions around federated identity and trust, and the biggest barriers to uptake are implementation complexity and relatively early rollout of the technology. This, however, is the broad direction that federated identity on the web appears to be headed and we intend to follow that current.
- for Version 1 of the protocol the focus of development is on developing endpoints, defining the data structure of requests, defining end to end state transitions of the requests, and development of non-technical processes around this protocol.
- Implementers will work with minimal technical trust mechanisms and instead rely on an operating agreement between implementers deploying this protocol in production. See [System Rules](./governance.md) documentation. [XXX: this is still being drafted]
- Working Group intends to explore best practices in federated identity and emerging technologies like [OpenID Identity Assurance (eKYC)](https://openid.net/specs/openid-connect-4-identity-assurance-1_0-ID2.html).

Given the long-term goal of supporting OpenID Connect, protocol implementers SHALL encapsulate identity using [RFC7515-encoded JSON Web Tokens](https://datatracker.ietf.org/doc/html/rfc7515). Tokens can either be represented in their Compact Serialization or JSON Serialization representations; for complex JWTs containing sub-tokens (consider an Authorized Agent with a set of self-attested claims alongside a Covered Business-provided identity token), the JSON Serialization should be considered preferred, but for simple tokens compact serialization should be accepted. (these are purposefully NOT RFC1191 SHOULDs...)

Subject to further refinement of trust mechanisms and authorization workflow, JWTs MAY contain custom claims, and contain the following [OIDC Standard Claims](https://openid.net/specs/openid-connect-core-1_0.html#rfc.section.5.1):

| name                    | type    | description                                                                                                                                                                                              |
|-------------------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `aud`                   | str     | audience claim MUST contain reference to the legal entity which is responsible for processing rights action                                                                                              |
| `sub`                   | str     | if known, subject claim SHALL contain the Covered Business's preferred public identifier for the user, for example a user-name or account email address.                                                 |
| `name`                  | str     | if known, claim SHALL contain the user's full name most likely known by the Covered Business                                                                                                             |
| `email`                 | str     | if known, claim SHALL contain the user's email address.                                                                                                                                                  |
| `email_verified`        | bool    | if the user's email address has been affirmatively verified according to the level of assurance specified in the System Rules, this field SHALL be specified as `true`                                |
| `phone_number`          | str     | if known, claim SHALL contain the user's phone number in E.164 encoding.                                                                                                                                 |
| `phone_number_verified` | bool    | if the user's phone number has been affirmatively verified according to the level of assurance specified in the System Rules, this field SHALL be specified as `true`                                 |
| `address`               | address | if known, claim SHALL contain the user's preferred address. This claim is specified fully in [OpenID Connect Core 1.0 section 5.1.1](https://openid.net/specs/openid-connect-core-1_0.html#AddressClaim) |
| `address_verified`      | bool    | if the user's address has been affirmatively verified according to the level of assurance specified in the System Rules, this field SHALL be specified as `true`                                      |
| `power_of_attorney`     | str     | this custom claim MAY contain a reference to a User-signed document delegating power of attorney to the submitting AA. Implementation details of this claim will be defined later.                       |

Covered Businesses SHALL determine for themselves the level of reliance they will place on a given token. Authorized Agents SHALL make reasonable efforts to provide trustworthy tokens, by verifying user-attested claims according to the practices agreed under the System Rules, by attaching user-attested claims as available, and by ensuring their JWTs are signed by a key which the Covered Businesses and PIPs can verify against.

[XXX] JWTs should probably not be encrypted? managing the encryption key exchange here is very strange and necessarily happening out-of-scope of the protocol. but we already have shared-secret API authentication in [section 3.07](#307-api-authentication); I am queasy about having user tokens identity floating in the open here....

[XXX] discussion about what happens in `need_user_verification` stage; it would be nice if the UA could specify a redirect URL to return back to the app.

### 3.06 Error States

Servers SHALL respond with HTTP 200 response codes when requests are processed successfully. In exceptional cases, servers SHALL respond with non-200 response codes and an `application/json` body with the following keys:

- `code` MUST contain a string encoding of the HTTP response code for clients which cannot process the headers. 
- `message` MUST contain a string explaining the nature of the error.
- `fatal` MAY contain a Boolean value of `true` if the request will move to a `denied`/`other` state. Requests which are not `fatal` shall be assumed to be retryable.

```
{
  "code": "400",
  "message": "Unsupported rights actions submitted."
}
```

PIPi servers MAY signal that an existing request will no longer be processed due to this error. PIPi SHOULD move the request to a `denied`/`other` state and call the [Status Callback endpoint](#204-post-status_callback-data-rights-status-callback-endpoint) accordingly.

Error codes are purposefully under-specified at the moment -- servers SHALL make a best effort to map to known 4XX and 5XX codes.

Note that these error states only represent *request errors*; workflow errors SHOULD be specified in the request status fields.

### 3.07 API Authentication

In short:
- for v.0.5 we specify that client shared secrets will be used for authentication to all endpoints except the Data rights Discovery endpoint.
- Participating parties will need to exchange shared secrets out of band for now
  - the intention is to eventually leverage OAuth2 to secure these resources, either in concert with OIDC or out of band
- Each party MUST include an HTTP `Authorization` header in each response containing the SHA-512 hash of their secret.
- Requests which do not have an `Authorization` header MUST receive an `401` HTTP response.

### 3.08 Processing Extensions & "Expected By" dates

When a Covered Business acknowledges receipt of a Data Rights Request and moves it in to `in_progress` state, the request's `expected_by` field SHOULD be populated based on either an estimate provided by the Covered Business or the deadline prescribed by the legal regime the request is submitted under. Consider, for example, [California's legal regime](https://transcend.io/laws/cpra/#section-15) prescribes up to 90 days extension so long as they are made within 45 days; If a request is extended, this request must also be extended with a `processing_details` field detailing a reason for the Request's extension to notify the consumer of this delay. The intent of the `processing_details` field is to add additional color to already-defined `state`/`reason` combinations. States which cannot be encoded without reaching for free-form text should be integrated in to the state transition table.

When applying changes to Data Rights Requests in this fashion, the Privacy Infrastructure Provider SHALL attempt to notify the Authorized Agent using the [Data Rights Status Callback](#2041-post-status_callback-response).

## 4.0 Protocol Roadmap

In its current implementation, DRP should not be used to process data of Users who are not involved in the implementers group. There are known shortcomings in security, privacy, and identity verification that will need to be solved before a "1.0" protocol version which is suitable for production-ready systems.

- Governance and operating model
- Protocol Compliance suite
- OIDC identity provider flows
- Secure OAuth2 client authentication (eg [FAPI baseline security profile](https://openid.net/specs/openid-financial-api-part-1-1_0.html))
- Successful DRP pilot between multiple Agents and Covered Businesses

## Specification Change Log

In general, please put major change log items at the top of the file. When a new protocol version is "cut", move the previous versions' change log down here.

Protocol Changes from 0.3 to 0.4:

- [relationship hints](https://github.com/consumer-reports-digital-lab/data-rights-protocol/pull/17) allow users and agents to provide "hints" for the type of customer relationship, or a set of subsidiary brands to query.
- [shift in language from regulatory framework to broader legal bases](https://github.com/consumer-reports-digital-lab/data-rights-protocol/pull/16)
- [medium-term protocol development road-map](https://github.com/consumer-reports-digital-lab/data-rights-protocol/pull/21)

Changes in v0.2 to v0.3:
- donotsell -> sale:opt-in opt-out
- terminology changes
- Request status chart
- identity tiger team recommendations
- API Authentication details
- Moved non-essential sections out of protocol spec

## Footnotes and Errata

