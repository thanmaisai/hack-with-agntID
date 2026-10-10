---
title: Documentation Style Guide
last_verified: 2026-09-04
owner: docs-team
---

<div class="page-intro" markdown>

# Documentation Style Guide

Use these rules to create clear, accurate AgntID documentation for readers around the world.

</div>

## Required page header

Every page must include:

- `title`
- `last_verified` in `YYYY-MM-DD` format
- `owner`

Use `version` only when the page describes a versioned workflow.

```yaml
---
title: Page Title
last_verified: 2026-09-04
owner: docs-team
---
```

Update `last_verified` only after checking the page against the current product or runnable source. If part of the flow was not tested, say so on the page.

## Start with the outcome

Open with one sentence that tells the reader what they will complete. Use the shared green introduction style:

```html
<div class="page-intro" markdown>

# Add an MCP server

Connect an MCP server to an AgntID runtime and review which tools are available.

</div>
```

Do not begin with product history, architecture detail, or a list of internal components.

## Use simple international English

- Use short sentences and familiar words.
- Write in active voice: “Select **Connect**,” not “The connection should be initiated.”
- Give one instruction at a time.
- Define an acronym the first time it appears unless it is a navigation label.
- Use the same word for the same object throughout a page.
- Explain a necessary technical term in plain language before using it repeatedly.

Avoid idioms and phrases that are difficult to translate, such as:

- “day-two workspace”
- “happy path”
- “under the hood”
- “blast radius”
- “dummy policy”
- “simply,” “obviously,” or “just” when a step has real requirements

Prefer “Use this page after setup” over “This is your day-two workspace.”

## Use product terms consistently

| Use | Meaning |
| --- | --- |
| **AgntID portal** | The browser-based control plane |
| **local runtime UI** | The interface running on `localhost` for connecting and checking a customer runtime |
| **AgntID runtime** | The customer-hosted service that filters tools and checks calls |
| **protection profile** | The Low, Medium, or High boundary that determines which reviewed actions are eligible |
| **MCP server** | A service or process that provides tools |
| **MCP client** | An application such as Cursor, Claude, or Codex that uses tools |
| **tool** | One action provided by an MCP server |

Do not call both the AgntID portal and the local runtime UI “the runtime portal.”

Use **select** for buttons, tabs, menu items, and options. Use **enter** for text fields and **run** for commands.

## Structure a task page

Use this order when it fits the task:

1. Outcome and expected time.
2. A small journey diagram when the flow has several stages.
3. Prerequisites.
4. Numbered steps in the order the user performs them.
5. Expected result after an important step.
6. Troubleshooting for likely failures.
7. **What’s next** links.

Use numbered lists for procedures and bullets for unordered facts. Keep one main user action in each numbered item. Put optional or advanced work after the required flow.

## Describe access correctly

Tool access is not “deny everything until a policy is created.” Current documentation must explain that:

- the protection profile determines the maximum eligible tool set
- only reviewed actions can become available
- individual tool settings and verified role grants can reduce the visible list
- baseline allow policies permit eligible tools
- detailed policies can restrict inputs or deny individual calls
- changing one tool does not automatically deny every other tool

Always separate these two OAuth connections:

1. MCP client to AgntID runtime.
2. AgntID runtime to an external MCP server.

Do not claim that Inspector or Simulator proves an external client's OAuth flow. Test sign-in with the actual client.

## Make commands copyable

- Test commands from the rendered page in a clean directory.
- Include the required working directory before a command.
- Use placeholders such as `your-profile`; never use a personal path, account, hostname, token, or ID.
- Keep commands short and explain the expected output.
- Use operating-system tabs only when syntax differs.
- Pin released customer artifacts to the documented version.
- Do not provide setup commands for source that users cannot download.

If an example is not public or not complete, mark it **under development** and do not present it as runnable.

## Use code examples carefully

- Prefer a small complete example over an isolated fragment.
- State required package and source versions.
- Use tool names and argument names that exist in the current runtime.
- Use neutral identities such as `user-42` and `docs-agent`.
- Never let model-generated values replace trusted user, agent, or session identity.
- Explain which call performs real work and which call is only a mock or validation.

## Create useful diagrams

Use a diagram only when it makes a multi-step flow, boundary, or relationship easier to understand.

- Use SVG for documentation diagrams.
- Provide matching light and dark files.
- Use a responsive `viewBox`; do not set a fixed rendered width.
- Keep text inside its blocks at desktop and narrow widths.
- Use arrows with one clear direction.
- Add an SVG `<title>` and `<desc>`.
- Add descriptive HTML `alt` text that explains the relationship, not the colors.
- Validate the SVG as XML and inspect it in both themes.

Do not repeat the same information in a diagram and a long paragraph.

## Capture screenshots safely

- Use a clean demonstration environment with neutral names.
- Use a consistent desktop viewport, 100% zoom, light theme, and cropped browser chrome.
- Capture only the area needed for the instruction.
- Never show tokens, credentials, personal data, production events, internal IDs, or unrelated browser tabs.
- Use current product labels and realistic but non-sensitive sample data.
- Write alt text that states what the reader should notice.
- Remove an old screenshot only after checking that no other page uses it.

Screenshots should support a step, not replace its written instruction.

## Be honest about validation

Use clear labels:

| Status | When to use it |
| --- | --- |
| **Verified** | The documented flow passed from its stated starting point to its expected result |
| **Partially verified** | Some checks passed, but a named external or destructive step was not run |
| **Under development** | The public source or complete workflow is not available yet |
| **Planned** | No usable implementation is available |

Never turn an internal prototype into a public quick start unless its source and dependencies are available to the reader.

## Write release notes for users

- Put the newest dated entry first.
- Describe shipped behavior and available documentation, not internal implementation work.
- Group related changes under short headings.
- Link to the guide that helps the user act on the change.
- State important availability limits, such as an unpublished package or unverified OAuth client.
- Keep historical entries, but clearly point to the replacement when a workflow is obsolete.

## Final review checklist

Before publishing, confirm:

- the outcome is clear in the first paragraph
- prerequisites are complete
- every UI label matches the current portal or runtime
- commands and examples run as written
- tool visibility and policy behavior are accurate
- public links work without internal access
- screenshots contain no sensitive information
- diagrams render in light and dark themes without clipped text
- spelling, AgntID capitalization, links, headings, and alt text are correct
- `last_verified` reflects the checks actually completed

## Link to the portal

Use `[AgntID portal](https://app.agntid.ai/)` for the first prose mention on a page and instructions that send readers to the portal. The root `agntid.ai` is the marketing website. Keep links to documentation pages and local runtime URLs intact. For custom instances, tell readers to use their instance's portal URL. Link to specific portal pages only after verifying their routes. Do not add Markdown links inside code blocks, diagrams, or image alt text.
