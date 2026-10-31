# BrandHub Documentation & Figure Portal (`brandhub-docs-portal`)

Interactive documentation portal for the **BrandHub SEP490 Capstone Exam Committee (Ban Giám Khảo)**, hosting all **312 high-resolution UML Diagrams & Screen Mockups** (321 Cloudinary images) and **141 Atomic CRUD Functional Requirements (`3.2.1` – `3.10.14`)** across Reports 1, 2, 3, and 4.

## Key Features

- **312 High-Resolution Figures (`/figures/:figureId`)**:
  - Report 1 (`r1-fig-1` .. `r1-fig-5`): Context, Swimlane As-Is/To-Be, Mindmap.
  - Report 2 (`r2-fig-1` .. `r2-fig-7`): Org Chart, Scrum Process, Gantt Roadmap, WBS.
  - Report 3 (`r3-fig-1` .. `r3-fig-150`): Overall & Package Use Case Diagrams, State Machine, Activity Diagrams, ERD, and 141 Screen Layout Mockups.
  - Report 4 (`cd-3.2` .. `cd-3.10`, `seq-3.2.1` .. `seq-3.10.14`): 9 Domain Class Diagrams and 141 Sequence Diagrams.
- **141 Functional Requirements Explorer (`/frs` & `/frs/:frCode`)**:
  - 3-Diagram Switcher per FR (Screen Layout, Sequence Diagram, Class Diagram).
  - Practical, easy-to-understand explanations, execution steps, error handling, and linked Business Rules (`BR-01` – `BR-65`) & System Messages (`MSG01` – `MSG60`).
- **System Matrices (`/matrices`) & Business Rules (`/rules`)**:
  - 141 Use Cases (`UC-001` – `UC-141`), 38 Screens × 6 Canonical Roles (`Guest`, `Owner`, `Manager`, `Creator`, `Client`, `Admin`), 12 Background Tasks, and 28 Database Entities.
- **Word Deep-Link Manager (`/links`)**:
  - One-click copy and CSV export for attaching deep-links to `Figure X - ...` captions in Word reports (`Report1` – `Report4`).
- **System-Synced Light/Dark Theme & Bilingual (`VI` / `EN`) UI**:
  - Automatically syncs with OS/mobile `prefers-color-scheme`, supports touch pan/zoom on diagrams, and includes a responsive mobile bottom navigation bar.

## Project Structure

```text
src/
├── components/         # Navbar, InteractiveImageViewer, GlobalSearchModal, RoleBadge
├── context/            # AppPreferencesContext (Light/Dark/System theme & VI/EN i18n)
├── data/               # Modular JSON data files (easy to edit & maintain)
│   ├── project.json
│   ├── useCases.json
│   ├── rulesAndMessages.json
│   ├── matrices.json
│   ├── figures/        # report1.json, report2.json, report3-overview.json, report3-screens.json, report4-class.json, report4-sequence.json
│   └── frs/            # domain-3.2.json .. domain-3.10.json
├── pages/              # Catalog, Detail, Explorer, Matrix, Rules, WordLinkManager
└── types/              # TypeScript interfaces
```

## Quick Start

```bash
# 1. Install dependencies
npm install

# 2. Configure environment variables (optional, only needed when re-uploading images to Cloudinary)
cp .env.example .env

# 3. Start development server on port 5180
npm run dev

# 4. Build for production
npm run build
```
