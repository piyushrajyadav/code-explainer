import React from 'react';
import { Box, Paper, Typography, Skeleton, Divider, List, ListItem, ListItemIcon, ListItemText, Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import CodeIcon from '@mui/icons-material/Code';
import FunctionsIcon from '@mui/icons-material/Functions';
import ClassIcon from '@mui/icons-material/Class';
import VariableIcon from '@mui/icons-material/CompareArrows';
import LoopIcon from '@mui/icons-material/Loop';
import EventIcon from '@mui/icons-material/Event';
import DnsIcon from '@mui/icons-material/Dns';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import BuildIcon from '@mui/icons-material/Build';
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import StorageIcon from '@mui/icons-material/Storage';
import SyncIcon from '@mui/icons-material/Sync';

const CodeExplanation = ({ explanation, loading }) => {
  // Split explanation into lines for better formatting
  const lines = explanation ? explanation.split('\n') : [];

  // Group explanation sections
  const sections = groupExplanationSections(lines);

  // Helper to determine which icon to use for each explanation line
  const getIconForLine = (line) => {
    if (line.includes('imports')) return <CodeIcon />;
    if (line.includes('Function')) return <FunctionsIcon />;
    if (line.includes('Class')) return <ClassIcon />;
    if (line.includes('Variables')) return <VariableIcon />;
    if (line.includes('loop')) return <LoopIcon />;
    if (line.includes('conditional')) return <FunctionsIcon />;
    if (line.includes('async')) return <EventIcon />;
    if (line.includes('DOM')) return <DnsIcon />;
    if (line.includes('network')) return <SyncIcon />;
    if (line.includes('storage')) return <StorageIcon />;
    if (line.includes('Purpose')) return <AccountTreeIcon />;
    return <CodeIcon />;
  };

  // Group explanation lines into meaningful sections
  function groupExplanationSections(lines) {
    const sections = [];
    let currentSection = { title: 'Summary', lines: [] };
    let currentSectionIndex = 0;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      
      // Detect section headers
      if (line === 'Functional Analysis:') {
        if (currentSection.lines.length > 0) {
          sections.push(currentSection);
        }
        currentSection = { title: 'Functional Analysis', lines: [] };
        currentSectionIndex++;
        continue;
      }
      
      // Check for subsection headers
      if (line === 'Variables defined:') {
        if (currentSection.lines.length > 0 && currentSection.title !== 'Variables') {
          sections.push(currentSection);
          currentSection = { title: 'Variables', lines: [line] };
          currentSectionIndex++;
        } else {
          currentSection.lines.push(line);
        }
        continue;
      }

      // Add line to current section
      currentSection.lines.push(line);
    }

    // Add the last section if it has content
    if (currentSection.lines.length > 0) {
      sections.push(currentSection);
    }

    return sections;
  }

  return (
    <Paper 
      elevation={0} 
      sx={{ 
        p: 3, 
        height: '100%',
        border: '1px solid',
        borderColor: 'divider',
        bgcolor: 'background.paper',
        display: 'flex',
        flexDirection: 'column'
      }}
    >
      <Typography variant="h6" component="h2" gutterBottom>
        Code Explanation
      </Typography>
      
      <Divider sx={{ mb: 2 }} />
      
      {loading ? (
        <Box sx={{ mt: 2 }}>
          <Skeleton animation="wave" height={40} />
          <Skeleton animation="wave" height={40} />
          <Skeleton animation="wave" height={40} />
          <Skeleton animation="wave" height={40} />
          <Skeleton animation="wave" height={40} />
        </Box>
      ) : !explanation ? (
        <Box 
          sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            flexDirection: 'column',
            height: '100%',
            color: 'text.secondary',
            flexGrow: 1
          }}
        >
          <CodeIcon sx={{ fontSize: 60, mb: 2, opacity: 0.3 }} />
          <Typography variant="body1">
            Enter your code and click "Analyze Code" to see the explanation
          </Typography>
        </Box>
      ) : (
        <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
          {sections.map((section, sectionIndex) => (
            <Accordion 
              key={sectionIndex} 
              defaultExpanded={sectionIndex === 0}
              sx={{ 
                mb: 2, 
                '&:before': { display: 'none' },
                boxShadow: 'none',
                border: '1px solid',
                borderColor: 'divider',
              }}
            >
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                sx={{ 
                  bgcolor: (theme) => theme.palette.primary.main,
                  color: 'white',
                  borderRadius: '4px 4px 0 0',
                  '& .MuiAccordionSummary-expandIconWrapper': {
                    color: 'white',
                  }
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  {section.title === 'Summary' && <CodeIcon sx={{ mr: 1 }} />}
                  {section.title === 'Functional Analysis' && <BuildIcon sx={{ mr: 1 }} />}
                  {section.title === 'Variables' && <VariableIcon sx={{ mr: 1 }} />}
                  <Typography variant="subtitle1" fontWeight="600">
                    {section.title}
                  </Typography>
                </Box>
              </AccordionSummary>
              <AccordionDetails sx={{ p: 0 }}>
                <List sx={{ py: 0 }}>
                  {section.lines.map((line, lineIndex) => (
                    line.trim() && (
                      <ListItem 
                        key={lineIndex} 
                        alignItems="flex-start" 
                        sx={{ 
                          py: 1, 
                          borderBottom: lineIndex !== section.lines.length - 1 ? '1px solid' : 'none',
                          borderColor: 'divider',
                          px: 2
                        }}
                      >
                        <ListItemIcon>
                          {getIconForLine(line)}
                        </ListItemIcon>
                        <ListItemText
                          primary={line}
                          sx={{
                            '& .MuiListItemText-primary': {
                              fontFamily: line.startsWith('-') ? '"Fira Code", monospace' : 'inherit',
                              fontSize: line.startsWith('-') ? '0.9rem' : 'inherit',
                            }
                          }}
                        />
                      </ListItem>
                    )
                  ))}
                </List>
              </AccordionDetails>
            </Accordion>
          ))}
        </Box>
      )}
    </Paper>
  );
};

export default CodeExplanation; 