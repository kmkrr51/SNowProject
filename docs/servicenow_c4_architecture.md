# ServiceNow C4 Architecture Diagrams

## Overview
This document contains C4 (Context, Container, Component, Code) architecture diagrams for the ServiceNow platform and its modules using Mermaid syntax.

---

## C1: System Context Diagram

```mermaid
graph TB
    User["👤 End Users<br/>(Employees, Customers)"]
    Admin["👤 Administrators<br/>(IT, HR, Finance)"]
    ExtSys["🔗 External Systems<br/>(ERP, CRM, Cloud)"]
    
    SN["ServiceNow Platform<br/>Digital Workflow Automation"]
    
    User -->|Uses Services| SN
    Admin -->|Manages & Configures| SN
    ExtSys -->|Integrates Data| SN
    SN -->|Provides Workflows| User
    SN -->|Sends Notifications| User
    SN -->|Manages Operations| Admin
    SN -->|Exchanges Data| ExtSys
    
    style SN fill:#0066cc,stroke:#003366,color:#fff
    style User fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Admin fill:#FF9800,stroke:#E65100,color:#fff
    style ExtSys fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

---

## C2: Container Diagram - ServiceNow Platform

```mermaid
graph TB
    subgraph "ServiceNow Platform"
        direction TB
        
        subgraph "User Interfaces"
            Portal["Service Portal<br/>(Customer/Employee)"]
            Workspace["Workspaces<br/>(Agent Interface)"]
            Mobile["Mobile Apps<br/>(iOS/Android)"]
        end
        
        subgraph "Core Platform"
            WFE["Workflow Engine<br/>(Process Automation)"]
            CMDB["CMDB<br/>(Configuration Data)"]
            IRE["Identification &<br/>Reconciliation Engine"]
            Discovery["Discovery Engine<br/>(Auto CI Detection)"]
        end
        
        subgraph "Application Modules"
            ITSM["ITSM<br/>(Incident, Change, Problem)"]
            ITOM["ITOM<br/>(Operations, Monitoring)"]
            CSM["CSM<br/>(Customer Service)"]
            HRSD["HRSD<br/>(HR Service Delivery)"]
            FSM["FSM<br/>(Field Service)"]
            GRC["GRC<br/>(Governance, Risk)"]
            PPM["PPM<br/>(Project Portfolio)"]
            Finance["Finance & Supply Chain"]
        end
        
        subgraph "Platform Services"
            Auth["Authentication<br/>(SSO, SAML)"]
            Integration["Integration Platform<br/>(APIs, IntegrationHub)"]
            Analytics["Performance Analytics<br/>(Reporting, Dashboards)"]
            Security["Security & Compliance<br/>(Encryption, Audit)"]
        end
        
        subgraph "Data & Storage"
            Database["Database<br/>(PostgreSQL/MySQL)"]
            Cache["Cache Layer<br/>(Redis)"]
            Storage["File Storage<br/>(Attachments)"]
        end
        
        Portal --> WFE
        Workspace --> WFE
        Mobile --> WFE
        
        WFE --> CMDB
        CMDB --> IRE
        Discovery --> CMDB
        
        ITSM --> CMDB
        ITOM --> CMDB
        CSM --> CMDB
        HRSD --> CMDB
        FSM --> CMDB
        GRC --> CMDB
        PPM --> CMDB
        Finance --> CMDB
        
        ITSM --> WFE
        ITOM --> WFE
        CSM --> WFE
        HRSD --> WFE
        FSM --> WFE
        
        Auth --> Portal
        Auth --> Workspace
        Integration --> WFE
        Analytics --> ITSM
        Analytics --> ITOM
        Security --> Database
        
        Database --> CMDB
        Cache --> WFE
        Storage --> Portal
    end
    
    style Portal fill:#2196F3,stroke:#1565C0,color:#fff
    style Workspace fill:#2196F3,stroke:#1565C0,color:#fff
    style Mobile fill:#2196F3,stroke:#1565C0,color:#fff
    
    style WFE fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style CMDB fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style IRE fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style Discovery fill:#FF6B6B,stroke:#C92A2A,color:#fff
    
    style ITSM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style ITOM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style CSM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style HRSD fill:#4CAF50,stroke:#2E7D32,color:#fff
    style FSM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style GRC fill:#4CAF50,stroke:#2E7D32,color:#fff
    style PPM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Finance fill:#4CAF50,stroke:#2E7D32,color:#fff
    
    style Auth fill:#FFC107,stroke:#F57F17,color:#000
    style Integration fill:#FFC107,stroke:#F57F17,color:#000
    style Analytics fill:#FFC107,stroke:#F57F17,color:#000
    style Security fill:#FFC107,stroke:#F57F17,color:#000
    
    style Database fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style Cache fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style Storage fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

