# ServiceNow Modules - Use Case Diagrams

## Overview
This document contains Mermaid use case diagrams for all ServiceNow modules, illustrating the key actors, use cases, and interactions for each module.

---

## 1. ITSM (IT Service Management) - Use Case Diagram

```mermaid
graph TB
    subgraph "ITSM Module"
        direction TB
        
        subgraph "Incident Management"
            UC_IM1["Create Incident"]
            UC_IM2["Assign Incident"]
            UC_IM3["Resolve Incident"]
            UC_IM4["Track SLA"]
            UC_IM5["Escalate Incident"]
        end
        
        subgraph "Problem Management"
            UC_PM1["Report Problem"]
            UC_PM2["Analyze Root Cause"]
            UC_PM3["Create Known Error"]
            UC_PM4["Resolve Problem"]
        end
        
        subgraph "Change Management"
            UC_CM1["Submit Change Request"]
            UC_CM2["Assess Impact"]
            UC_CM3["Approve Change"]
            UC_CM4["Implement Change"]
            UC_CM5["Validate Change"]
        end
        
        subgraph "Request Management"
            UC_RM1["Submit Service Request"]
            UC_RM2["Fulfill Request"]
            UC_RM3["Track Fulfillment"]
        end
        
        subgraph "Service Catalog"
            UC_SC1["Browse Services"]
            UC_SC2["Order Service"]
            UC_SC3["Configure Service"]
        end
        
        subgraph "Knowledge Management"
            UC_KM1["Create Article"]
            UC_KM2["Search Knowledge"]
            UC_KM3["Use Self-Service"]
        end
    end
    
    User["👤 End User"]
    Agent["👤 Service Desk Agent"]
    Manager["👤 Manager"]
    CMDB_Actor["🗄️ CMDB"]
    
    User -->|"Creates"| UC_IM1
    User -->|"Submits"| UC_RM1
    User -->|"Browses"| UC_SC1
    User -->|"Searches"| UC_KM2
    
    Agent -->|"Assigns"| UC_IM2
    Agent -->|"Resolves"| UC_IM3
    Agent -->|"Analyzes"| UC_PM2
    Agent -->|"Fulfills"| UC_RM2
    
    Manager -->|"Approves"| UC_CM3
    Manager -->|"Reviews"| UC_IM4
    
    UC_IM1 -->|"Triggers"| UC_IM2
    UC_IM2 -->|"Leads to"| UC_IM3
    UC_IM3 -->|"Checks"| UC_IM4
    UC_IM2 -->|"May need"| UC_IM5
    
    UC_IM3 -->|"References"| UC_KM2
    UC_CM1 -->|"Checks"| UC_CM2
    UC_CM2 -->|"Routes to"| UC_CM3
    UC_CM3 -->|"Enables"| UC_CM4
    UC_CM4 -->|"Requires"| UC_CM5
    
    UC_SC1 -->|"Leads to"| UC_SC2
    UC_SC2 -->|"Creates"| UC_RM1
    
    UC_CM4 -->|"Updates"| CMDB_Actor
    UC_IM3 -->|"Updates"| CMDB_Actor
    
    style UC_IM1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_IM2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_IM3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_IM4 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_IM5 fill:#4CAF50,stroke:#2E7D32,color:#fff
    
    style UC_PM1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_PM2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_PM3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_PM4 fill:#4CAF50,stroke:#2E7D32,color:#fff
    
    style UC_CM1 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_CM2 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_CM3 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_CM4 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_CM5 fill:#FF9800,stroke:#E65100,color:#fff
    
    style UC_RM1 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_RM2 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_RM3 fill:#2196F3,stroke:#1565C0,color:#fff
    
    style UC_SC1 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_SC2 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_SC3 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    
    style UC_KM1 fill:#FFC107,stroke:#F57F17,color:#000
    style UC_KM2 fill:#FFC107,stroke:#F57F17,color:#000
    style UC_KM3 fill:#FFC107,stroke:#F57F17,color:#000
    
    style User fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Agent fill:#FF9800,stroke:#E65100,color:#fff
    style Manager fill:#2196F3,stroke:#1565C0,color:#fff
    style CMDB_Actor fill:#FF6B6B,stroke:#C92A2A,color:#fff
```

---

## 2. ITOM (IT Operations Management) - Use Case Diagram

