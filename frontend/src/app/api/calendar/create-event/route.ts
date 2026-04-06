import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    console.log('Creating calendar event:', body);

    // For demo purposes, simulate Google Calendar API call
    const eventDetails = {
      title: body.title || "New Event",
      date: body.date || new Date().toISOString().split('T')[0],
      time: body.time || "12:00",
      description: body.description || "Created by CipherMate AI Assistant"
    };

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Create a realistic Google Calendar event URL
    const eventId = `event_${Date.now()}`;
    const calendarUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent(eventDetails.title)}&dates=${eventDetails.date.replace(/-/g, '')}T${eventDetails.time.replace(':', '')}00/${eventDetails.date.replace(/-/g, '')}T${eventDetails.time.replace(':', '')}00&details=${encodeURIComponent(eventDetails.description)}`;

    const result = {
      success: true,
      event: {
        id: eventId,
        title: eventDetails.title,
        date: eventDetails.date,
        time: eventDetails.time,
        description: eventDetails.description,
        calendar_url: calendarUrl,
        created_at: new Date().toISOString()
      },
      message: `✅ Calendar event "${eventDetails.title}" created successfully for ${eventDetails.date} at ${eventDetails.time}!`,
      instructions: "Click the link below to view/edit the event in Google Calendar:",
      action_url: calendarUrl
    };

    return NextResponse.json(result);

  } catch (error) {
    console.error('Error creating calendar event:', error);
    return NextResponse.json(
      { 
        success: false,
        error: 'Failed to create calendar event',
        message: "❌ Sorry, I couldn't create the calendar event. Please try again."
      },
      { status: 500 }
    );
  }
}