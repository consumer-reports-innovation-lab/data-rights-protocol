
This documents describes the basic technical components of the Data Rights Protocol system, with a
particular eye on how a company which has implemented 0.5 version of the protocol may look towards a
1.0 protocol implementation.

# Technical Overview

## Libsodium encryption

Authorized Agents submit data rights requests to Privacy Infrastructure Providers that are signed
using Ed25519 public/private key encryption as implemented by the public domain `libsodium`. This
signature system is used to issue bearer token authorization keys as defined under the **Auth
endpoints** section below.

Authorized Agents will be responsible for generating and securely managing signing keys and
exporting public verify keys based derived from those signing keys. Implementers should consult for
example the [PyNaCl](https://pynacl.readthedocs.io/en/latest/signing/) "Digital Signatures"
documentation.

Verify keys should be presented to the PIPs through an out of band channel (email/signal/etc to
start, eventually transitioning to a service directory model outlined under **Discovery**) and
encoded in `hex` as in `nacl.encoding.HexEncoder` for the sake of consistency.

The [DRP Security
Model](https://raw.githubusercontent.com/consumer-reports-digital-lab/data-rights-protocol/main/files/DRP_security_model.pdf)
technical note describes the rationale for this choice and the move away from JSON Web Tokens.

## Discovery

### 0.7: `~/.well-known/data-rights.json`

Currently a small JSON file is used to boot-strap communication from Authorized Agents to Covered
Businesses. This method is to be deprecated over the next few months in favor of a managed directory
service containing the same information but for all parties instead of delegating this to the
business.

The idea of hosting these resources was that if an Authorized Agent wanted to send a data rights
request to ACME, Inc. whose homepage is `acme.com`, they could `GET
https://acme.com/.well-known/data-rights.json` to discover where the API endpoints for the DRP are
as well as the supported features and whatnot. However, until DRP takes over the world, this is
likely to be less hit and more miss. In practice, network participants need to know the full shape
of the network and so in the next development period we will be moving to a model where the DRP
consortium operates services providing two light-weight JSON directory files:

### 0.8-1.0+: service directories

As part of their onboarding to the DRP, Authorized Agents will present their verify key as well as
technical and business contact information.

As part of their onboarding to the DRP, Covered Businesses will present the "base" of the
following API endpoints, the rights they support under DRP, and technical and business contracts.

Privacy Infrastructure Providers may also submit a covered business for integration testing purposes
with the same information but with no underlying business represented.

Authorized Agents will use the directory of Covered Businesses to submit automated requests to any
Covered Business in the directory. Covered Businesses will use the directory of Authorized Agents to
establish a cryptographic trust root and to establish communication with Agents in the event that
they suspect fraudulent or forged requests.

The exact details of the enrollment and presentation of these directories is still
undefined. Businesses may be able to delegate enrollment in the directory to the Privacy
Infrastructure Provider which provides their DRP API. AAs and PIPs can be expected to pull these
files in to their system when they have been updated, and there may be "web hook" endpoints which
can be implemented by the services.

## Auth endpoints (protocol section 2.06 and 2.07)

-   `POST /v1/agent/{id}`
-   `GET /v1/agent/{id}`

Data Rights Protocol uses a bespoke machine-to-machine API authentication system based on the same
public key cryptography which is used to sign the data rights requests. This was designed so that
relationships between Authorized Agents and Covered Businesses can be established using only the
public information stored in the service directory which acts as a root of trust between all of the
parties of the network. Rather than needing to exchange OAuth2 client tokens before data rights
requests can be processed, a new business can simply be advertised in the CB directory and use the
AA directory to ensure requests are coming from trusted parties without delay or confusion.

This token is used by PIPs to bootstrap the signature verification steps outlined in Section 3.07 of
the spec. Rather than work through a keyring containing every Authorized Agent's keys, the PIP can
map from the Bearer Token to a specific Authorized Agent and use that knowledge to pick the key
which should verify the incoming message. The can also use these tokens to: to route traffic to
particular businesses in multi-tenant scenarios without having to verify and deserialize the
requests themselves or keep a global mapping from request ID to business and to implement rate
limit, abuse control, etc without paying CPU cycles on cryptography.

PIPs implement handlers for these two endpoints under their `api_base`.

Authorized Agents will, before making a request to a new Covered Business, create a request to `POST
/v1/agent/{id}` signed by their Signing Key containing the pair of parties the returned key should
be controlling access to. The PIP will respond with a token which shall be used in any future
requests from that authorized agent to that covered business as a `Authorization: Bearer <token>`
"bearer token". `GET /v1/agent/{id}` exists to ensure that the generated token is valid but may be
extended to provide other functionality in the future.

**Authorized Agents are expected to make calls to these APIs from a trusted back-end rather than a
User Agent or uncontrolled device!**

## Request endpoints

The "shape" of the DRP API routes changed in significant ways between 0.6 and 0.7 -- this API
pattern is a "REST-ful" pattern with a major-version prefix signaling that these paths and the
shape of their requests will remain backward compatible. We believe these APIs will be more-or-less
set in stone until and through the DRP 1.0 go-live.

**Authorized Agents are expected to make calls to these APIs from a trusted back-end rather than a
User Agent or uncontrolled device!**

PIPs implement handlers for these endpoints under their `api_base`.

### `POST /v1/data-rights-request/`

`POST /v1/data-rights-request` was `POST /exercise` in 0.6.

The body of the request will be a `libsodium` signed object with the signature embedded in it; this
is referred to as "combined mode" as opposed to "detached mode". The inner JSON document
contains information about the consumer making the request, the specific rights they want to engage
in, the authorized agent submitting the request on behalf of the consumer, and business the request
is being sent to.

In version 0.5 the request was a "plain old JSON" request with only the user's identity
attributes signed and encoded as a JWT by the Authorized Agent but this design did not confer the
sorts of advantage we hoped for earlier in the design.

Section 3.07 of the protocol specification outlines an algorithm which PIPs need to engage in to
validate the messages are signed and coming from the expected party. Prior versions relied on a
pre-shared symmetric signing key.

The validated request should be persisted and mapped in to a privacy workflow system which the
Covered Business uses to process manual or e-mail based data rights requests as well; in theory it
should be possible for a Covered Business to "flip a switch" in their Privacy Infrastructure
Provider to start receiving DRP requests.

### `GET /v1/data-rights-request/{id}`

`GET /v1/data-rights-request/{id}` was `GET /status` in 0.6.

This endpoint returns the processing status of a previously submitted request. The critical fields
to include in response to this request are a pair of "status" and "reason" fields which
represent where in the request processing "state machine" a given request is in, but there are
additional fields for when a request may be expected to be delivered, or may be due. By providing an
estimate of delivery, Privacy Infrastructure Providers can signal to Authorized Agents when they
should next request a status update rather than pinging every hour or day while the request is in
queue or in process.

Conversely, Authorized Agents should take care to not cause a "thundering herd" by scheduling many
calls to this endpoint simultaneously. Smear requests to this endpoint to maximize resource
efficiency. Further gains can be made by implementing the "status callback" pattern described
below.

### `DELETE /v1/data-rights-request/{id}`

`DELETE /v1/data-rights-request/{id}` was `POST /revoke` in 0.6.

The exact semantics of this request are difficult to nail down and depend on the particularities of
a particular request type's work flow.  Consider a consumer who says "I don't actually care about
this access request any more because I got the information I wanted" compared to "actually, I want
you to stop deleting my account halfway through the process of clearing out my records". One of
these is as simple as terminating a background data-lake aggregation job, where the other may be
technically infeasible to say the least. However, even in the case of deletion, many companies'
deletion policies include a "cooling off period" where a user may choose not to delete their
account by logging in or otherwise signaling that they no longer want to follow through with this
request.

Thus, this endpoint is to be seen as a "best effort" action and the success of it largely comes
down to processes and policies outside of the scope of the Data Rights Protocol.

## Status callback

Authorized Agents may implement a handler for "status callback" requests sent from the Privacy
Infrastructure Provider when a request's status is updated.

Privacy Infrastructure Providers need to implement an HTTP client which `POST`'s a `GET
/v1/data-rights-request/{id}` response to the Authorized Agent's server. This is a **push** model
while the status endpoint above is a **pull** model.

Authorized Agents which implement this should ensure they are not requesting status updates in the
`GET` channel more than once every few days for each request.

This load-shedding behavior will become increasingly important as more data rights requests are sent
within the data rights protocol consortium.

## `in_progress` / `need_user_verification` state

A covered business may want to integrate their own account verification system, or a PIP may provide
a form-builder or ID card verification system for more sensitive types of data. This
`need_user_verification` flow exists to allow the PIP to signal to the AA that a user needs to load
a particular URL in their browser to make further progress on the data rights request. This should
only be used to validate identity attributes which the Authorized Agent has not previously
validated.

# State Machine Workflow

This sequence diagram lays out a sample of the sequence flow between all parties involved from user
to business and back.

Ultimately the DRP consortium is not really interested in the workflow that happens "behind the
curtain" as long as it exposes the status of a request under the standard's taxonomy. It's up to
Privacy Infrastructure Providers and Covered Businesses to design their privacy programs based on
business requirements, regulatory regimes, innovative mindsets, etc.

![](https://raw.githubusercontent.com/consumer-reports-digital-lab/data-rights-protocol/main/files/drp-1.0-sequence-diagram.svg){width="60em"}

It should be assumed that the PIP and CB more or less "owns" the status of the request, the AA has
little agency over a request once it's been submitted. If they need to be amended by the AA the
request should be revoked and resubmitted.

# Minimum Viable Actors

## Covered Business responsibilities

### What information does the Covered Business have access to?

-   information about the authorized agent submitting the request as pulled from the Service
    Directory or shared out of band including the LoA which the authorized agent verifies identity
    attributes to.
-   identity attributes of the consumer, and whether they are positively verified. A handful of
    standard claims will be included but there is ongoing discussion in [issue
    52](https://github.com/consumer-reports-digital-lab/data-rights-protocol/issues/52) about
    methods to specify which claims a business wishes to see in a data rights request.
-   the data rights actions requested: data sale opt-out, deletion, access, data-categorical
    transparency...
-   legal regime of the request. the DRP right now is designed around a **legal obligation to
    communicate with authorized agents**, a legal framework which currently only exists under the
    California Consumer Privacy Act and its amended statutes. Requests made outside of this legal
    regime are thus made on a **voluntary compliance** basis until other legal jurisdictions adopt
    Authorized Agent frameworks.
-   important deadline dates (45 days after ack for CCPA, for example)

### What actions can a Covered Business be expected to take

-   update a request's state with information about the status of a request in progress
-   request information or verification by providing a URL
-   a covered business could be running an OAuth2 or account server they want consumers to
    authenticate against

### What is expected of a participating Covered Business

-   Interoperate with Authorized Agents not only in a technical fashion but at the business/legal
    consortium layer
-   Participate in voluntary data rights requests in good faith
-   High-level status/statistical tracking of requests made through the system \[currently
    under-specified\]

## Privacy Infrastructure Provider responsibilities

It is perfectly possible and reasonable for Covered Businesses to "bring their own" PIP and
participate in the network as both a business and a technical contributor, and it's also perfectly
possible and reasonable for them to out-source this to a company providing automation
services. Businesses which "bring their own" PIP should read any of the PIP requirements as
requirements on their technical team and its interface with the Business's privacy legal/policy
programs.

-   Keep an up to date version of the Authorized Agent Service Directory
-   Maintain records in Covered Business Service Directory with the technical and business
    information for the Covered Businesses whose requests are managed by the PIP
-   Verify the cryptographic trust of incoming requests against the Consortium managed service
    directories
-   Generate and Persist API tokens for each Authorized Agent + Covered Business relationship
    pairing
-   Map DRP request states in to a workflow which the Privacy Program can work with and back out to
    the workflow states which the Authorized Agents expect to work against

## Authorized Agent responsibilities

-   Provide documentation of the practices the AA follows to verify identity attributes of Consumers
    -   Authorized Agent MUST verify the consumer's email address when the user first registers
    -   Authorized Agent MAY verify the consumer's phone number and/or physical address when they
        register as well.
    -   Authorized Agent MUST only present the "is verified" bits for attributes that have been
        verified according to this documentation
-   Generate and securely manage an Ed25519 signing key, this signing key is **not to be placed on a
    Consumer's user agent**
-   Keep an up to date version of the Covered Business Service Directory
-   Maintain records in the Authorized Agent Service Directory with the technical and business
    information used as trust mechanism for the AA, including the "verify key" corresponding to
    the Ed25519 signing key.
-   Interact with the "pair-wise API token" setup endpoint the first time it submits a request to
    a Covered Business and persist that API token
-   Interact with the Data Rights Request endpoints using the Ed25519 signed requests and API bearer
    token as appropriate
-   Authorized Agents must notify a user when the CB communicates a state change to the AA
-   Authorized Agents SHOULD provide a "status callback" URL pointing to a service they manage
    which can receive updates to data rights requests without needing to regularly poll from the
    PIP.
-   Authorized Agents MUST implement the `need_user_verification` flow allowing the Consumer to
    verify their identity in a system managed by the CB.
