## Follow-Ups Needed

```dataview
TABLE
  person as "Who",
  subject as "What",
  sent as "Sent",
  expected as "Due By",
  choice(expected < date(today), "🔴 OVERDUE",
         choice(expected = date(today), "🟡 TODAY", "🟢 Soon")) as "Status"
FROM "waiting-for/active"
WHERE status = "pending"
SORT expected asc
```

Currently waiting on **$= dv.pages('"waiting-for/active"').where(p => p.status === "pending").length** items

---

## All Active Waiting-For Items

```dataview
TABLE
  person,
  subject,
  sent,
  expected,
  priority
FROM "waiting-for/active"
WHERE status = "pending"
SORT priority desc, expected asc
```