```mermaid
graph TB
    subgraph "ITOM Module"
        direction TB
        
        subgraph "Discovery"
            UC_D1["Scan Network"]
            UC_D2["Detect Assets"]
            UC_D3["Identify Software"]
            UC_D4["Map Dependencies"]
        end
        
        subgraph "Service Mapping"
            UC_SM1["Create Service Map"]
            UC_SM2["Visualize Dependencies"]
            UC_SM3["Perform Impact Analysis"]
        end
        
        subgraph "Event Management"
            UC_EM1["Receive Alerts"]
            UC_EM2["Correlate Events"]
            UC_EM3["Create Incidents"]
            UC_EM4["Escalate Events"]
        end
        
        subgraph "Operational Intelligence"
            UC_OI1["Monitor Performance"]
            UC_OI2["Detect Anomalies"]
            UC_OI3["Predict Issues"]
            UC_OI4["Generate Insights"]
        end
        
        subgraph "Cloud Management"
            UC_CM1["Provision Cloud Resources"]
            UC_CM2["Manage Cloud Services"]
            UC_CM3["Optimize Cloud Costs"]
        end
    end
    
    Admin["👤 IT Administrator"]
    Monitor["👤 Operations Team"]
    CloudOps["👤 Cloud Operations"]
    CMDB_Actor["🗄️ CMDB"]
    ExternalSys["🔗 External Systems"]
    
    Admin -->|"Initiates"| UC_D1
    Monitor -->|"Monitors"| UC_EM1
    Monitor -->|"Reviews"| UC_OI1
    CloudOps -->|"Manages"| UC_CM1
    
    UC_D1 -->|"Discovers"| UC_D2
    UC_D2 -->|"Identifies"| UC_D3
    UC_D3 -->|"Maps"| UC_D4
    
    UC_D4 -->|"Feeds"| UC_SM1
    UC_SM1 -->|"Enables"| UC_SM2
    UC_SM2 -->|"Supports"| UC_SM3
    
    ExternalSys -->|"Sends"| UC_EM1
    UC_EM1 -->|"Correlates"| UC_EM2
    UC_EM2 -->|"Creates"| UC_EM3
    UC_EM3 -->|"May"| UC_EM4
    
    UC_EM1 -->|"Triggers"| UC_OI1
    UC_OI1 -->|"Detects"| UC_OI2
    UC_OI2 -->|"Predicts"| UC_OI3
    UC_OI3 -->|"Generates"| UC_OI4
    
    UC_CM1 -->|"Provisions"| UC_CM2
    UC_CM2 -->|"Enables"| UC_CM3
    
    UC_D4 -->|"Updates"| CMDB_Actor
    UC_SM1 -->|"Uses"| CMDB_Actor
    UC_SM3 -->|"References"| CMDB_Actor
    
    style UC_D1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_D2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_D3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_D4 fill:#4CAF50,stroke:#2E7D32,color:#fff
    
    style UC_SM1 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_SM2 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_SM3 fill:#2196F3,stroke:#1565C0,color:#fff
    
    style UC_EM1 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_EM2 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_EM3 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_EM4 fill:#FF9800,stroke:#E65100,color:#fff
    
    style UC_OI1 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_OI2 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_OI3 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_OI4 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    
    style UC_CM1 fill:#FFC107,stroke:#F57F17,color:#000
    style UC_CM2 fill:#FFC107,stroke:#F57F17,color:#000
    style UC_CM3 fill:#FFC107,stroke:#F57F17,color:#000
    
    style Admin fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Monitor fill:#FF9800,stroke:#E65100,color:#fff
    style CloudOps fill:#2196F3,stroke:#1565C0,color:#fff
    style CMDB_Actor fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style ExternalSys fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

---

## 3. ITAM (IT Asset Management) - Use Case Diagram

```mermaid
graph TB
    subgraph "ITAM Module"
        direction TB
        
        subgraph "Hardware Asset Management"
            UC_HAM1["Track Hardware"]
            UC_HAM2["Manage Inventory"]
            UC_HAM3["Track Lifecycle"]
            UC_HAM4["Depreciate Assets"]
        end
        
        subgraph "Software Asset Management"
            UC_SAM1["Track Software"]
            UC_SAM2["Manage Licenses"]
            UC_SAM3["Ensure Compliance"]
            UC_SAM4["Optimize Usage"]
        end
        
        subgraph "License Management"
            UC_LM1["Purchase Licenses"]
            UC_LM2["Allocate Licenses"]
            UC_LM3["Track Usage"]
            UC_LM4["Renew Licenses"]
        end
        
        subgraph "Contract Management"
            UC_CM1["Create Contracts"]
            UC_CM2["Track Terms"]
            UC_CM3["Manage Renewals"]
            UC_CM4["Monitor Costs"]
        end
    end
    
    AssetMgr["👤 Asset Manager"]
    Procurement["👤 Procurement"]
    Finance["👤 Finance"]
    Compliance["👤 Compliance Officer"]
    
    AssetMgr -->|"Tracks"| UC_HAM1
    AssetMgr -->|"Manages"| UC_HAM2
    AssetMgr -->|"Tracks"| UC_SAM1
    
    Procurement -->|"Purchases"| UC_LM1
    Procurement -->|"Creates"| UC_CM1
    
    Finance -->|"Monitors"| UC_CM4
    Finance -->|"Tracks"| UC_HAM4
    
    Compliance -->|"Ensures"| UC_SAM3
    Compliance -->|"Verifies"| UC_LM3
    
    UC_HAM1 -->|"Enables"| UC_HAM2
    UC_HAM2 -->|"Tracks"| UC_HAM3
    UC_HAM3 -->|"Leads to"| UC_HAM4
    
    UC_SAM1 -->|"Enables"| UC_SAM2
    UC_SAM2 -->|"Ensures"| UC_SAM3
    UC_SAM3 -->|"Optimizes"| UC_SAM4
    
    UC_LM1 -->|"Enables"| UC_LM2
    UC_LM2 -->|"Requires"| UC_LM3
    UC_LM3 -->|"Triggers"| UC_LM4
    
    UC_CM1 -->|"Defines"| UC_CM2
    UC_CM2 -->|"Requires"| UC_CM3
    UC_CM3 -->|"Impacts"| UC_CM4
    
    UC_HAM1 -->|"Links to"| UC_CM1
    UC_SAM1 -->|"Links to"| UC_CM1
    
    style UC_HAM1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_HAM2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_HAM3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_HAM4 fill:#4CAF50,stroke:#2E7D32,color:#fff
    
    style UC_SAM1 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_SAM2 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_SAM3 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_SAM4 fill:#2196F3,stroke:#1565C0,color:#fff
    
    style UC_LM1 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_LM2 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_LM3 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_LM4 fill:#FF9800,stroke:#E65100,color:#fff
    
    style UC_CM1 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_CM2 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_CM3 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_CM4 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    
    style AssetMgr fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Procurement fill:#FF9800,stroke:#E65100,color:#fff
    style Finance fill:#2196F3,stroke:#1565C0,color:#fff
    style Compliance fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

