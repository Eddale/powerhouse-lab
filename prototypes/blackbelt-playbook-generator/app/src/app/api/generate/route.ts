import { NextRequest, NextResponse } from 'next/server';
import Anthropic from '@anthropic-ai/sdk';
import { PlaybookFormData, GenerateResponse } from '@/lib/types';
import { buildPrompt } from '@/lib/prompt';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

export async function POST(request: NextRequest): Promise<NextResponse<GenerateResponse>> {
  try {
    const data: PlaybookFormData = await request.json();

    // Validate required fields
    if (!data.company || !data.role || !data.coreFunction) {
      return NextResponse.json(
        { success: false, error: 'Missing required fields: company, role, and coreFunction are required' },
        { status: 400 }
      );
    }

    const prompt = buildPrompt(data);

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4096,
      messages: [
        {
          role: 'user',
          content: prompt,
        },
      ],
    });

    // Extract text content from the response
    const textContent = message.content.find((block) => block.type === 'text');
    if (!textContent || textContent.type !== 'text') {
      return NextResponse.json(
        { success: false, error: 'No text content in response' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      content: textContent.text,
    });
  } catch (error) {
    console.error('Error generating playbook:', error);
    return NextResponse.json(
      { success: false, error: error instanceof Error ? error.message : 'Failed to generate playbook' },
      { status: 500 }
    );
  }
}
