import Home from '../pages/Home';
import LoginPage from '../pages/LoginPage';

export const publicRoutes = [
  {
    path: '/',
    element: <Home />,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
];

export const protectedRoutes = [
  {
    path: '/trips',
    element: <Home />, // Temporarily using Home component
  }
];