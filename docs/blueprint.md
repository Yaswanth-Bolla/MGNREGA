# **App Name**: MGNREGA Sarathi

## Core Features:

- Data Ingestion and Storage: Automatically fetch data from the data.gov.in API for Karnataka districts and store it in a SQLite database.
- District Auto-Detection: Automatically detect the user's district based on their location (optional, with permission request).
- Performance Visualization: Display district-wise MGNREGA performance data using charts and graphs in an easy-to-understand format.
- Historical Data Comparison: Allow users to compare current performance with past performance and with other districts.
- Terminology Explanation: Provide explanations of MGNREGA terminologies in both English and Kannada.
- User Feedback: Collect feedback from users via UI elements to understand common issues.
- Intelligent summary: Use an LLM tool to summarize the data in simple terms, providing human-readable insights about the district's performance. This will also suggest areas of improvement. The LLM reasons on what to include in the generated summary and its suggestions for the UI.

## Style Guidelines:

- Primary color: Earthy Green (#558B2F) to represent growth and nature.
- Background color: Light Beige (#F5F5DC), a desaturated version of the primary color for readability.
- Accent color: Warm Orange (#FF7043) to highlight important data points and call to action.
- Body font: 'PT Sans', a humanist sans-serif font that is readable on all devices.
- Headline font: 'PT Sans', a humanist sans-serif font that is readable on all devices.
- Use simple, culturally relevant icons to represent different data points and categories.
- Clean, uncluttered layout with clear visual hierarchy, optimized for low-literacy users.