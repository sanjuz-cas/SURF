# 🌊 SURF Customer Feedback Dashboard - Frontend

## Overview

Professional React + TypeScript dashboard for displaying prioritized customer feedback analyzed by the SURF AI Agent Pipeline. Features a visually striking interface with animated warning boxes for financial risk forecasts.

---

## 🎨 Features

- **Real-time Priority Display**: Fetches and displays prioritized feedback items from backend API
- **Financial Risk Warnings**: Visually striking red warning boxes with animations for pre-mortem forecasts
- **Responsive Design**: Mobile-first approach with responsive grid layouts
- **Professional UI/UX**: 
  - Gradient backgrounds and glass-morphism effects
  - Loading states with animated spinners
  - Error handling with retry functionality
  - Empty state messaging
- **Type Safety**: Full TypeScript implementation with comprehensive interfaces
- **Modular Components**: Clean component architecture for maintainability

---

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── components/
│   │   ├── PriorityCard.tsx           # Individual feedback card component
│   │   ├── PriorityCard.css           # Card styling with warning box animations
│   │   ├── PrioritizationDashboard.tsx # Main dashboard component
│   │   └── PrioritizationDashboard.css # Dashboard styling
│   ├── types/
│   │   └── index.ts            # TypeScript interfaces
│   ├── mockData.ts             # Mock data for development
│   ├── App.tsx                 # Root component
│   ├── App.css                 # App styles
│   ├── index.tsx               # Entry point
│   └── index.css               # Global styles
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
└── README.md                   # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js**: v16 or higher
- **npm**: v7 or higher

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### Development

```bash
# Start development server (runs on http://localhost:3000)
npm start
```

The app will automatically reload when you make changes.

### Build

```bash
# Create production build
npm run build
```

The optimized build will be in the `build/` folder.

### Type Checking

```bash
# Run TypeScript compiler check
npm run type-check
```

---

## 🔌 API Integration

### Endpoint

The dashboard fetches data from:

```
GET /api/priorities
```

### Response Schema

```typescript
interface PrioritiesResponse {
  items: PrioritizedItem[];
  total_analyzed: number;
  total_risk_estimate: string;
  generated_at: string;
  agent_pipeline_version?: string;
  metadata?: {
    analysis_duration_seconds: number;
    llm_model: string;
    confidence_score: number;
  };
}
```

### Mock Data

For development without backend:

```typescript
import { mockPrioritiesData } from './mockData';

// Use mock data in development
const response = mockPrioritiesData;
```

---

## 🎯 Component Overview

### PrioritizationDashboard

Main dashboard component that:
- Fetches prioritized items from `/api/priorities`
- Displays loading/error/empty states
- Shows summary statistics
- Renders list of PriorityCard components

**Props**: None (uses internal state management)

### PriorityCard

Displays individual prioritized feedback items:
- **Rank badge**: Visual priority indicator
- **Title & Score**: Feedback title with numerical score
- **Category & Team**: Metadata badges
- **Pre-Mortem Warning Box**: Animated red warning box with financial forecast
- **Action Plan**: Expandable immediate/medium/long-term steps
- **Timeline & Resources**: Project planning details

**Props**:
```typescript
interface PriorityCardProps {
  item: PrioritizedItem;
}
```

---

## 🎨 Design System

### Color Palette

- **Primary Gradient**: `#667eea → #764ba2` (Purple)
- **Background**: `#f5f7fa → #c3cfe2` (Light blue-gray gradient)
- **Warning (Critical)**: `#ff4444 → #cc0000` (Red gradient)
- **Text**: `#333` (Dark gray)
- **Accent**: `#ffeb3b` (Yellow for risk values)

### Typography

- **Font Family**: System fonts (-apple-system, Segoe UI, Roboto)
- **Headings**: 700 weight, letter-spacing -0.5px
- **Body**: 400 weight, line-height 1.6

### Animations

- **Pulse Warning**: 2s infinite shadow pulse on warning boxes
- **Shake**: 0.5s error icon shake
- **Spin**: 1s loading spinner rotation
- **Hover Effects**: Transform translateY(-4px) with shadow

---

## 📱 Responsive Breakpoints

- **Desktop**: > 768px (full layout)
- **Tablet**: 481px - 768px (adjusted spacing)
- **Mobile**: ≤ 480px (single column, compressed stats)

---

## 🔧 Configuration

### API Base URL

Update in `PrioritizationDashboard.tsx`:

```typescript
const response = await axios.get<PrioritiesResponse>('/api/priorities');
```

For different backend URLs:

```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const response = await axios.get(`${API_BASE_URL}/api/priorities`);
```

### Environment Variables

Create `.env` file:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development
```

---

## 🐛 Troubleshooting

### TypeScript Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Module Not Found

Ensure all dependencies are installed:

```bash
npm install react react-dom typescript axios @types/react @types/react-dom
```

### API Connection Issues

1. Check backend is running on correct port
2. Verify CORS is enabled on backend
3. Use mock data for offline development

---

## 🔐 Security Notes

- **No Secrets in Frontend**: Never commit API keys or credentials
- **Environment Variables**: Use `.env` files (gitignored)
- **HTTPS in Production**: Always use secure connections
- **Input Sanitization**: Backend should validate all inputs

---

## 📈 Performance Optimization

- **Code Splitting**: React.lazy() for large components
- **Memoization**: React.memo() for expensive components
- **Virtual Scrolling**: For large lists (100+ items)
- **Image Optimization**: Use WebP format
- **Bundle Analysis**: `npm run build -- --stats`

---

## 🧪 Testing (Future)

```bash
# Run tests (when implemented)
npm test

# Coverage report
npm test -- --coverage
```

---

## 📦 Deployment

### Netlify

```bash
npm run build
# Deploy build/ folder
```

### Vercel

```bash
vercel --prod
```

### Docker

```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npx", "serve", "-s", "build"]
```

---

## 🤝 Integration with Backend

### Backend API (FastAPI)

The backend should expose:

```python
@app.get("/api/priorities")
async def get_priorities():
    # Query database
    items = fetch_prioritized_items()
    return {
        "items": items,
        "total_analyzed": len(all_feedback),
        "total_risk_estimate": calculate_total_risk(),
        "generated_at": datetime.now().isoformat()
    }
```

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📚 Dependencies

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "typescript": "^5.3.3",
  "axios": "^1.6.2",
  "@types/react": "^18.2.45",
  "@types/react-dom": "^18.2.18"
}
```

---

## 🎓 Learning Resources

- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Axios Documentation](https://axios-http.com/docs/intro)
- [CSS Animations Guide](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations)

---

## 📝 License

Part of the SURF Customer Feedback Agent project.

---

## 👥 Team

Developed for strategic customer retention and feedback prioritization.

---

## 🚧 Roadmap

- [ ] Add real-time WebSocket updates
- [ ] Implement user authentication
- [ ] Add filtering and search functionality
- [ ] Create export to PDF feature
- [ ] Build admin configuration panel
- [ ] Add dark mode theme toggle
- [ ] Implement A/B testing framework

---

## 📞 Support

For issues or questions:
1. Check existing documentation
2. Review mock data examples
3. Verify backend API is running
4. Check browser console for errors

---

**Built with ❤️ using React + TypeScript**
