# DataPLANT ARC Symposium 2024-04-08 - ARC Validation

This document describes the current state of the ARC validation pipeline in DataHUB and what improvements has been done to it during the hackathon. 

## Flowchart

```mermaid
flowchart LR;

subgraph mandatory[AutoDevOps Pipeline]
    direction LR
    arcjson(Create ISA\nARC JSON)
    qrgen(Check\nyml)
    qrtrigger(Generate child\npipeline/jobs)
    arcjson --> qrgen
    qrgen -- exists --> qrtrigger
end

subgraph optional[Dynamic Child Pipeline]
    direction LR
    subgraph p1[Package 1]
        direction LR
        p1validate(Validate ARC)
        p1badge(Create result badge)
        p1publish(Publication link)
        p1test(Link to tests)
        p1badge -- "#9989;" --> p1publish
        p1badge -- #10060; --> p1test
        p1validate --> p1badge
    end
    ...
    subgraph pn[Package n]
        direction LR
        pnvalidate(Validate ARC)
        pnbadge(Create result badge)
        pnpublish(Publication link)
        pntest(Link to tests)
        pnbadge--   "#9989;"  --> pnpublish
        pnbadge--   #10060;   --> pntest
        pnvalidate --> pnbadge
    end
end
qrtrigger --> optional

```
