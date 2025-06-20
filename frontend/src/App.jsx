import { BrowserRouter as Router, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Login from './pages/Login';
import Register from './pages/Register';
import Posts from './pages/Posts';
import Profile from './pages/Profile';
import theme from './theme';
import './App.css';

function Logout() {
  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };
  return (
    <Button color="inherit" onClick={handleLogout} sx={{ ml: 2 }}>Logout</Button>
  );
}

function App() {
  const isLoggedIn = !!localStorage.getItem('access_token');
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              Kira Blog
            </Typography>
            {!isLoggedIn && <Button color="inherit" component={Link} to="/login">Login</Button>}
            {!isLoggedIn && <Button color="inherit" component={Link} to="/register">Register</Button>}
            <Button color="inherit" component={Link} to="/posts">Posts</Button>
            {isLoggedIn && <Button color="inherit" component={Link} to="/profile">Profile</Button>}
            {isLoggedIn && <Logout />}
          </Toolbar>
        </AppBar>
        <Box sx={{ p: 3 }}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/posts" element={<Posts />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/" element={<Navigate to="/posts" />} />
          </Routes>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