---

## 4. GRC (Governance, Risk, and Compliance) - Use Case Diagram

```mermaid
graph TB
    subgraph "GRC Module"
        direction TB
        
        subgraph "Policy Management"
            UC_PM1["Create Policy"]
            UC_PM2["Distribute Policy"]
            UC_PM3["Track Acknowledgment"]
            UC_PM4["Update Policy"]
        end
        
        subgraph "Risk Management"
            UC_RM1["Identify Risks"]
            UC_RM2["Assess Risk"]
            UC_RM3["Mitigate Risk"]
            UC_RM4["Monitor Risk"]
        end
        
        subgraph "Audit Management"
            UC_AM1["Plan Audit"]
            UC_AM2["Execute Audit"]
            UC_AM3["Collect Evidence"]
            UC_AM4["Report Findings"]
        end
        
        subgraph "Compliance Management"
            UC_CM1["Map Regulations"]
            UC_CM2["Track Compliance"]
            UC_CM3["Generate Reports"]
            UC_CM4["Remediate Issues"]
        end
    end
    
    Compliance["👤 Compliance Officer"]
    RiskMgr["👤 Risk Manager"]
    Auditor["👤 Internal Auditor"]
    Executive["👤 Executive"]
    
    Compliance -->|"Creates"| UC_PM1
    Compliance -->|"Tracks"| UC_CM2
    Compliance -->|"Generates"| UC_CM3
    
    RiskMgr -->|"Identifies"| UC_RM1
    RiskMgr -->|"Assesses"| UC_RM2
    RiskMgr -->|"Mitigates"| UC_RM3
    RiskMgr -->|"Monitors"| UC_RM4
    
    Auditor -->|"Plans"| UC_AM1
    Auditor -->|"Executes"| UC_AM2
    Auditor -->|"Collects"| UC_AM3
    Auditor -->|"Reports"| UC_AM4
    
    Executive -->|"Reviews"| UC_CM3
    Executive -->|"Reviews"| UC_AM4
    
    UC_PM1 -->|"Enables"| UC_PM2
    UC_PM2 -->|"Requires"| UC_PM3
    UC_PM3 -->|"Leads to"| UC_PM4
    
    UC_RM1 -->|"Leads to"| UC_RM2
    UC_RM2 -->|"Enables"| UC_RM3
    UC_RM3 -->|"Requires"| UC_RM4
    
    UC_AM1 -->|"Enables"| UC_AM2
    UC_AM2 -->|"Requires"| UC_AM3
    UC_AM3 -->|"Leads to"| UC_AM4
    
    UC_CM1 -->|"Enables"| UC_CM2
    UC_CM2 -->|"Enables"| UC_CM3
    UC_CM3 -->|"Triggers"| UC_CM4
    
    UC_PM1 -->|"Supports"| UC_CM1
    UC_RM1 -->|"Informs"| UC_CM2
    
    style UC_PM1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_PM2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_PM3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_PM4 fill:#4CAF50,stroke:#2E7D32,color:#fff
    
    style UC_RM1 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_RM2 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_RM3 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_RM4 fill:#2196F3,stroke:#1565C0,color:#fff
    
    style UC_AM1 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_AM2 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_AM3 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_AM4 fill:#FF9800,stroke:#E65100,color:#fff
    
    style UC_CM1 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_CM2 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_CM3 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_CM4 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    
    style Compliance fill:#4CAF50,stroke:#2E7D32,color:#fff
    style RiskMgr fill:#2196F3,stroke:#1565C0,color:#fff
    style Auditor fill:#FF9800,stroke:#E65100,color:#fff
    style Executive fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

---

## 5. CSM (Customer Service Management) - Use Case Diagram

```mermaid
graph TB
    subgraph "CSM Module"
        direction TB
        
        subgraph "Case Management"
            UC_CM1["Create Case"]
            UC_CM2["Assign Case"]
            UC_CM3["Resolve Case"]
            UC_CM4["Close Case"]
        end
        
        subgraph "Customer Portal"
            UC_CP1["Browse Services"]
            UC_CP2["Submit Case"]
            UC_CP3["Track Case Status"]
            UC_CP4["Access Knowledge"]
        end
        
        subgraph "Virtual Agent"
            UC_VA1["Chat with Bot"]
            UC_VA2["Get Recommendations"]
            UC_VA3["Escalate to Agent"]
        end
        
        subgraph "Entitlements & SLAs"
            UC_ES1["Define Entitlements"]
            UC_ES2["Track SLAs"]
            UC_ES3["Escalate on Breach"]
        end
        
        subgraph "Communities"
            UC_CO1["Post Question"]
            UC_CO2["Share Knowledge"]
            UC_CO3["Get Peer Support"]
        end
    end
    
    Customer["👤 Customer"]
    Agent["👤 Support Agent"]
    Manager["👤 Support Manager"]
    
    Customer -->|"Submits"| UC_CM1
    Customer -->|"Uses"| UC_CP1
    Customer -->|"Chats"| UC_VA1
    Customer -->|"Posts"| UC_CO1
    
    Agent -->|"Assigns"| UC_CM2
    Agent -->|"Resolves"| UC_CM3
    Agent -->|"Closes"| UC_CM4
    Agent -->|"Escalates"| UC_VA3
    
    Manager -->|"Monitors"| UC_ES2
    Manager -->|"Defines"| UC_ES1
    
    UC_CM1 -->|"Leads to"| UC_CM2
    UC_CM2 -->|"Leads to"| UC_CM3
    UC_CM3 -->|"Leads to"| UC_CM4
    
    UC_CP1 -->|"Enables"| UC_CP2
    UC_CP2 -->|"Creates"| UC_CM1
    UC_CP2 -->|"Enables"| UC_CP3
    UC_CP1 -->|"Provides"| UC_CP4
    
    UC_VA1 -->|"May"| UC_VA2
    UC_VA2 -->|"May"| UC_VA3
    UC_VA3 -->|"Creates"| UC_CM1
    
    UC_ES1 -->|"Enables"| UC_ES2
    UC_ES2 -->|"May"| UC_ES3
    UC_ES3 -->|"Triggers"| UC_CM2
    
    UC_CO1 -->|"Enables"| UC_CO2
    UC_CO2 -->|"Provides"| UC_CO3
    UC_CO3 -->|"May resolve"| UC_CM1
    
    style UC_CM1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_CM2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_CM3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_CM4 fill:#4CAF50,stroke:#2E7D32,color:#fff
    
    style UC_CP1 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_CP2 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_CP3 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_CP4 fill:#2196F3,stroke:#1565C0,color:#fff
    
    style UC_VA1 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_VA2 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_VA3 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    
    style UC_ES1 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_ES2 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_ES3 fill:#FF9800,stroke:#E65100,color:#fff
    
    style UC_CO1 fill:#FFC107,stroke:#F57F17,color:#000
    style UC_CO2 fill:#FFC107,stroke:#F57F17,color:#000
    style UC_CO3 fill:#FFC107,stroke:#F57F17,color:#000
    
    style Customer fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Agent fill:#FF9800,stroke:#E65100,color:#fff
    style Manager fill:#2196F3,stroke:#1565C0,color:#fff
