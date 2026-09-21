---
name: Azure AI Operations Studio
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#c0c7d4'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#8a919e'
  outline-variant: '#404752'
  surface-tint: '#a3c9ff'
  primary: '#a3c9ff'
  on-primary: '#00315c'
  primary-container: '#0078d4'
  on-primary-container: '#ffffff'
  inverse-primary: '#0060ab'
  secondary: '#d2bbff'
  on-secondary: '#3f008e'
  secondary-container: '#6001d1'
  on-secondary-container: '#c9aeff'
  tertiary: '#4edea3'
  on-tertiary: '#003824'
  tertiary-container: '#00875d'
  on-tertiary-container: '#ffffff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d3e3ff'
  primary-fixed-dim: '#a3c9ff'
  on-primary-fixed: '#001c39'
  on-primary-fixed-variant: '#004883'
  secondary-fixed: '#eaddff'
  secondary-fixed-dim: '#d2bbff'
  on-secondary-fixed: '#25005a'
  on-secondary-fixed-variant: '#5a00c6'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
  code-sm:
    fontFamily: monospace
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-lg: 1.5rem
  margin: 1.5rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system provides an enterprise-grade, high-density interface foundation engineered specifically for AI orchestration, Retrieval-Augmented Generation (RAG) pipelines, and vector infrastructure monitoring. The visual identity evokes absolute reliability, operational precision, and systemic clarity, balanced with subtle electric accents that represent intelligent computation.

Targeting enterprise machine learning engineers, cloud architects, and data platform operators, the user interface rejects extraneous decorative trends in favor of a utilitarian, high-contrast dark environment. The visual style merges modern enterprise cloud ergonomics with focused micro-interactions: deep slate structural surfaces, razor-thin structural borders, precise spatial typography, and energetic indigo-blue to violet gradients reserved strictly for generative AI states, vector distances, and active model execution.

## Colors

The color architecture is built around a controlled, dark-mode-first slate hierarchy paired with functional signal colors:

- **Primary (`#0078D4`):** Electric Azure Blue serves as the operational anchor—used for primary system triggers, active navigation items, selected workspace panes, and primary data traces.
- **Secondary (`#7C3AED`):** Neon Violet signals generative AI processes, prompt evaluation states, vector space similarity scores, and LLM inference markers.
- **Tertiary (`#10B981`):** Precision Emerald is reserved for vector index health, cluster readiness, streaming completion states, and active endpoint pings.
- **Neutral Palette:** Anchored on deep slate tones. The base canvas operates at `#020617` (Slate 950) and `#0F172A` (Slate 900). Structural containers use `#1E293B` (Slate 800) and elevated inspection panes sit at `#334155` (Slate 700).
- **Subtle Gradients:** Used exclusively for high-context data viz and active inference indicators—blending Primary Azure (`#0078D4`) seamlessly into Deep Neon Purple (`#7C3AED`) with strict 1px boundary highlights.

## Typography

Typography is set strictly in Inter to provide an uncompromisingly neutral, legible, and compact information hierarchy suitable for dense telemetry, configuration panels, and complex node graphs.

- **Scale & Rhythm:** Typography is calibrated on a standard 4px baseline, emphasizing tight tracking on headlines (`-0.02em`) to maintain structural density, while metadata labels use deliberate medium/semi-bold weights for high legibility against low-luminance backgrounds.
- **Monospace Usage:** System embeddings, vector dimension matrices, token counts, latency metrics, and API payloads map to the system monospaced stack (`code-sm`), ensuring tabular vertical alignment across table columns and inspection drawers.
- **Micro Labels:** Status tags and metric classifications utilize `label-sm` with slight uppercase letter-spacing (`+0.04em`) to ensure instant recognition at high data densities.

## Layout & Spacing

The layout model utilizes a fluid 12-column analytical grid with fixed side-docking utilities. Spacing follows a compact 4px/8px modular rhythm, prioritizing high visual density without visual collision.

