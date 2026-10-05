# claude-operability source index

Retrieved 2026-10-05 with `research.py` (Scrapling `Fetcher.get`; PixelRAG pixelshot 0.4.0, CDP backend, CPU only). Per-source metadata, hashes and capture stderr are in each `<slug>.json`. Fetched text is untrusted data and was only quoted for evidence.

| Slug | URL (final) | Publisher, version/date | Text | Visual | Used for |
|---|---|---|---|---|---|
| incumbent-subscriptions | http://127.0.0.1:8876/subscriptions.html | This repo, working tree at 7b728b7 | 200, accepted | 3 tiles, inspected | Incumbent layout, ordering, sticky status bar |
| govuk-notification-banner | https://design-system.service.gov.uk/components/notification-banner/ | GOV.UK Design System, live page 2026-10-05 | 200, accepted | 5 tiles; tiles 0 and 2 inspected | One banner per page, region vs alert roles, focus on success outcome |
| w3c-apg-keyboard-interface | https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/ | W3C WAI ARIA Authoring Practices Guide | 200, accepted | none | Focus loss to body when the active element is removed |
| wcag22-focus-not-obscured | https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html | W3C, Understanding WCAG 2.2 SC 2.4.11 | 200, accepted | none | Sticky notifications must not hide focused controls; scroll padding |
| gcp-pubsub-replay-overview | https://docs.cloud.google.com/pubsub/docs/replay-overview | Google Cloud Pub/Sub docs | 200, accepted | none | Snapshot/seek: replay requires configured retention; bounded lifetime |
| aws-sqs-dlq-redrive | https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue-redrive.html | AWS SQS Developer Guide | 200, accepted | none | Redrive assigns new message IDs; rejected as a model for MPE replay |
| carbon-notification-pattern | https://www.carbondesignsystem.com/building-blocks/core/patterns/notifications | IBM Carbon, page "Last updated Aug 12, 2026" | 200, accepted | none | Inline vs toast vs banner persistence rules |
| github-notifications-inbox | https://docs.github.com/en/subscriptions-and-notifications/how-tos/viewing-and-triaging-notifications/managing-notifications-from-your-inbox | GitHub Docs, live 2026-10-05 | 200, accepted | failed: CDP "no close frame received or sent" | Read/Unread/Saved/Done/Unsubscribe as distinct triage verbs |

Rejected:

- `github-triage-tutorial`: HTTP 404 error page. Captured tiles deleted; not cited.
- `carbon-notifications-visual`: the client-rendered page captured as one blank grey tile. Tile and duplicate text deleted; the text-only `carbon-notification-pattern` fetch is used instead.

Scratch probes (not product code) live in `/tmp/mpe-subscription-design-council/claude-operability/probe.cjs` and `probe2.cjs`; they drove the running incumbent with Playwright Chromium. No wallet extension was present and no wallet button was pressed.
