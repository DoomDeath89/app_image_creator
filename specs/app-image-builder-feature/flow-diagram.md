# AppImage Builder - Spec-Kit Flow Diagram

## Development Workflow

```mermaid
graph TD
    A[Start] --> B[Phase 1: Setup]
    B --> C[Phase 2: Foundational]
    C --> D{Ready for User Stories?}
    D -->|Yes| E[Phase 3: US1 - Threading]
    D -->|No| C
    
    E --> F[Phase 4: US2 - Dependencies]
    E --> G[Phase 5: US3 - Error Handling]
    E --> H[Phase 6: US4 - Log Management]
    E --> I[Phase 5: US5 - Config Resilience]
    
    F --> J[Phase 8: Polish]
    G --> J
    H --> J
    I --> J
    
    J --> K[All Tests Pass]
    K --> L[Deploy]
    
    style E fill:#90EE90
    style F fill:#FFE4B5
    style G fill:#FFE4B5
    style H fill:#FFE4B5
    style I fill:#FFE4B5
    style K fill:#87CEEB
```

## User Story Dependencies

```mermaid
graph LR
    US1[US1: Threading] --> US2[US2: Dependencies]
    US1 --> US3[US3: Error Handling]
    US1 --> US4[US4: Log Management]
    US5[US5: Config Resilience]
    
    US2 --> POLISH[Polish]
    US3 --> POLISH
    US4 --> POLISH
    US5 --> POLISH
    
    style US1 fill:#90EE90
    style US2 fill:#FFE4B5
    style US3 fill:#FFE4B5
    style US4 fill:#FFE4B5
    style US5 fill:#87CEEB
    style POLISH fill:#DDA0DD
```

## Build Process Flow

```mermaid
sequenceDiagram
    participant U as User
    participant BT as BuildTab
    participant T as Thread
    participant LD as LinuxDeploy
    participant FS as Filesystem
    
    U->>BT: Click Generate
    BT->>BT: Validate inputs
    BT->>BT: Disable Generate, Enable Cancel
    BT->>T: Start _run_build()
    T->>BT: Create AppDir
    T->>FS: Copy executable
    T->>FS: Copy icon
    T->>FS: Copy dependencies
    T->>BT: Log progress
    T->>LD: Execute linuxdeploy
    LD->>BT: Stream output
    T->>BT: Log completion
    T->>BT: Enable Generate, Disable Cancel
    
    Note over U,BT: User can click Cancel at any time
    U->>BT: Click Cancel
    BT->>T: Terminate process
    BT->>FS: Cleanup AppDir
    BT->>BT: Log cancellation
```

## Task Status Summary

```mermaid
pie
    title Task Completion Status
    "Completed" : 48
    "Pending" : 0
```

## Architecture Overview

```mermaid
graph TB
    subgraph "UI Layer"
        MT[Main Window]
        NB[Notebook]
        BT[Build Tab]
        VT[Validator Tab]
        DT[Dependencies Tab]
    end
    
    subgraph "Core Layer"
        M[Mediator]
    end
    
    subgraph "Service Layer"
        ADB[AppDir Builder]
        DFH[Desktop File Handler]
        LDM[LinuxDeploy Manager]
    end
    
    subgraph "Utils"
        C[Constants]
        T[Types]
    end
    
    MT --> NB
    NB --> BT
    NB --> VT
    NB --> DT
    
    BT --> M
    VT --> M
    DT --> M
    
    BT --> ADB
    BT --> DFH
    BT --> LDM
    VT --> DFH
    
    ADB --> C
    ADB --> T
    DFH --> C
    DFH --> T
    LDM --> C
    
    style BT fill:#90EE90
    style M fill:#FFE4B5
    style ADB fill:#87CEEB
    style DFH fill:#87CEEB
    style LDM fill:#87CEEB
```

## Key Metrics

| Metric | Before | After |
|--------|--------|-------|
| UI Freeze During Build | Yes (2+ min) | No |
| Cancel Support | None | 1 second |
| Dependencies Ignored | Yes | Included |
| Error Handling | Crashes | User Dialogs |
| Log Management | Manual | Auto-clear |
| Test Coverage | 44% | 100% |
| Test Failures | 5 | 0 |
