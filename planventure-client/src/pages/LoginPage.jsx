import { Typography } from '@mui/material';
import AuthLayout from '../layouts/AuthLayout';
import LoginForm from '../components/auth/LoginForm';

const LoginPage = () => {
  return (
    <AuthLayout>
      <Typography 
        variant="h4" 
        component="h1" 
        gutterBottom 
        textAlign="center"
        sx={{ mb: 4 }}
      >
        Welcome Back
      </Typography>
      <LoginForm />
    </AuthLayout>
  );
};

export default LoginPage;