---

## C3: Component Diagram - ITSM Module

```mermaid
graph TB
    subgraph "ITSM Module Components"
        direction TB
        
        subgraph "Service Desk"
            IM["Incident Management<br/>- Create/Track Incidents<br/>- Assignment & Routing<br/>- SLA Tracking"]
            PM["Problem Management<br/>- Root Cause Analysis<br/>- Known Errors<br/>- Problem Resolution"]
            CM["Change Management<br/>- Change Requests<br/>- Approval Workflows<br/>- Implementation"]
        end
        
        subgraph "Service Delivery"
            RM["Request Management<br/>- Service Requests<br/>- Fulfillment<br/>- Tracking"]
            SC["Service Catalog<br/>- Service Items<br/>- Ordering Interface<br/>- Item Templates"]
            KM["Knowledge Management<br/>- Knowledge Base<br/>- FAQs<br/>- Troubleshooting"]
        end
        
        subgraph "Infrastructure"
            CMDB_ITSM["CMDB<br/>- Configuration Items<br/>- Relationships<br/>- Dependencies"]
            SLM["Service Level Management<br/>- SLA Definition<br/>- SLA Tracking<br/>- Reporting"]
        end
        
        IM --> CMDB_ITSM
        PM --> CMDB_ITSM
        CM --> CMDB_ITSM
        RM --> SC
        SC --> KM
        IM --> SLM
        PM --> SLM
        CM --> SLM
    end
    
    style IM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style PM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style CM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style RM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style SC fill:#4CAF50,stroke:#2E7D32,color:#fff
    style KM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style CMDB_ITSM fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style SLM fill:#FFC107,stroke:#F57F17,color:#000
```

---

## C3: Component Diagram - ITOM Module

```mermaid
graph TB
    subgraph "ITOM Module Components"
        direction TB
        
        subgraph "Discovery & Mapping"
            Discovery_Comp["Discovery<br/>- Auto CI Detection<br/>- Asset Scanning<br/>- Relationship Mapping"]
            ServiceMap["Service Mapping<br/>- Service Dependencies<br/>- Infrastructure Mapping<br/>- Visual Topology"]
        end
        
        subgraph "Monitoring & Events"
            EventMgmt["Event Management<br/>- Alert Correlation<br/>- Event Normalization<br/>- Incident Creation"]
            OpIntel["Operational Intelligence<br/>- Anomaly Detection<br/>- Predictive Analytics<br/>- Health Scoring"]
        end
        
        subgraph "Cloud & Infrastructure"
            CloudMgmt["Cloud Management<br/>- Cloud Provisioning<br/>- Resource Orchestration<br/>- Multi-Cloud Support"]
            InfraMgmt["Infrastructure Management<br/>- Server Monitoring<br/>- Network Monitoring<br/>- Performance Tracking"]
        end
        
        Discovery_Comp --> ServiceMap
        EventMgmt --> OpIntel
        CloudMgmt --> InfraMgmt
        ServiceMap --> EventMgmt
    end
    
    style Discovery_Comp fill:#4CAF50,stroke:#2E7D32,color:#fff
    style ServiceMap fill:#4CAF50,stroke:#2E7D32,color:#fff
    style EventMgmt fill:#4CAF50,stroke:#2E7D32,color:#fff
    style OpIntel fill:#4CAF50,stroke:#2E7D32,color:#fff
    style CloudMgmt fill:#4CAF50,stroke:#2E7D32,color:#fff
    style InfraMgmt fill:#4CAF50,stroke:#2E7D32,color:#fff
```

