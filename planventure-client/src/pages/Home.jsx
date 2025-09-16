import { Box, Typography, Container, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import planventureLogo from '../assets/planventure-logo.svg';
import MainLayout from '../layouts/MainLayout';

const Home = () => {
  const navigate = useNavigate();

  const content = (
    <Container maxWidth="sm">
      <Box 
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          py: 4,
        }}
      >
        <img 
          src={planventureLogo} 
          alt="Planventure Logo"
          style={{
            height: '200px',
            marginBottom: '2rem'
          }}
        />
        <Typography 
          variant="h3" 
          component="h1"
          sx={{ 
            mb: 2, 
            textAlign: 'center',
            color: 'secondary.main'
          }}
        >
          Welcome to Planventure
        </Typography>
        <Typography 
          variant="body1"
          sx={{ 
            mb: 4, 
            textAlign: 'center',
            color: 'secondary.light'
          }}
        >
          Your next adventure begins here. Start planning unforgettable trips with our intuitive planning tools and make every journey memorable.
        </Typography>
        <Button
          variant="contained"
          size="large"
          onClick={() => navigate('/login')}
          sx={{
            py: 2,
            px: 4,
            fontSize: '1.1rem'
          }}
        >
          Get Started
        </Button>
      </Box>
    </Container>
  );

  return (
    <MainLayout>
      {content}
    </MainLayout>
  );
};

export default Home;