```

---

## 6. HRSD (HR Service Delivery) - Use Case Diagram

```mermaid
graph TB
    subgraph "HRSD Module"
        direction TB
        
        subgraph "Employee Service Center"
            UC_ESC1["Submit HR Request"]
            UC_ESC2["Track Request"]
            UC_ESC3["Access HR Services"]
            UC_ESC4["View HR Documents"]
        end
        
        subgraph "Onboarding"
            UC_OB1["Create Onboarding Plan"]
            UC_OB2["Assign Tasks"]
            UC_OB3["Track Progress"]
            UC_OB4["Complete Onboarding"]
        end
        
        subgraph "Offboarding"
            UC_OB1["Create Offboarding Plan"]
            UC_OB2["Assign Exit Tasks"]
            UC_OB3["Track Completion"]
            UC_OB4["Archive Employee"]
        end
        
        subgraph "HR Surveys"
            UC_SV1["Create Survey"]
            UC_SV2["Distribute Survey"]
            UC_SV3["Collect Responses"]
            UC_SV4["Analyze Results"]
        end
        
        subgraph "Case Management"
            UC_CM1["Create HR Case"]
            UC_CM2["Route to HR"]
            UC_CM3["Resolve Case"]
            UC_CM4["Close Case"]
        end
    end
    
    Employee["👤 Employee"]
    Manager["👤 Manager"]
    HR["👤 HR Specialist"]
    
    Employee -->|"Submits"| UC_ESC1
    Employee -->|"Tracks"| UC_ESC2
    Employee -->|"Accesses"| UC_ESC3
    Employee -->|"Views"| UC_ESC4
    Employee -->|"Responds"| UC_SV3
    
    Manager -->|"Creates"| UC_OB1
    Manager -->|"Assigns"| UC_OB2
    Manager -->|"Tracks"| UC_OB3
    
    HR -->|"Creates"| UC_CM1
    HR -->|"Routes"| UC_CM2
    HR -->|"Resolves"| UC_CM3
    HR -->|"Closes"| UC_CM4
    HR -->|"Creates"| UC_SV1
    HR -->|"Distributes"| UC_SV2
    HR -->|"Analyzes"| UC_SV4
    
    UC_ESC1 -->|"Enables"| UC_ESC2
    UC_ESC3 -->|"Provides"| UC_ESC4
    
    UC_OB1 -->|"Enables"| UC_OB2
    UC_OB2 -->|"Requires"| UC_OB3
    UC_OB3 -->|"Leads to"| UC_OB4
    
    UC_SV1 -->|"Enables"| UC_SV2
    UC_SV2 -->|"Enables"| UC_SV3
    UC_SV3 -->|"Enables"| UC_SV4
    
    UC_CM1 -->|"Leads to"| UC_CM2
    UC_CM2 -->|"Leads to"| UC_CM3
    UC_CM3 -->|"Leads to"| UC_CM4
    
    style UC_ESC1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_ESC2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_ESC3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_ESC4 fill:#4CAF50,stroke:#2E7D32,color:#fff
    
    style UC_OB1 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_OB2 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_OB3 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_OB4 fill:#2196F3,stroke:#1565C0,color:#fff
    
    style UC_SV1 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_SV2 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_SV3 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_SV4 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    
    style UC_CM1 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_CM2 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_CM3 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_CM4 fill:#FF9800,stroke:#E65100,color:#fff
    
    style Employee fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Manager fill:#2196F3,stroke:#1565C0,color:#fff
    style HR fill:#FF9800,stroke:#E65100,color:#fff
