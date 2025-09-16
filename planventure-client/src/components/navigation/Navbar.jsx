import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { useNavigate, Link as RouterLink } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();

  return (
    <AppBar 
      position="static" 
      sx={{ 
        width: '100%',
        left: 0,
        right: 0,
        position: 'fixed',
      }}
    >
      <Toolbar sx={{ width: '100%' }}>
        <Typography 
          variant="h6" 
          component={RouterLink} 
          to="/"
          sx={{ 
            flexGrow: 1, 
            textAlign: 'left',
            textDecoration: 'none',
            color: 'inherit',
            cursor: 'pointer'
          }}
        >
          Planventure
        </Typography>
        <Button 
          color="inherit"
          onClick={() => navigate('/login')}
        >
          Login
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;