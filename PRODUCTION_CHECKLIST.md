# 🔐 Production Checklist

Use this checklist before deploying to production.

## Security ✅

- [ ] Change `SECRET_KEY` to a random 32-character string
- [ ] Implement password hashing (bcrypt) in auth routes
- [ ] Enable HTTPS in production config
- [ ] Set `DEBUG = False` in production
- [ ] Remove development API keys from repository
- [ ] Set strong CORS_ORIGINS (not `*`)
- [ ] Enable CSRF protection
- [ ] Rate limit API endpoints
- [ ] Validate all user inputs
- [ ] Implement request logging
- [ ] Set up error monitoring (Sentry)
- [ ] Never commit `.env` files

## Database ✅

- [ ] Use PostgreSQL (not SQLite) in production
- [ ] Enable database backups (automated daily)
- [ ] Test database restore process
- [ ] Create database indexes for frequently queried columns
- [ ] Set up connection pooling
- [ ] Validate database constraints
- [ ] Run schema migrations
- [ ] Test database transactions

## API ✅

- [ ] All endpoints return proper HTTP status codes
- [ ] Error responses are consistent
- [ ] Pagination works correctly
- [ ] Rate limiting is enforced
- [ ] Authentication is required where needed
- [ ] API documentation is up to date
- [ ] Timeout values are appropriate
- [ ] All database queries have indexes

## Frontend ✅

- [ ] Build succeeds: `npm run build`
- [ ] No console errors in production build
- [ ] Environment variables are correctly set
- [ ] API base URL points to production backend
- [ ] All links are relative or use environment variables
- [ ] Image optimization is enabled
- [ ] Caching headers are set correctly
- [ ] Service worker is configured
- [ ] Error boundaries are implemented
- [ ] Analytics are configured

## AI Integration ✅

- [ ] OpenAI API key is valid and has sufficient balance
- [ ] Gemini API key is valid
- [ ] AI endpoints have proper error handling
- [ ] API quotas are sufficient for expected usage
- [ ] Fallback AI provider is configured
- [ ] Temperature and max_tokens are appropriate
- [ ] Prompts are tested and optimized
- [ ] Cost monitoring is set up

## Monitoring & Logging ✅

- [ ] Application logging is configured
- [ ] Error tracking is enabled (Sentry/Bugsnag)
- [ ] Performance monitoring is set up (New Relic/DataDog)
- [ ] Uptime monitoring is configured
- [ ] Database performance is monitored
- [ ] API response times are tracked
- [ ] User analytics are tracked
- [ ] Email notifications are set up for errors

## Performance ✅

- [ ] Database queries are optimized (no N+1)
- [ ] Caching is implemented for static assets
- [ ] Gzip compression is enabled
- [ ] Images are optimized
- [ ] CSS/JS are minified
- [ ] Lazy loading is implemented
- [ ] Bundle size is reasonable
- [ ] Load times are under 3 seconds

## Testing ✅

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass (if implemented)
- [ ] Test coverage is above 70%
- [ ] Manual testing checklist completed
- [ ] Cross-browser testing done
- [ ] Mobile responsiveness verified
- [ ] Accessibility testing completed

## Deployment ✅

- [ ] Repository is pushed to GitHub
- [ ] CI/CD pipeline is configured
- [ ] Auto-deployments are working
- [ ] Rollback procedure is documented
- [ ] Deployment logs are accessible
- [ ] Environment variables are secured
- [ ] Secrets are not in code
- [ ] Database migrations are automated

## Operations ✅

- [ ] Backup strategy is documented
- [ ] Disaster recovery plan exists
- [ ] Runbooks are created
- [ ] On-call rotation is established
- [ ] Incident response plan is ready
- [ ] Documentation is complete
- [ ] SLA/SLO is defined
- [ ] Cost monitoring is set up

## Post-Deployment ✅

- [ ] Verify all features work end-to-end
- [ ] Test payment processing (if applicable)
- [ ] Verify email notifications work
- [ ] Check database performance
- [ ] Review application logs
- [ ] Monitor error rates
- [ ] Gather user feedback
- [ ] Plan maintenance window

---

## Quick Verification Commands

### Backend
```bash
# Test API
curl https://your-backend-url/api/health

# Check logs
tail -f logs/app.log

# Database connection
psql -h host -U user -d database -c "SELECT 1;"
```

### Frontend
```bash
# Build size
npm run build -- --report

# Test production build locally
npm run preview
```

---

## Common Issues & Prevention

| Issue | Prevention |
| :--- | :--- |
| CORS errors | Configure CORS_ORIGINS correctly for prod URL |
| 502 Bad Gateway | Check Render/AWS status and restart |
| Database connection timeouts | Increase connection pool size |
| API rate limiting | Implement with proper user quotas |
| Out of memory | Monitor heap usage, optimize queries |
| Slow queries | Add database indexes, use EXPLAIN ANALYZE |
| Token expiration | Implement token refresh mechanism |

---

**Last Reviewed:** May 15, 2026
**Next Review:** Every deployment
