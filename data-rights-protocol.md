# [Data Rights Protocol](https://github.com/consumer-reports-innovation-lab/data-rights-protocol) v.0.9

**DRAFT FOR COMMENT**: To provide feedback on this draft protocol, make a [new issue](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/issues/new) or [pull request](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/pulls) in this repository or you may provide feedback by emailing <b>datarightsprotocol@cr.consumer.org</b>.

Protocol Changes from 0.8 to 0.9:

- Remove obsolete references to JWT/IANA specification for identity attributes in favor of schema.org
- Specify the shape of Business and Authorized Agent entities in the DRP Service Directory
- Remove obsolete Data Rights Discovery endpoint (`/.well-known/data-rights.json`)

## 1.0 Introduction

This specification defines a web protocol encoding a set of standardized request/response data flows such that Users can exercise Personal Data Rights provided under regulations like the California Consumer Privacy Act, General Data Protection Regulation, and other regulatory or voluntary bases, and receive affirmative responses in standardized formats.

We aim to make the data rights protocol integrable with an ecosystem of data rights middlewares, agent services, automation tool kits, and privacy-respecting businesses which empower and build trust with consumers while driving the cost of compliance towards zero.

### 1.01 Motivation

Data Rights are increasingly becoming universal, but the method of request and protocol for communicating those requests varies and there is no universal interchange format. Companies operating under these regulatory regimes face not only technical challenges in collecting and delivering responses to users’ data rights requests but also face significant process burdens as consumers increasingly make use of these rights. At the same time, consumers find it tough to execute their data rights under new privacy laws, partially due to a lack of standardization among companies.

By providing a shared protocol and vocabulary for expressing these data rights, we aim to minimize the administrative burdens on consumers and businesses while providing a basis of trust for verifiable identity attestation which can be used by (individual) consumers (or by an agent intermediating the relationship on behalf of consumers) and businesses.


### 1.02 Scope

In this initial phase of the Data Rights Protocol, we want to enable a group of peers to form a voluntary trust network while expanding the protocol to support wider trust models and additional data flows.

