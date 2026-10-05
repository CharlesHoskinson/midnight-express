# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Product Purpose

Midnight Express proposes private event distribution with explicit business meaning and local subscription selection. The website explains the architecture, data contracts, implementation evidence and remaining work. Its subscription interface is a browser-local proof of concept.

## Users and Workflows

The user confirmed that discovering and organizing subscriptions through a feed directory is the default subscription workflow. The requested design must handle hundreds of feeds, search and stateful information. Human readers, wallets, DApps and agents are audiences named in the product brief. Inbox reading and delivery operations support the directory workflow.

## Capabilities and Constraints

The existing site uses static HTML, CSS and JavaScript on GitHub Pages. The demo has synthetic events, fixed-context validator receipts and an optional Moth connection adapter. It has no live protocol transport or production permission service. Installed v0.2 reference contracts cover quotes, payment observations and sandbox approvals; other demo categories remain mock-only.

A category is local organization, not a network business topic. Delivery, processing and effects have different meanings. Saved interface preferences cannot establish authenticated source identity, wallet permission or protocol authority. Moth connection requires an explicit click and acknowledges an origin-wide grant.

## Brand Commitments

The product is Midnight Express. The user requires clear explanations and rejects artificial counting in headings and prose. Original project code and documentation use Apache License 2.0; imported references and fonts retain their own licenses.

## Evidence on Hand

The repository contains the proposed architecture and requirements, a bounded local reference model, a checked Lean model and finite validation bridge. Subscription research is stored in `wiki-llm/pubsub`. The new design council records primary-source research and recommendations in `wiki-llm/subscription-design-council`.

## Open Decisions

Independent feed scopes, publisher metadata and production source discovery need explicit contracts. The council recommends the directory workspace in `design/subscriptions/directory-workspace.md`; browser persistence and the replacement interface remain implementation work. No customer validation or production performance result establishes the proposed experience.
