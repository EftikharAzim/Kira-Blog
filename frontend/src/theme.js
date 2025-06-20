import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#457b9d',
    },
    secondary: {
      main: '#1d3557',
    },
    background: {
      default: '#f5f6fa',
      paper: '#fff',
    },
  },
  shape: {
    borderRadius: 8,
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
  components: {
    MuiContainer: {
      styleOverrides: {
        root: {
          backgroundColor: '#fff',
          borderRadius: 8,
          boxShadow: '0 2px 8px rgba(0,0,0,0.07)',
          padding: '2rem',
          marginBottom: '2rem',
          maxWidth: 500,
        },
      },
    },
  },
});

export default theme;
