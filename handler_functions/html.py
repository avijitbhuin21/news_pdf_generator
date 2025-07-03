import json

style = """
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
            display:block;
        }

        .card-container {
            background-color: #F8F6F2;
            padding: 24px;
            max-width: 600px;
            width: 100%;
            box-sizing: border-box;
            border: 1px solid #EAE8E3;
            border-radius: 8px;
            margin-top:1rem;
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
            max-height: 300px;
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
            .main-image {
                width: 100%;
                height: auto;
                max-height: 300px;
                border-radius: 12px;
                display: block;
            }
            .profile-pic {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                object-fit: cover;
            }

            .card-container {
                /* Remove card styling for a clean document look */
                max-width: 100%;
                border: none;
                box-shadow: none;
                padding: 0;
                background-color: transparent;
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
        }"""

def get_body_content(data:dict):
    print(data)
    return f"""<div class="card-container">
        <header class="post-header">
            <a href="https://www.google.com" style="display: flex; align-items: center; gap: 12px; text-decoration: none; color: inherit;">
                <img class="profile-pic" src="https://picsum.photos/id/237/40/40" alt="Profile picture of Rakesh Gohel">
                <span class="username">@username</span>
            </a>
        </header>

        <div class="main-image-container" style="width: 100%; aspect-ratio: 16/9; overflow: hidden; border-radius: 12px;">
            <img class="main-image" src="{data['media_url']}" alt="Abstract tech-related image" style="width: 100%; height: 100%; object-fit: cover;">
        </div>

        <div class="post-content">
            <h1>{data['title'].upper()}</h1>
            
            <p>Major finding:</p>
            
            <p>
                {data['description']}
            </p>
            

            <a href="{data['link']}" class="learn-more-link">Click here to learn more</a>
        </div>
    </div>"""
def get_page_html(data):
    
    body = []
    if not isinstance(data, list):
        data = json.loads(data)
    for i in data:
        body.append(get_body_content(i))

    template = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>News PDF Generator</title>
            <style>
            {style}
            </style>
        </head>
        <body>
        {"\n\n".join(body)}
        </body>
        </html>"""
    return template

def get_pdf_html(data:dict):
    return [f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>News PDF Generator</title>
            <style>
            {style}
            </style>
        </head>
        <body>
        {get_body_content(i)}
        </body>
        </html>""" for i in data]

    

    
# def get_html_content(data:dict):
#     return {
#         "page_html": get_page_html(data),
#         "pdf_html": get_pdf_html(data)
#     }