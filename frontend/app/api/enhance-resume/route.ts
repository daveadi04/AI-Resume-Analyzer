import { NextResponse } from 'next/server';
import OpenAI from 'openai';

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(request: Request) {
    try {
        const { projects, workExperience, skills } = await request.json();

        // Create a prompt for the AI to enhance the content
        const prompt = `Please enhance the following resume content to make it more impactful and professional. 
        Focus on using action verbs, quantifying achievements, and highlighting key skills.
        
        Projects: ${projects}
        Work Experience: ${workExperience}
        Skills: ${skills.join(', ')}
        
        Please provide:
        1. Enhanced project descriptions
        2. Enhanced work experience descriptions
        3. A list of 5-7 powerful action verbs or phrases that could be used to describe achievements
        4. 3-4 industry-specific keywords that could be added to make the resume more ATS-friendly`;

        const completion = await openai.chat.completions.create({
            model: "gpt-4",
            messages: [
                {
                    role: "system",
                    content: "You are a professional resume writer and career coach. Your task is to enhance resume content to make it more impactful and ATS-friendly."
                },
                {
                    role: "user",
                    content: prompt
                }
            ],
            temperature: 0.7,
            max_tokens: 1000,
        });

        const response = completion.choices[0].message.content;
        
        // Parse the AI response
        const sections = response.split('\n\n');
        const enhancedProjects = sections[0]?.replace('Projects:', '').trim() || projects;
        const enhancedWorkExperience = sections[1]?.replace('Work Experience:', '').trim() || workExperience;
        const actionVerbs = sections[2]?.split('\n').map(v => v.trim()).filter(v => v) || [];
        const keywords = sections[3]?.split('\n').map(k => k.trim()).filter(k => k) || [];

        return NextResponse.json({
            projects: enhancedProjects,
            workExperience: enhancedWorkExperience,
            suggestions: [...actionVerbs, ...keywords]
        });

    } catch (error) {
        console.error('Error enhancing resume:', error);
        return NextResponse.json(
            { error: 'Failed to enhance resume content' },
            { status: 500 }
        );
    }
} 