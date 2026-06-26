---
title: 'ARC Publication and Review Workflow'
tags:
  - ARC Publication
  - ARC Review
authors:
  - name: Cristina Schmale Rodrigues
    orcid: orcid.org/0000-0002-4849-1537
    affiliation: 1
    role: Reviewer
  - name: Dominik Brilhaus
    orcid: https://orcid.org/0000-0001-9021-3197
    affiliation: 2
    role: Reviewer
affiliations:
  - name: DataPLANT, eScience Department, University of Freiburg, Freiburg im Breisgau, Germany; Office for Research, University Development Department, RPTU University Kaiserslautern-Landau, Kaiserslautern, Germany
    index: 1
  - name: Cluster of Excellence on Plant Sciences (CEPLAS), Faculty of Mathematics and Natural Science, Heinrich Heine University Düsseldorf, Düsseldorf, Germany
    index: 2
date: 25 June 2026
---

# ARC Publication and Review

This directory documents discussions and concepts related to the further development of the DataPLANT ARC publication and review workflow.

The topics collected here summarize ideas, requirements and implementation suggestions that emerged from discussions between developers and ARC reviewers. The primary focus is on improving the publication process, reviewer experience and tasks, reviewer-user-interaction, and the technical implementation of ARC publication within the DataPLANT environment.

## Scope

Topics covered include:

* ARC publication workflow
  * Including publication embargos
* Reviewer workflow
  * Community-based reviewing
  * Reviewer onboarding and communication
* Technical implementation
  * ARChigator and Invenio integration

## Background

The discussions documented here build upon the existing ARC publication workflow and are intended to refine and extend the current process rather than redesign it from scratch.

Several meetings contributed to the concepts documented in this directory, including focused discussions during the ARC Symposium in Frankenstein (June 2026).

## Related Components

The discussed workflow involves several DataPLANT components:

| Component        | Role                                   | Repository                                          |
| ---------------- | -------------------------------------- | --------------------------------------------------- |
| ARC              | Research object to be published        | https://github.com/nfdi4plants/ARC-specification    |
| ARChigator       | Submission interface                   | https://github.com/nfdi4plants/archigator2.0        |
| Invenio/ARChive  | Publication backend and DOI management | https://github.com/nfdi4plants/ARChive              |
| DataHUB          | Repository and collaboration platform  | https://github.com/nfdi4plants/DataHUB              |
| Storage Resolver | Resolves storage locations of data     | https://github.com/nfdi4plants/storage-resolver     |
| arc-validate-package-registry (avpr) | Provides validation package for Invenio | https://github.com/nfdi4plants/arc-validate-package-registry |

---

## Ideas and Concepts from the Discussions

The following ideas reflect the current state of the discussion and do not yet represent final decisions.

### Review Process

* Introduction of a structured ARC review prior to publication
* Separation into three phases:
  1. ARC submission for revision initiated by users via the DataHUB interface
  2. ARC-revision as bilateral exchange between ARC-reviewer and users via issues in the DataHUB interface
  3. ARC publication and DOI-registration via Invenio triggered by the ARC-reviewer
* Reviewer-driven creation of issues during the review process—ideally summarized in a milestone
* Clear status transitions (e.g., submitted → under review → revision → accepted)

### Access and Accounts for Reviewers

* Dedicated ARC reviewer accounts in DataHUB for accessing ARCs during the review process 
** Ideally, two accounts. One with, for example, owner rights, which would be automatically added to the ARC under review and would then either add the second reviewer account (maintainer) or the corresponding real-name account. 
* Access control for ARCs with embargoes via controlled reviewer roles
* Temporary assignment of reviewers during the active review phase

### Handling Embargo Periods

* Treat private ARC submissions as subject to an embargo by default
* One idea for how to handle this would be:
** Time-limited embargo periods (e.g., 6 months by default)
** Automatic transition to public status if no extension is requested
* Controlled access for external reviewers during the embargo

### ARChigator Integration

* Submission automatically triggers the review workflow (including assigning the reviewer account to the ARC to be reviewed)
* Visual display of review status (e.g., badge: “Under Review”)
* Ability to cancel submissions and cleanly revoke reviewers’ access via ARChigator dashboard
* Resubmission triggers an updated review cycle
* Selection of the community during the submission process

### Infrastructure / Data Location Stability
* Decoupling of ARC publication from physical storage location
* Use of Storage Resolver for stable references to datasets
* Enable relocation of underlying data without breaking published ARCs
* Integration of Storage Resolver into ARChigator and Invenio resolution layer
* Requirement: ARC identifiers must remain stable while storage backend may change

### Invenio Integration

* Visibility of reviewers in ARC records
* Tracking of publication status linked to the ARC lifecycle
* Automatic DOI publication notification upon acceptance
* Access management for records with an embargo period versus public records
* Create reviewer accounts for different communities

### Communication and Onboarding

* Onboarding process for reviewers (guidance on reviewing an ARC)
* Setting up mailing lists and community distribution lists
* Templates for review invitations and status emails
* Clear instructions for topic-specific feedback on Reviews

---

## Next Steps

Next Actions include:

Development Team:
* Create reviewer account 1 (Owner) at the GitLab level
* Directly assign this account to the ARC to be reviewed upon initial submission
* Define and implement the embargo workflow
* Implementation of review milestones
* Design of ARChigator review state transitions
* Community selection mechanism during submission

Reviewer Team:
* Set up Reviewer accounts on Invenio (in collaboration with the development team)
* Create a Reviewer 2 account in DataHUB
* Develop an MS365-independent review process
* How to submit a Reviewer article through the review process
* Announce updates to the Reviewer group
