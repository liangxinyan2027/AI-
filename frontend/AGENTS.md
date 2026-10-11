# Prototype Instructions

User-selected design: warm ivory #FAF4EF, blush #D995A4, mauve #8C6AAE, plum #34283B. Hero follows the supplied VaultShield video and spacing specification. Only the supplied SVG logo, Chinese heading/subheading and one scroll CTA appear above the fold. No right-side dashboard or top navigation. The workspace below uses the selected minimal style C. Actual Python/EconML data is required; illustrative mockup figures are not valid data.

Run the local server yourself and open the preview in the browser available to this environment. Do not give the user server-start instructions when you can run it.

Before making substantial visual changes, use the Product Design plugin's `get-context` skill when the visual source is unclear or no longer matches the current goal. When the user gives durable prototype-specific design feedback, preferences, or decisions, record them in `AGENTS.md`.

When implementing from a selected generated mock, treat that image as the source of truth for layout, component anatomy, density, spacing, color, typography, visible content, and hierarchy.

Build app UI in `src/`. Keep `.openai/hosting.json`, `worker/index.js`, `scripts/prepare-sites-build.mjs`, and `tests/sites-worker.test.mjs` intact so the same local prototype can be handed to Sites. Before a Sites handoff, run `npm run build` and `npm run test:sites`; the build must leave `dist/client/index.html`, `dist/server/index.js`, and `dist/.openai/hosting.json`.
