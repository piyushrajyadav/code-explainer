import React from 'react';
import { AppBar, Toolbar, Typography, Box, Button, useTheme, useMediaQuery, Chip } from '@mui/material';
import CodeIcon from '@mui/icons-material/Code';
import GitHubIcon from '@mui/icons-material/GitHub';
import LightModeIcon from '@mui/icons-material/LightMode';
import SchoolIcon from '@mui/icons-material/School';

const Header = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <AppBar position="static" elevation={0} sx={{ mb: 4 }}>
      <Toolbar>
        <Box display="flex" alignItems="center" sx={{ flexGrow: 1 }}>
          <Box sx={{ 
            backgroundColor: 'rgba(255,255,255,0.2)', 
            p: 1, 
            borderRadius: 2,
            display: 'flex',
            alignItems: 'center',
            mr: 2
          }}>
            <CodeIcon sx={{ fontSize: 28 }} />
          </Box>
          <Box>
            <Typography variant="h5" component="div" sx={{ fontWeight: 700, lineHeight: 1.2 }}>
              Explain My Code
            </Typography>
            <Typography variant="caption" sx={{ opacity: 0.8 }}>
              Understand code structure & functionality
            </Typography>
          </Box>
        </Box>
        
        {!isMobile && (
          <Box>
            
            <Button 
              color="inherit" 
              startIcon={<GitHubIcon />}
              href="https://github.com/piyushrajyadav" 
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Header; 