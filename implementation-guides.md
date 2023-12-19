# PermissionSlip API for Data Rights Requests: Implementer's Guide for Covered Businesses


This document describes the basic components of the PermissionSlip API for Data Rights Requests, and serves as a high-level introduction for new implementers.  The PermissionSlip API is based on (a profile of) the Data Rights Protocol (DRP), an open source protocol which has been developed by Consumer Reports and a consortium of privacy infrastructure companies.

Data Rights Protocol (DRP) is centered on an API for communication between Authorized Agents acting on behalf of a consumer exercising their digital rights, and a Covered Business or Privacy Infrastructure Provider acting on the business’s behalf to honor those rights as prescribed by laws in California and elsewhere.  It is designed to track data rights requests from consumers to companies, and their ongoing updates to the status of those requests.

PermissionSlip API is a subset of the protocol, designed to work directly with multiple Covered Businesses with Permission Slip in the role of Authorized Agent.  If, in the future, multiple interoperating AA’s and/or PIPs create demand, we can expand the implementation to the full spec by introducing Service Directories, but that is out of scope for now.

For more information see the PermissionSlip API spec at: https://github.com/consumer-reports-innovation-lab/data-rights-protocol-lite-permissionslip/ and the full DRP spec at: https://github.com/consumer-reports-innovation-lab/data-rights-protocol.


## Authorized Agent Responsibilities

Permission Slip acts as an Authorized Agent on behalf of a consumer to communicate with a Covered Business to exercise the consumer’s digital rights via API requests.  It is important that the CB can trust the authenticity of a request and the accuracy of the information therein.  Therefore, the Authorized Agent shall:

-   Verify identity attributes of Consumers
    -   Authorized Agent MUST verify the consumer's email address when the user first registers
    -   Authorized Agent MAY verify the consumer's phone number and/or physical address when they register as well.
    -   Authorized Agent MUST only present the "is verified" flags for attributes that have been verified according to this Identity Assurance documentation
-   Generate and securely manage an Ed25519 signing key. This signing key is not to be placed on a Consumer's user agent.
-   Maintain records with the technical and business information used as trusting mechanism for the AA, including the "verify key" corresponding to the Ed25519 signing key.
-   Invoke the "pair-wise API token" setup endpoint the first time it submits a request to a Covered Business and persist that API token.
-   Invoke the Data Rights Request endpoints using the Ed25519 signed requests and API bearer token as appropriate.
-   Generate a unique request Id for each unique request, and use it to track and update a request throughout its lifecycle.  Note that the CB may also independently create and maintain a request Id for use in their system.
-   Notify a user when the CB communicates a state change to the AA in a timely manner.


## Covered Business Responsibilities

In a DRP request the Covered Business receives information about the user, provided in the Authorized Agent and informed by the legal regime under which the request is made. This includes:

-   Information about the authorized agent submitting the request including the Letter of Authority to which the authorized agent verifies identity attributes.
-   Identity attributes of the consumer, and whether they are positively verified. A small set of standard claims will be included.
-   A unique request Id.
-   The data rights action requested: data sale opt-out, or deletion.
-   The legal regime of the request. DRP is designed around a legal obligation to communicate with an authorized agent, currently supported under the California Consumer Privacy Act and its amended statutes (as of 2023). Requests made outside of this legal regime are made on a voluntary compliance basis until other legal jurisdictions adopt Authorized Agent frameworks.  Note that other states are actively creating similar legislation to protect consumers’ digital privacy rights, so the jurisdiction landscape is continuously evolving.
-   Important deadline dates (for example, 45 days after request is sent for CCPA).

A Covered Business is expected to take certain actions upon receipt of a DRP request:

-   Provide the Authorized Agent with technical and business information used to discover API endpoints and API requirements (one time only)
-   Generate and Persist API tokens for each Authorized Agent + Covered Business relationship pairing
-   Verify the cryptographic trust of incoming requests against Agent public keys in service directories
-   Acknowledge data requests made under PS API.
-   Map request states into a workflow in the Covered Business's privacy program, and back out to the workflow states which the Authorized Agents can access.
-   Update a request's state with information about the status of a request in progress.
-   Encouraged to affirmatively respond to voluntary data requests.


## Endpoint Discovery

