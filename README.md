# Data Rights Interface Protocol

*DRAFT FOR COMMENT*

* README: [https://github.com/dazzaji/DRIP](https://github.com/dazzaji/DRIP)
* Swimlane Diagram: [https://github.com/dazzaji/data-rights-protocol/blob/main/swimlane.md](https://github.com/dazzaji/data-rights-protocol/blob/main/swimlane.md)
* Data Model: [https://github.com/dazzaji/data-rights-protocol/blob/main/data-request.json](https://github.com/dazzaji/data-rights-protocol/blob/main/data-request.json)


## Goal

The goal for this protocol is an open specification for issuing and processing data subject requests. We therefore seek to define a voluntary specification that describes a legally-conformant machine interface for users to exercise their data rights. This would seek to provide the missing foundation for industry self-organization and greater certainty needed to process requests at high scale and low cost.

We are iterating versions of this protcol in this open public repository to encourage feedback and good thinking on an informal basis on an ongoing basis.


## Background

A new class of consumer data rights—created by privacy laws like Europe’s GDPR and the California Consumer Privacy Act (CCPA)—grant consumers greater agency and control over their personal data. They also include provisions for “authorized agents” that consumers can use to more easily exercise their rights.

However, while both GDPR and CCPA require that companies honor requests from authorized agents, the utility of these services are limited. First, most companies have not established any machine interfaces for data subject access requests, so request issuing and processing is handled through laborious manual processes. It’s as if consumers gained a “right to connect” but were lacking in a protocol like TCP/IP. Though companies have access to enterprise DSAR Subject Request Management Solutions, which manage workflows of all tasks & activities associated with processing requests from consumers, the cost and friction involved in processing agent requests is still significant.

## Definitions

## Architecture

[In process]

![DRIP-Swimlane-V 0 0 3](https://github.com/dazzaji/data-rights-protocol/blob/main/DRIP-Key-Life-Cycle-Interactions-v-0-1-3.png)

Consumer->Authorized Agent: 0. Registration Request   
Authorized Agent->Consumer: Onboard Consumer   
Consumer->Authorized Agent: Verify Identity and Authorization   
Consumer->Authorized Agent: 1. Do-Not-Sell Request   
Authorized Agent->+DSAR Provider: Do-Not-Sell Request   
DSAR Provider-->-Authorized Agent: Do-Not-Sell Request Ticket Opened   
note right of DSAR Provider: Business Matches Consumer   
DSAR Provider-->-Authorized Agent: Do-Not-Sell Response   
Authorized Agent-->-Consumer: Do-Not-Sell Response   
Authorized Agent-->-DSAR Provider: Do-Not-Sell Ticket Closed   


Consumer->Authorized Agent: 2. Data Deletion Request   
Authorized Agent->+DSAR Provider: Data Deletion Request   
DSAR Provider-->-Authorized Agent: Data Deletion Ticket Opened   
note right of DSAR Provider: Business Matches Consumer   
note right of DSAR Provider: Alt Path: Direct Consumer Verification Required   
DSAR Provider-->-Authorized Agent: Data Deletion Response   
Authorized Agent-->-Consumer: Data Deletion Response   
Authorized Agent-->-DSAR Provider: Data DeletionTicket Closed   


Consumer->Authorized Agent: 3. Data Access Request   
Authorized Agent->+DSAR Provider: Data Access  Request   
DSAR Provider-->-Authorized Agent: Data Access Ticket Opened   
note right of DSAR Provider: Business Matches Consumer   
note right of DSAR Provider: Alt Path:Direct Consumer Verification Required   
DSAR Provider-->-Authorized Agent: Data Access Response   
Covered Business-->-Consumer: Data Access Package Delivery   
DSAR Provider->Authorized Agent: Data Access Package Delivery Confirmed   
Authorized Agent-->-DSAR Provider: Data Access Ticket Closed   

**Direct Verfification of Consumer** 



Consumer->Authorized Agent: Consumer Logs Into AA App   
Consumer->Authorized Agent: Consumer Chooses to Verify for a Business   
Consumer->Covered Business: Consumer Grants OAuth2/OIDC Authorization between AA and Business Endpoints   
Covered Business->Authorized Agent: Business Confirms Consumer Verification Success   
Authorized Agent->+Covered Business: Data Access Request   
Covered Business-->-Consumer: Data Access Response   


### Scope of Transactions

The Data Rights Interface Protocol, fully realized, would cover each key functional rights request authorized under the California Consumer Privacy Act (CCPA), including:

* The so-called "right to opt-out" (Cal. Civ. Code § 1798.120(a));
* The so-called "right to delete"  (Cal. Civ. Code § 1798.105(a)) subject to denial for certain statutory business reasons (Cal. Civ. Code § 1798.105(d)); and 
* The so-called "right to know" what personal information a business has, including the categories of third parties purchasing or receiving their data and the specific pieces of personal information held (Cal. Civ. Code §§ 1798.100, 1798.110, 1798.115, and 1798.130; (Cal. Code Regs tit. 11, §§ 999.313(c) and 999.318).

The interface specified by the protocol focuses on the data exchange, including requests, replies, and ticket tracking, between Consumers and Businesses, including intermediation by an Authorized Agent acting on behalf of the Consumer and by a DSAR Provider acting on behalf of the business.

## Discovery of End-Points

Businesses may host a .well-known/drip.json resource that defines an API endpoint where authorized agents can POST a request. This is a JSON file hosted at the .well-known/drip.json endpoint. 

## Expression of Data Rights

[In Process]

### Do Not Sell Request

#### Legal Basis and Requirements

[In Process]

### Deletion Request

#### Legal Basis and Requirements

[In Process]

### Data Access Request

#### Legal Basis and Requirements

[In Process]

```javascript
{
    "subject": {
        "name": "Susie User",
        "email": "suser@gmail.com",
        "phone": "111-111-1111",
        "userid": "susie.user.1"
    },
    "controller": {
        "name": "Facebook",
        "url": "https://facebook.com"
    },
    "request_authority": "ccpa",
    "request_type": "right_to_know",
}

Response:
{
    "request_id": "ausdfh4938ijh",
    "status": "pending",
}

Subsequent poll:
{
     "request_type": "status",
     "request_id": "ausdfh4938ijh"
}

Subsequent response:
{
    "request_id": "ausdfh4938ijh",
    "status": "closed",
    "dispensation": "success",
    "response_timestamp": "20210622T03:07:25.000UTC",
    "response_url": "https://facebook.com/ccpr/request/ausdfh4938ijh"
}
```

## Consumer Identity and Authorization

### OAuth 2

## Legal Effects

[In process]

## Conformance

[In process]

## A.Implementation Considerations

[In process]

## B.Acknowledgments

[In process]

## C.References

[In process]

### C.1Normative references

[In process]

### Further Reading

[In process]

## How to Contribute

* Make a [new issue](https://github.com/dazzaji/data-rights-protocol/issues/new) in the repository
* Make a [pull request](https://github.com/dazzaji/data-rights-protocol/pulls) in this repository
* Provide feedback through our form: [https://forms.gle/YC7nKRs3ZQMWLvw27](https://forms.gle/YC7nKRs3ZQMWLvw27)