Version 0.9 encodes the rights as specified in the California Consumer Privacy act of 2018, referred herein as the “CCPA”. This is further enumerated in the [Supported Rights Actions](#301-supported-rights-actions) section of this document below.

### 1.03 Terminology

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

- *User* is the individual who is exercising their rights. This User may or may not have a direct business relationship or login credentials with the Covered Business.
- *User Agent* (**UA**) is the application, software, or browser which is used by the User to mediate their interaction with the *Data Rights Protocol*.
- *Authorized Agent* (**AA**) is an entity (most likely a business or nonprofit organization) that a User has authorized to act on their behalf to exercise the rights encoded in this protocol and to accept status callbcks by implementing the ["Data Rights Status Callback" endpoint](#2041-post-status_callback-response).
- *Covered Business* (**CB**) is the business entity which the *User* is exercising their rights with.
- A *Privacy Infrastucture Provider* (**PIP**) is responsible for providing the endpoints specified in sections [2.02](#202-post-exercise-data-rights-exercise-endpoint), [2.03](#203-get-status-data-rights-status-endpoint), [2.05](#205-post-revoke-data-rights-revoke-endpoint), and [Data Rights Discovery endpoint](#201-get-well-knowndata-rightsjson-data-rights-discovery-endpoint).  These may either be implemented by a third-party service provider with whom a Covered Business contracts to process incoming Data Rights Requests on their behalf, or directly by the Covered Business.

## 2.0 HTTP Endpoint Specification

[note about including schemas by-reference from below.]

DRP 0.9 implementors MUST support text/plain requests and application/json responses for signed POST an DELETE requests

[expand endpoints with their failure states]

### 2.01 `POST /v1/data-rights-request/` ("Data Rights Exercise" endpoint)

This is the Data Rights Exercise endpoint which Users and Authorized Agents can use to exercise enumerated data rights.

A Data Rights Exercise request SHALL contain a JSON-encoded message body containing the following fields, with a `libsodium`/`NaCl`/`ED25119` binary signature immediately prepended to it[^1], and then base64 encoded. The decoded, verified JSON body SHALL be structured as follows:


```
{
  # 1
  "agent-id": "aa-id",
  "business-id": "cb-id",
  "expires-at": "<ISO 8601 Timestamp>",
  "issued-at":  "<ISO 8601 Timestamp>",

  # 2
  "drp.version": "0.9"
  "exercise": "sale:opt-out",
  "regime": "ccpa",
  "relationships": ["customer", "marketing"],
  "status_callback": "https://dsr-agent.example.com/update_status"

  # 3
  # claims in schema.org/Person
  # https://schema.org/Person
}
```

These keys identify the Authorized Agent making the request and the Covered Business of whom the request is being made, the time the request is being made, and the duration for which it will be valid.  Taken together, they describe where trust in the request is rooted (the AA), and aim to constrain the scope of the Data Rights Request to a single AA-CB relationship at a particular moment in time in order to prevent re-use or mis-use of the request by any party.
- `agent-id` MUST contain a string identifying the Authorized Agent which is submitting the data rights request and attesting to its validity, particularly that they have validated the identity of the user submitting the request to the standards of the network.
- `business-id` MUST contain a string identifying the *Covered Business* which the request is being sent to. These identifiers will be shared out-of-band by participants but will eventually be represented in a Service Directory managed by a DRP consortium or working group.
- `expires-at` MUST contain an ISO 8601-encoded timestamp expressing when the request should no longer be considered viable. This should be kept short, we recommend no more than 15 minute time windows to prevent re-use while still allowing for backend-processing delays in the Privacy Infrastructure Provider pipeline. Privacy Infrastructure Providers SHOULD discard requests made at a time after this value and respond with a `fatal` Error State.
- `issued-at` MUST contain an ISO 8601-encoded timestamp expressing when the request was *created*.

The second grouping contains data about the Data Rights Request.
- `drp.version` MUST contain a string referencing the current protocol version "0.9".
- `exercise` MUST contain a string specifying the [Rights Action](#301-supported-rights-actions) which is to be taken by the Covered Business.
- `regime` MAY contain a string specifying the legal regime under which the Data Request is being taken.  Requests which do not supply a `regime` MAY be considered for voluntary processing.
  - The legal regime is a system of applicable rules, whether enforceable by statute, regulations, voluntary contract, or other legal frameworks which prescribe data rights to the User. See [3.01 Supported Rights Actions](#301-supported-rights-actions) for more discussion.
- `relationships` MAY contain a list of string 'hints' for the Covered Business signaling that the Covered Business may have data of the User's outside of the expected Customer/Business relationship, and which the User would like to be considered as part of this Data Rights Exercise.
- `status_callback` MAY be specified with a URL that the Status Callback can be sent to. See ["Data Rights Status Callback" endpoint](#204-post-status_callback-data-rights-status-callback-endpoint).

The JSON object may contain any other [IANA JSON Web Token Claims](https://www.iana.org/assignments/jwt/jwt.xhtml#claims) but minimally must contain the claims outlined in [section 3.04](#304-schema-identity-encapsulation) regarding identity encapsulation.

This request SHALL contain an Bearer Token header containing the key for this AA-CB pairwise relationship in it in the form `Authorization: Bearer <token>`. This token is generated by calling `POST /agent/{id}` in section 2.06.

The Privacy Infrastructure Provider SHALL validate the message is signed according to the guidance in section 3.07.

#### 2.01.1 `POST /v1/data-rights-request` Response

Responses to this request MUST adhere to the [Exercise Status Schema](#303-schema-status-of-a-data-subject-exercise-request).

### 2.02 `GET /v1/data-rights-request/{request_id}` ("Data Rights Status" endpoint)

This is the Data Rights Status endpoint which Users and Authorized Agents can use to query for the status of an existing data rights request.

This request SHALL contain an Bearer Token header containing the key for this AA-CB pairwise relationship in it in the form `Authorization: Bearer <token>`. This token is generated by calling `POST /agent/{id}` in section 2.06.

#### 2.02.1 `GET /v1/data-rights-request/{request_id}` Response

Responses to this request MUST adhere to the [Exercise Status Schema](#303-schema-status-of-a-data-subject-exercise-request).

Privacy Infrastructure Providers SHALL take care to respond affirmatively only if the Authorized Agent associated with the Bearer Token is the agent which is managing the `requeset_id`-referenced request. If the requesting agent is not responsible for managing the requested resource, Privacy Infrastructure Providers SHALL respond with a `403 Forbidden`.

### 2.03 `POST $status_callback` ("Data Rights Status Callback" endpoint)

The Status Callback endpoint SHOULD be implemented by Authorized Agents which will be exercising data rights for multiple Users. This endpoint exists to remove the need for Authorized Agents to query the Data Rights Status endpoint and instead allow a “push model” where AAs are notified when a request's status changes. The destination for a Status Callback URL is specified in the initial [Data Rights Exercise](#202-post-exercise-data-rights-exercise-endpoint) request. If a Data Rights Request specifies a `status_callback` field, the Privacy Infrastructure Provider SHALL use that mechanism to notify Authorized Agents of status updates.

The request body MUST adhere to the [Exercise Status Schema](#303-schema-status-of-a-data-subject-exercise-request).

#### 2.03.1 `POST $status_callback` Response

Privacy Infrastructure Providers SHOULD make a best effort to ensure that a 200 response is issued by the Authorized Agent for the most recent status update. The body of the callback's response SHOULD be discarded and not be considered for parsing by the Covered Business.

### 2.04 `DELETE /v1/data-rights-request/{request_id}` ("Data Rights Revoke" endpoint)

An Authorized Agent SHALL provide Users with a mechanism to request cancellation of an open or in progress request by sending a Data Rights Revoke request containing a JSON-encoded message body containing the following fields, with a `libsodium`/`NaCl`/`ED25119` binary signature immediately prepended to it[^1], and then base64 encoded. The decoded, verified JSON body SHALL be structured as follows:

```
{
  "reason": "i don't want my account deleted"
}
```

Requests to this endpoint contain a single field:
- `reason` MAY contain a user provided reason for the request to be not processed.

This request SHALL contain an Bearer Token header containing the key for this AA-CB pairwise relationship in it in the form `Authorization: Bearer <token>`. This token is generated by calling `POST /agent/{id}` in section 2.06.

The Privacy Infrastructure Provider SHALL validate the message is signed according to the guidance in section 3.07.

#### 2.04.1 `DELETE /v1/data-rights-request/{request_id}` response

Responses to this request MUST adhere to the [Exercise Status Schema](#303-schema-status-of-a-data-subject-exercise-request). Responses MUST contain the *new* `revoked` state.

### 2.05 `POST /v1/agent/{agent-id}` ("Pair-wise Key Setup" endpoint)

This endpoint allows the Data Rights Protocol network to operate without pre-shared API tokens or client secrets by providing Authorized Agents a method to generate API tokens for Privacy Infrastructure Providers by POSTing a message signed with a key whose public portion resides in a trustworthy registry.

These keys will allow the Privacy Infrastructure Provider to disambiguate the Data Rights Request's submitting Agent for cryptographic verification purposes, request routing, and rate limiting. See section 3.07 below for a full discussion.

This request consists of a single signed message following the same validation semantics as the Data Rights Exercise endpoint laid out in in section 3.07.1, with the signed object being a JSON message with the following keys:

```
{
  "agent-id": "aa-id",
  "business-id": "cb-id",
  "expires-at": "<ISO 8601 Timestamp>",
  "issued-at":  "<ISO 8601 Timestamp>"
}
```

These keys listed in this message MUST follow the same semantics outlined in section 2.02, and SHALL be validated using the same chain as described in section 3.07, with the following proviso:

Because there will be no Bearer Token associated with this request, presenting an agent-id in the request will be necessary for callers to disambiguate to a single public key to validate the message with. The `agent-id` presented in the URL parameters MUST match the `agent-id` key within the signed message, and the signing identity MUST map back to the `agent-id` in the Authorized Agent Service Directory. Once the signature has been verified in this manner, the rest of the keys will be validated in the fashion outlined in 3.07.

#### 2.05.1 `POST /v1/agent/{agent-id}` Response

After validating the signature and semantics of the request, the Privacy Infrastructure Provider SHALL return the following JSON response:


```
{
  "agent-id": "presented-agent-id",
  "token": "<str>"
}
```

- the `agent-id` key SHALL match the `agent-id` presented in the signed request.
- the `token` SHALL be a string which Authorized Agents SHALL present in subsequent authenticated requests. PIPs SHOULD generate this token using a cryptographically secure source such as `libsodium`'s CSPRNG. Authorized Agents SHALL treat this token as an opaque string.

Agents SHALL present this token as an HTTP Bearer Token in any request made against resources **on the same domain** this request was submitted to.

If the validation failed, the Privacy Infrastructure Provider SHALL return an `HTTP 403 Forbidden` response with no response body. The Authorized Agent and Privacy Infrastructure Provider SHOULD resolve this issue out of band utilizing the Technical Contact Address in the Data Rights Network Directory.

### 2.06 `GET /v1/agent/{agent-id}` ("Agent Information" endpoint)

This endpoint is provided by Privacy Infrastructure Providers to allow Authorized Agents to ensure that their Bearer Token is still valid without querying stateful endpoints.

This request SHALL contain an Bearer Token header containing the key for this AA-CB pairwise relationship in it in the form `Authorization: Bearer <token>`. This token is generated by calling `POST /agent/{id}` in section 2.06.

#### 2.06.1 `GET /v1/agent/{agent-id}` Response

This request currently does not *need* to return anything more than an empty JSON document and HTTP 200 response code, but may be extended at a later date.

```
{}
```

If the `agent-id` presented in the REST URL argument does not match the presented Bearer Token, the Privacy Infrastructure Provider MUST return a `403 Forbidden` response.

## 3.0 Data Schemas

These Schemas are referenced in Section 2 outlining the HTTP endpoints and their semantics.

### 3.01 Supported Rights Actions

These are the CCPA rights which are encoded in v0.9 of the protocol:

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

[☆] The schema and semantics of the `access:categories` and `access:specific` rights shall be declared at a later date. Discussion in [GitHub issue #9](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/issues/9).

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
| denied      | claim_not_covered      | user requesting data not covered under legal bases[2]             | processing_details                           | x      |
| denied      | outside_jurisdiction   | user requesting data under bases they are not covered by[2]       | processing_details                           | x      |
| denied      | too_many_requests      | user has submitted more requests than the CB is legally obliged to process | details?
| denied      | other                  | some other unspecified failure state reached                        | processing_details                           | x      |
| expired     |                        | the time is currently after the `expires_at` in the request.        |                                              | x      |

[2]: In the case of claim_not_covered, this may be about asking for categories of data which Covered Businesses are not required to present to the User. In the case of outside_jurisdiction, this may be because the business is not honoring CCPA requests for non-California residents and there is no other basis on which to honor the request. See [#28](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/issues/28) for discussion on `too_many_requests`.

#### 3.02.1: `need_user_verification` State Flow Semantics

*This has not been implemented or explored by any DRP implementers. If the need for this arises in your implementation, please reach out to DRP protocol developers to work towards implementation and improvement.* There is a alternate proposal for machine-legible signaling preferred/required attributes before the request is submitted in [github #52](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/issues/52).

This `need_user_verification` flow allows a Covered Business to signal to the User that additional User attributes or actions are necessary to confirm or match the identity of the User to an account. The Authorized Agent will navigate the User to a URL specified by the Privacy Infrastructure Provider which will provide the necessary interface to resolve this identification issue.

When a Data Rights Request enters the `in_progress`/`need_user_verification` state, the PIP SHALL inform the Agent through either the [Data Rights Status Callback](#2041-post-status_callback-response) or the [Data Rights Status endpoint](#203-get-status-data-rights-status-endpoint). A Data Rights Request can enter this state if the identity tokens are not already sufficiently verifiable by the Covered Business, or they could not unambiguously match the User to an account based on those tokens.

These request statuses MUST contain a `user_verification_url` string which is an HTTPS or otherwise secure URL; the user's identity token will be included in requests to that URL. The Authorized Agent is responsible for presenting the URL in the Status's `user_verification_url` with some URL parameters attached to it:

- `redirect_to` MUST contain a URL-safe encoded URL which the PIP will redirect to upon successful identity verification.
- `request_id` MUST contain the `request_id` of the Data Rights Request under consideration.

The PIP SHOULD provide a `user_verification_url` which refers to a unique Data Rights Request and then SHALL verify that the `request_id` specified by the Authorized Agent refers to the same Data Rights Request before presenting a verification.

The PIP SHOULD NOT redirect the user back to the Authorized Agent's `redirect_to` URL when the user verification fails or is canceled, but the Authorized Agent SHOULD NOT assume that loading that URL is enough to assume the verification is complete and request is ready to proceed; they should query the [Data Rights Status endpoint](#203-get-status-data-rights-status-endpoint) or wait for a Status callback.

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
* `received_at` SHOULD contain a string which is the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)-encoded time which the initial request was registered by the Covered Business.
  * When a Covered Business receives a request, this field MUST be present.
* `expected_by` SHOULD contain a date before which the Authorized Agent can expect to see an update on the status of the Data Rights Request. This field should conform to the legal regime's deadline guidances, and may be amended by the PIP or Covered Business according to those same regulations. `processing_details` MUST be updated to reflect the reason for this extension.
* `processing_details` MAY contain a string reflecting the state of the Data Rights Request so that the Agent may communicate this state to the End User.
* `user_verification_url` MAY contain a URI which can be presented in a User Agent for identity verification.
* `expires_at` MAY contain an [ISO 8601]-encoded time after which time the **Covered Business** will no longer oblige themselves to record-keep the request under consideration.

[1]: `request_id` SHOULD be an UUID generated by the Covered Business or Privacy Infrastructure Provider immediately. This `request_id` SHOULD NOT be taken as an assumption that the **Covered Business** has received and is acting on the request, simply that the "middle layer" between has. If the Data Rights endpoints are operated directly by the Covered Business, requests SHOULD pass immediately from `open` to `in_progress`.


### 3.04 Schema: Identity Encapsulation

In development of this protocol a simple question with complex answers is raised repeatedly: how do we securely encode a user's identity in a way that is trustworthy to all implementing parties? This has traditionally been done in an ad-hoc fashion. In the scope of a Data Rights Protocol, this can be seen as a barrier to exercise: if a consumer has 50 companies they would like to access their data from, they should not need to complete 50 identity verification processes to exercise those rights. To that end, the parties implementing the protocol have spent some time researching the state of the art and the wider identity ecosystem and come to the following set of conclusions:

- Federated trust models introduce a technical and operational complexity for protocol implementers that does not match the risk and effort required to identify users within the system.
- No Implementers within the Data Rights Protocol network are currently building on top of OIDC for their Users' identity management.
- OIDC eKYC and their federated KYC networks are still pretty far off and building version 1.0 protocol around this design ideology doesn't make as much sense as being pragmatic about identity verification.
- Authorized Agents involved in the Data Rights Protocol Network will act within a closed trust network for the forseeable future.
- Implementers will work with minimal technical trust mechanisms and instead rely on an operating agreement between implementers deploying this protocol in production. See [System Rules](./governance.md) documentation. [XXX: this is still being drafted]
- for Version 1 of the protocol the focus of development is on developing endpoints, defining the data structure of requests, defining end to end state transitions of the requests, and development of non-technical processes around this protocol.
- Working Group continues to track federated identity work and emerging technologies like [OpenID Identity Assurance (eKYC)](https://openid.net/specs/openid-connect-4-identity-assurance-1_0-ID2.html).

Subject to further refinement of trust mechanisms and authorization workflow, Requests MAY contain custom claims, but SHOULD contain the following [schema.org/Person](https://schema.org/Person):

| name                    | type    | description                                                                                                                                                                                              |
|-------------------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`                  | str     | if known, claim SHALL contain the user's full name most likely known by the Covered Business                                                                                                             |
| `email`                 | str     | if known, claim SHALL contain the user's email address.                                                                                                                                                  |
| `email_verified`        | bool    | if the user's email address has been affirmatively verified according to the level of assurance specified in the System Rules, this field SHALL be specified as `true`                                |
| `phone_number`          | str     | if known, claim SHALL contain the user's phone number in E.164 encoding.                                                                                                                                 |
| `phone_number_verified` | bool    | if the user's phone number has been affirmatively verified according to the level of assurance specified in the System Rules, this field SHALL be specified as `true`                                 |
| `address`               | address | if known, claim SHALL contain the user's preferred address. This claim is specified fully in [OpenID Connect Core 1.0 section 5.1.1](https://openid.net/specs/openid-connect-core-1_0.html#AddressClaim) |
| `address_verified`      | bool    | if the user's address has been affirmatively verified according to the level of assurance specified in the System Rules, this field SHALL be specified as `true`                                      |
| `power_of_attorney`     | str     | this custom claim MAY contain a reference to a User-signed document delegating power of attorney to the submitting AA. Implementation details of this claim will be defined later.                       |

Covered Businesses SHALL determine for themselves the level of reliance they will place on a given token. Authorized Agents SHALL make reasonable efforts to provide trustworthy tokens, by verifying user-attested claims according to the practices agreed under the System Agreement, by attaching user-attested claims as available, and by ensuring their envelopes are signed by a key which the Covered Businesses and PIPs can verify against.

### 3.05 Schema: Agent/Business Discovery Documents

The pre-1.0 design of the Data Rights Protocol envisioned it as a public network driven by a "`well-known`" resource the "Data Rights Discovery" endpoint. As the development of the protocol and implementations has progressed, this model has shown a number of limitations which in 2022 we began to address in the [Draft DRP Security Model](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/blob/main/files/2022-June-14%20Draft%20DRP%20Security%20Model.pdf) document. 

The model of the current DRP is a closed network with fairly low barrier to entry where Agents provide a cryptographic key and process accountability information to the DRP operators, and businesses provide the information previously hosted by the `well-known` resources to the same operators, and the operators provide a pair of JSON documents which list all agents and all businesses represented under the network. 

This inversion of the model makes discovery of new businesses trivial, and provides a trust-root for the cryptographic tokens which Data Rights Requests rely on. Future iterations of the DRP may open up the design of the network  as consumer identity technologies evolve and as the network itself evolves. To protect the personal information of technical and business contacts the service directory itself is left as an semi-private repository accessible to DRP implementers.

#### 3.05.1 Agent Discovery Document Schema

These entities act as the "root of trust" for Data Rights Requests and Pairwise Key Setup requests; requests are signed with the private key paired with the `verify_key` in this document. The other keys contain information about the business.

Here is an example of the JSON document with description of each entity:

```
{
    "id": "unique identifier matching [A-Z_]+ regular expression",
    "name": "Consumer Legible Agent App Name",
    "verify_key": "Hex encoded Libsodium public verifying key for signed requests",
    "web_url": "business's homepage",
    "technical_contact": "an email contact for the techical integration",
    "business_contact": "an email address for contacting a person within the business who is knowledgeable about the privacy program and DRP integration",
    "identity_assurance_url": "a link to an HTML or PDF document describing the process the agent enacts to verify a consumer's identity; a signed request containing these identities should be understood to have gone through this process."
}
```

Here is a JSON-Schema document describing a single entry in the Authorized Agent directory:

```
{
    "$id": "https://sd.datarightsprotocol.org/agent.schema.json",
    "type": "object",
    "properties": {
        "id": { "type": "string", "pattern": "[A-Z_]+" },
        "name": { "type": "string" },
        "verify_key": { "type": "string", "pattern": "[A-Fa-f0-9]+" },
        "web_url": { "type": "string", "pattern": "https://[a-z./-]+" },
        "identity_assurance_url": { "type": "string", "pattern": "https://[a-z./-]+" },
        "technical_contact": { "type": "string" },
        "business_contact": { "type": "string" }
    }
}
```

#### 3.05.2 Business Discovery Document Schema

These entities are used by Authorized Agents to discover businesses which accept DRP requests and which types of requests.

Here is an example of the JSON document with description of each entity:

```
{
    "id": "unique identifier matching [A-Z_]+ regular expression",
    "name": "Consumer Legible Business Name",
    "logo": "https link to hi-res or vector image square logo suitable for display in agent app",
    "api_base": "URL to DRP API base",
    "supported_actions": ["list", "of", "drp", "request types"],
    "web_url": "business's homepage",
    "technical_contact": "an email contact for the techical integration. this may be a contact at a PIP which the business has delegated to",
    "business_contact": "an email address for contacting a person within the business who is knowledgeable about the privacy program and DRP integration"
}
```

Here is a JSON-Schema document describing a single entry in the Covered Business directory:

```
{
    "$id": "https://sd.datarightsprotocol.org/business.schema.json",
    "type": "object",
    "properties": {
        "id": { "type": "string", "pattern": "[A-Z_]+" },
        "name": { "type": "string" },
        "logo": { "type": ["null", "string"] },
        "api_base": { "type": "string", "pattern": "https://[a-z/.-]+" },
        "supported_actions": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "access", "deletion",
                    "sale:opt_out", "sale:opt_in",
                    "access:categories", "access:specific"
                ]
            }
        },
        "privacy_policy_url": { "type": "string", "pattern": "https://[a-z/.-]+" },
        "web_url": { "type": "string", "pattern": "https://[a-z/.-]+" },
        "technical_contact": { "type": "string" },
        "business_contact": { "type": "string" }
    }
}
```

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

PIP servers MAY signal that an existing request will no longer be processed due to this error. PIP SHOULD move the request to a `denied`/`other` state and call the [Status Callback endpoint](#204-post-status_callback-data-rights-status-callback-endpoint) accordingly.

Error codes are purposefully under-specified at the moment -- servers SHALL make a best effort to map to known 4XX and 5XX codes.

Note that these error states only represent *request errors*; workflow errors SHOULD be specified in the request status fields.

### 3.07 API Authentication

The ultimate design of this API is to allow Covered Businesses to join the network, and immediately have the ability to process automated requests from trusted Authorized Agents, and for those Agents to discover new businesses participating in the network. Key to this is the idea that pre-exchanging secrets and establishing business relationships should be a technical process back-stopped by the business rules of participating in the network. Thus, the network will be primarily secured by **modern public key cryptography signatures** commonly known as Ed25519. There are multiple implementations and language bindings for this algorithm starting from [the public domain, patent un-encumbered NaCl and libsodium](https://en.wikipedia.org/wiki/NaCl_(software)) software APIs which shall ensure that all members of the network are able to integrate simple, secure, high-level cryptographic APIs.  Implementers are STRONGLY ENCOURAGED to use libsodium.

We do, however, understand that the needs of an API Authentication extend beyond purely on the security aspects, towards rate-limiting, request routing, and the like so this version of the Data Rights Protocol includes a `POST /agent/{id}` API which is used to generate API Bearer Tokens which can be used to identify the agent submitting a request, load the associated public key, and bootstrap a message validation algorithm:

Privacy Infrastructure Providers MUST validate the message in this order:
- That the message decodes from a base64 request in to a binary buffer.
- That the signature at the beginning of that buffer validates to the key associated with the out of band Authorized Agent identity presented in the Bearer Token.
  - This link between the signing body and the Service Directory is the root of the chain of trust.
- That the Authorized Agent specified in the `agent-id` claim in the request matches the Authorized Agent associated with the presented Bearer Token
  - This is very important to prevent requests generated by one AA from being reused by another AA.
- That they are the Covered Business specified inside the `business-id` claim
  - This is very important to prevent requests originally destined for one CB from being resent to other CBs
- That the current time is after the Timestamp `issued-at` claim
  - This is a very important check for clock-skew, to ensure that requests aren't being generated with expiration times far in the future because the clock of the system generating the requests is running fast.
- That the current time is before the Expiration `expires-at` claim
  - This is very important to prevent old requests from being replayed

Privacy Infrastructure Providers SHOULD store the `agent-id` alongside the Bearer Tokens when they are generated to ensure that the key which an Exercise request was signed with can be intuited using the presented Bearer token.

We believe that providing these signed messages will ensure message integrity and prevent re-use or re-appropriation of requests: A data rights request represents a single action of one user acting against one covered business one time.

#### 3.07.1 Ed25519 Key Semantics, Request Signing, and Management

The Data Rights Protocol authors **strongly** recommend the use of a [libsodium](https://doc.libsodium.org/)-based Ed25519 implementation. There is a [wide selection](https://doc.libsodium.org/bindings_for_other_languages) of language bindings for `libsodium` and in general is considered to be a high-quality, trustworthy API. Requests SHALL be signed by prepending the JSON document with the signature (so-called "combined mode" libsodium APIs will do this by default), base64 encoding the resulting binary buffer, and then sending that request with Content-Type `text/plain`.

The Open Source Implementers' Reference contains an implementation of both sides of the `libsodium` key exchange in [drp_aa_mvp/data_rights_request/views.py#sign_request](https://github.com/consumer-reports-innovation-lab/osiraa/blob/main/drp_aa_mvp/data_rights_request/views.py#L450-L454) and [drp_aa_mvp/drp_pip/views.py#validate_message_to_agent](https://github.com/consumer-reports-innovation-lab/osiraa/blob/main/drp_aa_mvp/drp_pip/views.py#L199-L248) which illustrate the use of the PyNACL API.

### 3.08 Processing Extensions & "Expected By" dates

When a Covered Business acknowledges receipt of a Data Rights Request and moves it in to `in_progress` state, the request's `expected_by` field SHOULD be populated based on either an estimate provided by the Covered Business or the deadline prescribed by the legal regime the request is submitted under. Consider, for example, [California's legal regime](https://transcend.io/laws/cpra/#section-15) prescribes up to 90 days extension so long as they are made within 45 days; If a request is extended, this request must also be extended with a `processing_details` field detailing a reason for the Request's extension to notify the consumer of this delay. The intent of the `processing_details` field is to add additional color to already-defined `state`/`reason` combinations. States which cannot be encoded without reaching for free-form text should be integrated in to the state transition table.

When applying changes to Data Rights Requests in this fashion, the Privacy Infrastructure Provider SHALL attempt to notify the Authorized Agent using the [Data Rights Status Callback](#2041-post-status_callback-response).

### 3.09 Request State Flow Diagram

![Sequence Diagram showing Data Rights Request event flow](https://raw.githubusercontent.com/consumer-reports-innovation-lab/data-rights-protocol/main/files/drp-1.0-sequence-diagram.svg)

## 4.0 Protocol Roadmap

In its current implementation, DRP should not be used to process data of Users who are not involved in the implementers group or implemented by organizations not in the implementers group. This protocol is undergoing significant technical design changes, security evaluation, and implementation work, which should preclude the transfer of arbitrary Users' data rights.

In steps:

- [x] Moving to signed data rights requests from the Authorized Agents
- [x] Moving from JWT to libsodium for singing requests
- Developing a directory service for Authorized Agents to discover businesses participating in a Data Rights Network, and a directory service for Covered Businesses to resolve message signatures to specific Authorized Agents
- Developing system rules and legal agreements for implementers.

## Specification Change Log

In general, please put major change log items at the top of the file. When a new protocol version is "cut", move the previous versions' change log down here.

Protocol Changes from 0.7.1 to 0.8:

- Libsodium signed requests will now be base64 encoded to ensure they can traverse the web safely.

Protocol Changes from 0.7 to 0.7.1:

- Fix path in 2.02 from `POST /v1/data-right-request` to `POST /v1/data-rights-request/`

Protocol Changes from 0.6 to 0.7:

- PIP endpoints are re-structured to be more [REST](https://en.wikipedia.org/wiki/Representational_state_transfer)-like
- Move from JWT to NaCl/libsodium/Ed25519 signatures
- Renaming security claims from JWT short codes to more expressive identifiers
- Add `POST /v1/agent/{agent-id}` endpoint to provide mechanism for generating pair-wise API Authorization/routing tokens
- Specify timestamps as ISO-8601 instead of RFC-3339
- Re-draft API Authentication and Security Guidance sections.


Protocol changes from 0.5 to 0.6:

- Breaking data model changes to fully sign data rights requests
  - Move all attributes of the request in to JWT envelope
  - Allow for only one right to be exercised per request
  - Provide guidance for signing JWKs to test and signal movement in 0.7 toward libsodium or similar cryptographic primitives library.
- Elimination of distinction between technical actor and technical interface (CBi and PIPi and AAi terminology eliminated)
- Remove old Certification Test repo link and replace with link to [OSIRAA](https://osirra.datarightsprotocol.org).

Protocol Changes from 0.4 to 0.5:

- [new request state "denied/`too_many_requests`"](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/commit/14fea83a1b7856da55a2075a6233039f8a7c9c81)
- [openapi.yaml](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/blob/0.5/openapi.yaml) specification for PIP server interface
- [encode time-extensions in to the request status, along with a `processing_details` field](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/commit/f758f164e33b862e990526b8a2aafba49d777862)
- [draft minimal implementation guide](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/blob/0.5/implementation-guide.org)
- [draft PIP certification/conformance suite](https://github.com/consumer-reports-innovation-lab/data-rights-protocol-cert/)
- [respecification of identity tokens to match OIDC Core 1.0](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/pull/44)

Protocol Changes from 0.3 to 0.4:

- [relationship hints](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/pull/17) allow users and agents to provide "hints" for the type of customer relationship, or a set of subsidiary brands to query.
- [shift in language from regulatory framework to broader legal bases](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/pull/16)
- [medium-term protocol development road-map](https://github.com/consumer-reports-innovation-lab/data-rights-protocol/pull/21)

Changes in v0.2 to v0.3:
- donotsell -> sale:opt-in opt-out
- terminology changes
- Request status chart
- identity tiger team recommendations
- API Authentication details
- Moved non-essential sections out of protocol spec

## Footnotes and Errata

[^1]: See section 3.07 and
    [OSIRAA](https://github.com/consumer-reports-innovation-lab/osiraa/blob/main/drp_aa_mvp/data_rights_request/pynacl_validator.py)'s
    validation example.
