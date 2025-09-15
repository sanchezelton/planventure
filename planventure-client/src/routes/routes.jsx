import Home from '../pages/Home';

export const publicRoutes = [
  {
    path: '/',
    element: <Home />,
  },
  {
    path: '/login',
    element: <Home />, // Temporarily using Home component
  },
];

export const protectedRoutes = [
  {
    path: '/trips',
    element: <Home />, // Temporarily using Home component
  }
];