```

---

## 7. FSM (Field Service Management) - Use Case Diagram

```mermaid
graph TB
    subgraph "FSM Module"
        direction TB
        
        subgraph "Work Order Management"
            UC_WO1["Create Work Order"]
            UC_WO2["Assign Technician"]
            UC_WO3["Schedule Service"]
            UC_WO4["Complete Work"]
        end
        
        subgraph "Mobile Execution"
            UC_ME1["View Assignment"]
            UC_ME2["Navigate to Site"]
            UC_ME3["Complete Tasks"]
            UC_ME4["Capture Data"]
        end
        
        subgraph "Workforce Optimization"
            UC_WO1["Optimize Routes"]
            UC_WO2["Balance Workload"]
            UC_WO3["Predict Capacity"]
            UC_WO4["Allocate Resources"]
        end
        
        subgraph "Predictive Maintenance"
            UC_PM1["Monitor Assets"]
            UC_PM2["Predict Failures"]
            UC_PM3["Schedule Maintenance"]
            UC_PM4["Prevent Downtime"]
        end
    end
    
    Customer["👤 Customer"]
    Dispatcher["👤 Dispatcher"]
    Technician["👤 Field Technician"]
    Manager["👤 Service Manager"]
    
    Customer -->|"Requests"| UC_WO1
    Dispatcher -->|"Creates"| UC_WO1
    Dispatcher -->|"Assigns"| UC_WO2
    Dispatcher -->|"Schedules"| UC_WO3
    Dispatcher -->|"Optimizes"| UC_WO1
    
    Technician -->|"Views"| UC_ME1
    Technician -->|"Navigates"| UC_ME2
    Technician -->|"Completes"| UC_ME3
    Technician -->|"Captures"| UC_ME4
    
    Manager -->|"Monitors"| UC_PM1
    Manager -->|"Reviews"| UC_WO4
    
    UC_WO1 -->|"Leads to"| UC_WO2
    UC_WO2 -->|"Leads to"| UC_WO3
    UC_WO3 -->|"Leads to"| UC_WO4
    
    UC_ME1 -->|"Enables"| UC_ME2
    UC_ME2 -->|"Enables"| UC_ME3
    UC_ME3 -->|"Requires"| UC_ME4
    
    UC_WO1 -->|"Enables"| UC_WO2
    UC_WO2 -->|"Enables"| UC_WO3
    UC_WO3 -->|"Enables"| UC_WO4
    
    UC_PM1 -->|"Enables"| UC_PM2
    UC_PM2 -->|"Enables"| UC_PM3
    UC_PM3 -->|"Enables"| UC_PM4
    
    UC_WO3 -->|"Informs"| UC_PM3
    
    style UC_WO1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_WO2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_WO3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_WO4 fill:#4CAF50,stroke:#2E7D32,color:#fff
    
    style UC_ME1 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_ME2 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_ME3 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_ME4 fill:#2196F3,stroke:#1565C0,color:#fff
    
    style UC_PM1 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_PM2 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_PM3 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_PM4 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    
    style Customer fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Dispatcher fill:#FF9800,stroke:#E65100,color:#fff
    style Technician fill:#2196F3,stroke:#1565C0,color:#fff
    style Manager fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

