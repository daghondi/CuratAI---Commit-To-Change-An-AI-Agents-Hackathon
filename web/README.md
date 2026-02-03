# CuratAI Web UI Setup Guide

## Quick Start (5 minutes)

### Prerequisites
- Node.js 18+ (https://nodejs.org)
- npm or yarn package manager

### Installation

```bash
cd web
npm install
```

### Development

```bash
npm run dev
```

Visit `http://localhost:3000` in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
web/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx         # Root layout with header/footer
│   ├── page.tsx           # Home page
│   ├── login/page.tsx     # Login page
│   ├── register/page.tsx  # Registration page
│   ├── dashboard/page.tsx # Main dashboard
│   ├── opportunities/page.tsx # Browse opportunities
│   ├── proposals/page.tsx      # View proposals
│   └── globals.css        # Global styles
├── components/            # Reusable React components
│   ├── Header.tsx         # Navigation header
│   ├── OpportunityCard.tsx # Opportunity display
│   ├── ProposalEditor.tsx  # Proposal writing interface
│   └── DashboardCharts.tsx # Analytics visualizations
├── lib/
│   ├── api.ts            # API client with axios
│   └── store.ts          # Zustand state management
├── package.json          # Dependencies and scripts
├── next.config.js        # Next.js configuration
├── tailwind.config.js    # Tailwind CSS configuration
└── tsconfig.json         # TypeScript configuration
```

## Key Features

### Authentication
- **Login Page** (`/login`): Email/password authentication
- **Register Page** (`/register`): New artist account creation
  - Password strength validation
  - Email verification
  - Profile setup

### Dashboard
- **Dashboard** (`/dashboard`): Main user hub
  - Metrics visualization (opportunities, proposals, submissions)
  - Activity charts and trends
  - Performance indicators
  - Quick action buttons

### Opportunity Discovery
- **Opportunities Page** (`/opportunities`): Browse and filter
  - AI-discovered opportunities
  - Search and filtering by type
  - Relevance scoring (color-coded)
  - Bookmark/track opportunities
  - Links to opportunity sources

### Proposal Management
- **Proposals Page** (`/proposals`): View all proposals
  - Draft and submitted proposals
  - Status tracking (draft, submitted, accepted, rejected)
  - Quick edit access
  - Proposal statistics

### Proposal Editor
- Write proposals with rich text
- AI-assisted generation with tone selection
  - Formal & Professional
  - Engaging & Creative
  - Impact-Driven
- Copy to clipboard
- Save drafts or submit directly

### User Profile
- Profile information management
- Subscription tier display
- Account settings
- Notification preferences

## Components

### Header
Responsive navigation with:
- Logo and branding
- Navigation links (authenticated users)
- Notification bell with unread count
- User menu with profile and logout
- Mobile hamburger menu

### OpportunityCard
Displays individual opportunity with:
- Relevance score (color-coded)
- Type badge (exhibition, grant, residency, call)
- Deadline countdown
- Budget range
- Location
- Track/bookmark button
- Link to original opportunity

### ProposalEditor
Full-featured proposal writing tool:
- Tone selection
- AI generation button (calls GPT-4)
- Rich text editor
- Character counter
- Save to drafts
- Direct submission
- Copy to clipboard

### DashboardCharts
Data visualization with:
- Stat cards (tracked, proposals, submissions, acceptance rate)
- Activity over time (line chart)
- Opportunity breakdown (pie chart)
- Relevance score distribution (donut chart)

## State Management (Zustand)

### useAuthStore
```typescript
{
  user: User | null,
  isLoading: boolean,
  error: string | null,
  setUser, setLoading, setError
}
```

### useOpportunityStore
```typescript
{
  opportunities: Opportunity[],
  filteredOpportunities: Opportunity[],
  filters: { type?, minScore?, searchTerm? },
  setOpportunities, setFilters, addOpportunity, removeOpportunity
}
```

### useProposalStore
```typescript
{
  proposals: Proposal[],
  currentProposal: Proposal | null,
  setProposals, setCurrentProposal, updateProposal, addProposal
}
```

### useNotificationStore
```typescript
{
  notifications: Notification[],
  unreadCount: number,
  setNotifications, addNotification, markAsRead, clearAll
}
```

## API Integration

All API calls use the `lib/api.ts` client with automatic:
- Base URL configuration
- Authorization header injection
- Error handling
- Token management

### Authentication Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - Create account
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout

### Opportunity Endpoints
- `GET /api/opportunities` - List all opportunities
- `POST /api/opportunities/scout` - Run opportunity scout
- `POST /api/opportunities/track` - Save opportunity
- `GET /api/opportunities/tracked` - Get saved opportunities

### Proposal Endpoints
- `GET /api/proposals` - List user proposals
- `POST /api/proposals` - Create new proposal
- `PUT /api/proposals/{id}` - Update proposal
- `POST /api/proposals/generate` - AI generate with tone
- `POST /api/proposals/{id}/submit` - Submit proposal

### Dashboard Endpoints
- `GET /api/dashboard/metrics` - User metrics
- `GET /api/dashboard/analytics` - Detailed analytics

## Styling

Built with **Tailwind CSS**:
- Pre-configured dark mode support
- Custom gradient utilities
- Responsive grid system
- Card and button components

Custom theme colors:
- Primary: Purple (`#a855f7`)
- Secondary: Blue (`#3b82f6`)
- Success: Green (`#10b981`)
- Warning: Orange (`#f59e0b`)
- Error: Red (`#ef4444`)

## Environment Variables

Create `.env.local` from `.env.local.example`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## Development Tips

### Hot Reload
- Changes to files in `/app` and `/components` automatically reload
- State is preserved using Zustand

### TypeScript
- Full type safety for props and API responses
- Type definitions for all major data structures
- Auto-completion in IDE

### Performance
- Image optimization with Next.js Image component
- Code splitting for faster page loads
- Lazy loading for components

### Testing
Run tests with:
```bash
npm test
npm run test:watch
```

## Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Docker
```bash
docker build -t curataai-web .
docker run -p 3000:3000 curataai-web
```

### Manual
```bash
npm run build
npm start
```

## Common Issues

**Issue**: API calls fail with CORS error
**Solution**: Ensure backend is running on configured `NEXT_PUBLIC_API_URL`

**Issue**: Login token not persisting
**Solution**: Check if localStorage is enabled in browser
**Fix**: Verify `Authorization` header in API requests

**Issue**: Proposals not saving
**Solution**: Check backend `/api/proposals` endpoint is available

## Support

For issues or feature requests:
1. Check the [CuratAI main README](../README.md)
2. Review [Quick Start Guide](../QUICK_START.md)
3. Check [Opik Integration](../docs/OpikIntegration.md)
4. Contact the development team

## Next Steps

After setting up the UI:
1. Start the Python backend: `python src/main.py`
2. Login with test credentials
3. Scout opportunities from dashboard
4. Create and submit proposals
5. Monitor metrics and analytics

Enjoy discovering your next opportunity with CuratAI! 🎨✨