---

## C3: Component Diagram - CSM Module

```mermaid
graph TB
    subgraph "CSM Module Components"
        direction TB
        
        subgraph "Case Management"
            CaseCreate["Case Creation<br/>- Multi-channel Intake<br/>- Auto-categorization<br/>- Assignment"]
            CaseResolve["Case Resolution<br/>- Tracking & Updates<br/>- Knowledge Integration<br/>- Escalation"]
        end
        
        subgraph "Customer Experience"
            Portal_CSM["Customer Portal<br/>- Self-Service<br/>- Case Tracking<br/>- Knowledge Access"]
            VirtualAgent["Virtual Agent<br/>- AI Chatbot<br/>- Auto-Resolution<br/>- Escalation"]
        end
        
        subgraph "Service Management"
            Entitlements["Entitlements & SLAs<br/>- Service Levels<br/>- Entitlement Rules<br/>- SLA Tracking"]
            Communities["Communities<br/>- Peer Support<br/>- Knowledge Sharing<br/>- User Forums"]
        end
        
        CaseCreate --> CaseResolve
        Portal_CSM --> CaseCreate
        VirtualAgent --> CaseCreate
        CaseResolve --> Entitlements
        Portal_CSM --> Communities
    end
    
    style CaseCreate fill:#4CAF50,stroke:#2E7D32,color:#fff
    style CaseResolve fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Portal_CSM fill:#2196F3,stroke:#1565C0,color:#fff
    style VirtualAgent fill:#2196F3,stroke:#1565C0,color:#fff
    style Entitlements fill:#FFC107,stroke:#F57F17,color:#000
    style Communities fill:#2196F3,stroke:#1565C0,color:#fff
```

---

## C3: Component Diagram - Workflow Engine

