# ITSM Frontend - React.js

Modern, responsive React.js frontend for the ITSM microservices backend.

## Technology Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Redux Toolkit** - State management
- **Tailwind CSS** - Styling
- **React Hook Form** - Form management
- **Zod** - Schema validation
- **Axios** - HTTP client

## Project Structure

```
frontend/
├── src/
│   ├── components/      # React components
│   ├── pages/          # Page components
│   ├── store/          # Redux store
│   ├── services/       # API services
│   ├── hooks/          # Custom hooks
│   ├── types/          # TypeScript types
│   ├── utils/          # Utilities
│   ├── styles/         # Global styles
│   ├── context/        # React context
│   ├── App.tsx         # Main app component
│   └── index.tsx       # Entry point
├── tests/              # Test files
├── public/             # Static assets
├── package.json        # Dependencies
├── tsconfig.json       # TypeScript config
├── vite.config.ts      # Vite config
└── tailwind.config.js  # Tailwind config
```

## Getting Started

### Prerequisites

- Node.js 16+ (LTS recommended)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Create .env file
cp .env.example .env.local

# Update API base URL in .env.local if needed
```

### Development

```bash
# Start development server
npm run dev

# Server runs on http://localhost:3000
```

### Building

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Available Scripts

```bash
# Development
npm run dev              # Start dev server

# Building
npm run build            # Production build
npm run preview          # Preview production build

# Code Quality
npm run lint             # Run ESLint
npm run format           # Format code with Prettier

# Testing
npm run test             # Run tests
npm run test:watch       # Run tests in watch mode
npm run test:cov         # Generate coverage report

# Documentation
npm run storybook        # Start Storybook
npm run build-storybook  # Build Storybook
```

## Environment Variables

Create `.env.local` file:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_APP_NAME=ITSM Management System
VITE_APP_VERSION=1.0.0
VITE_LOG_LEVEL=info
```

## Features

### Incident Management
- Create, view, list, assign incidents
- Work note management
- Real-time SLA countdown
- Status workflow

### Problem Management
- Create, view, list problems
- RCA workflow
- Known error documentation

### Change Management
- Create, view, list changes
- Impact assessment
- Approval workflow
- Implementation tracking

### Service Request Management
- Create, view, list requests
- Task management
- Progress tracking

### Cross-Cutting Features
- Global search
- Real-time notifications
- Audit trail
- User profile
- Dashboard

## Code Quality

### ESLint Configuration

```bash
npm run lint
```

### Code Formatting

```bash
npm run format
```

### TypeScript

Strict mode enabled. All files use TypeScript for type safety.

## Testing

### Unit Tests

```bash
npm run test
```

### Watch Mode

```bash
npm run test:watch
```

### Coverage Report

```bash
npm run test:cov
```

## Performance

### Bundle Size

Target: < 500KB (gzipped)

### Optimization

- Code splitting by route
- Lazy loading components
- Image optimization
- Memoization strategies

### Lighthouse Targets

- Performance: > 90
- Accessibility: > 90
- Best Practices: > 90
- SEO: > 90

## Accessibility

WCAG 2.1 AA compliance:
- Semantic HTML
- ARIA labels
- Keyboard navigation
- Color contrast
- Screen reader support

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Deployment

### Development

```bash
npm run dev
```

### Staging

```bash
npm run build
# Deploy dist/ folder
```

### Production

```bash
npm run build
# Deploy dist/ folder with CDN
```

## Contributing

1. Create feature branch
2. Make changes
3. Run tests and linting
4. Create pull request

## License

MIT
