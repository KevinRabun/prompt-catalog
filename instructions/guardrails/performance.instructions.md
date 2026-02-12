---
name: Performance Guardrails
description: Ensure AI agents generate performant code and recommend efficient architectures
---

<!-- Catalog Metadata
id: INST-GUARD-004
version: 1.0.0
scope: guardrail
applies_to: all
priority: high
author: community
last_reviewed: 2026-02-12
-->

# Performance Guardrails

## Objective
Performance must be considered from the start, not optimized after deployment. These guardrails ensure AI agents produce **efficient code** and recommend **performant architectures** while avoiding premature optimization.

## Core Principles

1. **Measure first** — Don't optimize without data showing a problem
2. **Optimize the right thing** — Focus on bottlenecks, not micro-optimizations
3. **Design for performance** — Architecture decisions have the biggest performance impact
4. **Set targets** — Every system should have defined performance requirements
5. **Test continuously** — Performance regression should be caught in CI/CD

## Code-Level Performance

### DO
- Use **appropriate data structures** — HashMap for lookups, arrays for sequential access
- Use **efficient algorithms** — understand Big-O complexity of operations
- Implement **pagination** for large result sets — never return unbounded collections
- Use **async/await** for I/O-bound operations — don't block threads on I/O
- Use **streaming** for large data processing — don't load everything into memory
- Implement **connection pooling** for database and HTTP connections
- Use **caching** at appropriate levels (memory, distributed, CDN)
- **Batch operations** where possible (bulk inserts, batch API calls)
- Dispose of resources properly (**close connections, streams, file handles**)
- Use **lazy loading** when data may not be needed

### DO NOT
- Create **N+1 query problems** — eager-load or batch related data
- Allocate **unnecessary objects** in hot paths (loops, request handlers)
- Use **synchronous I/O** in async contexts (blocking the thread pool)
- **Serialize/deserialize** unnecessarily — pass objects by reference when possible
- Perform **string concatenation in loops** — use StringBuilder or equivalent
- Make **network calls inside loops** — batch or parallelize instead
- **Log excessively** in hot paths — debug logging should be conditionally enabled
- Use **regular expressions** for simple string operations
- Ignore **memory leaks** — especially in long-running services
- Perform **premature optimization** — profile first, optimize the bottleneck

## Architecture-Level Performance

### Database
- **Index strategically** — cover frequent query patterns, don't over-index
- Use **query execution plans** to verify query efficiency
- Implement **read replicas** for read-heavy workloads
- Use **materialized views** for complex, frequently-run analytics
- Implement **connection pooling** — size pools based on measured concurrency
- Consider **sharding** for datasets that exceed single-node capacity
- Use **appropriate isolation levels** — don't over-serialize transactions

### Caching Strategy
```
Layer 1: Application memory (ms latency, limited capacity)
  └── Hot data, computed results, config values
Layer 2: Distributed cache (1-5ms latency, scalable)
  └── Session data, API responses, database query results
Layer 3: CDN (10-50ms latency, global)
  └── Static assets, rendered pages, API responses for public data
  
Cache Invalidation Strategy:
  - TTL-based for data that can be slightly stale
  - Event-based for data that must be immediately consistent
  - Hybrid for cost-effective near-real-time consistency
```

### API Performance
- Set **timeout budgets** for every external call
- Implement **circuit breakers** to prevent cascade failures
- Use **compression** for large response payloads (gzip, brotli)
- Support **conditional requests** (ETags, If-Modified-Since)
- Implement **request coalescing** for duplicate concurrent requests
- Use **efficient serialization** — JSON for readability, Protobuf for throughput
- Return only **requested fields** (GraphQL, sparse fieldsets, projections)

### Concurrency and Parallelism
- Use **thread pools** with bounded sizes — don't create unlimited threads
- Use **async patterns** for I/O-bound work
- Use **parallel processing** for CPU-bound work with independent chunks
- Implement **back-pressure** to prevent overload
- Use **lock-free data structures** in high-contention scenarios where possible
- Prefer **immutable data** to avoid synchronization overhead

## Performance Budgets

Define and enforce budgets per component:

| Metric | Web Frontend | API Endpoint | Background Job |
|--------|-------------|--------------|----------------|
| Response Time (P50) | < 200ms | < 100ms | N/A |
| Response Time (P99) | < 2s | < 500ms | N/A |
| Time to Interactive | < 3s | N/A | N/A |
| Bundle Size | < 200KB gzipped | N/A | N/A |
| Memory Usage | N/A | < 512MB per instance | < 2GB |
| CPU per Request | N/A | < 50ms | N/A |

## Performance Testing

- **Load testing** — Does it handle expected concurrent users?
- **Stress testing** — Where does it break?
- **Endurance testing** — Does performance degrade over time (memory leaks)?
- **Spike testing** — How does it handle sudden traffic bursts?
- **Baseline testing** — Track performance across code changes

## Performance Review Checklist

- [ ] Queries are indexed and execution plans are reviewed
- [ ] N+1 query patterns are eliminated
- [ ] Async/await is used for I/O operations
- [ ] Caching is implemented where beneficial
- [ ] Pagination is used for large result sets
- [ ] Connection pooling is configured
- [ ] Memory allocation is reasonable (no unnecessary object creation in hot paths)
- [ ] Performance budgets are defined and tested
- [ ] Monitoring tracks key performance metrics
- [ ] Load tests cover expected peak traffic
