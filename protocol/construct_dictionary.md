# Construct dictionary for the DD-DSF (Protocol C, step 3)

Written on 2026-11-12, after the framework, Figure 5 and propositions P1–P4 were
drafted. It fixes the meaning of each construct used in manuscript Sections 5.2,
5.5 and 5.6 and in Figure 5. The DD-DSF is conceptual; none of these constructs
has been measured in this review. Indicators are proposals for later studies.

| Construct | Definition | Layer / step in Figure 5 | Proposed indicator | Used in |
|---|---|---|---|---|
| Policy interpretability | How easily a participant can tell which obligations and conditions of use apply to a given data set and partner | Governance; step 2 (obligations) | Time and expert effort to classify a request; share of requests needing legal advice | P1 |
| Rule–routine consistency | Agreement between the formally defined sharing rules and the routines by which an organization decides what to share | Governance → actors | Policy compliance records; interviews coded for divergence between rule and practice | P1 |
| Semantic compatibility | Whether the parties' data models and vocabularies can be mapped so that the recipient can interpret the data | Infrastructure; step 3 | Share of fields mapped without manual work; unresolved mappings per exchange | P2 |
| Policy compatibility | Whether the required usage conditions can be expressed and enforced by both parties' connectors | Infrastructure; step 3 | Share of usage conditions expressible in the connector policy language | P2 |
| Integration effort | Work needed to set up a new exchange | Infrastructure → actors | Onboarding time; engineering person-days | P2 |
| Actor decision cost | Expected effort, cost and remaining risk that an organization weighs before agreeing to an exchange | Actors; step 4 | Self-reported cost and skill requirements; share of requests withdrawn for cost | P3 |
| Implementation capability | Skills and resources to operate privacy-preserving controls | Actors (moderator) | Dedicated security function (yes/no); staff with relevant skills | P3 |
| Participation | Whether an organization takes part in exchanges | Actors; step 4 | Completed exchange agreements per eligible organization | P3 |
| Completed exchange | An approved request whose data was delivered under the agreed conditions | Step 5 | Share of eligible requests completed | P1 |
| Reuse | Use of exchanged data by the recipient beyond the first transfer | Application | Number of downstream uses per completed exchange | P1 (mediator) |
| Innovation outcome | New or improved product, service, analytical capability or process that depends on contributions from more than one organization | Application | Counted separately from exchange performance | P1 (distal) |
| Governance adaptation | Change in a governance rule or technical standard following feedback | Feedback loop | Time from an identified issue to the change (adaptation latency) | P4 |

## Moderators

Organization size and technical maturity, and regulatory complexity (number of
instruments that apply to a data set), are treated as moderators, not as layers.
P2 and P3 name capability as a moderator explicitly.

## Direction of the links

Policy interpretability and rule–routine consistency → completed exchange →
reuse → innovation outcome (P1). Semantic and policy compatibility → lower
integration effort (P2). Decision cost × implementation capability →
participation (P3). Feedback procedures → shorter adaptation latency (P4).
These are proposed directions, not tested causal effects.

## What the DD-DSF predicts that a connector-only or compliance-only view does not

A connector-only view predicts that exchanges follow once policies are machine
enforceable. A compliance-only view predicts that they follow once the rules are
clear. The DD-DSF predicts that neither is sufficient alone: completion depends
on the actor decision in step 4, so organizations with the same connector and
the same rules should still differ in completed exchanges according to decision
cost and implementation capability (P3), and rule–routine consistency should
predict completion after connector capability is held constant (P1).

The falsifying observation for each proposition is in `proposition_test_map.csv`.