```mermaid
graph TB
    subgraph "Workflow Engine Components"
        direction TB
        
        subgraph "Workflow Design"
            WFDesigner["Workflow Designer<br/>- Visual Design<br/>- Activity Library<br/>- Template Management"]
            FlowDesigner["Flow Designer<br/>- Low-Code Design<br/>- Action Library<br/>- Subflows"]
        end
        
        subgraph "Execution Engine"
            Executor["Workflow Executor<br/>- Activity Execution<br/>- Condition Evaluation<br/>- State Management"]
            Scheduler["Scheduler<br/>- Trigger Management<br/>- Queue Management<br/>- Priority Handling"]
        end
        
        subgraph "Automation Components"
            Actions["Actions<br/>- Core Actions<br/>- Custom Actions<br/>- Integration Actions"]
            Conditions["Conditions<br/>- If/Switch Logic<br/>- Wait Conditions<br/>- Decision Tables"]
        end
        
        subgraph "Monitoring & Debugging"
            Debugger["Flow Debugger<br/>- Breakpoints<br/>- Step Execution<br/>- Variable Inspection"]
            Monitor["Execution Monitor<br/>- History Tracking<br/>- Performance Metrics<br/>- Error Logging"]
        end
        
        WFDesigner --> Executor
        FlowDesigner --> Executor
        Executor --> Scheduler
        Actions --> Executor
        Conditions --> Executor
        Executor --> Debugger
        Executor --> Monitor
    end
    
    style WFDesigner fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style FlowDesigner fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style Executor fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style Scheduler fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style Actions fill:#FFC107,stroke:#F57F17,color:#000
    style Conditions fill:#FFC107,stroke:#F57F17,color:#000
    style Debugger fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style Monitor fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

---

## C3: Component Diagram - CMDB

```mermaid
graph TB
    subgraph "CMDB Components"
        direction TB
        
        subgraph "CI Management"
            CICreate["CI Creation<br/>- Manual Entry<br/>- Auto Discovery<br/>- Import/Sync"]
            CIUpdate["CI Updates<br/>- Attribute Management<br/>- Status Tracking<br/>- Versioning"]
        end
        
        subgraph "Relationships"
            RelCreate["Relationship Creation<br/>- Dependency Mapping<br/>- Service Mapping<br/>- Impact Analysis"]
            RelMgmt["Relationship Management<br/>- Relationship Editor<br/>- Validation<br/>- Reconciliation"]
        end
        
        subgraph "Data Quality"
            Health["CMDB Health<br/>- Completeness Metrics<br/>- Accuracy Checks<br/>- Duplicate Detection"]
            IRE_Comp["IRE (Identification)<br/>- CI Matching<br/>- Duplicate Resolution<br/>- Data Reconciliation"]
        end
        
        subgraph "Tools & Features"
            Query["Query Builder<br/>- Advanced Search<br/>- Custom Reports<br/>- Data Export"]
            Workspace_CMDB["CMDB Workspace<br/>- Unified Interface<br/>- Health Dashboards<br/>- Data Management"]
        end
        
        CICreate --> CIUpdate
        RelCreate --> RelMgmt
        CIUpdate --> RelMgmt
        Health --> IRE_Comp
        IRE_Comp --> CIUpdate
        Query --> Workspace_CMDB
        Health --> Workspace_CMDB
    end
    
    style CICreate fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style CIUpdate fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style RelCreate fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style RelMgmt fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style Health fill:#FFC107,stroke:#F57F17,color:#000
    style IRE_Comp fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style Query fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style Workspace_CMDB fill:#2196F3,stroke:#1565C0,color:#fff
```

---

## C2: Deployment Diagram - Multi-Tenant Architecture

```mermaid
graph TB
    subgraph "ServiceNow Cloud Infrastructure"
        direction TB
        
        subgraph "Load Balancing"
            LB["Load Balancer<br/>(Traffic Distribution)"]
        end
        
        subgraph "Application Nodes"
            Node1["Application Node 1<br/>- Workflow Engine<br/>- API Server<br/>- Cache"]
            Node2["Application Node 2<br/>- Workflow Engine<br/>- API Server<br/>- Cache"]
            Node3["Application Node N<br/>- Workflow Engine<br/>- API Server<br/>- Cache"]
        end
        
        subgraph "Data Layer"
            PrimaryDB["Primary Database<br/>(PostgreSQL/MySQL)<br/>- CMDB<br/>- Workflows<br/>- Modules"]
            ReplicaDB["Replica Database<br/>(Read-Only)<br/>- Analytics<br/>- Reporting"]
            Cache_Cluster["Cache Cluster<br/>(Redis)<br/>- Session Data<br/>- Performance"]
        end
        
        subgraph "Storage"
            FileStore["File Storage<br/>(S3/Blob)<br/>- Attachments<br/>- Documents"]
            Backup["Backup Storage<br/>- Daily Backups<br/>- Disaster Recovery"]
        end
        
        subgraph "Integration"
            APIGateway["API Gateway<br/>- REST APIs<br/>- Authentication<br/>- Rate Limiting"]
            IntegrationHub["IntegrationHub<br/>- External Integrations<br/>- Webhooks<br/>- Connectors"]
        end
        
        LB --> Node1
        LB --> Node2
        LB --> Node3
        
        Node1 --> PrimaryDB
        Node2 --> PrimaryDB
        Node3 --> PrimaryDB
        
        PrimaryDB --> ReplicaDB
        Node1 --> Cache_Cluster
        Node2 --> Cache_Cluster
        Node3 --> Cache_Cluster
        
        Node1 --> FileStore
        Node2 --> FileStore
        Node3 --> FileStore
        
        PrimaryDB --> Backup
        
        APIGateway --> Node1
        APIGateway --> Node2
        APIGateway --> Node3
        
        IntegrationHub --> APIGateway
    end
    
    style LB fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style Node1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Node2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Node3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style PrimaryDB fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style ReplicaDB fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style Cache_Cluster fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style FileStore fill:#2196F3,stroke:#1565C0,color:#fff
    style Backup fill:#2196F3,stroke:#1565C0,color:#fff
    style APIGateway fill:#FFC107,stroke:#F57F17,color:#000
    style IntegrationHub fill:#FFC107,stroke:#F57F17,color:#000