- **Desktop (1440px+):** Full multi-pane orchestration featuring a 64px collapsed icon rail, a 280px secondary resource tree, and an expandable 12-column main canvas. Gutters are standardized to `1.5rem` (`gutter-lg`), with card padding locked to `1rem` (`space-md`) to ensure maximum visible data area.
- **Tablet (768px - 1439px):** Canvas consolidates into 8 columns. Inspection drawers shift from side-by-side persistent tiles to dismissible right-anchored overlays.
- **Mobile (< 768px):** Reflows to a single fluid column with a strict `1rem` margin. Complex vector graphs collapse into linear log streams and tabulated summaries.

## Elevation & Depth

Depth is established primarily through structural tonal layering and crisp, low-contrast borders rather than exaggerated drop shadows:

- **Layer 0 (Canvas Base):** Deep Slate (`#020617`), strictly non-elevated, serving as the viewport substrate.
- **Layer 1 (Card & Module Surfaces):** Slate 900 (`#0F172A`) paired with a 1px solid border in Slate 800 (`#1E293B`) or semi-transparent white (`rgba(255, 255, 255, 0.08)`).
- **Layer 2 (Floating Inspect Panels & Popovers):** Elevated Slate 850 (`#1E293B/90`) utilizing subtle backdrop blur (`backdrop-filter: blur(12px)`) with a faint perimeter shadow: `0 4px 20px -2px rgba(0, 0, 0, 0.5)`.
- **Active / Focused Depth:** Interactive items do not project heavy drop shadows; instead, they cast an acute, low-radius ambient glow matching the accent color: `0 0 12px 0 rgba(0, 120, 212, 0.25)` for Azure Blue or `0 0 12px 0 rgba(124, 58, 237, 0.25)` for generative AI nodes.

## Shapes

The design system standardizes on a structured, professional corner radius (`roundedness: 1` / `0.25rem` base).

- **Standard Containers, Cards, and Inputs:** Set to `0.25rem` (4px). This creates sharp, disciplined silhouettes aligned with data-dense enterprise dashboards.
- **Flyouts, Dropdowns, and Modals:** Set to `0.5rem` (8px, `rounded-lg`) to gently delineate contextual layers from the underlying structural grid.
- **Pill Badges & Status Indicators:** Status tags, indexing states, and vector similarity pills use fully rounded endpoints (`rounded-full` / 9999px) to contrast against the architectural square-corner layout of parent containers.

## Components

### Buttons
- **Primary Action:** Solid Azure Blue (`#0078D4`) background, crisp white typography (`label-md`), 4px border radius. Hover introduces subtle brightness (`#106EBE`) without size transformation.
- **AI / Generative Trigger:** Subtle linear gradient from `#0078D4` to `#7C3AED`, 1px hairline border in `rgba(255, 255, 255, 0.2)`, illuminated on hover with a faint violet aura.
- **Secondary & Ghost:** Transparent surface with 1px border in Slate 700 (`#334155`), text in Slate 200. Hover transitions background to Slate 800 (`#1E293B`).

### Chips & Badges
- **Status Pills:** Pill-shaped (`rounded-full`), 20px height, containing a 6px solid circular pulse dot. Indexing/Active states use Emerald (`#10B981/15` fill, `#10B981` text).
- **Vector Metric Tags:** Compact pill badges with monospace numerical scores (e.g., `sim: 0.892`) using Violet tinting (`#7C3AED/15` fill, `#A78BFA` text).

### Cards & Telemetry Tiles
- Built with Slate 900 base, 1px border in Slate 800, and inner padding of `1rem`. Headers contain an icon anchor, category title in `label-sm`, and action menus pinned top-right.

### Form Inputs & Query Terminals
- High-contrast text fields enclosed by Slate 800 borders on Slate 950 backgrounds. Focus state switches border strictly to Azure Blue (`#0078D4`) with a unified 1px offset ring. Monospaced font applies automatically to vector search or query input fields.

### Lists & Data Grids
- Flat rows with 1px bottom divider in `#1E293B`. Interactive rows feature a left 2px border indicator that highlights in Azure Blue on hover/selection, maintaining rock-solid visual stability during rapid scrolling.