---

## 8. PPM (Project Portfolio Management) - Use Case Diagram

```mermaid
graph TB
    subgraph "PPM Module"
        direction TB
        
        subgraph "Demand Management"
            UC_DM1["Submit Demand"]
            UC_DM2["Evaluate Demand"]
            UC_DM3["Prioritize Demand"]
            UC_DM4["Approve Demand"]
        end
        
        subgraph "Project Management"
            UC_PM1["Create Project"]
            UC_PM2["Plan Project"]
            UC_PM3["Execute Project"]
            UC_PM4["Close Project"]
        end
        
        subgraph "Resource Management"
            UC_RM1["Allocate Resources"]
            UC_RM2["Track Utilization"]
            UC_RM3["Balance Workload"]
            UC_RM4["Optimize Allocation"]
        end
        
        subgraph "Portfolio Management"
            UC_PO1["Create Portfolio"]
            UC_PO2["Align Projects"]
            UC_PO3["Monitor Portfolio"]
            UC_PO4["Report Status"]
        end
    end
    
    Requester["👤 Business Requester"]
    PMO["👤 PMO Manager"]
    PM["👤 Project Manager"]
    Executive["👤 Executive"]
    
    Requester -->|"Submits"| UC_DM1
    PMO -->|"Evaluates"| UC_DM2
    PMO -->|"Prioritizes"| UC_DM3
    PMO -->|"Approves"| UC_DM4
    PMO -->|"Creates"| UC_PM1
    PMO -->|"Creates"| UC_PO1
    
    PM -->|"Plans"| UC_PM2
    PM -->|"Executes"| UC_PM3
    PM -->|"Closes"| UC_PM4
    PM -->|"Tracks"| UC_RM2
    
    Executive -->|"Reviews"| UC_PO3
    Executive -->|"Reviews"| UC_PO4
    
    UC_DM1 -->|"Leads to"| UC_DM2
    UC_DM2 -->|"Leads to"| UC_DM3
    UC_DM3 -->|"Leads to"| UC_DM4
    UC_DM4 -->|"Enables"| UC_PM1
    
    UC_PM1 -->|"Leads to"| UC_PM2
    UC_PM2 -->|"Leads to"| UC_PM3
    UC_PM3 -->|"Leads to"| UC_PM4
    
    UC_RM1 -->|"Enables"| UC_RM2
    UC_RM2 -->|"Enables"| UC_RM3
    UC_RM3 -->|"Enables"| UC_RM4
    
    UC_PO1 -->|"Includes"| UC_PM1
    UC_PO1 -->|"Enables"| UC_PO2
    UC_PO2 -->|"Enables"| UC_PO3
    UC_PO3 -->|"Enables"| UC_PO4
    
    UC_PM1 -->|"Requires"| UC_RM1
    
    style UC_DM1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_DM2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_DM3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_DM4 fill:#4CAF50,stroke:#2E7D32,color:#fff
    
    style UC_PM1 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_PM2 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_PM3 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_PM4 fill:#2196F3,stroke:#1565C0,color:#fff
    
    style UC_RM1 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_RM2 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_RM3 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_RM4 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    
    style UC_PO1 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_PO2 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_PO3 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_PO4 fill:#FF9800,stroke:#E65100,color:#fff
    
    style Requester fill:#4CAF50,stroke:#2E7D32,color:#fff
    style PMO fill:#FF9800,stroke:#E65100,color:#fff
    style PM fill:#2196F3,stroke:#1565C0,color:#fff
    style Executive fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

---

## 9. Finance & Supply Chain - Use Case Diagram

```mermaid
graph TB
    subgraph "Finance & Supply Chain Module"
        direction TB
        
        subgraph "Procurement"
            UC_PR1["Create PO"]
            UC_PR2["Send to Vendor"]
            UC_PR3["Receive Goods"]
            UC_PR4["Process Invoice"]
        end
        
        subgraph "Supplier Management"
            UC_SM1["Onboard Supplier"]
            UC_SM2["Manage Performance"]
            UC_SM3["Track Compliance"]
            UC_SM4["Renew Contracts"]
        end
        
        subgraph "Supply Chain Planning"
            UC_SCP1["Forecast Demand"]
            UC_SCP2["Plan Inventory"]
            UC_SCP3["Optimize Stock"]
            UC_SCP4["Track Shipments"]
        end
        
        subgraph "Finance Operations"
            UC_FO1["Record Transactions"]
            UC_FO2["Manage Accounts"]
            UC_FO3["Generate Reports"]
            UC_FO4["Close Period"]
        end
    end
    
    Requester["👤 Requester"]
    Procurement["👤 Procurement"]
    Supplier["👤 Supplier"]
    Finance["👤 Finance"]
    Executive["👤 Executive"]
    
    Requester -->|"Requests"| UC_PR1
    Procurement -->|"Creates"| UC_PR1
    Procurement -->|"Sends"| UC_PR2
    Procurement -->|"Receives"| UC_PR3
    Procurement -->|"Onboards"| UC_SM1
    Procurement -->|"Manages"| UC_SM2
    
    Supplier -->|"Receives"| UC_PR2
    Supplier -->|"Complies"| UC_SM3
    
    Finance -->|"Processes"| UC_PR4
    Finance -->|"Records"| UC_FO1
    Finance -->|"Manages"| UC_FO2
    Finance -->|"Generates"| UC_FO3
    Finance -->|"Closes"| UC_FO4
    
    Executive -->|"Reviews"| UC_FO3
    Executive -->|"Reviews"| UC_SCP4
    
    UC_PR1 -->|"Leads to"| UC_PR2
    UC_PR2 -->|"Leads to"| UC_PR3
    UC_PR3 -->|"Leads to"| UC_PR4
    
    UC_SM1 -->|"Enables"| UC_SM2
    UC_SM2 -->|"Enables"| UC_SM3
    UC_SM3 -->|"Leads to"| UC_SM4
    
    UC_SCP1 -->|"Enables"| UC_SCP2
    UC_SCP2 -->|"Enables"| UC_SCP3
    UC_SCP3 -->|"Enables"| UC_SCP4
    
    UC_FO1 -->|"Enables"| UC_FO2
    UC_FO2 -->|"Enables"| UC_FO3
    UC_FO3 -->|"Enables"| UC_FO4
    
    UC_PR4 -->|"Triggers"| UC_FO1
    UC_SCP1 -->|"Informs"| UC_PR1
    
    style UC_PR1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_PR2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_PR3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_PR4 fill:#4CAF50,stroke:#2E7D32,color:#fff
    
    style UC_SM1 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_SM2 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_SM3 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_SM4 fill:#2196F3,stroke:#1565C0,color:#fff
    
    style UC_SCP1 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_SCP2 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_SCP3 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_SCP4 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    
    style UC_FO1 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_FO2 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_FO3 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_FO4 fill:#FF9800,stroke:#E65100,color:#fff
    
    style Requester fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Procurement fill:#FF9800,stroke:#E65100,color:#fff
    style Supplier fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style Finance fill:#2196F3,stroke:#1565C0,color:#fff
    style Executive fill:#FF6B6B,stroke:#C92A2A,color:#fff