```

---

## C3: Data Flow Diagram - Incident Management Process

```mermaid
graph LR
    User["👤 User<br/>(Portal)"]
    Portal_UI["Service Portal<br/>(UI)"]
    WF["Workflow Engine"]
    CMDB_Flow["CMDB<br/>(CI Data)"]
    Notif["Notification<br/>Service"]
    DB["Database<br/>(Incident Table)"]
    Analytics["Analytics<br/>Engine"]
    Dashboard["Dashboard<br/>(Reporting)"]
    
    User -->|"1. Create Incident"| Portal_UI
    Portal_UI -->|"2. Submit Request"| WF
    WF -->|"3. Lookup CI"| CMDB_Flow
    WF -->|"4. Assign & Route"| DB
    WF -->|"5. Send Notification"| Notif
    DB -->|"6. Store Data"| DB
    DB -->|"7. Send Metrics"| Analytics
    Analytics -->|"8. Update Dashboard"| Dashboard
    Dashboard -->|"9. Display Status"| Portal_UI
    Notif -->|"10. Email Alert"| User
    
    style User fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Portal_UI fill:#2196F3,stroke:#1565C0,color:#fff
    style WF fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style CMDB_Flow fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style Notif fill:#FFC107,stroke:#F57F17,color:#000
    style DB fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style Analytics fill:#FFC107,stroke:#F57F17,color:#000
    style Dashboard fill:#2196F3,stroke:#1565C0,color:#fff
```

---

## C3: Data Flow Diagram - Change Management Process

```mermaid
graph LR
    Requester["👤 Change Requester"]
    ChangeForm["Change Request<br/>Form"]
    WF_Change["Change Workflow"]
    CMDB_Change["CMDB<br/>(CI Impact)"]
    Approval["Approval<br/>Queue"]
    Implement["Implementation<br/>Activity"]
    Validation["Validation<br/>Activity"]
    Notify["Notification<br/>Service"]
    
    Requester -->|"1. Submit Change"| ChangeForm
    ChangeForm -->|"2. Trigger Workflow"| WF_Change
    WF_Change -->|"3. Check Impact"| CMDB_Change
    WF_Change -->|"4. Route for Approval"| Approval
    Approval -->|"5. Approve/Reject"| WF_Change
    WF_Change -->|"6. Schedule Implementation"| Implement
    Implement -->|"7. Execute Change"| CMDB_Change
    Implement -->|"8. Validate"| Validation
    Validation -->|"9. Close Change"| WF_Change
    WF_Change -->|"10. Notify Stakeholders"| Notify
    
    style Requester fill:#4CAF50,stroke:#2E7D32,color:#fff
    style ChangeForm fill:#2196F3,stroke:#1565C0,color:#fff
    style WF_Change fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style CMDB_Change fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style Approval fill:#FFC107,stroke:#F57F17,color:#000
    style Implement fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Validation fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Notify fill:#FFC107,stroke:#F57F17,color:#000
