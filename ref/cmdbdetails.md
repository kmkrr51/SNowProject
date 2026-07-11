# ServiceNow CMDB (Configuration Management Database) - Detailed Summary

## Table of Contents
1. [Overview](#overview)
2. [What is CMDB?](#what-is-cmdb)
3. [Core Concepts](#core-concepts)
4. [Configuration Items (CIs)](#configuration-items-cis)
5. [CI Relationships](#ci-relationships)
6. [CMDB Architecture](#cmdb-architecture)
7. [Key Features](#key-features)
8. [CMDB Workspace](#cmdb-workspace)
9. [Identification and Reconciliation Engine (IRE)](#identification-and-reconciliation-engine-ire)
10. [CMDB Health](#cmdb-health)
11. [Best Practices](#best-practices)
12. [Implementation Considerations](#implementation-considerations)

---

## Overview

The Configuration Management Database (CMDB) is the central repository in ServiceNow that stores and manages information about all IT infrastructure components and their relationships. It serves as the single source of truth for IT operations, providing visibility into the entire IT landscape and enabling better decision-making across all ServiceNow modules.

---

## What is CMDB?

### Definition
The CMDB is a database that maintains detailed information about all configuration items (CIs) in an organization's IT infrastructure, including their attributes, relationships, and dependencies. It acts as the foundation for IT Service Management (ITSM) and other ServiceNow applications.

### Purpose
- **Single Source of Truth** – Provides accurate, up-to-date information about IT infrastructure
- **Dependency Mapping** – Shows how IT components depend on each other
- **Impact Analysis** – Enables assessment of how changes affect services and users
- **Service Delivery** – Supports service mapping and service delivery optimization
- **Compliance & Governance** – Maintains audit trails and compliance records
- **Incident Resolution** – Provides context for faster incident diagnosis and resolution

### Key Benefits
- **Improved Visibility** – Complete view of IT infrastructure and services
- **Better Decision Making** – Data-driven insights for IT operations
- **Reduced Downtime** – Faster incident resolution through dependency mapping
- **Change Management** – Better control and planning of IT changes
- **Cost Optimization** – Identify redundancies and optimize resource utilization
- **Risk Management** – Understand service dependencies and potential risks

---

## Core Concepts

### Configuration Items (CIs)
Configuration Items are the fundamental building blocks of the CMDB. A CI is any component of IT infrastructure that needs to be managed to deliver or support a service.

**Examples of CIs:**
- Servers (physical and virtual)
- Network devices (routers, switches, firewalls)
- Applications and software
- Databases
- Storage systems
- Cloud resources
- Middleware components
- Load balancers
- Users and groups
- Business services

### CI Attributes
Each CI has attributes that describe its characteristics and properties:
- **Identification Attributes** – Name, ID, serial number
- **Operational Attributes** – Status, location, owner
- **Technical Attributes** – Version, configuration, specifications
- **Business Attributes** – Cost center, business owner, criticality
- **Relationship Attributes** – Links to related CIs

### CI Classes
CIs are organized into classes based on their type and function. ServiceNow provides out-of-the-box (OOB) CI classes:

**Hardware Classes:**
- `cmdb_ci_computer` – Computers and workstations
- `cmdb_ci_server` – Physical and virtual servers
- `cmdb_ci_network_device` – Network equipment
- `cmdb_ci_storage` – Storage systems
- `cmdb_ci_printer` – Printers and peripherals

**Software Classes:**
- `cmdb_ci_application` – Business applications
- `cmdb_ci_database` – Database systems
- `cmdb_ci_service` – IT services
- `cmdb_ci_software` – Software packages
- `cmdb_ci_middleware` – Middleware components

**Cloud Classes:**
- `cmdb_ci_cloud_service` – Cloud services
- `cmdb_ci_vm_instance` – Virtual machine instances
- `cmdb_ci_cloud_database` – Cloud databases

---

## CI Relationships

### What are CI Relationships?
CI Relationships define how configuration items are connected and depend on each other. They represent the logical and physical connections between CIs in the IT infrastructure.

### Relationship Structure
A relationship consists of:
- **Parent CI** – The source configuration item
- **Child CI** – The destination configuration item
- **Relationship Type** – The nature of the connection

### Types of CI Relationships

#### Dependent Relationships
Dependent relationships are used by the Identification and Reconciliation Engine (IRE) for CI identification and should not be deleted.

**Common Dependent Relationships:**
- **Runs On** – Application runs on a server
  - Example: Apache Web Server runs on Linux Server
- **Hosted On** – Service hosted on infrastructure
  - Example: Email Service hosted on Exchange Server
- **Depends On** – Service depends on another component
  - Example: Web Application depends on Database
- **Contains** – Parent CI contains child CI
  - Example: Server contains Hard Drive

#### Non-Dependent Relationships
Non-dependent relationships provide additional context but are not used for CI identification and can be safely deleted if no longer needed.

**Common Non-Dependent Relationships:**
- **Connects To** – Network connections between CIs
- **Manages** – Management relationships
- **Communicates With** – Communication between CIs
- **Supports** – Support relationships
- **Logs Reviewed By** – Audit relationships

### Key Relationship Types

| Relationship Type | Parent | Child | Description |
|---|---|---|---|
| **Runs On** | Application | Server | Application runs on a server |
| **Hosted On** | Service | Infrastructure | Service is hosted on infrastructure |
| **Depends On** | Service | Component | Service depends on a component |
| **Contains** | Parent | Child | Containment relationship |
| **Connects To** | Endpoint | Endpoint | Network connections |
| **Manages** | Manager | Managed | Management relationship |
| **Exposes** | CI | Endpoint | CI exposes an endpoint |
| **Communicates With** | CI | CI | Communication between CIs |
| **Connects To** | CI | CI | Connection between CIs |

### Relationship Discovery
Relationships can be automatically discovered through the Discovery process:
- **Horizontal Discovery** – Populates point-to-point relationships between CIs (e.g., web servers and load balancers)
- **Vertical Discovery** – Creates service maps by taking a vertical cut of CIs and relationships representing end-to-end services

### Managing CI Relationships

#### Creating Relationships
- Use the CI Relationship Editor from the CI form
- Select relationship type and target CI
- Use suggested relationships for guided creation
- Manually create relationships for custom scenarios

#### Editing Relationships
- Modify existing relationships through the CI Relationship Editor
- Update relationship types and target CIs
- Add or remove relationships as needed

#### Deleting Relationships
- Non-dependent relationships can be safely deleted
- Dependent relationships should not be directly deleted
- Check Relationship Sources table to determine if safe to delete

---

## CMDB Architecture

### CMDB Tables and Structure

#### Core CMDB Tables
- **cmdb_ci** – Base CI table (parent table for all CIs)
- **cmdb_rel_ci** – CI Relationships table
- **sys_rel_source** – Relationship Sources (tracks discovery source and last scanned time)
- **cmdb_ci_service** – Business Services
- **cmdb_ci_application** – Applications

#### CI Class Hierarchy
```
cmdb_ci (Base)
├── cmdb_ci_computer (Computers)
│   ├── cmdb_ci_server (Servers)
│   └── cmdb_ci_workstation (Workstations)
├── cmdb_ci_network_device (Network Devices)
├── cmdb_ci_storage (Storage)
├── cmdb_ci_application (Applications)
├── cmdb_ci_database (Databases)
├── cmdb_ci_service (Services)
└── [Other CI Classes]
```

### Data Flow in CMDB

```
Discovery Process
    ↓
Automatic CI Creation
    ↓
Identification & Reconciliation (IRE)
    ↓
Relationship Creation
    ↓
CMDB Population
    ↓
Service Mapping
    ↓
Impact Analysis & Reporting
```

---

## Key Features

### 1. CMDB Workspace
A unified interface for managing CMDB data and operations.

**Features:**
- Centralized CMDB management
- Health dashboards and metrics
- Data quality monitoring
- Query builder for advanced searches
- Intelligent search with natural language queries
- CI relationship visualization
- Bulk operations and data management

### 2. Identification and Reconciliation Engine (IRE)
Automatically identifies and reconciles CIs to prevent duplicates and maintain data quality.

**Functions:**
- Identifies duplicate CIs
- Reconciles CI data from multiple sources
- Maintains CI uniqueness
- Uses dependent relationships for identification
- Prevents CI proliferation
- Ensures data consistency

**How IRE Works:**
1. Receives CI data from discovery or import
2. Applies identification rules
3. Matches against existing CIs
4. Reconciles attributes
5. Creates or updates CI records
6. Maintains relationship integrity

### 3. CMDB Health
Monitors and reports on CMDB data quality and health.

**Health Metrics:**
- **Completeness** – Percentage of required attributes populated
- **Accuracy** – Validation of CI data against rules
- **Timeliness** – How current the data is
- **Consistency** – Alignment across related CIs
- **Uniqueness** – Detection of duplicate CIs

**Health Dashboards:**
- Overall CMDB health score
- CI class-specific health metrics
- Data quality trends
- Relationship health
- Discovery status

### 4. Query Builder
Advanced query tool for searching and analyzing CMDB data.

**Capabilities:**
- Build complex queries without coding
- Filter CIs by multiple criteria
- Create custom reports
- Export query results
- Save and reuse queries
- Combine multiple conditions

### 5. Intelligent Search (NLQ Search)
Natural language query search for finding CIs and information.

**Features:**
- Search using natural language
- AI-powered query interpretation
- Quick access to CI information
- Contextual results
- Reduced learning curve

### 6. Data Manager
Tool for managing and maintaining CMDB data.

**Functions:**
- Bulk import of CI data
- Data validation and cleansing
- Attribute mapping
- Reconciliation management
- Data export capabilities
- Duplicate detection

### 7. CMDB 360
Comprehensive view of a CI showing all related information.

**Includes:**
- CI attributes and details
- Related CIs and relationships
- Service dependencies
- Incidents and changes
- Compliance information
- Historical data
- Impact analysis

### 8. Service Mapping
Maps services to supporting infrastructure CIs.

**Components:**
- Service CIs representing digital services
- Infrastructure CIs supporting services
- Dependency relationships
- Service flow visualization
- Impact analysis
- Service health monitoring

---

## CMDB Workspace

### Overview
The CMDB Workspace is a modern interface for managing CMDB operations and data.

### Key Components

#### 1. Health Dashboards
- Real-time CMDB health metrics
- Data quality indicators
- Trend analysis
- Alert notifications
- Health score by CI class

#### 2. CI Management
- View and edit CI records
- Manage CI relationships
- Update CI attributes
- Bulk operations
- CI lifecycle management

#### 3. Discovery Integration
- Monitor discovery jobs
- View discovery results
- Manage discovery sources
- Configure discovery rules
- Track CI creation from discovery

#### 4. Reporting & Analytics
- CMDB metrics and KPIs
- Custom reports
- Data visualization
- Trend analysis
- Export capabilities

#### 5. Data Quality Tools
- Duplicate detection
- Missing data identification
- Validation rules
- Data cleansing workflows
- Quality improvement recommendations

---

## Identification and Reconciliation Engine (IRE)

### Purpose
The IRE ensures CMDB data quality by automatically identifying and reconciling configuration items from multiple data sources.

### Key Functions

#### 1. CI Identification
- Identifies unique CIs based on identification rules
- Prevents duplicate CI creation
- Matches CIs across multiple sources
- Uses dependent relationships for identification

#### 2. Reconciliation
- Merges CI data from multiple sources
- Resolves conflicting attributes
- Updates existing CI records
- Maintains data consistency

#### 3. Relationship Management
- Creates and maintains CI relationships
- Uses dependent relationships for identification
- Validates relationship integrity
- Prevents orphaned CIs

### Identification Rules
Rules that determine how CIs are identified and matched:
- **Unique Identifiers** – Serial numbers, MAC addresses, hostnames
- **Attribute Matching** – Name, IP address, location
- **Relationship-Based** – Dependent relationships
- **Custom Rules** – Organization-specific identification logic

### IRE Configuration
- Define identification rules per CI class
- Set attribute matching priorities
- Configure reconciliation logic
- Manage duplicate handling
- Set relationship validation rules

---

## CMDB Health

### Health Metrics

#### 1. Completeness
Measures the percentage of required attributes that are populated.
- Target: 90%+ for critical CIs
- Identifies missing data
- Tracks by CI class

#### 2. Accuracy
Validates CI data against defined rules and standards.
- Checks data format and validity
- Validates relationships
- Identifies invalid values
- Tracks accuracy trends

#### 3. Timeliness
Measures how current the CMDB data is.
- Tracks last update time
- Identifies stale data
- Monitors discovery frequency
- Alerts on outdated information

#### 4. Consistency
Ensures alignment of related CIs and attributes.
- Validates relationship consistency
- Checks for conflicting data
- Identifies orphaned CIs
- Monitors data synchronization

#### 5. Uniqueness
Detects and reports duplicate CIs.
- Identifies potential duplicates
- Tracks duplicate resolution
- Prevents new duplicates
- Maintains CI uniqueness

### Health Dashboards
- Overall CMDB health score (0-100)
- Health by CI class
- Trend analysis over time
- Alerts and recommendations
- Drill-down capabilities

### Health Improvement
- Address data quality issues
- Populate missing attributes
- Resolve duplicates
- Update stale data
- Validate relationships

---

## Best Practices

### 1. CI Class Management
- **Use Out-of-Box (OOB) Classes** – Leverage standard CI classes instead of creating custom ones
- **Extend Appropriately** – Extend from specific classes (e.g., Hardware) rather than base CMDB_CI
- **Avoid Over-Customization** – Use OOB attributes when possible
- **Naming Convention** – Custom CMDB tables should begin with `u_cmdb_ci_`

### 2. Attribute Management
- **Place Attributes at Right Level** – Put OS-specific attributes (BIOS_date) in OS classes, not Server class
- **Use Standard Attributes** – Leverage OOB attributes instead of creating new ones
- **Avoid Duplication** – Don't duplicate attributes across classes
- **Document Custom Attributes** – Clearly document purpose and usage

### 3. Relationship Management
- **Don't Alter OOB Relationships** – Keep standard relationships unchanged
- **Use Suggested Relationships** – Leverage system-suggested relationships
- **Maintain Relationship Integrity** – Ensure relationships remain valid
- **Document Custom Relationships** – Clearly define custom relationship types
- **Regular Validation** – Periodically validate relationship accuracy

### 4. Data Quality
- **Enable CMDB Health Dashboard** – Monitor health metrics continuously
- **Regular Data Audits** – Conduct periodic data quality reviews
- **Duplicate Management** – Regularly identify and resolve duplicates
- **Attribute Validation** – Validate required attributes are populated
- **Relationship Validation** – Ensure relationships are accurate and current

### 5. Discovery Integration
- **Automate Discovery** – Use discovery to automatically populate CMDB
- **Configure Discovery Rules** – Set up appropriate discovery patterns
- **Monitor Discovery Results** – Review and validate discovered CIs
- **Manage Discovery Sources** – Track and manage multiple discovery sources
- **Reconciliation** – Ensure discovered data is properly reconciled

### 6. Service Mapping
- **Map Services to Infrastructure** – Create service maps for critical services
- **Maintain Service Dependencies** – Keep service-to-CI relationships current
- **Document Service Flows** – Clearly document how services are delivered
- **Regular Updates** – Update service maps when infrastructure changes
- **Impact Analysis** – Use service maps for change impact analysis

### 7. Business Owner Assignment
- **Assign Business Owners** – Each application should have a designated business owner
- **Define Responsibilities** – Clearly define owner responsibilities
- **Communication** – Establish communication channels with owners
- **Escalation Path** – Define escalation procedures

### 8. CI Granularity
- **Level at Lowest Independent Change** – Model CIs at the level of independent change
- **Balance Detail and Manageability** – Don't over-decompose CIs
- **Consider Management Needs** – Model CIs based on how they will be managed
- **Consistency** – Apply consistent leveling across CI classes

### 9. Performance Optimization
- **Limit CI Relationships** – Avoid excessive relationships per CI
- **Optimize Queries** – Use efficient queries for CMDB searches
- **Archive Old Data** – Archive historical CI data when appropriate
- **Index Key Attributes** – Index frequently searched attributes
- **Monitor Performance** – Track CMDB query and update performance

### 10. Governance
- **Define CMDB Policies** – Establish clear CMDB governance policies
- **Access Control** – Implement role-based access control
- **Change Management** – Require approval for CMDB structure changes
- **Audit Trail** – Maintain audit logs of CMDB changes
- **Regular Reviews** – Conduct periodic CMDB governance reviews

---

## Implementation Considerations

### Phase 1: Planning & Design
- Define CI classes and attributes
- Design CI relationships
- Establish data quality standards
- Plan discovery strategy
- Define governance model

### Phase 2: Setup & Configuration
- Configure CI classes
- Set up attributes
- Define relationships
- Configure discovery
- Set up IRE rules

### Phase 3: Data Population
- Discover existing CIs
- Import CI data
- Reconcile duplicates
- Validate data quality
- Establish baseline

### Phase 4: Integration
- Integrate with ITSM modules
- Connect to other systems
- Set up service mapping
- Configure impact analysis
- Enable reporting

### Phase 5: Optimization & Maintenance
- Monitor CMDB health
- Optimize performance
- Refine discovery rules
- Update CI relationships
- Continuous improvement

### Common Challenges

#### 1. Data Quality
- **Challenge** – Incomplete or inaccurate CI data
- **Solution** – Implement data validation rules, regular audits, and automated discovery

#### 2. Duplicate CIs
- **Challenge** – Multiple records for same CI
- **Solution** – Use IRE identification rules, regular duplicate detection, reconciliation

#### 3. Relationship Accuracy
- **Challenge** – Incorrect or missing relationships
- **Solution** – Automate relationship discovery, regular validation, documentation

#### 4. Performance
- **Challenge** – Slow CMDB queries and updates
- **Solution** – Optimize queries, index key attributes, archive old data

#### 5. Adoption
- **Challenge** – Users not maintaining CMDB data
- **Solution** – Training, clear ownership, integration with daily workflows

### Success Factors
- **Executive Sponsorship** – Leadership commitment to CMDB
- **Clear Governance** – Well-defined policies and procedures
- **Data Quality Focus** – Emphasis on data accuracy and completeness
- **Automation** – Use discovery and IRE to automate data population
- **Training & Support** – Comprehensive user training and support
- **Continuous Improvement** – Regular monitoring and optimization

---

## CMDB and Other ServiceNow Modules

### ITSM Integration
- **Incident Management** – Uses CMDB for incident context and impact analysis
- **Change Management** – References CIs affected by changes
- **Problem Management** – Tracks problems related to CIs
- **Service Catalog** – Links services to supporting CIs

### ITOM Integration
- **Discovery** – Automatically populates CMDB
- **Service Mapping** – Maps services to infrastructure
- **Event Management** – Correlates events to CIs
- **Operational Intelligence** – Analyzes CI health and performance

### Other Integrations
- **GRC** – Tracks compliance of CIs
- **FSM** – Manages field service assets
- **CSM** – Links customer services to infrastructure
- **PPM** – Tracks application portfolio

---

## Conclusion

The CMDB is the foundation of ServiceNow's IT operations capabilities, providing a comprehensive view of IT infrastructure and services. By implementing best practices, maintaining data quality, and leveraging automation through discovery and the IRE, organizations can maximize the value of their CMDB and improve IT service delivery, incident resolution, and change management.

A well-maintained CMDB enables:
- Faster incident resolution
- Better change planning
- Improved service quality
- Reduced operational risk
- Better compliance and governance
- Data-driven decision making
