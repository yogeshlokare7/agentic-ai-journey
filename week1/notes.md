# Week 1 notes

## Day 6: sync (day5.py) vs async (day6.py)

Both scripts make 11 requests: `GET /users`, then `GET /posts?userId=N` for each of the 10 users.
Times are for the report only, measured with `time.perf_counter()`, run on 2026-10-31.

| Run | day5.py (sync, sequential) | day6.py (async, `asyncio.gather`) |
|-----|----------------------------|-----------------------------------|
| 1   | 0.18s | 1.21s |
| 2   | 1.31s | 0.98s |
| 3   | 0.20s | 1.43s |
| 4   | 1.53s | 1.75s |
| 5   | 0.24s | 1.55s |
| 6   | 0.92s | 1.73s |
| 7   | 0.23s | 1.53s |
| 8   | 0.87s | 0.75s |

**Result: async was usually slower here.** Breakdown of where the time goes:

| Step | Time |
|------|------|
| One request on an already-open connection | ~15ms |
| Sync: 10 posts requests, one after another, over 1 reused connection | 0.15s |
| Async: 10 posts requests at once, first time (opens ~9 new connections) | 1.33s |
| Async: the same 10 requests at once again (connections already open) | 0.06s |

Why:
- `httpx` keeps a connection open and reuses it. The sync client opens one HTTPS connection
  and sends all 11 requests down it, so each request costs only ~15ms.
- `gather` fires all 10 requests at the same moment. None can wait to reuse the connection,
  so the client opens ~9 new ones, each with its own TLS handshake. That setup cost (~1.3s)
  is far larger than the ~0.15s that concurrency saves.
- Once connections are open, async wins: 0.06s vs 0.15s, about 2.5x faster.
- The sync times jump around (0.18s to 1.53s) because sometimes the first connection itself
  is slow to set up (DNS, TLS). Network noise matters more than code at this scale.

Takeaways:
- Concurrency pays off when each request is slow (hundreds of ms) or there are many of them.
  JSONPlaceholder answers in ~15ms, so there is little waiting to overlap.
- Reuse one client for many calls; creating connections is the expensive part.
- To limit how many connections `gather` opens at once, use `httpx.Limits(max_connections=...)`
  or an `asyncio.Semaphore`.