```

---

## C3: Data Flow Diagram - Discovery & CMDB Population

```mermaid
graph LR
    Scanner["Discovery<br/>Scanner"]
    Network["Network<br/>Scan"]
    Agents["Discovery<br/>Agents"]
    RawData["Raw CI<br/>Data"]
    IRE_Process["IRE<br/>(Identification &<br/>Reconciliation)"]
    Matching["CI Matching<br/>& Deduplication"]
    CMDB_Populate["CMDB<br/>Population"]
    Relationships["Relationship<br/>Creation"]
    Health["Health<br/>Check"]
    
    Scanner -->|"1. Scan Network"| Network
    Agents -->|"2. Collect Data"| RawData
    Network -->|"3. Send Data"| RawData
    RawData -->|"4. Process"| IRE_Process
    IRE_Process -->|"5. Match CIs"| Matching
    Matching -->|"6. Deduplicate"| CMDB_Populate
    CMDB_Populate -->|"7. Store CIs"| CMDB_Populate
    CMDB_Populate -->|"8. Create Relationships"| Relationships
    Relationships -->|"9. Validate"| Health
    Health -->|"10. Update Health Score"| CMDB_Populate
    
    style Scanner fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Network fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Agents fill:#4CAF50,stroke:#2E7D32,color:#fff
    style RawData fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style IRE_Process fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style Matching fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style CMDB_Populate fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style Relationships fill:#FF6B6B,stroke:#C92A2A,color:#fff
    style Health fill:#FFC107,stroke:#F57F17,color:#000
```

---

## Integration Architecture Diagram

```mermaid
graph TB
    subgraph "ServiceNow Instance"
        SN_Core["ServiceNow Core<br/>(Modules & Workflows)"]
    end
    
    subgraph "External Systems"
        ERP["ERP System<br/>(SAP, Oracle)"]
        CRM["CRM System<br/>(Salesforce)"]
        Cloud["Cloud Services<br/>(AWS, Azure)"]
        ITSM_Tools["ITSM Tools<br/>(Monitoring)"]
        LDAP["LDAP/AD<br/>(User Directory)"]
    end
    
    subgraph "Integration Layer"
        IntHub["IntegrationHub<br/>- Spokes<br/>- Connections<br/>- Actions"]
        API["REST APIs<br/>- Webhooks<br/>- Inbound<br/>- Outbound"]
        Middleware["Middleware<br/>- Message Queue<br/>- ETL<br/>- Transformations"]
    end
    
    SN_Core -->|"Sync Data"| IntHub
    IntHub -->|"Connect"| ERP
    IntHub -->|"Connect"| CRM
    IntHub -->|"Connect"| Cloud
    IntHub -->|"Connect"| ITSM_Tools
    
    SN_Core -->|"API Calls"| API
    API -->|"Integrate"| ERP
    API -->|"Integrate"| CRM
    API -->|"Integrate"| LDAP
    
    Middleware -->|"Transform"| SN_Core
    ERP -->|"Send Data"| Middleware
    CRM -->|"Send Data"| Middleware
    
    style SN_Core fill:#0066cc,stroke:#003366,color:#fff
    style IntHub fill:#FFC107,stroke:#F57F17,color:#000
    style API fill:#FFC107,stroke:#F57F17,color:#000
    style Middleware fill:#FFC107,stroke:#F57F17,color:#000
    style ERP fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style CRM fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style Cloud fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style ITSM_Tools fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style LDAP fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

---

## Module Interaction Diagram

