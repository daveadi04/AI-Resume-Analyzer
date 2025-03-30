import React, { useState } from 'react';
import { Button, TextField, Select, MenuItem, FormControl, InputLabel, Box, Typography, Paper, CircularProgress, Chip } from '@mui/material';

interface ResumeData {
    fullName: string;
    address: string;
    phone: string;
    email: string;
    university: string;
    programmingSkills: string[];
    otherLanguages: string;
    projects: string;
    workExperience: string;
}

interface AIEnhancedContent {
    projects: string;
    workExperience: string;
    skills: string[];
}

const ResumeBuilder = () => {
    const [resumeData, setResumeData] = useState<ResumeData>({
        fullName: '',
        address: '',
        phone: '',
        email: '',
        university: '',
        programmingSkills: [],
        otherLanguages: '',
        projects: '',
        workExperience: ''
    });

    const [showResume, setShowResume] = useState(false);
    const [loading, setLoading] = useState(false);
    const [aiEnhancedContent, setAiEnhancedContent] = useState<AIEnhancedContent | null>(null);
    const [suggestions, setSuggestions] = useState<string[]>([]);

    const handleInputChange = (field: keyof ResumeData, value: string | string[]) => {
        setResumeData(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const enhanceContent = async () => {
        setLoading(true);
        try {
            const response = await fetch('/api/enhance-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    projects: resumeData.projects,
                    workExperience: resumeData.workExperience,
                    skills: resumeData.programmingSkills
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to enhance content');
            }

            const data = await response.json();
            setAiEnhancedContent(data);
            setSuggestions(data.suggestions);
        } catch (error) {
            console.error('Error enhancing content:', error);
        } finally {
            setLoading(false);
        }
    };

    const generateResume = async () => {
        await enhanceContent();
        setShowResume(true);
    };

    const getSkillDescription = (skill: string) => {
        const descriptions: { [key: string]: string } = {
            'Python': 'I am proficient in the Python programming language with a solid understanding of its syntax and features. I am comfortable writing Python code and effectively using its built-in functions and libraries. I have a good grasp of object-oriented programming (OOP) concepts and data structures.',
            'Java': 'I am proficient in Java with strong command of its syntax and features. I am skilled in writing Java code and utilizing its extensive libraries and frameworks. I have solid understanding of OOP concepts including classes, objects, inheritance, and polymorphism.',
            'C': 'I am proficient in C programming with strong grasp of its syntax and features. I am experienced in writing efficient and concise C code, utilizing its libraries and functions effectively.',
            'C++': 'I am proficient in C++ with strong command of its syntax and features. I am experienced in writing clean and efficient C++ code and effectively utilizing the language\'s powerful libraries and functionalities.',
            'Web Development': 'I work as a web developer, specializing in creating and maintaining websites. I am skilled in front-end development using HTML, CSS, and JavaScript, as well as back-end development with various frameworks.',
            'Freelancing': 'I have experience as a freelancer, taking on various projects and assignments. I enjoy the flexibility and independence while delivering high-quality work to clients.'
        };
        return descriptions[skill] || '';
    };

    return (
        <Box sx={{ maxWidth: 800, margin: '0 auto', padding: 4 }}>
            {!showResume ? (
                <Box component={Paper} sx={{ padding: 3 }}>
                    <Typography variant="h4" gutterBottom>Resume Builder</Typography>
                    
                    <TextField
                        fullWidth
                        label="Full Name"
                        value={resumeData.fullName}
                        onChange={(e) => handleInputChange('fullName', e.target.value)}
                        margin="normal"
                    />
                    
                    <TextField
                        fullWidth
                        label="Address"
                        value={resumeData.address}
                        onChange={(e) => handleInputChange('address', e.target.value)}
                        margin="normal"
                    />
                    
                    <TextField
                        fullWidth
                        label="Phone Number"
                        value={resumeData.phone}
                        onChange={(e) => handleInputChange('phone', e.target.value)}
                        margin="normal"
                    />
                    
                    <TextField
                        fullWidth
                        label="Email"
                        value={resumeData.email}
                        onChange={(e) => handleInputChange('email', e.target.value)}
                        margin="normal"
                    />
                    
                    <TextField
                        fullWidth
                        label="University"
                        value={resumeData.university}
                        onChange={(e) => handleInputChange('university', e.target.value)}
                        margin="normal"
                    />
                    
                    <FormControl fullWidth margin="normal">
                        <InputLabel>Programming Skills</InputLabel>
                        <Select
                            multiple
                            value={resumeData.programmingSkills}
                            onChange={(e) => handleInputChange('programmingSkills', e.target.value as string[])}
                        >
                            <MenuItem value="Python">Python</MenuItem>
                            <MenuItem value="Java">Java</MenuItem>
                            <MenuItem value="C">C</MenuItem>
                            <MenuItem value="C++">C++</MenuItem>
                            <MenuItem value="Web Development">Web Development</MenuItem>
                            <MenuItem value="Freelancing">Freelancing</MenuItem>
                        </Select>
                    </FormControl>
                    
                    <TextField
                        fullWidth
                        label="Other Languages"
                        value={resumeData.otherLanguages}
                        onChange={(e) => handleInputChange('otherLanguages', e.target.value)}
                        margin="normal"
                    />
                    
                    <TextField
                        fullWidth
                        label="Projects"
                        value={resumeData.projects}
                        onChange={(e) => handleInputChange('projects', e.target.value)}
                        margin="normal"
                        multiline
                        rows={3}
                    />
                    
                    <TextField
                        fullWidth
                        label="Work Experience"
                        value={resumeData.workExperience}
                        onChange={(e) => handleInputChange('workExperience', e.target.value)}
                        margin="normal"
                        multiline
                        rows={3}
                    />
                    
                    <Button 
                        variant="contained" 
                        color="primary" 
                        onClick={generateResume}
                        disabled={loading}
                        sx={{ marginTop: 2 }}
                    >
                        {loading ? <CircularProgress size={24} /> : 'Generate Resume'}
                    </Button>
                </Box>
            ) : (
                <Box component={Paper} sx={{ padding: 3, backgroundColor: '#0c0b14', color: 'white' }}>
                    <Typography variant="h4" gutterBottom>Generated Resume</Typography>
                    
                    <Typography variant="h6">Personal Information</Typography>
                    <Typography paragraph>Name: {resumeData.fullName}</Typography>
                    <Typography paragraph>Address: {resumeData.address}</Typography>
                    <Typography paragraph>Phone: {resumeData.phone}</Typography>
                    <Typography paragraph>Email: {resumeData.email}</Typography>
                    
                    <Typography variant="h6" sx={{ mt: 2 }}>Objective</Typography>
                    <Typography paragraph>
                        Highly motivated computer science student seeking an internship position to apply and further develop my technical skills in software development and gain real-world experience in the industry.
                    </Typography>
                    
                    <Typography variant="h6" sx={{ mt: 2 }}>Education</Typography>
                    <Typography paragraph>
                        Bachelor of Science in Computer Science<br />
                        {resumeData.university}
                    </Typography>
                    
                    <Typography variant="h6" sx={{ mt: 2 }}>Technical Skills</Typography>
                    {resumeData.programmingSkills.map((skill) => (
                        <Typography key={skill} paragraph>
                            {getSkillDescription(skill)}
                        </Typography>
                    ))}
                    
                    {resumeData.otherLanguages && (
                        <>
                            <Typography variant="h6" sx={{ mt: 2 }}>Languages</Typography>
                            <Typography paragraph>{resumeData.otherLanguages}</Typography>
                        </>
                    )}
                    
                    {aiEnhancedContent && (
                        <>
                            <Typography variant="h6" sx={{ mt: 2 }}>Projects</Typography>
                            <Typography paragraph>{aiEnhancedContent.projects}</Typography>
                            
                            <Typography variant="h6" sx={{ mt: 2 }}>Work Experience</Typography>
                            <Typography paragraph>{aiEnhancedContent.workExperience}</Typography>
                        </>
                    )}
                    
                    {suggestions.length > 0 && (
                        <>
                            <Typography variant="h6" sx={{ mt: 2, color: '#ff00ff' }}>AI-Enhanced Suggestions</Typography>
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
                                {suggestions.map((suggestion, index) => (
                                    <Chip
                                        key={index}
                                        label={suggestion}
                                        sx={{
                                            backgroundColor: 'rgba(255, 0, 255, 0.1)',
                                            color: '#ff00ff',
                                            '&:hover': {
                                                backgroundColor: 'rgba(255, 0, 255, 0.2)',
                                            }
                                        }}
                                    />
                                ))}
                            </Box>
                        </>
                    )}
                    
                    <Typography paragraph sx={{ mt: 4 }}>
                        Thank you for reviewing my resume. I am available upon request.
                    </Typography>
                    
                    <Button 
                        variant="contained" 
                        color="primary" 
                        onClick={() => setShowResume(false)}
                        sx={{ mt: 2 }}
                    >
                        Edit Resume
                    </Button>
                </Box>
            )}
        </Box>
    );
};

export default ResumeBuilder; 