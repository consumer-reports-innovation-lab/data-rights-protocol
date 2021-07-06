# Data Rights Interface Protocol Swimlane
*V.0.03*      
*[Feedback](https://forms.gle/YC7nKRs3ZQMWLvw27)*.    

The Data Rights Interface Protocol, fully realized, would cover each key functional rights request authorized under the California Consumer Privacy Act (CCPA), including:
* The so-called "right to opt-out" (Cal. Civ. Code § 1798.120(a));
* The so-called "right to delete"  (Cal. Civ. Code § 1798.105(a)) subject to denial for certain statutory business reasons (Cal. Civ. Code § 1798.105(d)); and 
* The so-called "right to know" what personal information a business has, including the categories of third parties purchasing or receiving their data and the specific pieces of personal information held (Cal. Civ. Code §§ 1798.100, 1798.110, 1798.115, and 1798.130; (Cal. Code Regs tit. 11, §§ 999.313(c) and 999.318).

The interface specified by the protocol focuses on the data exchange, including requests, replies, and ticket tracking, between Consumers and Businesses, including intermediation by an Authorized Agent acting on behalf of the Consumer and by a DSAR Provider acting on behalf of the business.

The following is an initial conceptual design approach to how such a protocol could work and is intended primarily as a starting point from which to elicit questions, identify potential alternatives, and catalyze new ideas.


![DRIP-Swimlane-V 0 0 3](https://user-images.githubusercontent.com/2357755/124527699-36f89c80-ddd4-11eb-8a02-015066345e34.png)


Consumer->Authorized Agent: Registration Request     
Consumer->Authorized Agent: Do-Not-Sell Request     
Authorized Agent->+Business: Do-Not-Sell Request     
Business-->-Authorized Agent: Do-Not-Sell Request Ticket Opened     
note right of Business: Business Matches Consumer     
Business-->-Authorized Agent: Do-Not-Sell Response     
Authorized Agent-->-Consumer: Do-Not-Sell Response     
Authorized Agent-->-Business: Do-Not-Sell Ticket Closed     


Consumer->Authorized Agent: Data Deletion Request     
Authorized Agent->+Business: Data Deletion Request     
Business-->-Authorized Agent: Data Deletion Ticket Opened     
note right of Business: Business Matches Consumer     
Business-->-Authorized Agent: Data Deletion Response     
Authorized Agent-->-Consumer: Data Deletion Response     
Authorized Agent-->-Business: Data DeletionTicket Closed     


Consumer->Authorized Agent: Data Access Request     
Authorized Agent->+Business: Data Access  Request     
Business-->-Authorized Agent: Data Access Ticket Opened     
note right of Business: Business Matches Consumer     
Business-->-Authorized Agent: Data Access Response     
Business-->-Consumer: Data Access Package Delivery     
Business->Authorized Agent: Data Access Package Delivery Confirmed     
Authorized Agent-->-Business: Data Access Ticket Closed     



- - - - - - - - - - - -

*NOTE: The above swimlane diagram aims to describe fundamentally legal processes.  For more background on using swimlane diagrams for legal engineering and for legal process description and design see: [https://github.com/mitmedialab/CoreID/blob/master/diagrams/README.md](https://github.com/mitmedialab/CoreID/blob/master/diagrams/README.md)*