```

---

## 10. Workflow Engine & Automation - Use Case Diagram

```mermaid
graph TB
    subgraph "Workflow Engine & Automation"
        direction TB
        
        subgraph "Workflow Design"
            UC_WD1["Design Workflow"]
            UC_WD2["Define Activities"]
            UC_WD3["Set Conditions"]
            UC_WD4["Test Workflow"]
        end
        
        subgraph "Flow Designer"
            UC_FD1["Create Flow"]
            UC_FD2["Add Actions"]
            UC_FD3["Define Logic"]
            UC_FD4["Deploy Flow"]
        end
        
        subgraph "Automation Execution"
            UC_AE1["Trigger Workflow"]
            UC_AE2["Execute Activities"]
            UC_AE3["Evaluate Conditions"]
            UC_AE4["Send Notifications"]
        end
        
        subgraph "Monitoring & Debugging"
            UC_MD1["Monitor Execution"]
            UC_MD2["Debug Flow"]
            UC_MD3["View History"]
            UC_MD4["Optimize Performance"]
        end
    end
    
    Developer["👤 Developer"]
    BusinessUser["👤 Business User"]
    Admin["👤 Administrator"]
    
    Developer -->|"Designs"| UC_WD1
    Developer -->|"Creates"| UC_FD1
    Developer -->|"Debugs"| UC_MD2
    
    BusinessUser -->|"Defines"| UC_WD2
    BusinessUser -->|"Tests"| UC_WD4
    
    Admin -->|"Deploys"| UC_FD4
    Admin -->|"Monitors"| UC_MD1
    Admin -->|"Optimizes"| UC_MD4
    
    UC_WD1 -->|"Enables"| UC_WD2
    UC_WD2 -->|"Enables"| UC_WD3
    UC_WD3 -->|"Enables"| UC_WD4
    
    UC_FD1 -->|"Enables"| UC_FD2
    UC_FD2 -->|"Enables"| UC_FD3
    UC_FD3 -->|"Enables"| UC_FD4
    
    UC_FD4 -->|"Triggers"| UC_AE1
    UC_AE1 -->|"Executes"| UC_AE2
    UC_AE2 -->|"Evaluates"| UC_AE3
    UC_AE3 -->|"Triggers"| UC_AE4
    
    UC_AE1 -->|"Enables"| UC_MD1
    UC_MD1 -->|"Enables"| UC_MD2
    UC_MD2 -->|"Enables"| UC_MD3
    UC_MD3 -->|"Enables"| UC_MD4
    
    style UC_WD1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_WD2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_WD3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style UC_WD4 fill:#4CAF50,stroke:#2E7D32,color:#fff
    
    style UC_FD1 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_FD2 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_FD3 fill:#2196F3,stroke:#1565C0,color:#fff
    style UC_FD4 fill:#2196F3,stroke:#1565C0,color:#fff
    
    style UC_AE1 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_AE2 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_AE3 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style UC_AE4 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    
    style UC_MD1 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_MD2 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_MD3 fill:#FF9800,stroke:#E65100,color:#fff
    style UC_MD4 fill:#FF9800,stroke:#E65100,color:#fff
    
    style Developer fill:#4CAF50,stroke:#2E7D32,color:#fff
    style BusinessUser fill:#2196F3,stroke:#1565C0,color:#fff
    style Admin fill:#FF9800,stroke:#E65100,color:#fff
