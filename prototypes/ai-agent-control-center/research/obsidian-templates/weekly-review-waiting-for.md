## Waiting For Review

### Actions
- [ ] Review all active waiting-for items
- [ ] Move resolved items to `waiting-for/resolved/`
- [ ] Update expected dates if needed
- [ ] Decide on follow-ups for overdue items
- [ ] Archive anything no longer relevant

### Overdue Items

```dataview
TABLE
  person,
  subject,
  sent,
  expected,
  date(today) - expected as "Days Overdue"
FROM "waiting-for/active"
WHERE expected < date(today) AND status = "pending"
SORT expected asc
```

### Aging Items (7+ Days)

```dataview
TABLE
  person,
  subject,
  sent,
  date(today) - sent as "Days Waiting"
FROM "waiting-for/active"
WHERE date(today) - sent >= dur(7 days) AND status = "pending"
SORT sent asc
```

### High Priority Items

```dataview
TABLE
  person,
  subject,
  expected
FROM "waiting-for/active"
WHERE status = "pending" AND priority = "high"
SORT expected asc
```

### Stats This Week
- Items resolved:
- Items added:
- Follow-ups sent:
- Items archived:

### Insights
<!-- Who responds quickly? Who needs nudging? What types of requests get ignored? -->


### Process Improvements