```mermaid
graph TB
    CMDB["CMDB<br/>(Central Repository)"]
    
    ITSM["ITSM<br/>(Incident, Change,<br/>Problem)"]
    ITOM["ITOM<br/>(Operations,<br/>Monitoring)"]
    ITAM["ITAM<br/>(Asset<br/>Management)"]
    CSM["CSM<br/>(Customer<br/>Service)"]
    HRSD["HRSD<br/>(HR Service<br/>Delivery)"]
    FSM["FSM<br/>(Field<br/>Service)"]
    GRC["GRC<br/>(Governance,<br/>Risk)"]
    PPM["PPM<br/>(Project<br/>Portfolio)"]
    Finance["Finance &<br/>Supply Chain"]
    
    WFE["Workflow Engine<br/>(Orchestration)"]
    Analytics["Analytics<br/>(Reporting)"]
    
    ITSM -->|"Uses"| CMDB
    ITOM -->|"Uses"| CMDB
    ITAM -->|"Uses"| CMDB
    CSM -->|"Uses"| CMDB
    HRSD -->|"Uses"| CMDB
    FSM -->|"Uses"| CMDB
    GRC -->|"Uses"| CMDB
    PPM -->|"Uses"| CMDB
    Finance -->|"Uses"| CMDB
    
    ITSM -->|"Orchestrates"| WFE
    ITOM -->|"Orchestrates"| WFE
    CSM -->|"Orchestrates"| WFE
    HRSD -->|"Orchestrates"| WFE
    FSM -->|"Orchestrates"| WFE
    
    ITSM -->|"Reports"| Analytics
    ITOM -->|"Reports"| Analytics
    CSM -->|"Reports"| Analytics
    HRSD -->|"Reports"| Analytics
    FSM -->|"Reports"| Analytics
    
    ITOM -->|"Discovers"| CMDB
    ITAM -->|"Tracks"| CMDB
    
    style CMDB fill:#FF6B6B,stroke:#C92A2A,color:#fff,stroke-width:3px
    style WFE fill:#FF6B6B,stroke:#C92A2A,color:#fff,stroke-width:3px
    style Analytics fill:#FFC107,stroke:#F57F17,color:#000,stroke-width:2px
    
    style ITSM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style ITOM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style ITAM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style CSM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style HRSD fill:#4CAF50,stroke:#2E7D32,color:#fff
    style FSM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style GRC fill:#4CAF50,stroke:#2E7D32,color:#fff
    style PPM fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Finance fill:#4CAF50,stroke:#2E7D32,color:#fff
```

---

## Legend

### Color Coding
- **Red (#FF6B6B)** – Core Platform Components (CMDB, Workflow Engine)
- **Green (#4CAF50)** – Application Modules
- **Blue (#2196F3)** – User Interfaces & Portals
- **Yellow (#FFC107)** – Platform Services & Integration
- **Purple (#9C27B0)** – Data & Storage Layer

### Diagram Types
- **C1 (Context)** – System boundaries and external actors
- **C2 (Container)** – Major components and their interactions
- **C3 (Component)** – Internal structure of containers
- **C4 (Code)** – Detailed implementation (not shown here)
- **Data Flow** – How data moves through the system
- **Deployment** – Infrastructure and deployment topology

---

## Key Architectural Principles

### 1. Centralized Data Model
- CMDB serves as single source of truth
- All modules reference CMDB data
- Ensures data consistency across platform

### 2. Workflow-Driven Automation
- Workflow Engine orchestrates all processes
- Enables complex multi-step automation
- Supports approvals, notifications, and integrations

### 3. Multi-Tenant Architecture
- Isolated instances for each organization
- Shared infrastructure for cost efficiency
- Separate databases and security contexts

### 4. API-First Design
- RESTful APIs for all functionality
- Enables integrations and extensions
- Supports mobile and web clients

### 5. Scalability & Performance
- Load balancing across multiple nodes
- Caching layer for performance
- Database replication for read scaling
- Asynchronous processing for long-running tasks

### 6. Security & Compliance
- Role-based access control (RBAC)
- Encryption at rest and in transit
- Audit trails for compliance
- Multi-factor authentication support

---

## Conclusion

These C4 architecture diagrams provide a comprehensive view of ServiceNow's platform structure, from system context through detailed component interactions. The diagrams illustrate how the CMDB and Workflow Engine serve as the foundation for all ServiceNow modules, enabling organizations to automate and manage their entire digital workflow ecosystem.