As part of their onboarding to the PermissionSlip API, Covered Businesses will declare the API root of the following endpoints, the rights they support under DRP, and technical and business contacts. The Authorized Agent will submit automated requests to registered Covered Businesses. To enable this, Covered Businesses establish a cryptographic trust root and communication with Agents in the event that they suspect fraudulent or forged requests.


## Libsodium encryption

PermissionSlip API requests submitted to Covered Businesses are signed using Ed25519 public/private key encryption as implemented by the public domain library `libsodium`. This signature system is used to issue bearer token authorization keys as defined under the **Auth endpoints** section below. The Authorized Agent is responsible for generating and securely managing signing keys and exporting public verify keys derived from those signing keys. See the [PyNaCl](https://pynacl.readthedocs.io/en/latest/signing/) "Digital Signatures" documentation for more information. Verify keys will be exchanged through an out of band channel and encoded in `base64` as in `nacl.encoding.Base64Encoder`. The The [DRP Security
Model](https://raw.githubusercontent.com/consumer-reports-digital-lab/data-rights-protocol/main/files/DRP_security_model.pdf) technical note describes the rationale for this choice.


## Auth endpoints (protocol section [2.05](https://github.com/consumer-reports-innovation-lab/data-rights-protocol-lite-permissionslip/blob/main/data-rights-protocol.md#205-post-v1agentagent-id-pair-wise-key-setup-endpoint) and [2.06](https://github.com/consumer-reports-innovation-lab/data-rights-protocol-lite-permissionslip/blob/main/data-rights-protocol.md#206-get-v1agentagent-id-agent-information-endpoint))

-   `POST /v1/agent/{id}`
-   `GET /v1/agent/{id}`

Data Rights Protocol uses a machine-to-machine API authentication system based on the same public key cryptography used to sign the data rights requests. Relationships between Authorized Agents and Covered Businesses are established using stored shared information, which acts as a root of trust between all of the parties of the network. A privately shared token is used by CBs to bootstrap the signature verification steps outlined in Section 3.07 of the spec. CBs implement these two endpoints under their `api_base`.

Before the first request to a new Covered Business, the Authorized Agent will create a request to `POST
/v1/agent/{id}` signed by their Signing Key, containing the pair of parties for whom the returned key should be controlling access. The CB will respond with a token which shall be used in any future requests from that Authorized Agent to that Covered Business as a `Authorization: Bearer <token>` "bearer token".  Subsequently, use `GET /v1/agent/{id}` to ensure that the generated token is valid. The Authorized Agent shall make calls to these APIs from a trusted back-end rather than a User Agent or uncontrolled device.


## Request endpoints

The API follows a "REST-ful" pattern with a major-version prefix signaling that these paths and the shape of their requests will remain backward compatible. Authorized Agents make calls to these APIs from a trusted back-end rather than a User Agent or uncontrolled device. CBs implement handlers for these endpoints under their `api_base`.

### `POST /v1/data-rights-request/` ([2.01](https://github.com/consumer-reports-innovation-lab/data-rights-protocol-lite-permissionslip#201-post-v1data-rights-request-data-rights-exercise-endpoint))



This call declares a new digital rights request from an Authorized Agent on behalf of a consumer. The body of the request will be a libsodium signed object with the signature embedded in it. The inner JSON document contains information about the consumer making the request, the specific rights they want to exercise, the authorized agent submitting the request on behalf of the consumer, the unique request Id, and the business to which the request is being sent. Section 3.07 of the protocol specification outlines an algorithm which CBs use to validate the messages are signed and coming from the expected party. The validated request should be persisted and mapped into a privacy workflow system which the Covered Business uses to process data rights requests.

### `GET /v1/data-rights-request/{id}` ([2.02](https://github.com/consumer-reports-innovation-lab/data-rights-protocol-lite-permissionslip#202-get-v1data-rights-requestrequest_id-data-rights-status-endpoint))

This endpoint returns the processing status of a previously submitted request. The critical fields to include in response to this request are "status" and "reason", which represent the state of a given request.  Additional fields specify when a request may be expected to be delivered, or may be due.


## E2E Implementation Testing Path

-   Conformance test using OSIRAA - CB’s API correctly implements DRP
-   Interoperability test data on staging environment - their workflow correctly models the request state
-   Production deploy with live data - woo-hoo!

