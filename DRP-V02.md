# Data Rights Protocol V.0.2

*DRAFT FOR COMMENT*

* README: [DataRightsProtocol.org](http://datarightsprotocol.org)
* Data Rights Protocol Version 0.2: [https://github.com/consumer-reports-digital-lab/data-rights-protocol/blob/main/DRP-V02.md](https://github.com/consumer-reports-digital-lab/data-rights-protocol/blob/main/DRP-V02.md)
* Data Model: [https://github.com/consumer-reports-digital-lab/data-rights-protocol/blob/main/data-request.json](https://github.com/consumer-reports-digital-lab/data-rights-protocol/blob/main/data-request.json)

**Version 0.2 of the Data Rights Protocol is intended as an intial rough outline draft.  We expect to post a further updated version in early October 2021 based on a collaborative drafting effort among a multistakeholder group and to present and discuss the direction of this emerging protocol at the Data Rights Summit hosted by MIT on October 19th, 2021.  Information about and a link to register to attend the Data Rights Summit will be posted here in late September, 2021.**

## Introduction

This specification defines a web protocol encoding a set of standardized request/response data flows such that End-Users can exercise Personal Data Rights provided under regulations like the California Consumer Privacy Act, General Data Protection Regulation, and other regulatory or voluntary bases, and receive affirmative responses in standardized formats.

We aim to make the data rights protocol integrable with an ecosystem of data rights middlewares, agent services, automation tool kits, and privacy-respecting businesses which empower and build trust with consumers while driving the cost of compliance towards zero.

## Motivation

Data Rights are increasingly becoming universal, but the method of request and protocol for communicating those requests varies and there is no universal interchange format. Companies operating under these regulatory regimes face not only technical challenges in collecting and delivering responses to users’ data rights requests but also face significant process burdens as consumers increasingly make use of these rights. At the same time, consumers find it tough to execute their data rights under new privacy laws, partially due to a lack of standardization among companies.

By providing a shared protocol and vocabulary for expressing these data rights, we aim to minimize the administrative burdens on consumers and businesses while providing a basis of trust for verifiable identity attestation which can be used by (individual) consumers (or by an agent intermediating the relationship on behalf of consumers) and businesses.

## Scope

## Terminology

### Actors

## Trust Models
“level 1”: Authorized Agent in a trust-relationship with Covered Businesses
“Level 2”: Covered Business verifies End-User identity
“Level ‘0’”: Trust-less systems

## Data Flows
Agent - DSR Provider
Agent - Covered Business
End User - DSR Provider
End User - Covered Business
End User Verification step
Login Claims

## Data Schemas
Supported Rights Actions
Request Statuses
Schema: Status of a Data Subject Exercise Request
Schema: Identity encapsulation
Identity Elements
Error States

## Endpoints
GET /.well-known/data-rights
POST /exercise
Response
GET /status
GET /status Response
POST $status_callback
POST /cancel
Semantics of Canceling a Request

## future roadmap
To-considers
Footnotes


# How to Contribute

* Make a [new issue](https://github.com/consumer-reports-digital-lab/data-rights-protocol/issues/new) in the repository
* Make a [pull request](https://github.com/consumer-reports-digital-lab/data-rights-protocol/pulls) in this repository
* Provide feedback through our form: [https://forms.gle/YC7nKRs3ZQMWLvw27](https://forms.gle/YC7nKRs3ZQMWLvw27)
