# Data Rights Interface Protocol

* README: [https://github.com/dazzaji/DRIP](https://github.com/dazzaji/DRIP)
* Swimlane Diagram: [https://github.com/dazzaji/DRIP/blob/main/swimlane.md](https://github.com/dazzaji/DRIP/blob/main/swimlane.md)
* Data Model: [https://github.com/dazzaji/DRIP/blob/main/data-request.json](https://github.com/dazzaji/DRIP/blob/main/data-request.json)


The Data Rights Interface Protocol, fully realized, would cover each key functional rights request authorized under the California Consumer Privacy Act (CCPA), including:

* The so-called "right to opt-out" (Cal. Civ. Code § 1798.120(a));
* The so-called "right to delete"  (Cal. Civ. Code § 1798.105(a)) subject to denial for certain statutory business reasons (Cal. Civ. Code § 1798.105(d)); and 
* The so-called "right to know" what personal information a business has, including the categories of third parties purchasing or receiving their data and the specific pieces of personal information held (Cal. Civ. Code §§ 1798.100, 1798.110, 1798.115, and 1798.130; (Cal. Code Regs tit. 11, §§ 999.313(c) and 999.318).

The interface specified by the protocol focuses on the data exchange, including requests, replies, and ticket tracking, between Consumers and Businesses, including intermediation by an Authorized Agent acting on behalf of the Consumer and by a DSAR Provider acting on behalf of the business.

## Goal

The goal for this protocol is an open specification for issuing and processing data subject requests. We therefore seek to define a voluntary specification that describes a legally-conformant machine interface for users to exercise their data rights. This would seek to provide the missing foundation for industry self-organization and greater certainty needed to process requests at high scale and low cost.

We are iterating versions of this protcol in this open public repository to encourage feedback and good thinking on an informal basis on an ongoing basis.


## Background

A new class of consumer data rights—created by privacy laws like Europe’s GDPR and the California Consumer Privacy Act (CCPA)—grant consumers greater agency and control over their personal data. They also include provisions for “authorized agents” that consumers can use to more easily exercise their rights.

However, while both GDPR and CCPA require that companies honor requests from authorized agents, the utility of these services are limited. First, most companies have not established any machine interfaces for data subject access requests, so request issuing and processing is handled through laborious manual processes. It’s as if consumers gained a “right to connect” but were lacking in a protocol like TCP/IP. Though companies have access to enterprise DSAR Subject Request Management Solutions, which manage workflows of all tasks & activities associated with processing requests from consumers, the cost and friction involved in processing agent requests is still significant.

## Architecture

[In process]

![DRIP-Swimlane-V 0 0 3](https://user-images.githubusercontent.com/2357755/124527699-36f89c80-ddd4-11eb-8a02-015066345e34.png)


## Further Reading



## How to Contribute

* Make a [new issue](https://github.com/dazzaji/data-rights-protocol/issues/new) in the repository
* Make a [pull request](https://github.com/dazzaji/data-rights-protocol/pulls) in this repository
* Provide feedback through our form: [https://forms.gle/YC7nKRs3ZQMWLvw27](https://forms.gle/YC7nKRs3ZQMWLvw27)
