import pdfkit
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIT Study on ChatGPT - Report</title>
    <style>
        /* --- Styles for Screen View --- */
        body {
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #F0EEE9;
            color: #3D3D3D;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
        }

        .card-container {
            background-color: #F8F6F2;
            padding: 24px;
            max-width: 600px;
            width: 100%;
            box-sizing: border-box;
            border: 1px solid #EAE8E3;
            border-radius: 8px;
        }

        .post-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
        }

        .profile-pic {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
        }

        .username {
            font-size: 1rem;
            font-weight: 500;
        }

        .main-image {
            width: 100%;
            height: auto;
            border-radius: 12px;
            display: block;
        }

        .post-content {
            margin-top: 24px;
        }

        h1 {
            font-size: 1.6rem;
            font-weight: 700;
            text-transform: uppercase;
            line-height: 1.3;
            margin: 0 0 20px 0;
        }

        p {
            font-size: 1.1rem;
            line-height: 1.6;
            margin: 0 0 1.2em 0;
        }

        .learn-more-link {
            color: #3D3D3D;
            text-decoration: underline;
            font-size: 1rem;
        }
        
        .learn-more-link:hover {
            color: #000;
        }

        /* --- Styles for PDF / Print View --- */
        @media print {
            body {
                /* Reset for print: white background, black text, serif font */
                background-color: #fff;
                color: #000;
                font-family: Georgia, "Times New Roman", Times, serif;
                font-size: 12pt;
                padding: 1in; /* Add standard document margins */
                display: block; /* Disable flexbox for print */
            }

            .card-container {
                /* Remove card styling for a clean document look */
                max-width: 100%;
                border: none;
                box-shadow: none;
                padding: 0;
                background-color: transparent;
            }

            .profile-pic {
                /* Hide decorative profile picture in print */
                display: none;
            }

            .post-header {
                margin-bottom: 20pt;
            }

            .username {
                font-size: 14pt;
                font-weight: bold;
            }

            h1 {
                font-size: 22pt;
                line-height: 1.2;
                margin-bottom: 18pt;
            }

            p {
                font-size: 12pt;
                line-height: 1.5;
                margin-bottom: 12pt;
            }

            .main-image, h1, p {
                /* Try to prevent these elements from breaking across pages */
                page-break-inside: avoid;
            }

            .learn-more-link {
                color: #000;
                text-decoration: none; /* Underlines can look messy in print */
            }

            /* Show the URL next to the link in the printed PDF */
            .learn-more-link::after {
                content: " (" attr(href) ")";
                font-size: 10pt;
                font-style: italic;
                color: #444;
            }
        }
    </style>
</head>
<body>

    <div class="card-container">
        <header class="post-header">
            <img class="profile-pic" src="https://picsum.photos/id/237/40/40" alt="Profile picture of Rakesh Gohel">
            <span class="username">@rakeshgohel01</span>
        </header>

        <img class="main-image" src="https://picsum.photos/id/30/600/300" alt="An abstract image representing brain function and technology.">

        <div class="post-content">
            <h1>MIT SHARES STUDY ON NEGATIVE EFFECTS OF CHATGPT ON BRAIN FUNCTION</h1>
            
            <p><strong>Major finding:</strong></p>
            
            <p>
                People using ChatGPT showed the lowest brain connectivity and engagement, especially in regions linked to executive function.
            </p>
            
            <p>
                They also struggled to recall or summarize their own essays and reported the lowest sense of ownership over their work.
            </p>

            <!-- This link uses a placeholder URL that will be displayed in the PDF -->
            <a href="https://example.com/mit-chatgpt-study" class="learn-more-link">Click here to learn more</a>
        </div>
    </div>

</body>
</html>
"""
import os
options = {
    'page-size': 'A4',
    'margin-top': '0',
    'margin-right': '0',
    'margin-bottom': '0',
    'margin-left': '0',
    'encoding': "UTF-8",
    'print-media-type': '', # This tells wkhtmltopdf to use the @media print styles
    'no-outline': None
}

path = os.path.abspath(r"d:\Normal_apps\wkhtmltopdf\bin\wkhtmltopdf.exe")
config = pdfkit.configuration(wkhtmltopdf=path)
pdfkit.from_string(html, 'output.pdf', configuration=config, options=options)