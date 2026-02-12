---
name: Web Development Platform Instructions
description: Platform-specific guidance for web application development
---

<!-- Catalog Metadata
id: INST-PLAT-001
version: 1.0.0
scope: platform
applies_to: web
priority: high
author: community
last_reviewed: 2026-02-12
-->

# Web Development — Platform Instructions

## Scope
These instructions apply when building **web applications** — frontend, backend, or full-stack.

## Frontend

### Framework Selection
- **React**: Component-based, large ecosystem, good for SPAs and complex UIs
- **Angular**: Full framework, TypeScript-first, good for enterprise applications
- **Vue**: Progressive framework, gentle learning curve, flexible architecture
- **Svelte**: Compile-time framework, minimal runtime, excellent performance
- **Astro/Next.js/Nuxt.js**: SSR/SSG options for content-heavy or SEO-important sites

When recommending a framework, consider: team experience, project size, performance requirements, and ecosystem needs. Don't recommend based on popularity alone.

### Frontend Best Practices
- Implement **responsive design** — mobile-first approach
- Follow **WCAG 2.1 AA** accessibility standards minimum
- Optimize **Core Web Vitals**: LCP < 2.5s, FID < 100ms, CLS < 0.1
- Use **lazy loading** for images and below-the-fold content
- Implement **code splitting** to reduce initial bundle size
- Use **semantic HTML** — not everything is a `<div>`
- Implement **proper state management** — component state, context/stores, server state
- Handle **loading, error, and empty states** for every async operation
- Support **keyboard navigation** and screen readers
- Implement **proper form validation** — client-side for UX, server-side for security

### Frontend Security
- Implement **Content Security Policy (CSP)** headers
- Sanitize any **user-generated content** before rendering
- Use **SRI (Subresource Integrity)** for CDN-hosted scripts
- Store tokens in **httpOnly, secure, sameSite cookies** — not localStorage
- Implement **CSRF tokens** for state-changing requests
- Validate **redirect URLs** to prevent open redirect attacks

## Backend

### API Design
- Use **RESTful conventions** or **GraphQL** with clear justification for choice
- Version APIs from day one (`/api/v1/`)
- Return **consistent response envelopes** with proper HTTP status codes
- Implement **pagination** for list endpoints (cursor-based preferred for large datasets)
- Use **rate limiting** and **request throttling**
- Support **CORS** with explicit origin allowlists (never `*` in production)
- Document APIs with **OpenAPI/Swagger** specifications

### Backend Security
- Validate **every input** — don't trust the client
- Use **parameterized queries** — always
- Implement **authentication middleware** — check on every request
- Use **HTTPS everywhere** — redirect HTTP to HTTPS
- Set **security headers**: HSTS, X-Frame-Options, X-Content-Type-Options
- Implement **request size limits** to prevent abuse
- Use **structured logging** — never log credentials or PII

### Performance
- Use **CDN** for static assets and cacheable API responses
- Implement **gzip/brotli compression** for text-based responses
- Use **HTTP/2 or HTTP/3** where supported
- Implement **server-side caching** (Redis, Memcached) for hot data
- Use **database connection pooling**
- Implement **health check endpoints** for load balancers

## Full-Stack Patterns
- **SSR (Server-Side Rendering)**: Better SEO, faster FCP, higher server load
- **SSG (Static Site Generation)**: Best performance, limited to static content
- **CSR (Client-Side Rendering)**: Rich interactivity, needs loading states
- **ISR (Incremental Static Regeneration)**: Balance of SSG and dynamic content
- **Edge rendering**: Low-latency, geo-distributed computation

Choose based on the content type, update frequency, and performance requirements.
