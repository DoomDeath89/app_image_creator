# Tasks: AppImage Builder Improvements

**Input**: Design documents from `/specs/app-image-builder-feature/`

**Prerequisites**: plan.md, spec.md

**Tests**: All tasks include test requirements

**Organization**: Tasks grouped by user story for independent implementation

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Read current build_tab.py and understand existing code
- [x] T002 Read current tests and understand test patterns
- [x] T003 Identify all bugs and improvement areas

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Add threading import to build_tab.py
- [x] T005 Add subprocess import for process management
- [x] T006 Add shutil import for dependency copying

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Non-Blocking Build Process (Priority: P1) 🎯 MVP

**Goal**: Build runs in background thread with cancel support

**Independent Test**: Launch build, verify UI responsive, verify cancel works

### Implementation for User Story 1

- [x] T007 [US1] Add `_build_process`, `_build_thread`, `_builder` instance variables in `__init__`
- [x] T008 [US1] Add Cancel button to button_frame in `_build_ui()`
- [x] T009 [US1] Store references to Generate and Cancel buttons as instance variables
- [x] T010 [US1] Implement `_set_build_state(building: bool)` method to enable/disable buttons
- [x] T011 [US1] Implement `_cancel_build()` method to terminate process and cleanup
- [x] T012 [US1] Implement `_run_build()` wrapper that calls `_execute_build()` with try/except
- [x] T013 [US1] Modify `build_appimage()` to start `_build_thread` instead of direct call
- [x] T014 [US1] Rename original build logic to `_execute_build()`
- [x] T015 [US1] Replace `self.frame.update()` with `self.frame.update_idletasks()` in `log_message()`
- [x] T016 [US1] Use `self.frame.after(0, lambda: ...)` for thread-safe UI updates in `_execute_build()`

### Tests for User Story 1

- [x] T017 [US1] Test `_set_build_state(True)` disables Generate, enables Cancel
- [x] T018 [US1] Test `_set_build_state(False)` enables Generate, disables Cancel
- [x] T019 [US1] Test `_cancel_build()` calls terminate on process

**Checkpoint**: Build process is non-blocking and cancellable

---

## Phase 4: User Story 2 - Dependency Integration (Priority: P2)

**Goal**: Dependencies from Dependencies tab are included in build

**Independent Test**: Add .so files, build, verify they appear in AppDir

### Implementation for User Story 2

- [x] T020 [US2] In `_execute_build()`, get dependencies via `self.mediator.get_dependencies()`
- [x] T021 [US2] Loop through dependencies and copy each to `appdir/usr/lib/` using `shutil.copy2()`
- [x] T022 [US2] Log each dependency copy operation
- [x] T023 [US2] Add `--library` flags to linuxdeploy command for each dependency

### Tests for User Story 2

- [x] T024 [US2] Test dependencies are copied to AppDir (mock mediator returns deps)
- [x] T025 [US2] Test --library flags are added to linuxdeploy command

**Checkpoint**: Dependencies are included in AppImage

---

## Phase 5: User Story 3 - Robust Error Handling (Priority: P3)

**Goal**: All errors result in user-friendly dialogs

**Independent Test**: Trigger errors, verify dialogs appear

### Implementation for User Story 3

- [x] T026 [US3] Wrap `_save_config_to_file()` in try/except for OSError
- [x] T027 [US3] Show `messagebox.showerror()` on save failure
- [x] T028 [US3] Wrap `_load_config_from_file()` in try/except for JSON decode and IO errors
- [x] T029 [US3] Show `messagebox.showerror()` on load failure
- [x] T030 [US3] Wrap `_run_build()` in try/except for unexpected errors
- [x] T031 [US3] Call `builder.cleanup()` on build failure
- [x] T032 [US3] Call `builder.cleanup()` on build cancellation

### Tests for User Story 3

- [x] T033 [US3] Test `_save_config_to_file()` handles permission error
- [x] T034 [US3] Test `_load_config_from_file()` handles invalid JSON
- [x] T035 [US3] Test `_run_build()` handles unexpected exceptions

**Checkpoint**: All errors are handled gracefully

---

## Phase 6: User Story 4 - Log Management (Priority: P4)

**Goal**: Clean logs between builds with manual clear option

**Independent Test**: Run multiple builds, verify log clears

### Implementation for User Story 4

- [x] T036 [US4] Add `_clear_log()` method that deletes log content
- [x] T037 [US4] Add "Clear" button next to "Build Log:" label
- [x] T038 [US4] Call `_clear_log()` at start of `build_appimage()`

### Tests for User Story 4

- [x] T039 [US4] Test `_clear_log()` empties log_text widget

**Checkpoint**: Logs are managed properly

---

## Phase 7: User Story 5 - Config Resilience (Priority: P5)

**Goal**: Config save/load handles all edge cases

**Independent Test**: Test with corrupted files, missing fields, errors

### Implementation for User Story 5

- [x] T040 [US5] Add `str()` conversion for config values in `_load_config_from_file()` to handle non-string types
- [x] T041 [US5] Add log message on successful config save
- [x] T042 [US5] Add log message on successful config load

### Tests for User Story 5

- [x] T043 [US5] Test config load with missing fields uses defaults
- [x] T044 [US5] Test config load with corrupted JSON shows error

**Checkpoint**: Config handling is robust

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and cleanup

- [x] T045 Fix existing test failures (mock notebook issue)
- [x] T046 Update tests to use real ttk.Notebook instead of MagicMock
- [x] T047 Add new tests for all new features
- [x] T048 Verify all 49 tests pass

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (Threading) - No dependencies on other stories
  - US2 (Dependencies) - Can start after US1
  - US3 (Error Handling) - Can start after US1
  - US4 (Log Management) - Can start after US1
  - US5 (Config Resilience) - Independent, can start anytime
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies
- **User Story 2 (P2)**: Depends on US1 (build logic refactored)
- **User Story 3 (P3)**: Depends on US1 (error handling in threaded build)
- **User Story 4 (P4)**: Depends on US1 (log clearing before build)
- **User Story 5 (P5)**: Independent - can start anytime

### Parallel Opportunities

- US2, US3, US4 can run in parallel after US1 completes
- US5 is fully independent
- All test tasks within a story can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Threading)
4. **STOP and VALIDATE**: Test non-blocking build
5. Deploy if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Threading) → Test independently → Deploy (MVP!)
3. Add US2 (Dependencies) → Test independently → Deploy
4. Add US3 (Error Handling) → Test independently → Deploy
5. Add US4 (Log Management) → Test independently → Deploy
6. Add US5 (Config Resilience) → Test independently → Deploy

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests pass before committing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