```

---

## Summary of Use Cases by Module

| Module | Primary Actors | Key Use Cases | Primary Benefits |
|--------|---|---|---|
| **ITSM** | End Users, Agents, Managers | Incident, Problem, Change, Request Management | Faster resolution, Better service quality |
| **ITOM** | Admins, Operations Team | Discovery, Monitoring, Event Management | Proactive issue detection, Infrastructure visibility |
| **ITAM** | Asset Managers, Finance, Compliance | Asset Tracking, License Management, Compliance | Cost optimization, Compliance assurance |
| **GRC** | Compliance, Risk, Auditors | Policy, Risk, Audit, Compliance Management | Regulatory compliance, Risk mitigation |
| **CSM** | Customers, Agents, Managers | Case Management, Portal, Virtual Agent | Customer satisfaction, Self-service |
| **HRSD** | Employees, HR, Managers | Onboarding, Offboarding, HR Services | Employee experience, Efficiency |
| **FSM** | Customers, Dispatchers, Technicians | Work Orders, Mobile Execution, Optimization | First-time fix, Resource optimization |
| **PPM** | Requesters, PMO, Executives | Demand, Project, Portfolio Management | Strategic alignment, Resource optimization |
| **Finance & Supply Chain** | Procurement, Finance, Suppliers | Procurement, Supplier, Finance Management | Cost reduction, Supply chain visibility |
| **Workflow Engine** | Developers, Business Users, Admins | Design, Execution, Monitoring | Process automation, Efficiency |

---

## Color Legend

- **Green (#4CAF50)** – Primary/Core Use Cases
- **Blue (#2196F3)** – Secondary/Support Use Cases
- **Purple (#9C27B0)** – Advanced/Specialized Use Cases
- **Orange (#FF9800)** – Management/Administrative Use Cases
- **Yellow (#FFC107)** – Collaborative/Community Use Cases

---

## Conclusion

These use case diagrams provide a comprehensive view of the key actors, use cases, and interactions for each ServiceNow module. They illustrate how different user roles interact with each module to achieve business objectives and deliver value across the organization.
