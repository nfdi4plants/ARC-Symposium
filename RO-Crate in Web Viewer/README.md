---
title: 'Investigation of ARC-RO-Crate Visualization in ARC Web Viewer'
tags:
  - HHU-Datahub
  - RO-Crate-Metadata
authors:
  - name: Yaser Alashloo
    orcid: 0000-0001-6858-8961
    role: Data steward
  
affiliations:
  - name: CEPLAS, HHU Düsseldorf
  
date: 17 June 2026
---


<!--

The paper.md, bibtex and figure file can be found in this repo:

  https://github.com/nfdi4plants/ARC-Symposium

To modify, please clone the repo. You can generate PDF of the paper by
pasting above link (or yours) in

  
-->

# Introduction

Opening the ARC-RO-Crate metadata JSON file in the ARC Web Viewer (https://nfdi4plants.github.io/ARCWebView/#) was investigated. The main issue observed is that the viewer displays only metadata, while the associated dataset is not rendered or made available for download.

Following a modification to the DataHUB by the DataPLANT team, the HHU DataHUB was updated to the latest version and the validation pipelines were re-executed to regenerate the most recent RO-Crate metadata file. However, this update did not resolve the issue.

It was further identified that DataPLANT is working on a project called the Storage Resolver (https://github.com/nfdi4plants/storage-resolver), a microservice designed to resolve and provide access links for downloadable resources associated with ARC publications and referenced via RO-Crate.

# Discussion

The investigation indicates that the limitation is not primarily caused by the locally generated RO-Crate metadata or the HHU DataHUB configuration, but rather by the current capabilities of the ARC Web Viewer (https://nfdi4plants.github.io/ARCWebView/#) in handling dataset resolution and access.
While metadata from the ARC-RO-Crate is correctly parsed and displayed, the actual dataset contents are neither rendered nor made available for download, suggesting a missing or incomplete linkage between metadata representation and data access mechanisms within the viewer.

<img width="1592" height="562" alt="image" src="https://github.com/user-attachments/assets/fe536ee5-5db1-4704-8c09-53c41fe4309b" />

